#!/usr/bin/env python3
"""Tests for release approval matching."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from verify_approval import verify


class ApprovalVerifierTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "release_id": "fbweb-test-001",
            "repository": "devnechi/fbwebltd",
            "commit_sha": "a" * 40,
            "application_image": "ghcr.io/devnechi/fbwebltd-app@sha256:" + "b" * 64,
            "web_image": "ghcr.io/devnechi/fbwebltd-web@sha256:" + "c" * 64,
            "approval_reference": "approved-test-001",
            "created_at": "2026-10-09T12:00:00Z",
        }

        self.approval = {
            key: value
            for key, value in self.manifest.items()
            if key != "created_at"
        }

    def test_matching_approval(self):
        self.assertTrue(verify(self.manifest, self.approval))

    def test_different_commit(self):
        approval = copy.deepcopy(self.approval)
        approval["commit_sha"] = "f" * 40
        with self.assertRaises(ValueError):
            verify(self.manifest, approval)

    def test_different_app_digest(self):
        approval = copy.deepcopy(self.approval)
        approval["application_image"] = (
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "d" * 64
        )
        with self.assertRaises(ValueError):
            verify(self.manifest, approval)

    def test_different_web_digest(self):
        approval = copy.deepcopy(self.approval)
        approval["web_image"] = (
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "e" * 64
        )
        with self.assertRaises(ValueError):
            verify(self.manifest, approval)

    def test_missing_approval_field(self):
        approval = copy.deepcopy(self.approval)
        del approval["approval_reference"]
        with self.assertRaises(ValueError):
            verify(self.manifest, approval)

    def test_unexpected_approval_field(self):
        approval = copy.deepcopy(self.approval)
        approval["extra"] = "unexpected"
        with self.assertRaises(ValueError):
            verify(self.manifest, approval)

    def test_invalid_manifest(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["application_image"] = "ghcr.io/devnechi/fbwebltd-app:latest"
        with self.assertRaises(ValueError):
            verify(manifest, self.approval)


if __name__ == "__main__":
    unittest.main()
