#!/usr/bin/env python3
"""Strict read-only view of durable laboratory rollback attempts.

Caller must hold the global deployment lock. No directory creation,
Docker calls, journal mutation or execution.
"""

import os
import re
import stat
import json
from pathlib import Path

from rollback_attempt_policy import Attempt, AttemptStatus
from rollback_attempt_store import validate_attempt_record
from recovery_simulator import RecoverySimulator


FILE_NAME = re.compile(r"^[0-9]{6}\.json$")


def _private_directory(path):
    if path.is_symlink():
        raise ValueError("Attempt directory symlink prohibited")

    info = path.stat()

    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o700
    ):
        raise ValueError("Invalid attempt directory")

    return path


def read_attempts_locked(simulator, release_id):
    """Read attempt history without acquiring another global lock.

    This function must only be called while deployment_lock is held.
    It does not prove that condition itself.
    """
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    simulator.journal.path(release_id)

    root = simulator.journal.root / "rollback-attempts"

    if not root.exists() and not root.is_symlink():
        return []

    _private_directory(root)

    directory = root / release_id

    if not directory.exists() and not directory.is_symlink():
        return []

    _private_directory(directory)

    records = []

    for path in sorted(directory.iterdir()):
        # Unpublished temporary files may remain after a crash.
        if path.name.startswith(".attempt-"):
            if path.is_symlink():
                raise ValueError("Temporary attempt symlink prohibited")
            info = path.stat()
            if (
                not stat.S_ISREG(info.st_mode)
                or info.st_uid != os.geteuid()
                or stat.S_IMODE(info.st_mode) != 0o600
            ):
                raise ValueError("Invalid temporary attempt file")
            continue

        if not FILE_NAME.fullmatch(path.name):
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

        if (
            path.name != f"{sequence:06d}.json"
            or record["attempt_id"] != f"attempt-{sequence:06d}"
            or record["release_id"] != release_id
        ):
            raise ValueError("Attempt sequence mismatch")

        records.append(record)

    active_count = sum(
        record["status"] == AttemptStatus.STARTED.value
        for record in records
    )

    if active_count > 1:
        raise ValueError("Multiple unfinished attempts")

    return [
        Attempt(
            attempt_id=record["attempt_id"],
            status=AttemptStatus(record["status"]),
        )
        for record in records
    ]
