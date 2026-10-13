#!/usr/bin/env python3
"""Exclusive deployment lock with an explicit active lease.

A lease establishes cooperative lock ownership inside this Python
process. It is not deployment authorization or Docker isolation.
"""

import fcntl
import os
import stat
import threading
from contextlib import contextmanager
from pathlib import Path


LOCK_NAME = "deployment.lock"


def _validate_directory(directory):
    directory = Path(directory)

    if directory.is_symlink():
        raise ValueError("Lock directory cannot be a symlink")

    info = directory.stat()

    if not stat.S_ISDIR(info.st_mode):
        raise ValueError("Lock directory must be a directory")

    if info.st_uid != os.geteuid():
        raise ValueError("Lock directory owner mismatch")

    if stat.S_IMODE(info.st_mode) != 0o700:
        raise ValueError("Lock directory must have mode 0700")

    return directory


class DeploymentLease:
    """Non-transferable, process-local lease for one lock context."""

    __slots__ = ("_directory", "_pid", "_thread", "_active")

    def __init__(self, directory):
        self._directory = Path(directory).resolve(strict=True)
        self._pid = os.getpid()
        self._thread = threading.get_ident()
        self._active = True

    def require(self, directory):
        if (
            not self._active
            or os.getpid() != self._pid
            or threading.get_ident() != self._thread
            or Path(directory).resolve(strict=True) != self._directory
        ):
            raise RuntimeError("Active matching deployment lease required")

        return True

    def _invalidate(self):
        self._active = False


@contextmanager
def deployment_lock(directory):
    """Acquire and hold the exclusive, nonblocking deployment lock."""
    directory = _validate_directory(directory)

    fd = os.open(
        directory / LOCK_NAME,
        os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW,
        0o600,
    )

    acquired = False
    lease = None

    try:
        info = os.fstat(fd)

        if not stat.S_ISREG(info.st_mode):
            raise ValueError("Lock must be a regular file")

        if info.st_uid != os.geteuid():
            raise ValueError("Lock file owner mismatch")

        if stat.S_IMODE(info.st_mode) != 0o600:
            raise ValueError("Lock file must have mode 0600")

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(
                "Another deployment or recovery operation is active"
            ) from exc

        acquired = True
        lease = DeploymentLease(directory)

        try:
            yield lease
        finally:
            lease._invalidate()

    finally:
        if acquired:
            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
