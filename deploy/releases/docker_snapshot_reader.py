#!/usr/bin/env python3
"""Read-only Docker inspection restricted to FBWeb laboratory projects.

A single Docker observation can be validated against several allowed
image pairs without repeating the inspection.

No container-modifying Docker commands are implemented.
"""

import json
import re
import subprocess

from docker_identity import validate_inspection
from rollback_planner import ImagePair


DOCKER = "/usr/bin/docker"
LAB_PROJECT = re.compile(r"^fbweb-gate[a-z0-9-]*-lab$")
LOCAL_IMAGE_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
CONTAINER_ID = re.compile(r"^[0-9a-f]{12,64}$")


def _validate_project(project):
    if not isinstance(project, str) or not LAB_PROJECT.fullmatch(project):
        raise ValueError(
            "Only isolated FBWeb laboratory projects are allowed"
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


def collect_raw_snapshot(project, runner=None):
    """Collect containers and images once, without deciding image policy."""
    _validate_project(project)

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

    if len(ids) != 3 or len(set(ids)) != 3:
        raise ValueError("Expected exactly three unique lab containers")

    if not all(CONTAINER_ID.fullmatch(value) for value in ids):
        raise ValueError("Invalid container listing")

    containers = _docker_json(
        ["inspect", "--type", "container", *ids],
        runner,
    )

    if len(containers) != 3:
        raise ValueError("Incomplete container inspection")

    image_ids = []

    for item in containers:
        if not isinstance(item, dict):
            raise ValueError("Malformed container inspection")

        image_id = item.get("Image")

        if not isinstance(image_id, str):
            raise ValueError("Missing container image identity")

        if not LOCAL_IMAGE_ID.fullmatch(image_id):
            raise ValueError("Invalid container image identity")

        if image_id not in image_ids:
            image_ids.append(image_id)

    images = _docker_json(
        ["image", "inspect", *image_ids],
        runner,
    )

    return containers, images


def collect_snapshot(project, expected_images, runner=None):
    """Preserve the existing single-pair validation interface."""
    _validate_project(project)

    if not isinstance(expected_images, ImagePair):
        raise ValueError("Expected ImagePair required")

    expected_images.validate()

    containers, images = collect_raw_snapshot(project, runner)

    return validate_inspection(
        containers,
        images,
        project,
        expected_images,
    )


def collect_allowed_snapshot(project, previous, candidate, runner=None):
    """Validate one observation against allowed previous/candidate pairs.

    Both app and web references must belong to the release journal.
    Returns exactly one matching identity or fails closed.
    """
    _validate_project(project)

    if not isinstance(previous, ImagePair):
        raise ValueError("Previous ImagePair required")

    if not isinstance(candidate, ImagePair):
        raise ValueError("Candidate ImagePair required")

    previous.validate()
    candidate.validate()

    if previous == candidate:
        raise ValueError("Identical release image pairs")

    containers, images = collect_raw_snapshot(project, runner)

    allowed_pairs = [
        ImagePair(app, web)
        for app in dict.fromkeys((previous.app, candidate.app))
        for web in dict.fromkeys((previous.web, candidate.web))
    ]

    matches = []

    for pair in allowed_pairs:
        try:
            identity = validate_inspection(
                containers,
                images,
                project,
                pair,
            )
        except ValueError:
            continue

        matches.append(identity)

    if len(matches) != 1:
        raise ValueError(
            "Docker observation does not resolve to one allowed image pair"
        )

    return matches[0]
