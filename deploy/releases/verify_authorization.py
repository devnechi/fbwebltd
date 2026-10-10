#!/usr/bin/env python3
"""Validate the content of a production release authorization.

This module does not establish the authenticity of the approver.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

from validate_manifest import validate


FIELDS = {
    "release_id",
    "repository",
    "commit_sha",
    "application_image",
    "web_image",
    "approval_reference",
    "approver",
    "decision",
    "approved_at",
    "evidence",
}

MATCH_FIELDS = {
    "release_id",
    "repository",
    "commit_sha",
    "application_image",
    "web_image",
    "approval_reference",
}


def verify_authorization(manifest, authorization):
    validate(manifest)

    if not isinstance(authorization, dict):
        raise ValueError("Authorization must be a JSON object")

    if set(authorization) != FIELDS:
        raise ValueError("Invalid authorization record fields")

    for field in MATCH_FIELDS:
        if authorization[field] != manifest[field]:
            raise ValueError(f"Authorization mismatch: {field}")

    if authorization["decision"] != "approved":
        raise ValueError("Release is not approved")

    if manifest["approval_reference"].startswith("pending-"):
        raise ValueError("Pending approval reference is not authorization")

    approver = authorization["approver"]
    if not isinstance(approver, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._@-]{2,127}", approver
    ):
        raise ValueError("Invalid approver identity")

    timestamp = authorization["approved_at"]
    if not isinstance(timestamp, str):
        raise ValueError("Invalid approval timestamp")

    try:
        parsed = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError("Invalid approval timestamp") from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Approval timestamp requires timezone")

    evidence = authorization["evidence"]
    if not isinstance(evidence, dict) or set(evidence) != {
        "ci_run",
        "application_attestation",
        "web_attestation",
    }:
        raise ValueError("Incomplete authorization evidence")

    for key, value in evidence.items():
        if not isinstance(value, str) or not value.startswith(
            "https://github.com/devnechi/fbwebltd/"
        ):
            raise ValueError(f"Invalid evidence reference: {key}")

    return True


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: verify_authorization.py MANIFEST AUTHORIZATION",
            file=sys.stderr,
        )
        return 2

    try:
        manifest = json.loads(Path(sys.argv[1]).read_text())
        authorization = json.loads(Path(sys.argv[2]).read_text())
        verify_authorization(manifest, authorization)
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: Authorization record content valid")
    print("NOTE: Approver authenticity has NOT been verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
