#!/usr/bin/env python3
"""Integrated, simulation-only recovery coordinator.

No Docker calls, deployment commands, approval issuance, or
production execution capabilities.
"""

import json
import os
import stat
import tempfile
from pathlib import Path

from deployment_lock import deployment_lock
from recovery_journal import RecoveryJournal, validate_record
from recovery_reconciler import (
    ContainerSnapshot,
    RecoveryAction,
    reconcile,
)


def validate_checkpoint(checkpoint, record):
    validate_record(record)

    if not isinstance(checkpoint, dict):
        raise ValueError("Recovery checkpoint required")

    expected_fields = {
        "release_id",
        "previous",
        "candidate",
        "db_identity",
    }

    if set(checkpoint) != expected_fields:
        raise ValueError("Invalid checkpoint fields")

    if checkpoint["release_id"] != record["release_id"]:
        raise ValueError("Checkpoint release mismatch")

    if checkpoint["previous"] != record["previous"]:
        raise ValueError("Checkpoint previous image mismatch")

    if checkpoint["candidate"] != record["candidate"]:
        raise ValueError("Checkpoint candidate image mismatch")

    identity = checkpoint["db_identity"]

    if not isinstance(identity, str) or not identity.strip():
        raise ValueError("Invalid database identity")

    if len(identity) > 256:
        raise ValueError("Database identity too long")

    return True


class RecoverySimulator:
    """Coordinate simulated recovery under a global lock."""

    def __init__(self, journal_dir, lock_dir):
        self.journal = RecoveryJournal(journal_dir)
        self.lock_dir = Path(lock_dir)

    def checkpoint_path(self, release_id):
        self.journal.path(release_id)
        return self.journal.root / (release_id + ".checkpoint.json")

    def create_checkpoint(self, release_id, db_identity):
        """Create checkpoint before activation, without overwriting."""
        with deployment_lock(self.lock_dir):
            record = self.journal.read(release_id)

            if record["state"] != "PRECHECK":
                raise ValueError("Checkpoint must precede activation")

            checkpoint = {
                "release_id": release_id,
                "previous": record["previous"],
                "candidate": record["candidate"],
                "db_identity": db_identity,
            }

            validate_checkpoint(checkpoint, record)

            destination = self.checkpoint_path(release_id)

            if destination.exists() or destination.is_symlink():
                raise FileExistsError("Checkpoint already exists")

            fd, temporary = tempfile.mkstemp(
                prefix=".checkpoint-",
                dir=self.journal.root,
            )

            try:
                os.fchmod(fd, 0o600)

                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    fd = -1
                    json.dump(checkpoint, handle, sort_keys=True)
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())

                os.link(temporary, destination)
                self.journal._sync_directory()

            finally:
                if fd >= 0:
                    os.close(fd)
                if os.path.exists(temporary):
                    os.unlink(temporary)

            return checkpoint

    def read_checkpoint(self, release_id, record):
        path = self.checkpoint_path(release_id)

        fd = os.open(
            path,
            os.O_RDONLY | os.O_NOFOLLOW,
        )

        try:
            info = os.fstat(fd)

            if not stat.S_ISREG(info.st_mode):
                raise ValueError("Checkpoint must be a regular file")

            if info.st_uid != os.geteuid():
                raise ValueError("Checkpoint ownership mismatch")

            if stat.S_IMODE(info.st_mode) != 0o600:
                raise ValueError("Checkpoint permissions invalid")

            with os.fdopen(fd, "r", encoding="utf-8") as handle:
                fd = -1
                checkpoint = json.load(handle)

        finally:
            if fd >= 0:
                os.close(fd)

        validate_checkpoint(checkpoint, record)
        return checkpoint

    def decide(self, release_id, snapshot):
        """Return a recovery decision. Never execute the decision."""
        with deployment_lock(self.lock_dir):
            record = self.journal.read(release_id)
            checkpoint = self.read_checkpoint(release_id, record)

            if not isinstance(snapshot, ContainerSnapshot):
                raise ValueError("Simulated container snapshot required")

            action = reconcile(
                record,
                snapshot,
                checkpoint["db_identity"],
            )

            return {
                "mode": "simulation-only",
                "release_id": release_id,
                "state": record["state"],
                "revision": record["revision"],
                "action": action.value,
                "database_identity_matched": (
                    snapshot.db_identity == checkpoint["db_identity"]
                ),
                "docker_executed": False,
                "production_execution_enabled": False,
            }
