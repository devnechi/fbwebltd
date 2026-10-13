#!/usr/bin/env python3
"""Non-executing Compose command planner for isolated release tests."""

from dataclasses import dataclass
from pathlib import Path

from rollback_planner import ImagePair


ALLOWED_SERVICES = ("app", "web")
FORBIDDEN_OPTIONS = (
    "--build",
    "--remove-orphans",
    "--volumes",
    "--renew-anon-volumes",
)

@dataclass(frozen=True)
class ComposeCommand:
    argv: tuple
    images: ImagePair

    def validate(self):
        self.images.validate()

        if not isinstance(self.argv, tuple):
            raise ValueError("Command arguments must be a tuple")

        expected = (
            "/usr/bin/docker",
            "compose",
            "-f",
            "compose.release.yml",
            "up",
            "--detach",
            "--no-deps",
            "--no-build",
            "--pull",
            "never",
            "--force-recreate",
            "app",
            "web",
        )

        if self.argv != expected:
            raise ValueError("Unauthorized Compose command")

        if any(option in self.argv for option in FORBIDDEN_OPTIONS):
            raise ValueError("Forbidden Compose option")

        return True


def activation_command(images):
    """Return an immutable, non-executing command specification."""
    if not isinstance(images, ImagePair):
        raise ValueError("ImagePair required")

    images.validate()

    command = ComposeCommand(
        argv=(
            "/usr/bin/docker",
            "compose",
            "-f",
            "compose.release.yml",
            "up",
            "--detach",
            "--no-deps",
            "--no-build",
            "--pull",
            "never",
            "--force-recreate",
            "app",
            "web",
        ),
        images=images,
    )

    command.validate()
    return command


def compose_environment(command):
    """Return only non-secret image selections.

    The real environment must be supplied separately by a
    future trusted executor. Never replace the process environment
    with only these values when executing Compose.
    """
    command.validate()

    return {
        "FBWEB_APP_IMAGE": command.images.app,
        "FBWEB_WEB_IMAGE": command.images.web,
    }


def inspect_compose_file(path):
    """Perform basic file-location checks, not a YAML security audit."""
    path = Path(path)

    if path.name != "compose.release.yml":
        raise ValueError("Unexpected Compose filename")

    if not path.is_file() or path.is_symlink():
        raise ValueError("Compose file must be a regular file")

    return True


def execution_enabled():
    return False
