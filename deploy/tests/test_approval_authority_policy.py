#!/usr/bin/env python3
"""Gate 4D.21C: fail-closed environment and authorization tests."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from approval_authority_policy import (
    assess_environment,
    assess_release_authority,
)


FINGERPRINT = "a" * 64


def protected_environment():
    return {
        "name": "production",
        "prevent_self_review": True,
        "can_admins_bypass": False,
        "deployment_branch_policy": {
            "protected_branches": True,
            "custom_branch_policies": False,
        },
        "protection_rules": [
            {
                "type": "required_reviewers",
                "reviewers": [
                    {
                        "type": "User",
                        "reviewer": {
                            "login": "independent-reviewer",
                            "id": 987654,
                        },
                    },
                ],
            },
        ],
    }


class ApprovalAuthorityPolicyTests(unittest.TestCase):
    def test_protected_environment_controls_valid(self):
        self.assertEqual(
            assess_environment(protected_environment()),
            (),
        )

    def test_missing_reviewers_rejected(self):
        payload = protected_environment()
        payload["protection_rules"] = []
        self.assertTrue(assess_environment(payload))

    def test_empty_reviewer_list_rejected(self):
        payload = protected_environment()
        payload["protection_rules"][0]["reviewers"] = []
        self.assertTrue(assess_environment(payload))

    def test_self_review_rejected(self):
        payload = protected_environment()
        payload["prevent_self_review"] = False
        self.assertTrue(assess_environment(payload))

    def test_admin_bypass_rejected(self):
        payload = protected_environment()
        payload["can_admins_bypass"] = True
        self.assertTrue(assess_environment(payload))

    def test_missing_branch_policy_rejected(self):
        payload = protected_environment()
        payload["deployment_branch_policy"] = None
        self.assertTrue(assess_environment(payload))

    def test_unrestricted_branch_policy_rejected(self):
        payload = protected_environment()
        payload["deployment_branch_policy"] = {
            "protected_branches": False,
            "custom_branch_policies": False,
        }
        self.assertTrue(assess_environment(payload))

    def test_wrong_environment_rejected(self):
        payload = protected_environment()
        payload["name"] = "staging"
        self.assertTrue(assess_environment(payload))

    def test_duplicate_reviewer_rejected(self):
        payload = protected_environment()
        entry = deepcopy(payload["protection_rules"][0]["reviewers"][0])
        payload["protection_rules"][0]["reviewers"].append(entry)
        self.assertTrue(assess_environment(payload))

    def test_invalid_fingerprint_rejected(self):
        result = assess_release_authority(
            protected_environment(), "invalid"
        )
        self.assertFalse(result.authorization_granted)
        self.assertTrue(result.reasons)

    def test_missing_environment_rejected(self):
        with self.assertRaises(ValueError):
            assess_environment(None)

    def test_real_audit_configuration_rejected(self):
        observed = {
            "name": "production",
            "prevent_self_review": None,
            "can_admins_bypass": True,
            "deployment_branch_policy": None,
            "protection_rules": [],
        }

        result = assess_release_authority(observed, FINGERPRINT)

        self.assertFalse(result.environment_controls_valid)
        self.assertFalse(result.authorization_granted)

    def test_perfect_controls_are_not_approval(self):
        result = assess_release_authority(
            protected_environment(), FINGERPRINT
        )

        self.assertTrue(result.environment_controls_valid)
        self.assertFalse(result.authorization_granted)
        self.assertIn(
            "No independently verified approval bound to this exact release",
            result.reasons,
        )

    def test_fake_approval_fields_are_ignored(self):
        payload = protected_environment()
        payload["approved"] = True
        payload["approval_verified"] = True
        payload["approver"] = "independent-reviewer"

        result = assess_release_authority(payload, FINGERPRINT)

        self.assertFalse(result.authorization_granted)


if __name__ == "__main__":
    unittest.main()
