#!/usr/bin/env python3
"""Validate Future Basics immutable release manifest structure."""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

REPOSITORY = "devnechi/fbwebltd"
APP_IMAGE = "ghcr.io/devnechi/fbwebltd-app"
WEB_IMAGE = "ghcr.io/devnechi/fbwebltd-web"

FIELDS = {
    "release_id",
    "repository",
    "commit_sha",
    "application_image",
    "web_image",
    "approval_reference",
    "created_at",
}

SHA256 = r"[0-9a-f]{64}"


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("Manifest must be a JSON object")

    if set(data) != FIELDS:
        missing = sorted(FIELDS - set(data))
        extra = sorted(set(data) - FIELDS)
        raise ValueError(f"Unexpected manifest fields: missing={missing}, extra={extra}")

    if any(not isinstance(value, str) for value in data.values()):
        raise ValueError("All manifest fields must be strings")

    if data["repository"] != REPOSITORY:
        raise ValueError("Incorrect repository")

    if not re.fullmatch(r"[0-9a-f]{40}", data["commit_sha"]):
        raise ValueError("Invalid Git commit SHA")

    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{2,79}", data["release_id"]):
        raise ValueError("Invalid release ID")

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/#-]{2,199}", data["approval_reference"]):
        raise ValueError("Invalid approval reference")

    for field, image in (
        ("application_image", APP_IMAGE),
        ("web_image", WEB_IMAGE),
    ):
        if not re.fullmatch(re.escape(image) + r"@sha256:" + SHA256, data[field]):
            raise ValueError(f"Invalid immutable image reference: {field}")

    try:
        timestamp = datetime.datetime.fromisoformat(
            data["created_at"].replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError("Invalid creation timestamp") from exc

    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("Creation timestamp requires timezone")

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: Release manifest structure valid")
    print("NOTE: Release approval and image authenticity are NOT verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
