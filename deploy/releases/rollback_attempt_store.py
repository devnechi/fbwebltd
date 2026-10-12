#!/usr/bin/env python3
"""Durable, laboratory-only rollback attempt storage.

No Docker execution, production authorization, or journal transitions.

Only FAILED and INTERRUPTED may be recorded by this component.
SUCCEEDED is reserved for a future verified restoration coordinator.
"""

import json
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from deployment_lock import deployment_lock
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import Attempt, AttemptStatus
from rollback_planner import State


FILE_PATTERN = re.compile(r"^[0-9]{6}\.json$")
MAX_ATTEMPTS = 999999
FIELDS = {
    "attempt_id",
    "release_id",
    "status",
    "revision",
    "journal_revision",
    "created_at",
    "updated_at",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def validate_private_directory(path):
    if path.is_symlink():
        raise ValueError("Attempt directory is a symlink")

    info = path.stat()

    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o700
    ):
        raise ValueError("Invalid attempt directory")

    return path


def validate_attempt_record(record):
    if not isinstance(record, dict) or set(record) != FIELDS:
        raise ValueError("Invalid attempt record schema")

    Attempt(
        record["attempt_id"],
        AttemptStatus(record["status"]),
    ).validate()

    if not isinstance(record["release_id"], str):
        raise ValueError("Invalid release identity")

    if (
        type(record["revision"]) is not int
        or record["revision"] < 0
        or type(record["journal_revision"]) is not int
        or record["journal_revision"] < 0
    ):
        raise ValueError("Invalid attempt revision")

    for key in ("created_at", "updated_at"):
        if not isinstance(record[key], str):
            raise ValueError("Invalid attempt timestamp")
        parsed = datetime.fromisoformat(record[key])
        if parsed.utcoffset() is None:
            raise ValueError("Attempt timestamp must include timezone")

    return record


class RollbackAttemptStore:
    """Persist restoration attempts under the global deployment lock."""

    def __init__(self, simulator):
        if not isinstance(simulator, RecoverySimulator):
            raise ValueError("RecoverySimulator required")

        self.simulator = simulator
        self.root = simulator.journal.root / "rollback-attempts"

        with deployment_lock(simulator.lock_dir):
            if not self.root.exists() and not self.root.is_symlink():
                self.root.mkdir(mode=0o700)
                sync_directory(simulator.journal.root)

            validate_private_directory(self.root)

    def directory(self, release_id):
        self.simulator.journal.path(release_id)
        return self.root / release_id

    def _ensure_directory(self, release_id):
        directory = self.directory(release_id)

        if not directory.exists() and not directory.is_symlink():
            directory.mkdir(mode=0o700)
            sync_directory(self.root)

        return validate_private_directory(directory)

    def _read_unlocked(self, release_id):
        directory = self.directory(release_id)

        if not directory.exists() and not directory.is_symlink():
            return []

        validate_private_directory(directory)
        records = []

        for path in sorted(directory.iterdir()):
            # A crash before atomic publication may leave a temporary
            # file. It is not a published attempt.
            if path.name.startswith(".attempt-"):
                if path.is_symlink() or not path.is_file():
                    raise ValueError("Invalid temporary attempt file")
                continue

            if not FILE_PATTERN.fullmatch(path.name):
                raise ValueError("Unexpected attempt file")

            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)

            try:
                info = os.fstat(fd)

                if (
                    not stat.S_ISREG(info.st_mode)
                    or info.st_uid != os.geteuid()
                    or stat.S_IMODE(info.st_mode) != 0o600
                ):
                    raise ValueError("Invalid attempt file permissions")

                with os.fdopen(fd, "r", encoding="utf-8") as handle:
                    fd = -1
                    record = json.load(handle)
            finally:
                if fd >= 0:
                    os.close(fd)

            validate_attempt_record(record)

            sequence = len(records) + 1
            expected_id = f"attempt-{sequence:06d}"

            if (
                path.name != f"{sequence:06d}.json"
                or record["attempt_id"] != expected_id
                or record["release_id"] != release_id
            ):
                raise ValueError("Attempt identity or sequence mismatch")

            records.append(record)

        active = sum(
            record["status"] == AttemptStatus.STARTED.value
            for record in records
        )

        if active > 1:
            raise ValueError("Multiple unfinished restoration attempts")

        return records

    def read(self, release_id):
        with deployment_lock(self.simulator.lock_dir):
            self.simulator.journal.read(release_id)
            return self._read_unlocked(release_id)

    def _write(self, directory, destination, record, replace):
        fd, temporary = tempfile.mkstemp(
            prefix=".attempt-",
            dir=directory,
        )

        try:
            os.fchmod(fd, 0o600)

            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                fd = -1
                json.dump(record, handle, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())

            if replace:
                if destination.is_symlink():
                    raise ValueError("Refusing attempt symlink")
                os.replace(temporary, destination)
            else:
                os.link(temporary, destination)

            sync_directory(directory)

        finally:
            if fd >= 0:
                os.close(fd)
            if os.path.exists(temporary):
                os.unlink(temporary)

    def begin(self, release_id):
        """Persist STARTED before any restoration execution."""
        with deployment_lock(self.simulator.lock_dir):
            journal = self.simulator.journal.read(release_id)

            if journal["state"] != State.ROLLING_BACK.value:
                raise ValueError("Journal must be ROLLING_BACK")

            self.simulator.read_checkpoint(release_id, journal)
            records = self._read_unlocked(release_id)

            if any(
                record["status"] == AttemptStatus.STARTED.value
                for record in records
            ):
                raise ValueError("Unfinished attempt requires reconciliation")

            sequence = len(records) + 1

            if sequence > MAX_ATTEMPTS:
                raise ValueError("Attempt sequence exhausted")

            directory = self._ensure_directory(release_id)
            timestamp = now()

            record = {
                "attempt_id": f"attempt-{sequence:06d}",
                "release_id": release_id,
                "status": AttemptStatus.STARTED.value,
                "revision": 0,
                "journal_revision": journal["revision"],
                "created_at": timestamp,
                "updated_at": timestamp,
            }

            validate_attempt_record(record)

            destination = directory / f"{sequence:06d}.json"
            self._write(directory, destination, record, replace=False)

            return record

    def finish(self, release_id, attempt_id, expected_revision, status):
        """Record FAILED or INTERRUPTED with revision protection."""
        if status not in (
            AttemptStatus.FAILED,
            AttemptStatus.INTERRUPTED,
        ):
            raise ValueError("Only FAILED or INTERRUPTED permitted")

        if type(expected_revision) is not int:
            raise ValueError("Invalid expected revision")

        with deployment_lock(self.simulator.lock_dir):
            journal = self.simulator.journal.read(release_id)

            if journal["state"] != State.ROLLING_BACK.value:
                raise ValueError("Journal must be ROLLING_BACK")

            records = self._read_unlocked(release_id)
            matching = [
                (index, record)
                for index, record in enumerate(records, start=1)
                if record["attempt_id"] == attempt_id
            ]

            if len(matching) != 1:
                raise ValueError("Unknown attempt ID")

            sequence, record = matching[0]

            if (
                record["revision"] != expected_revision
                or record["status"] != AttemptStatus.STARTED.value
            ):
                raise ValueError("Stale or completed attempt")

            updated = dict(record)
            updated["status"] = status.value
            updated["revision"] += 1
            updated["updated_at"] = now()

            validate_attempt_record(updated)

            directory = self.directory(release_id)
            destination = directory / f"{sequence:06d}.json"

            self._write(directory, destination, updated, replace=True)

            return updated

    def policy_attempts(self, release_id):
        """Return validated attempts for the pure retry policy."""
        return [
            Attempt(
                attempt_id=record["attempt_id"],
                status=AttemptStatus(record["status"]),
            )
            for record in self.read(release_id)
        ]
