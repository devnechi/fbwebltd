#!/usr/bin/env python3
"""Exclusive deployment lock. No Docker execution."""

import fcntl
import os
import stat
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


@contextmanager
def deployment_lock(directory):
    """Acquire a single exclusive nonblocking deployment lock.

    The caller must keep this context active throughout activation,
    health verification, rollback and final journal updates.
    """
    directory = _validate_directory(directory)

    fd = os.open(
        directory / LOCK_NAME,
        os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW,
        0o600,
    )

    acquired = False

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
        yield

    finally:
        if acquired:
            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
