#!/usr/bin/env python3
"""Validate Docker inspection snapshots without executing Docker.

This module verifies internal consistency between container image IDs,
locally inspected image metadata, registry digest references, and Compose
ownership labels.

Local Docker metadata is not independent registry or provenance proof.
"""

import re
from dataclasses import dataclass

from rollback_planner import ImagePair

IMAGE_ID_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
CONTAINER_ID_PATTERN = re.compile(r"^[0-9a-f]{64}$")

SERVICES = ("app", "web", "db")


@dataclass(frozen=True)
class VerifiedIdentity:
    project: str
    app_reference: str
    web_reference: str
    db_container_id: str
    app_container_id: str
    web_container_id: str
    app_healthy: bool
    web_healthy: bool


def _require_dict(value, description):
    if not isinstance(value, dict):
        raise ValueError(description + " must be an object")
    return value


def _require_image_id(value):
    if not isinstance(value, str) or not IMAGE_ID_PATTERN.fullmatch(value):
        raise ValueError("Invalid local image ID")
    return value


def _require_container_id(value):
    if not isinstance(value, str) or not CONTAINER_ID_PATTERN.fullmatch(value):
        raise ValueError("Invalid container ID")
    return value


def _container(containers, project, service):
    matches = []

    for value in containers:
        item = _require_dict(value, "Container")
        labels = _require_dict(
            item.get("Config", {}).get("Labels"),
            "Container labels",
        )

        if (
            labels.get("com.docker.compose.project") == project
            and labels.get("com.docker.compose.service") == service
        ):
            matches.append(item)

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one container for service " + service
        )

    item = matches[0]

    if item.get("State", {}).get("Running") is not True:
        raise ValueError(service + " container is not running")

    _require_container_id(item.get("Id"))
    _require_image_id(item.get("Image"))

    return item


def _resolve_image(images, container, required_reference):
    """Match container image ID to exactly one inspected local image."""
    image_id = container["Image"]

    matches = [
        item for item in images
        if isinstance(item, dict) and item.get("Id") == image_id
    ]

    if len(matches) != 1:
        raise ValueError("Missing or ambiguous local image metadata")

    metadata = matches[0]
    _require_image_id(metadata.get("Id"))

    digests = metadata.get("RepoDigests")

    if not isinstance(digests, list):
        raise ValueError("Missing registry digest metadata")

    if required_reference not in digests:
        raise ValueError("Required registry digest is not present")

    configured = container.get("Config", {}).get("Image")

    if configured != required_reference:
        raise ValueError(
            "Container was not created using the required digest reference"
        )

    return required_reference


def validate_inspection(
    containers,
    images,
    project,
    expected_images,
):
    """Validate a single externally collected Docker inspection snapshot.

    Inputs must be collected by a future trusted, read-only Docker adapter.
    No Docker commands are executed here.
    """
    if not isinstance(project, str) or not project.strip():
        raise ValueError("Invalid Compose project")

    if not isinstance(containers, list) or not isinstance(images, list):
        raise ValueError("Inspection collections must be lists")

    if not isinstance(expected_images, ImagePair):
        raise ValueError("Expected ImagePair required")

    expected_images.validate()

    app = _container(containers, project, "app")
    web = _container(containers, project, "web")
    db = _container(containers, project, "db")

    ids = [app["Id"], web["Id"], db["Id"]]

    if len(set(ids)) != 3:
        raise ValueError("Duplicate container identities")

    app_reference = _resolve_image(
        images, app, expected_images.app
    )
    web_reference = _resolve_image(
        images, web, expected_images.web
    )

    def healthy(item):
        status = item.get("State", {}).get("Health", {}).get("Status")
        if status not in ("healthy", "unhealthy", "starting"):
            raise ValueError("Missing or invalid health status")
        return status == "healthy"

    return VerifiedIdentity(
        project=project,
        app_reference=app_reference,
        web_reference=web_reference,
        db_container_id=db["Id"],
        app_container_id=app["Id"],
        web_container_id=web["Id"],
        app_healthy=healthy(app),
        web_healthy=healthy(web),
    )
