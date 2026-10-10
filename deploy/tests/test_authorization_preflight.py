#!/usr/bin/env python3
"""Tests for administrative authorization preflight."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from authorization_preflight import check_preflight


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "release_id": "fbweb-test-001",
            "repository": "devnechi/fbwebltd",
            "commit_sha": "a" * 40,
            "application_image":
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "b" * 64,
            "web_image":
                "ghcr.io/devnechi/fbwebltd-web@sha256:" + "c" * 64,
            "approval_reference": "review-test-001",
            "created_at": "2026-10-10T09:00:00Z",
        }

    def check(self, actor="samurai", root=True, sudo_valid=True):
        return check_preflight(
            self.manifest, actor, root, sudo_valid
        )

    def test_authorized_admin_preflight(self):
        result = self.check()
        self.assertFalse(result["authorization_issued"])
        self.assertFalse(result["evidence_verified"])
        self.assertFalse(result["production_activation_enabled"])

    def test_fbdeploy_rejected(self):
        with self.assertRaises(ValueError):
            self.check(actor="fbdeploy")

    def test_unprivileged_execution_rejected(self):
        with self.assertRaises(ValueError):
            self.check(root=False)

    def test_untrusted_identity_rejected(self):
        with self.assertRaises(ValueError):
            self.check(sudo_valid=False)

    def test_pending_release_rejected(self):
        self.manifest["approval_reference"] = "pending-review"
        with self.assertRaises(ValueError):
            self.check()

    def test_mutable_image_rejected(self):
        self.manifest["application_image"] = (
            "ghcr.io/devnechi/fbwebltd-app:latest"
        )
        with self.assertRaises(ValueError):
            self.check()


if __name__ == "__main__":
    unittest.main()
