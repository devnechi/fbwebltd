#!/usr/bin/env python3
"""Durable, lease-protected laboratory execution evidence.

Read-only operations require no lease. Every mutation, including the
internal writer, requires an active matching deployment lease.

No Docker execution, production approval, or automatic retry.
"""

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import tempfile

from deployment_lock import DeploymentLease
from docker_process_supervision import ProcessIdentity
from lab_rollback_command import LAB_PROJECT, PREVIOUS, plan_lab_rollback


HEX32 = re.compile(r"^[0-9a-f]{32}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
RELEASE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")

PREPARED = "PREPARED"
OBSERVED = "OBSERVED"
EXIT_OBSERVED = "EXIT_OBSERVED"


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def require_private_dir(path):
    if path.is_symlink():
        raise ValueError("Symlink directory prohibited")

    info = path.stat()

    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o700
    ):
        raise ValueError("Private owned directory required")


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def command_fingerprint(command):
    command.validate()
    return hashlib.sha256(canonical({
        "project": command.project,
        "compose_file": command.compose_file,
        "argv": list(command.argv),
        "environment": [list(pair) for pair in command.environment],
        "app": command.images.app,
        "web": command.images.web,
    })).hexdigest()


def validate_record(value):
    if not isinstance(value, dict):
        raise ValueError("Execution record must be an object")

    expected = {
        "schema_version", "release_id", "attempt_id",
        "execution_id", "operation_fingerprint",
        "command_fingerprint", "project", "phase",
        "pid", "start_ticks", "exit_code",
    }

    if set(value) != expected or value["schema_version"] != 1:
        raise ValueError("Invalid execution record schema")

    if (
        not isinstance(value["release_id"], str)
        or not RELEASE_ID.fullmatch(value["release_id"])
        or not isinstance(value["attempt_id"], str)
        or not re.fullmatch(r"attempt-[0-9]{6}", value["attempt_id"])
        or not isinstance(value["execution_id"], str)
        or not HEX32.fullmatch(value["execution_id"])
    ):
        raise ValueError("Invalid execution identity")

    for field in ("operation_fingerprint", "command_fingerprint"):
        if (
            not isinstance(value[field], str)
            or not HEX64.fullmatch(value[field])
        ):
            raise ValueError("Invalid execution fingerprint")

    if value["project"] != LAB_PROJECT:
        raise ValueError("Non-laboratory execution prohibited")

    phase = value["phase"]

    if phase not in (PREPARED, OBSERVED, EXIT_OBSERVED):
        raise ValueError("Invalid execution phase")

    if phase == PREPARED:
        if any(
            value[key] is not None
            for key in ("pid", "start_ticks", "exit_code")
        ):
            raise ValueError("PREPARED cannot claim process observation")
    else:
        ProcessIdentity(
            value["pid"], value["start_ticks"]
        ).validate()

        if phase == OBSERVED and value["exit_code"] is not None:
            raise ValueError("OBSERVED cannot contain exit result")

        if phase == EXIT_OBSERVED:
            code = value["exit_code"]
            if type(code) is not int or not -255 <= code <= 255:
                raise ValueError("Invalid process exit code")

    return value


@dataclass(frozen=True)
class EvidenceResult:
    phase: str
    docker_operation_settled: bool = False
    automatic_retry_permitted: bool = False
    manual_reconciliation_required: bool = True


class DockerExecutionEvidenceStore:
    """Read-only by default; mutation requires an active matching lease."""

    def __init__(self, root, lock_dir=None, lease=None):
        self.root = Path(root)
        require_private_dir(self.root)

        if (lock_dir is None) != (lease is None):
            raise RuntimeError(
                "Lock directory and deployment lease must be supplied together"
            )

        if lease is not None and not isinstance(lease, DeploymentLease):
            raise RuntimeError("DeploymentLease required")

        self.lock_dir = (
            Path(lock_dir) if lock_dir is not None else None
        )
        self.lease = lease

        if lease is not None:
            self.require_lease()

    def require_lease(self):
        if self.lease is None or self.lock_dir is None:
            raise RuntimeError(
                "Read-only evidence store cannot perform mutations"
            )

        self.lease.require(self.lock_dir)
        return True

    def path(self, release_id):
        if (
            not isinstance(release_id, str)
            or not RELEASE_ID.fullmatch(release_id)
        ):
            raise ValueError("Invalid release identity")

        return self.root / (release_id + ".json")

    def _read_path(self, path):
        if path.is_symlink():
            raise ValueError("Evidence symlink prohibited")

        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)

        try:
            info = os.fstat(fd)

            if (
                not stat.S_ISREG(info.st_mode)
                or info.st_uid != os.geteuid()
                or stat.S_IMODE(info.st_mode) != 0o600
            ):
                raise ValueError("Invalid evidence file permissions")

            with os.fdopen(fd, "r", encoding="utf-8") as handle:
                fd = -1
                return validate_record(json.load(handle))
        finally:
            if fd >= 0:
                os.close(fd)

    def read(self, release_id):
        return self._read_path(self.path(release_id))

    def _write(self, path, record, *, create):
        """Durable mutation boundary; never callable without a lease."""
        self.require_lease()
        validate_record(record)
        require_private_dir(self.root)

        expected = self.path(record["release_id"])
        if Path(path) != expected:
            raise ValueError("Evidence destination mismatch")

        fd, temporary = tempfile.mkstemp(
            prefix=".execution-", dir=self.root
        )

        try:
            os.fchmod(fd, 0o600)

            with os.fdopen(fd, "wb") as handle:
                fd = -1
                handle.write(canonical(record) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())

            self.require_lease()

            if create:
                os.link(temporary, path)
            else:
                if path.is_symlink():
                    raise ValueError("Evidence symlink prohibited")
                os.replace(temporary, path)

            sync_dir(self.root)
        finally:
            if fd >= 0:
                os.close(fd)
            if os.path.exists(temporary):
                os.unlink(temporary)

    def prepare(self, attempt, command):
        """Persist PREPARED for an already bound STARTED lab attempt."""
        self.require_lease()

        from rollback_attempt_store import validate_attempt_record

        validate_attempt_record(attempt)
        command.validate()

        if (
            attempt.get("schema_version") != 2
            or attempt["status"] != "STARTED"
            or attempt["project"] != LAB_PROJECT
            or attempt["previous_app"] != PREVIOUS.app
            or attempt["previous_web"] != PREVIOUS.web
            or command != plan_lab_rollback(PREVIOUS)
        ):
            raise ValueError("Attempt and command binding mismatch")

        record = {
            "schema_version": 1,
            "release_id": attempt["release_id"],
            "attempt_id": attempt["attempt_id"],
            "execution_id": attempt["execution_id"],
            "operation_fingerprint": attempt["operation_fingerprint"],
            "command_fingerprint": command_fingerprint(command),
            "project": LAB_PROJECT,
            "phase": PREPARED,
            "pid": None,
            "start_ticks": None,
            "exit_code": None,
        }

        self._write(
            self.path(record["release_id"]), record, create=True
        )
        return record

    def observe(self, release_id, identity):
        self.require_lease()

        if not isinstance(identity, ProcessIdentity):
            raise ValueError("ProcessIdentity required")

        identity.validate()
        current = self.read(release_id)

        if current["phase"] != PREPARED:
            raise ValueError("Process observation cannot be repeated")

        updated = dict(current)
        updated.update({
            "phase": OBSERVED,
            "pid": identity.pid,
            "start_ticks": identity.start_ticks,
        })

        self._write(self.path(release_id), updated, create=False)
        return updated

    def record_exit(self, release_id, exit_code):
        self.require_lease()

        if type(exit_code) is not int or not -255 <= exit_code <= 255:
            raise ValueError("Invalid process exit code")

        current = self.read(release_id)

        if current["phase"] != OBSERVED:
            raise ValueError("Exit requires OBSERVED process")

        updated = dict(current)
        updated.update({
            "phase": EXIT_OBSERVED,
            "exit_code": exit_code,
        })

        self._write(self.path(release_id), updated, create=False)
        return updated

    def assess(self, release_id):
        current = self.read(release_id)
        return EvidenceResult(phase=current["phase"])
