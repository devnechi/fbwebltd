#!/usr/bin/env python3
"""Linux child-start barrier for restricted laboratory processes.

The spawned child waits on an inherited pipe before executing its
fixed, inert test action.

The release decision is made by the parent after durable process
evidence is recorded.

This module does not execute Docker or grant production authorization.
"""

import os
import subprocess
import sys
from dataclasses import dataclass

from docker_process_supervision import (
    ProcessIdentity,
    capture_linux_identity,
    observe_linux_process,
    ProcessStatus,
)


CHILD_PROGRAM = r"""
import os
import sys

fd = int(sys.argv[1])
marker = sys.argv[2]

try:
    signal = os.read(fd, 1)
finally:
    os.close(fd)

if signal != b"R":
    sys.exit(76)

with open(marker, "xb") as handle:
    handle.write(b"RELEASED\n")
    handle.flush()
    os.fsync(handle.fileno())

sys.exit(0)
"""


@dataclass
class BarrierChild:
    process: subprocess.Popen
    identity: ProcessIdentity
    release_fd: int
    released: bool = False

    def close_without_release(self):
        """Close authorization pipe; blocked child receives EOF."""
        if self.release_fd >= 0:
            os.close(self.release_fd)
            self.release_fd = -1

    def release(self):
        """Release exactly once, only while original child is alive."""
        if self.released:
            raise ValueError("Child has already been released")

        if self.release_fd < 0:
            raise ValueError("Barrier already closed")

        if self.process.poll() is not None:
            raise ValueError("Child exited before barrier release")

        assessment = observe_linux_process(self.identity)

        if assessment.status != ProcessStatus.ACTIVE:
            raise ValueError("Original child process is not active")

        try:
            count = os.write(self.release_fd, b"R")
            if count != 1:
                raise ValueError("Barrier release write incomplete")
            self.released = True
        finally:
            self.close_without_release()

    def wait(self, timeout=10):
        return self.process.wait(timeout=timeout)


def spawn_blocked_child(marker):
    """Spawn an inert child waiting for one release byte.

    The child has no access to Docker commands. Parent obtains the
    kernel process identity before returning.

    A crash before the returned identity is persisted is safe for this
    inert child: closing all parent write descriptors yields EOF.
    """
    if not isinstance(marker, str) or not marker:
        raise ValueError("Marker path required")

    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux required")

    read_fd, write_fd = os.pipe()

    try:
        child = subprocess.Popen(
            [
                sys.executable,
                "-c",
                CHILD_PROGRAM,
                str(read_fd),
                marker,
            ],
            pass_fds=(read_fd,),
            close_fds=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except BaseException:
        os.close(read_fd)
        os.close(write_fd)
        raise

    os.close(read_fd)

    try:
        identity = capture_linux_identity(child.pid)
    except BaseException:
        os.close(write_fd)
        child.wait(timeout=10)
        raise

    return BarrierChild(
        process=child,
        identity=identity,
        release_fd=write_fd,
    )
