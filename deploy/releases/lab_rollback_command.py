#!/usr/bin/env python3
"""Non-executing Docker restoration contract for Gate 4D.16AE.

This module does not grant authorization, call Docker, access the
production Compose project, or modify the recovery journal.
"""

from dataclasses import dataclass
from pathlib import Path

from rollback_planner import ImagePair


LAB_PROJECT = "fbweb-gate16ae-lab"

LAB_COMPOSE = (
    "deploy/tests/recovery-integration-lab/compose.yml"
)

PREVIOUS = ImagePair(
    "ghcr.io/devnechi/fbwebltd-app@sha256:"
    "5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a",
    "ghcr.io/devnechi/fbwebltd-web@sha256:"
    "964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4",
)


@dataclass(frozen=True)
class LabRollbackCommand:
    project: str
    compose_file: str
    images: ImagePair
    argv: tuple
    environment: tuple

    def validate(self):
        PREVIOUS.validate()

        if self.project != LAB_PROJECT:
            raise ValueError("Unauthorized laboratory project")

        if self.compose_file != LAB_COMPOSE:
            raise ValueError("Unauthorized Compose file")

        if type(self.argv) is not tuple:
            raise ValueError("Command must be immutable")

        if type(self.environment) is not tuple:
            raise ValueError("Environment must be immutable")

        if not isinstance(self.images, ImagePair):
            raise ValueError("ImagePair required")

        self.images.validate()

        if self.images != PREVIOUS:
            raise ValueError("Unauthorized restoration image pair")

        expected_argv = (
            "/usr/bin/docker",
            "compose",
            "-p",
            LAB_PROJECT,
            "-f",
            LAB_COMPOSE,
            "up",
            "-d",
            "--no-deps",
            "--no-build",
            "--pull",
            "never",
            "--force-recreate",
            "app",
            "web",
        )

        if self.argv != expected_argv:
            raise ValueError("Unauthorized Docker restoration command")

        expected_environment = (
            ("LAB_APP_IMAGE", PREVIOUS.app),
            ("LAB_WEB_IMAGE", PREVIOUS.web),
        )

        if self.environment != expected_environment:
            raise ValueError("Unauthorized image environment")

        return True


def plan_lab_rollback(images, project=LAB_PROJECT):
    """Return a validated, non-executing laboratory command."""
    if not isinstance(images, ImagePair):
        raise ValueError("ImagePair required")

    command = LabRollbackCommand(
        project=project,
        compose_file=LAB_COMPOSE,
        images=images,
        argv=(
            "/usr/bin/docker",
            "compose",
            "-p",
            LAB_PROJECT,
            "-f",
            LAB_COMPOSE,
            "up",
            "-d",
            "--no-deps",
            "--no-build",
            "--pull",
            "never",
            "--force-recreate",
            "app",
            "web",
        ),
        environment=(
            ("LAB_APP_IMAGE", images.app),
            ("LAB_WEB_IMAGE", images.web),
        ),
    )

    command.validate()
    return command


def validate_lab_compose_file(repository_root):
    """Basic path checks, not a Compose content security audit."""
    root = Path(repository_root).resolve(strict=True)
    path = root / LAB_COMPOSE

    if path.is_symlink() or not path.is_file():
        raise ValueError("Laboratory Compose file unavailable")

    if not path.resolve(strict=True).is_relative_to(root):
        raise ValueError("Compose file escapes repository")

    return path


def execution_enabled():
    return False
