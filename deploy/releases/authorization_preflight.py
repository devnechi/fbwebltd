#!/usr/bin/env python3
"""Non-writing administrative authorization preflight."""

import argparse
import json
import os
import pwd
import sys
from pathlib import Path

from validate_manifest import validate


AUTHORIZED_ADMIN = "samurai"


def check_preflight(manifest, actor, is_root, sudo_identity_valid):
    validate(manifest)

    if not is_root:
        raise ValueError("Administrative execution required")

    if not sudo_identity_valid or actor != AUTHORIZED_ADMIN:
        raise ValueError("Unauthorized administrator identity")

    if manifest["approval_reference"].startswith("pending-"):
        raise ValueError("Release is still pending review")

    return {
        "release_id": manifest["release_id"],
        "administrator": actor,
        "identity_check": "passed",
        "authorization_issued": False,
        "evidence_verified": False,
        "production_activation_enabled": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        # SUDO_UID is trusted only after entry through the
        # administrator-controlled sudo mechanism.
        if os.geteuid() != 0 or os.getuid() != 0:
            raise ValueError("Run through sudo from an administrator account")

        sudo_uid = os.environ.get("SUDO_UID", "")
        if not sudo_uid.isdecimal():
            raise ValueError("Missing sudo administrator identity")

        sudo_uid = int(sudo_uid)

        if sudo_uid == 0:
            raise ValueError("Direct root invocation is not accepted")

        actor = pwd.getpwuid(sudo_uid).pw_name
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

        result = check_preflight(
            manifest,
            actor,
            is_root=True,
            sudo_identity_valid=True,
        )

    except (OSError, KeyError, ValueError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    print("PASS: Administrative identity preflight")
    print("NO AUTHORIZATION ISSUED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
