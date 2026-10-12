#!/usr/bin/env python3
"""Gate 4D.22C.3C.4: fail-closed daemon isolation declarations.

Checks a proposed laboratory daemon isolation specification.

A declaration is not evidence that the environment implements it.
Passing policy validation cannot authorize Docker execution.

No subprocess, Docker API call, network access or deployment.
"""

from dataclasses import dataclass
from pathlib import Path
import os
import stat


REQUIRED_CONTROLS = frozenset({
    "dedicated_daemon",
    "private_unix_socket",
    "separate_data_root",
    "production_credentials_absent",
    "production_mounts_absent",
    "production_networks_inaccessible",
    "daemon_privileges_constrained",
    "independent_lifecycle",
})

FORBIDDEN_LOCATIONS = frozenset({
    "/",
    "/var",
    "/var/lib",
    "/var/lib/docker",
    "/run",
    "/var/run",
    "/var/run/docker.sock",
    "/run/docker.sock",
    "/etc",
    "/root",
    "/home",
})


@dataclass(frozen=True)
class LabIsolationDeclaration:
    daemon_name: str
    socket_path: str
    runtime_dir: str
    data_root: str
    controls: tuple


@dataclass(frozen=True)
class LabIsolationAssessment:
    declaration_valid: bool
    missing_controls: tuple
    reason: str
    independent_evidence_verified: bool = False
    daemon_identity_proven: bool = False
    daemon_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _absolute_path(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Nonempty absolute path required")

    path = Path(value)

    if (
        not path.is_absolute()
        or ".." in path.parts
        or str(path) in FORBIDDEN_LOCATIONS
    ):
        raise ValueError("Unsafe or nonabsolute path")

    return path


def assess_lab_isolation(declaration):
    """Evaluate claimed configuration without trusting its truth."""
    if not isinstance(declaration, LabIsolationDeclaration):
        raise ValueError("LabIsolationDeclaration required")

    if declaration.daemon_name != "fbweb-dedicated-lab":
        raise ValueError("Unexpected laboratory daemon name")

    runtime = _absolute_path(declaration.runtime_dir)
    socket = _absolute_path(declaration.socket_path)
    data = _absolute_path(declaration.data_root)

    if (
        socket.parent != runtime
        or socket.name != "docker-lab.sock"
    ):
        raise ValueError("Unexpected laboratory socket location")

    if (
        runtime == data
        or runtime in data.parents
        or data in runtime.parents
    ):
        raise ValueError("Daemon runtime and data roots overlap")

    if (
        str(data).startswith("/var/lib/docker/")
        or str(runtime).startswith("/var/lib/docker/")
        or str(data).startswith("/run/docker/")
        or str(runtime).startswith("/run/docker/")
    ):
        raise ValueError("Host Docker storage overlap prohibited")

    if (
        not isinstance(declaration.controls, tuple)
        or any(
            not isinstance(item, str)
            for item in declaration.controls
        )
        or len(set(declaration.controls)) != len(
            declaration.controls
        )
    ):
        raise ValueError("Invalid isolation control declaration")

    declared = frozenset(declaration.controls)
    unexpected = declared - REQUIRED_CONTROLS

    if unexpected:
        raise ValueError("Unknown isolation control declarations")

    missing = tuple(sorted(REQUIRED_CONTROLS - declared))

    return LabIsolationAssessment(
        declaration_valid=not missing,
        missing_controls=missing,
        reason=(
            "All required controls were declared, but independent "
            "runtime isolation evidence is still required"
            if not missing
            else "Required isolation declarations are incomplete"
        ),
    )


def inspect_private_lab_directory(directory):
    """Read-only inspection of one existing private directory.

    This is supporting evidence only; it does not prove that Docker
    uses the directory or that the daemon is isolated.
    """
    path = _absolute_path(str(directory))

    if path.is_symlink():
        raise ValueError("Directory symlink prohibited")

    info = path.lstat()

    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o700
    ):
        raise ValueError("Private owned directory required")

    return True
