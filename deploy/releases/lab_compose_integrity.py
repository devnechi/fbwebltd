#!/usr/bin/env python3
"""Strict laboratory Compose-file integrity validation.

No Docker calls, file modifications, execution, or deployment approval.
The approved baseline is intentionally fixed in source control.
"""

from pathlib import Path


LAB_COMPOSE = "deploy/tests/recovery-integration-lab/compose.yml"

APPROVED_COMPOSE = """services:
  app:
    image: ${LAB_APP_IMAGE:?Required}
    entrypoint: ["/bin/sh", "-c"]
    command: ["sleep 600"]
    read_only: true
    cap_drop: ["ALL"]
    security_opt: ["no-new-privileges:true"]
    healthcheck:
      test: ["CMD-SHELL", "true"]
      interval: 2s
      timeout: 2s
      retries: 3

  web:
    image: ${LAB_WEB_IMAGE:?Required}
    entrypoint: ["/bin/sh", "-c"]
    command: ["sleep 600"]
    read_only: true
    cap_drop: ["ALL"]
    security_opt: ["no-new-privileges:true"]
    healthcheck:
      test: ["CMD-SHELL", "true"]
      interval: 2s
      timeout: 2s
      retries: 3

  db:
    image: busybox@sha256:73aaf090f3d85aa34ee199857f03fa3a95c8ede2ffd4cc2cdb5b94e566b11662
    command:
      - sh
      - -c
      - 'test -f /data/marker || echo preserved > /data/marker; sleep 600'
    volumes:
      - db_data:/data
    cap_drop: ["ALL"]
    security_opt: ["no-new-privileges:true"]

volumes:
  db_data:
"""


def validate_lab_compose_integrity(repository_root):
    """Validate the exact approved laboratory Compose configuration.

    This checks repository paths and bytes. It is not a substitute for
    isolating the Docker daemon, controlling environment variables, or
    independently authorizing execution.
    """
    root = Path(repository_root)

    if root.is_symlink() or not root.is_dir():
        raise ValueError("Invalid repository root")

    root = root.resolve(strict=True)
    relative = Path(LAB_COMPOSE)
    current = root

    for component in relative.parts:
        current = current / component

        if current.is_symlink():
            raise ValueError("Compose path contains a symlink")

    if not current.is_file():
        raise ValueError("Laboratory Compose file missing")

    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("Compose file escapes repository")

    actual = current.read_bytes()
    expected = APPROVED_COMPOSE.encode("utf-8")

    if actual != expected:
        raise ValueError(
            "Laboratory Compose content differs from approved baseline"
        )

    return current
