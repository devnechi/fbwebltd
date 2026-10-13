#!/usr/bin/env python3
"""Authorization-aware release controller tests."""

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
            "approval_reference": "review-test-001",
            "created_at": "2026-10-09T10:00:00Z",
        }

        self.approval = {
            key: value
            for key, value in self.manifest.items()
            if key != "created_at"
        }

        self.authorization = {
            **self.approval,
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
        }

    def plan(self, manifest=None, approval=None, authorization=None):
        return build_plan(
            self.manifest if manifest is None else manifest,
            self.approval if approval is None else approval,
            self.authorization if authorization is None else authorization,
        )

    def test_valid_records_produce_dry_run(self):
        plan = self.plan()
        self.assertEqual(plan["mode"], "dry-run")
        self.assertFalse(plan["execution_enabled"])
        self.assertTrue(plan["authorization_validated"])
        self.assertFalse(
            plan["authorization_authenticity_verified"]
        )

    def test_missing_authorization_rejected(self):
        with self.assertRaises(ValueError):
            self.plan(authorization=None if False else {})

    def test_wrong_authorization_commit_rejected(self):
        record = copy.deepcopy(self.authorization)
        record["commit_sha"] = "f" * 40
        with self.assertRaises(ValueError):
            self.plan(authorization=record)

    def test_rejected_decision_rejected(self):
        record = copy.deepcopy(self.authorization)
        record["decision"] = "rejected"
        with self.assertRaises(ValueError):
            self.plan(authorization=record)

    def test_mismatched_approval_rejected(self):
        record = copy.deepcopy(self.approval)
        record["web_image"] = (
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64
        )
        with self.assertRaises(ValueError):
            self.plan(approval=record)

    def test_pending_manifest_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        approval = copy.deepcopy(self.approval)
        authorization = copy.deepcopy(self.authorization)

        for record in (manifest, approval, authorization):
            record["approval_reference"] = "pending-review"

        with self.assertRaises(ValueError):
            self.plan(manifest, approval, authorization)

    def test_mutable_image_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["web_image"] = (
            "ghcr.io/devnechi/fbwebltd-web:latest"
        )
        with self.assertRaises(ValueError):
            self.plan(manifest=manifest)

    def test_plan_preserves_database(self):
        plan = self.plan()
        self.assertTrue(
            any(
                "Preserve database" in operation
                for operation in plan["operations"]
            )
        )


if __name__ == "__main__":
    unittest.main()
