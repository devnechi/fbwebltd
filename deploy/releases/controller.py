#!/usr/bin/env python3
"""Future Basics release controller: authorization-aware dry-run only."""

import argparse
import json
import sys
from pathlib import Path

from validate_manifest import validate
from verify_approval import verify
from verify_authorization import verify_authorization


DEFAULT_APPROVAL_DIR = Path("/etc/fbweb-deploy/approvals")
DEFAULT_AUTHORIZATION_DIR = Path("/etc/fbweb-deploy/authorizations")


def build_plan(manifest, approval, authorization):
    """Build a plan only when both records validate."""
    validate(manifest)
    verify(manifest, approval)
    verify_authorization(manifest, authorization)

    return {
        "mode": "dry-run",
        "release_id": manifest["release_id"],
        "commit_sha": manifest["commit_sha"],
        "application_image": manifest["application_image"],
        "web_image": manifest["web_image"],
        "approval_reference": manifest["approval_reference"],
        "authorization_required": True,
        "authorization_validated": True,
        "authorization_authenticity_verified": False,
        "operations": [
            "Verify image provenance independently",
            "Confirm authorized production approval",
            "Record previous approved image pair",
            "Preserve database and persistent volumes",
            "Activate application and web only",
            "Check application and public HTTPS health",
            "Restore previous pair if activation fails",
        ],
        "execution_enabled": False,
    }


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main():
    parser = argparse.ArgumentParser(
        description="Validate an authorized release without deploying"
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--approval-dir",
        type=Path,
        default=DEFAULT_APPROVAL_DIR,
    )
    parser.add_argument(
        "--authorization-dir",
        type=Path,
        default=DEFAULT_AUTHORIZATION_DIR,
    )
    args = parser.parse_args()

    try:
        manifest = load_json(args.manifest)
        validate(manifest)

        release_id = manifest["release_id"]

        approval = load_json(
            args.approval_dir / (release_id + ".json")
        )
        authorization = load_json(
            args.authorization_dir / (release_id + ".json")
        )

        plan = build_plan(
            manifest,
            approval,
            authorization,
        )

    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, indent=2))
    print("PASS: Release records passed content validation")
    print("NOTE: Approver authenticity is NOT established")
    print("DRY RUN ONLY: No Docker operations executed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
