#!/usr/bin/env python3
"""Gate 4D.22C.3C.3: non-executing endpoint continuity evidence.

Detects observable changes in the laboratory Unix socket and
its parent directory between two inspections.

No connection to Docker, subprocess creation, or authorization.
Stable filesystem identity is NOT proof of daemon isolation.
"""

from dataclasses import dataclass
from pathlib import Path
import os
import stat

from sealed_lab_launch_contract import validate_private_lab_socket


@dataclass(frozen=True)
class EndpointSnapshot:
    path: str
    runtime_path: str
    socket_device: int
    socket_inode: int
    socket_owner: int
    socket_mode: int
    runtime_device: int
    runtime_inode: int
    runtime_owner: int
    runtime_mode: int
    socket_ctime_ns: int = 0
    runtime_ctime_ns: int = 0


@dataclass(frozen=True)
class EndpointContinuityAssessment:
    unchanged: bool
    reason: str
    daemon_identity_proven: bool = False
    daemon_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def capture_endpoint_snapshot(socket_path, runtime_dir):
    """Read filesystem identity without connecting to the endpoint."""
    socket_path = Path(socket_path)
    runtime_dir = Path(runtime_dir)

    validate_private_lab_socket(socket_path, runtime_dir)

    before_socket = socket_path.lstat()
    before_runtime = runtime_dir.lstat()

    # Recheck paths to detect concurrent substitutions.
    validate_private_lab_socket(socket_path, runtime_dir)

    after_socket = socket_path.lstat()
    after_runtime = runtime_dir.lstat()

    if (
        (
            before_socket.st_dev,
            before_socket.st_ino,
            before_socket.st_ctime_ns,
        )
        != (
            after_socket.st_dev,
            after_socket.st_ino,
            after_socket.st_ctime_ns,
        )
        or (
            before_runtime.st_dev,
            before_runtime.st_ino,
            before_runtime.st_ctime_ns,
        )
        != (
            after_runtime.st_dev,
            after_runtime.st_ino,
            after_runtime.st_ctime_ns,
        )
    ):
        raise ValueError("Endpoint changed during inspection")

    if (
        not stat.S_ISSOCK(after_socket.st_mode)
        or not stat.S_ISDIR(after_runtime.st_mode)
        or after_socket.st_uid != os.geteuid()
        or after_runtime.st_uid != os.geteuid()
        or stat.S_IMODE(after_socket.st_mode) != 0o600
        or stat.S_IMODE(after_runtime.st_mode) != 0o700
    ):
        raise ValueError("Endpoint security attributes invalid")

    return EndpointSnapshot(
        path=str(socket_path),
        runtime_path=str(runtime_dir),
        socket_device=after_socket.st_dev,
        socket_inode=after_socket.st_ino,
        socket_owner=after_socket.st_uid,
        socket_mode=stat.S_IMODE(after_socket.st_mode),
        runtime_device=after_runtime.st_dev,
        runtime_inode=after_runtime.st_ino,
        runtime_owner=after_runtime.st_uid,
        runtime_mode=stat.S_IMODE(after_runtime.st_mode),
        socket_ctime_ns=after_socket.st_ctime_ns,
        runtime_ctime_ns=after_runtime.st_ctime_ns,
    )


def assess_endpoint_continuity(previous, current):
    """Compare two snapshots without treating equality as trust."""
    if (
        not isinstance(previous, EndpointSnapshot)
        or not isinstance(current, EndpointSnapshot)
    ):
        raise ValueError("EndpointSnapshot values required")

    unchanged = previous == current

    return EndpointContinuityAssessment(
        unchanged=unchanged,
        reason=(
            "Observed socket and runtime identities unchanged; "
            "daemon isolation still unverified"
            if unchanged
            else "Endpoint changed; laboratory launch must remain blocked"
        ),
    )


def inspect_endpoint_continuity(previous, socket_path, runtime_dir):
    """Capture a fresh snapshot and compare it with the baseline."""
    if not isinstance(previous, EndpointSnapshot):
        raise ValueError("EndpointSnapshot required")

    current = capture_endpoint_snapshot(socket_path, runtime_dir)
    return assess_endpoint_continuity(previous, current)
