#!/usr/bin/env python3
"""Tests for the dry-run Future Basics release controller."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from controller import build_plan


class ReleaseControllerTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "release_id": "fbweb-test-001",
            "repository": "devnechi/fbwebltd",
            "commit_sha": "a" * 40,
            "application_image": (
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "b" * 64
            ),
            "web_image": (
                "ghcr.io/devnechi/fbwebltd-web@sha256:" + "c" * 64
            ),
            "approval_reference": "approved-test-001",
            "created_at": "2026-10-09T12:00:00Z",
        }
        self.approval = {
            key: value
            for key, value in self.manifest.items()
            if key != "created_at"
        }

    def test_valid_release_produces_dry_run(self):
        plan = build_plan(self.manifest, self.approval)

        self.assertEqual(plan["mode"], "dry-run")
        self.assertFalse(plan["execution_enabled"])
        self.assertEqual(
            plan["release_id"],
            self.manifest["release_id"],
        )

    def test_unapproved_release_rejected(self):
        approval = copy.deepcopy(self.approval)
        approval["commit_sha"] = "f" * 40

        with self.assertRaises(ValueError):
            build_plan(self.manifest, approval)

    def test_mutable_image_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["web_image"] = "ghcr.io/devnechi/fbwebltd-web:latest"

        with self.assertRaises(ValueError):
            build_plan(manifest, self.approval)

    def test_plan_preserves_database(self):
        plan = build_plan(self.manifest, self.approval)

        self.assertTrue(
            any(
                "Preserve MySQL" in operation
                for operation in plan["operations"]
            )
        )


if __name__ == "__main__":
    unittest.main()
