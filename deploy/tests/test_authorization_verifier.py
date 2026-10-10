#!/usr/bin/env python3
"""Tests for production authorization content validation."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from verify_authorization import verify_authorization


class AuthorizationTests(unittest.TestCase):
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
            "approval_reference": "review-test-001",
            "created_at": "2026-10-09T10:00:00Z",
        }

        self.authorization = {
            key: value
            for key, value in self.manifest.items()
            if key != "created_at"
        }

        self.authorization.update({
            "approver": "release-admin",
            "decision": "approved",
            "approved_at": "2026-10-09T12:00:00Z",
            "evidence": {
                "ci_run": (
                    "https://github.com/devnechi/fbwebltd/"
                    "actions/runs/123"
                ),
                "application_attestation": (
                    "https://github.com/devnechi/fbwebltd/"
                    "attestations/app"
                ),
                "web_attestation": (
                    "https://github.com/devnechi/fbwebltd/"
                    "attestations/web"
                ),
            },
        })

    def test_valid_record(self):
        self.assertTrue(
            verify_authorization(self.manifest, self.authorization)
        )

    def test_rejected_decision(self):
        record = copy.deepcopy(self.authorization)
        record["decision"] = "rejected"
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)

    def test_wrong_commit(self):
        record = copy.deepcopy(self.authorization)
        record["commit_sha"] = "f" * 40
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)

    def test_wrong_app_image(self):
        record = copy.deepcopy(self.authorization)
        record["application_image"] = (
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "d" * 64
        )
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)

    def test_missing_approver(self):
        record = copy.deepcopy(self.authorization)
        del record["approver"]
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)

    def test_missing_evidence(self):
        record = copy.deepcopy(self.authorization)
        del record["evidence"]["web_attestation"]
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)

    def test_timestamp_without_timezone(self):
        record = copy.deepcopy(self.authorization)
        record["approved_at"] = "2026-10-09T12:00:00"
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)

    def test_pending_approval_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        record = copy.deepcopy(self.authorization)
        manifest["approval_reference"] = "pending-manual-review"
        record["approval_reference"] = "pending-manual-review"
        with self.assertRaises(ValueError):
            verify_authorization(manifest, record)

    def test_extra_field_rejected(self):
        record = copy.deepcopy(self.authorization)
        record["override"] = True
        with self.assertRaises(ValueError):
            verify_authorization(self.manifest, record)


if __name__ == "__main__":
    unittest.main()
