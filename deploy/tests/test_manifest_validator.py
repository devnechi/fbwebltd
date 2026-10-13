#!/usr/bin/env python3
"""Tests for the structural release manifest validator."""

import copy
import datetime
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from validate_manifest import validate


class ManifestValidationTests(unittest.TestCase):
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
            "approval_reference": "test-only",
            "created_at": "2026-10-09T12:00:00Z",
        }

    def test_valid_manifest(self):
        self.assertTrue(validate(self.manifest))

    def test_wrong_repository(self):
        data = copy.deepcopy(self.manifest)
        data["repository"] = "attacker/other"
        with self.assertRaises(ValueError):
            validate(data)

    def test_mutable_application_tag(self):
        data = copy.deepcopy(self.manifest)
        data["application_image"] = "ghcr.io/devnechi/fbwebltd-app:latest"
        with self.assertRaises(ValueError):
            validate(data)

    def test_unapproved_web_registry(self):
        data = copy.deepcopy(self.manifest)
        data["web_image"] = "evil.example/web@sha256:" + "c" * 64
        with self.assertRaises(ValueError):
            validate(data)

    def test_short_commit(self):
        data = copy.deepcopy(self.manifest)
        data["commit_sha"] = "a" * 7
        with self.assertRaises(ValueError):
            validate(data)

    def test_missing_approval_reference(self):
        data = copy.deepcopy(self.manifest)
        del data["approval_reference"]
        with self.assertRaises(ValueError):
            validate(data)

    def test_extra_field(self):
        data = copy.deepcopy(self.manifest)
        data["execute_command"] = "docker system prune"
        with self.assertRaises(ValueError):
            validate(data)

    def test_timestamp_without_timezone(self):
        data = copy.deepcopy(self.manifest)
        data["created_at"] = "2026-10-09T12:00:00"
        with self.assertRaises(ValueError):
            validate(data)

    def test_non_string_field(self):
        data = copy.deepcopy(self.manifest)
        data["release_id"] = 42
        with self.assertRaises(ValueError):
            validate(data)


if __name__ == "__main__":
    unittest.main()
