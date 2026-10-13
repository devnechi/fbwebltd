#!/usr/bin/env python3
"""Gate 4D.22C.3C.1: sealed, non-executing lab launch contract.

An exact command and environment are necessary but not sufficient
for safe Docker execution. A dedicated Docker daemon must be
independently provisioned and verified.

No subprocess, Docker API call or deployment is performed.
"""

from dataclasses import dataclass
from pathlib import Path
import os
import stat

from lab_compose_integrity import validate_lab_compose_integrity
from lab_rollback_command import PREVIOUS, plan_lab_rollback


REQUIRED_SOCKET_NAME = "docker-lab.sock"
FORBIDDEN_SOCKET = "/var/run/docker.sock"


@dataclass(frozen=True)
class SealedLabLaunch:
    argv: tuple
    environment: tuple
    repository_root: str
    docker_host: str
    compose_file: str
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False


def validate_private_lab_socket(socket_path, lab_runtime_dir):
    """Inspect a proposed dedicated socket without connecting to it."""
    runtime = Path(lab_runtime_dir)
    socket = Path(socket_path)

    if runtime.is_symlink() or socket.is_symlink():
        raise ValueError("Symlink in laboratory endpoint")

    if (
        not runtime.is_absolute()
        or not socket.is_absolute()
        or socket.name != REQUIRED_SOCKET_NAME
        or socket.parent != runtime
    ):
        raise ValueError("Unexpected laboratory Docker endpoint")

    runtime_info = runtime.stat()

    if (
        not stat.S_ISDIR(runtime_info.st_mode)
        or runtime_info.st_uid != os.geteuid()
        or stat.S_IMODE(runtime_info.st_mode) != 0o700
    ):
        raise ValueError("Private laboratory runtime directory required")

    socket_info = socket.lstat()

    if (
        not stat.S_ISSOCK(socket_info.st_mode)
        or socket_info.st_uid != os.geteuid()
        or stat.S_IMODE(socket_info.st_mode) != 0o600
    ):
        raise ValueError("Private owned Unix Docker socket required")

    if str(socket) == FORBIDDEN_SOCKET:
        raise ValueError("Host Docker daemon prohibited")

    return "unix://" + str(socket)


def seal_lab_launch(
    repository_root,
    lab_runtime_dir,
    socket_path,
    *,
    ambient_environment=None,
):
    """Construct a fixed launch description without starting a child."""
    command = plan_lab_rollback(PREVIOUS)
    command.validate()

    root = Path(repository_root)

    if root.is_symlink() or not root.is_dir():
        raise ValueError("Invalid repository root")

    root = root.resolve(strict=True)
    compose = validate_lab_compose_integrity(root)

    docker_host = validate_private_lab_socket(
        socket_path, lab_runtime_dir
    )

    ambient = (
        dict(os.environ)
        if ambient_environment is None
        else dict(ambient_environment)
    )

    forbidden = {
        "DOCKER_HOST",
        "DOCKER_CONTEXT",
        "DOCKER_CONFIG",
        "DOCKER_CERT_PATH",
        "DOCKER_TLS_VERIFY",
        "COMPOSE_PROJECT_NAME",
        "COMPOSE_FILE",
        "COMPOSE_PROFILES",
        "COMPOSE_ENV_FILES",
        "COMPOSE_DISABLE_ENV_FILE",
        "LAB_APP_IMAGE",
        "LAB_WEB_IMAGE",
        "BASH_ENV",
        "ENV",
        "PYTHONPATH",
        "LD_PRELOAD",
        "LD_LIBRARY_PATH",
    }

    if forbidden.intersection(ambient):
        raise ValueError(
            "Ambient execution environment contains forbidden overrides"
        )

    environment = (
        ("PATH", "/usr/bin:/bin"),
        ("HOME", str(root)),
        ("DOCKER_HOST", docker_host),
        ("DOCKER_CONFIG", str(root / ".docker-lab-config")),
        ("LAB_APP_IMAGE", PREVIOUS.app),
        ("LAB_WEB_IMAGE", PREVIOUS.web),
    )

    return SealedLabLaunch(
        argv=command.argv,
        environment=environment,
        repository_root=str(root),
        docker_host=docker_host,
        compose_file=str(compose),
    )
