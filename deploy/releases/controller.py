#!/usr/bin/env python3
"""Future Basics release controller: validation and dry-run only."""

import argparse
import json
import sys
from pathlib import Path

from validate_manifest import validate
from verify_approval import verify


def build_plan(manifest, approval):
    verify(manifest, approval)

    return {
        "mode": "dry-run",
        "release_id": manifest["release_id"],
        "commit_sha": manifest["commit_sha"],
        "application_image": manifest["application_image"],
        "web_image": manifest["web_image"],
        "approval_reference": manifest["approval_reference"],
        "operations": [
            "Verify exact application and web image digests",
            "Record previously approved image pair",
            "Preserve MySQL database and persistent volumes",
            "Activate application and web images only",
            "Verify application health and public HTTPS",
            "Restore previous approved image pair if activation fails",
        ],
        "execution_enabled": False,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Future Basics release without deploying it"
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--approval-dir",
        type=Path,
        default=Path("/etc/fbweb-deploy/approvals"),
    )
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        validate(manifest)

        approval_path = args.approval_dir / (
            manifest["release_id"] + ".json"
        )

        approval = json.loads(
            approval_path.read_text(encoding="utf-8")
        )

        plan = build_plan(manifest, approval)

    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, indent=2))
    print("PASS: Approved release matches trusted record")
    print("DRY RUN ONLY: No Docker operations executed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
