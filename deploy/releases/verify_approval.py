#!/usr/bin/env python3
"""Compare a validated release manifest with a trusted approval record."""

import argparse
import json
import sys
from pathlib import Path

from validate_manifest import validate


REQUIRED_APPROVAL_FIELDS = {
    "release_id",
    "repository",
    "commit_sha",
    "application_image",
    "web_image",
    "approval_reference",
}


def verify(manifest, approval):
    validate(manifest)

    if not isinstance(approval, dict):
        raise ValueError("Approval must be a JSON object")

    if set(approval) != REQUIRED_APPROVAL_FIELDS:
        raise ValueError("Invalid approval record fields")

    for field in REQUIRED_APPROVAL_FIELDS:
        if approval[field] != manifest[field]:
            raise ValueError(f"Approval mismatch: {field}")

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("approval", type=Path)
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        approval = json.loads(args.approval.read_text(encoding="utf-8"))
        verify(manifest, approval)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: Release matches trusted approval record")
    print("NOTE: Record provenance and image build authenticity require separate checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
