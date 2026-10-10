#!/usr/bin/env python3
"""Read-only Docker inspection for isolated FBWeb laboratory projects.

This module cannot deploy, restart, delete, or modify containers.
Production Compose projects are deliberately prohibited.
"""

import json
import re
import subprocess

from docker_identity import validate_inspection
from rollback_planner import ImagePair


DOCKER = "/usr/bin/docker"

LAB_PROJECT = re.compile(
    r"^fbweb-gate[a-z0-9-]*-lab$"
)


def _docker_json(argv, runner):
    result = runner(
        [DOCKER, *argv],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )

    try:
        value = json.loads(result.stdout)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid Docker JSON response") from exc

    if not isinstance(value, list):
        raise ValueError("Docker inspection must return a list")

    return value


def collect_snapshot(project, expected_images, runner=None):
    """Collect and validate read-only laboratory Docker metadata."""
    if not isinstance(project, str):
        raise ValueError("Invalid project")

    if not LAB_PROJECT.fullmatch(project):
        raise ValueError(
            "Only isolated fbweb-gate laboratory projects are allowed"
        )

    if not isinstance(expected_images, ImagePair):
        raise ValueError("Expected ImagePair required")

    expected_images.validate()

    if runner is None:
        runner = subprocess.run

    result = runner(
        [
            DOCKER,
            "ps",
            "--all",
            "--filter",
            "label=com.docker.compose.project=" + project,
            "--format",
            "{{.ID}}",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )

    ids = result.stdout.splitlines()

    if len(ids) != 3:
        raise ValueError(
            "Expected exactly three laboratory containers"
        )

    if len(set(ids)) != 3:
        raise ValueError("Duplicate container listing")

    if not all(re.fullmatch(r"[0-9a-f]{12,64}", x) for x in ids):
        raise ValueError("Invalid listed container identity")

    containers = _docker_json(
        ["inspect", "--type", "container", *ids],
        runner,
    )

    if len(containers) != 3:
        raise ValueError("Incomplete container inspection")

    image_ids = []

    for container in containers:
        if not isinstance(container, dict):
            raise ValueError("Malformed container inspection")

        image_id = container.get("Image")

        if not isinstance(image_id, str):
            raise ValueError("Missing container image ID")

        if image_id not in image_ids:
            image_ids.append(image_id)

    images = _docker_json(
        ["image", "inspect", *image_ids],
        runner,
    )

    return validate_inspection(
        containers,
        images,
        project,
        expected_images,
    )
