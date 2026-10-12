#!/usr/bin/env python3
"""Durable laboratory rollback failure evidence.

Records caller-reported failure observations in exclusive event files.
Does not execute Docker, authorize retries, or change journal states.
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
from rollback_planner import State


EVENT_NAME = re.compile(r"^[0-9]{6}\.json$")
KINDS = {
    "RESTORATION_COMMAND_FAILED",
    "HEALTH_CHECK_FAILED",
    "INSPECTION_FAILED",
    "DATABASE_IDENTITY_MISMATCH",
    "CONTROLLER_INTERRUPTED",
}


class RollbackFailureLedger:
    def __init__(self, simulator):
        if not isinstance(simulator, RecoverySimulator):
            raise ValueError("RecoverySimulator required")

        self.simulator = simulator
        self.root = simulator.journal.root / "failure-events"

        if self.root.is_symlink():
            raise ValueError("Failure directory cannot be a symlink")

        info = self.root.stat()

        if not stat.S_ISDIR(info.st_mode):
            raise ValueError("Failure directory must be a directory")

        if info.st_uid != os.geteuid():
            raise ValueError("Failure directory owner mismatch")

        if stat.S_IMODE(info.st_mode) != 0o700:
            raise ValueError("Failure directory must have mode 0700")

    def _directory(self, release_id):
        self.simulator.journal.path(release_id)
        return self.root / release_id

    def _read_unlocked(self, release_id):
        directory = self._directory(release_id)

        if not directory.exists():
            return []

        if directory.is_symlink():
            raise ValueError("Failure release directory is a symlink")

        info = directory.stat()

        if (
            not stat.S_ISDIR(info.st_mode)
            or info.st_uid != os.geteuid()
            or stat.S_IMODE(info.st_mode) != 0o700
        ):
            raise ValueError("Invalid failure release directory")

        events = []

        for path in sorted(directory.iterdir()):
            if not EVENT_NAME.fullmatch(path.name):
                raise ValueError("Unexpected failure evidence file")

            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)

            try:
                info = os.fstat(fd)

                if (
                    not stat.S_ISREG(info.st_mode)
                    or info.st_uid != os.geteuid()
                    or stat.S_IMODE(info.st_mode) != 0o600
                ):
                    raise ValueError("Invalid failure evidence permissions")

                with os.fdopen(fd, "r", encoding="utf-8") as handle:
                    fd = -1
                    event = json.load(handle)
            finally:
                if fd >= 0:
                    os.close(fd)

            if set(event) != {
                "release_id", "sequence", "journal_revision",
                "kind", "reason", "recorded_at",
            }:
                raise ValueError("Malformed failure evidence")

            expected_sequence = len(events) + 1

            if (
                type(event["sequence"]) is not int
                or event["sequence"] != expected_sequence
                or path.name != f"{expected_sequence:06d}.json"
                or event["release_id"] != release_id
                or type(event["journal_revision"]) is not int
                or event["journal_revision"] < 0
                or event["kind"] not in KINDS
                or not isinstance(event["reason"], str)
                or not 1 <= len(event["reason"]) <= 300
                or not isinstance(event["recorded_at"], str)
            ):
                raise ValueError("Invalid failure evidence content")

            try:
                recorded = datetime.fromisoformat(event["recorded_at"])
                if recorded.utcoffset() is None:
                    raise ValueError("Timestamp requires timezone")
            except (TypeError, ValueError) as exc:
                raise ValueError("Invalid failure timestamp") from exc

            events.append(event)

        return events

    def read(self, release_id):
        with deployment_lock(self.simulator.lock_dir):
            self.simulator.journal.read(release_id)
            return self._read_unlocked(release_id)

    def record(self, release_id, kind, reason):
        """Record one reported failure while journal is ROLLING_BACK."""
        if kind not in KINDS:
            raise ValueError("Unrecognized failure kind")

        if (
            not isinstance(reason, str)
            or not 1 <= len(reason) <= 300
            or not reason.strip()
        ):
            raise ValueError("Reason must contain 1-300 characters")

        # No credentials, tokens, or sensitive Docker output in reasons.
        with deployment_lock(self.simulator.lock_dir):
            record = self.simulator.journal.read(release_id)

            if record["state"] != State.ROLLING_BACK.value:
                raise ValueError("Failure record requires ROLLING_BACK")

            directory = self._directory(release_id)

            if not directory.exists() and not directory.is_symlink():
                directory.mkdir(mode=0o700)

            events = self._read_unlocked(release_id)
            sequence = len(events) + 1

            if sequence > 999999:
                raise ValueError("Failure evidence sequence exhausted")

            event = {
                "release_id": release_id,
                "sequence": sequence,
                "journal_revision": record["revision"],
                "kind": kind,
                "reason": reason,
                "recorded_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

            fd, temporary = tempfile.mkstemp(
                prefix=".failure-",
                dir=directory,
            )

            try:
                os.fchmod(fd, 0o600)

                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    fd = -1
                    json.dump(event, handle, sort_keys=True)
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())

                destination = directory / f"{sequence:06d}.json"

                # Exclusive publication: never replace an existing event.
                os.link(temporary, destination)

                dirfd = os.open(
                    directory,
                    os.O_RDONLY | os.O_DIRECTORY,
                )

                try:
                    os.fsync(dirfd)
                finally:
                    os.close(dirfd)

            finally:
                if fd >= 0:
                    os.close(fd)
                if os.path.exists(temporary):
                    os.unlink(temporary)

            return event
