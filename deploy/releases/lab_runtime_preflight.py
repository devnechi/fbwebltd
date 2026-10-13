#!/usr/bin/env python3
"""Gate 4D.22C.3D.1: read-only Linux Docker environment preflight.

Inspects local executable paths, socket metadata, environment
variable names, user namespace settings and rootless prerequisites.

Does not execute Docker, connect to sockets, invoke systemctl,
change configuration, or authorize a deployment.
"""

from pathlib import Path
import json
import os
import shutil
import stat
import sys


EXECUTABLES = (
    "docker",
    "dockerd",
    "dockerd-rootless.sh",
    "rootlesskit",
    "newuidmap",
    "newgidmap",
    "slirp4netns",
    "fuse-overlayfs",
)

ENVIRONMENT_KEYS = (
    "DOCKER_HOST",
    "DOCKER_CONTEXT",
    "DOCKER_CONFIG",
    "DOCKER_CERT_PATH",
    "DOCKER_TLS_VERIFY",
    "COMPOSE_PROJECT_NAME",
    "COMPOSE_FILE",
    "XDG_RUNTIME_DIR",
)


def inspect_path(path):
    """Inspect path metadata without opening sockets."""
    path = Path(path)

    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"exists": False}
    except OSError as exc:
        return {
            "exists": None,
            "error_type": type(exc).__name__,
        }

    mode = info.st_mode

    if stat.S_ISSOCK(mode):
        kind = "socket"
    elif stat.S_ISDIR(mode):
        kind = "directory"
    elif stat.S_ISLNK(mode):
        kind = "symlink"
    elif stat.S_ISREG(mode):
        kind = "regular_file"
    else:
        kind = "other"

    return {
        "exists": True,
        "kind": kind,
        "uid": info.st_uid,
        "gid": info.st_gid,
        "mode": oct(stat.S_IMODE(mode)),
        "device": info.st_dev,
        "inode": info.st_ino,
    }


def inspect_user_namespace():
    path = Path("/proc/sys/kernel/unprivileged_userns_clone")

    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError:
        return "unavailable"

    return value if value in ("0", "1") else "unexpected"


def inspect_subordinate_ids(filename):
    path = Path(filename)

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return {"readable": False}

    username = os.environ.get("USER", "")

    # Report only whether a matching mapping exists.
    # Do not disclose mappings for other local users.
    matching = [
        line for line in lines
        if line.split(":", 1)[0] == username
    ]

    return {
        "readable": True,
        "current_user_mapping_present": bool(matching),
    }


def collect():
    uid = os.getuid()

    xdg = os.environ.get(
        "XDG_RUNTIME_DIR", f"/run/user/{uid}"
    )

    return {
        "gate": "4D.22C.3D.1",
        "mode": "read-only",
        "platform": sys.platform,
        "uid": uid,
        "executables": {
            name: shutil.which(name)
            for name in EXECUTABLES
        },
        "paths": {
            path: inspect_path(path)
            for path in (
                "/var/run/docker.sock",
                "/run/docker.sock",
                f"/run/user/{uid}/docker.sock",
                str(Path(xdg) / "docker.sock"),
                str(Path(xdg) / "docker-lab.sock"),
            )
        },
        "environment_presence": {
            key: key in os.environ
            for key in ENVIRONMENT_KEYS
        },
        "user_namespace_setting": inspect_user_namespace(),
        "subuid": inspect_subordinate_ids("/etc/subuid"),
        "subgid": inspect_subordinate_ids("/etc/subgid"),
        "docker_daemon_isolation_proven": False,
        "docker_execution_permitted": False,
        "production_execution_enabled": False,
        "automatic_retry_permitted": False,
        "manual_verification_required": True,
    }


def main():
    print(json.dumps(
        collect(),
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
