#!/usr/bin/env python3
"""Durable recovery records. No Docker or production execution."""

import fcntl
import json
import os
import re
import stat
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from rollback_planner import (
    ImagePair,
    ReleasePlan,
    State,
    next_state,
)


RELEASE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}$")
SCHEMA_VERSION = 1

FIELDS = {
    "schema_version",
    "release_id",
    "revision",
    "state",
    "candidate",
    "previous",
    "updated_at",
}


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def validate_release_id(release_id):
    if not isinstance(release_id, str):
        raise ValueError("Invalid release ID")
    if not RELEASE_ID.fullmatch(release_id):
        raise ValueError("Invalid release ID")


def pair_to_dict(pair):
    if not isinstance(pair, ImagePair):
        raise ValueError("ImagePair required")
    pair.validate()
    return {"app": pair.app, "web": pair.web}


def validate_record(record):
    if not isinstance(record, dict) or set(record) != FIELDS:
        raise ValueError("Invalid recovery journal schema")

    if type(record["schema_version"]) is not int:
        raise ValueError("Invalid schema version")
    if record["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported journal schema")

    validate_release_id(record["release_id"])

    if type(record["revision"]) is not int:
        raise ValueError("Invalid revision")
    if record["revision"] < 0:
        raise ValueError("Invalid revision")

    try:
        State(record["state"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid recovery state") from exc

    for name in ("candidate", "previous"):
        value = record[name]
        if not isinstance(value, dict):
            raise ValueError("Invalid image pair")
        if set(value) != {"app", "web"}:
            raise ValueError("Invalid image pair")
        ImagePair(value["app"], value["web"]).validate()

    if record["candidate"] == record["previous"]:
        raise ValueError("Previous and candidate images are identical")

    value = record["updated_at"]
    if not isinstance(value, str):
        raise ValueError("Invalid timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Timestamp must contain timezone")

    return record


class RecoveryJournal:
    """Restricted, locally locked journal directory.

    The caller must provision a private directory first.
    This component cannot create production authorization.
    """

    def __init__(self, root):
        self.root = Path(root)
        if self.root.is_symlink():
            raise ValueError("Journal directory must not be a symlink")

        info = self.root.stat()
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError("Journal path is not a directory")
        if info.st_uid != os.geteuid():
            raise ValueError("Journal directory owner mismatch")
        if stat.S_IMODE(info.st_mode) != 0o700:
            raise ValueError("Journal directory must have mode 0700")

    def path(self, release_id):
        validate_release_id(release_id)
        return self.root / (release_id + ".json")

    @contextmanager
    def locked(self, release_id):
        validate_release_id(release_id)
        lock_path = self.root / (release_id + ".lock")
        fd = os.open(
            lock_path,
            os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW,
            0o600,
        )
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("Invalid lock file")
            if info.st_uid != os.geteuid():
                raise ValueError("Lock owner mismatch")
            if stat.S_IMODE(info.st_mode) != 0o600:
                raise ValueError("Lock permissions invalid")
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    def _read(self, release_id):
        path = self.path(release_id)
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("Journal must be a regular file")
            if info.st_uid != os.geteuid():
                raise ValueError("Journal owner mismatch")
            if stat.S_IMODE(info.st_mode) != 0o600:
                raise ValueError("Journal permissions invalid")
            with os.fdopen(fd, "r", encoding="utf-8") as handle:
                fd = -1
                record = json.load(handle)
        finally:
            if fd >= 0:
                os.close(fd)

        validate_record(record)
        if record["release_id"] != release_id:
            raise ValueError("Journal release identity mismatch")
        return record

    def read(self, release_id):
        with self.locked(release_id):
            return self._read(release_id)

    def _sync_directory(self):
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _replace(self, release_id, record):
        validate_record(record)
        destination = self.path(release_id)
        if destination.is_symlink():
            raise ValueError("Refusing symlink journal")

        fd, temporary = tempfile.mkstemp(
            prefix=".journal-",
            dir=self.root,
        )
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(record, handle, sort_keys=True, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            fd = -1
            os.replace(temporary, destination)
            self._sync_directory()
        finally:
            if fd >= 0:
                os.close(fd)
            if os.path.exists(temporary):
                os.unlink(temporary)

    def create(self, release_id, candidate, previous):
        validate_release_id(release_id)
        candidate_dict = pair_to_dict(candidate)
        previous_dict = pair_to_dict(previous)
        if candidate_dict == previous_dict:
            raise ValueError("Identical image pairs")

        record = {
            "schema_version": SCHEMA_VERSION,
            "release_id": release_id,
            "revision": 0,
            "state": State.PRECHECK.value,
            "candidate": candidate_dict,
            "previous": previous_dict,
            "updated_at": timestamp(),
        }

        with self.locked(release_id):
            destination = self.path(release_id)
            if destination.exists() or destination.is_symlink():
                raise FileExistsError("Recovery journal already exists")

            # Reserve the name to prevent accidental reuse.
            fd = os.open(
                destination,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
                0o600,
            )
            os.close(fd)
            self._sync_directory()
            self._replace(release_id, record)

        return record

    def advance(self, release_id, expected_revision, event, plan=None):
        with self.locked(release_id):
            record = self._read(release_id)

            if type(expected_revision) is not int:
                raise ValueError("Invalid expected revision")
            if record["revision"] != expected_revision:
                raise ValueError("Stale journal revision")

            if plan is not None:
                if not isinstance(plan, ReleasePlan):
                    raise ValueError("ReleasePlan required")
                if pair_to_dict(plan.candidate) != record["candidate"]:
                    raise ValueError("Candidate identity mismatch")
                if pair_to_dict(plan.previous) != record["previous"]:
                    raise ValueError("Previous identity mismatch")

            new_state = next_state(record["state"], event, plan)
            updated = dict(record)
            updated["state"] = new_state.value
            updated["revision"] += 1
            updated["updated_at"] = timestamp()
            self._replace(release_id, updated)
            return updated

    def interrupted(self, release_id):
        record = self.read(release_id)
        terminal = {
            State.SUCCEEDED.value,
            State.ABORTED.value,
            State.ROLLED_BACK.value,
            State.RECOVERY_FAILED.value,
        }
        return record["state"] not in terminal
