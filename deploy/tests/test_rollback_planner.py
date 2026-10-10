#!/usr/bin/env python3
"""State transition and failure-boundary tests for rollback planning."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from rollback_planner import (
    ImagePair,
    ReleasePlan,
    State,
    execution_policy,
    next_state,
)


class RollbackPlannerTests(unittest.TestCase):

    def setUp(self):
        self.plan = ReleasePlan(
            candidate=ImagePair(
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
                "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
            ),
            previous=ImagePair(
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
                "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
            ),
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

    def test_successful_lifecycle(self):
        state = State.PRECHECK
        for event in (
            "precheck_passed",
            "activate",
            "activated",
            "healthy",
        ):
            state = next_state(state, event, self.plan)

        self.assertEqual(state, State.SUCCEEDED)

    def test_activation_failure_rolls_back(self):
        state = next_state(State.ACTIVATING, "failed")
        self.assertEqual(state, State.ROLLING_BACK)
        self.assertEqual(
            next_state(state, "restored"),
            State.ROLLED_BACK,
        )

    def test_health_timeout_rolls_back(self):
        self.assertEqual(
            next_state(State.VERIFYING, "timeout"),
            State.ROLLING_BACK,
        )

    def test_rollback_failure_requires_intervention(self):
        self.assertEqual(
            next_state(State.ROLLING_BACK, "failed"),
            State.RECOVERY_FAILED,
        )

    def test_precheck_failure_aborts(self):
        self.assertEqual(
            next_state(State.PRECHECK, "precheck_failed"),
            State.ABORTED,
        )

    def test_missing_approval_blocks_activation(self):
        invalid = replace(self.plan, approval_verified=False)
        with self.assertRaises(ValueError):
            next_state(State.READY, "activate", invalid)

    def test_missing_provenance_blocks_activation(self):
        invalid = replace(self.plan, provenance_verified=False)
        with self.assertRaises(ValueError):
            next_state(State.READY, "activate", invalid)

    def test_missing_recovery_record_blocks_activation(self):
        invalid = replace(
            self.plan, recovery_record_persisted=False
        )
        with self.assertRaises(ValueError):
            next_state(State.READY, "activate", invalid)

    def test_missing_backup_blocks_activation(self):
        invalid = replace(self.plan, backup_verified=False)
        with self.assertRaises(ValueError):
            next_state(State.READY, "activate", invalid)

    def test_missing_lock_blocks_activation(self):
        invalid = replace(
            self.plan, deployment_lock_acquired=False
        )
        with self.assertRaises(ValueError):
            next_state(State.READY, "activate", invalid)

    def test_current_health_required(self):
        invalid = replace(
            self.plan, current_health_verified=False
        )
        with self.assertRaises(ValueError):
            next_state(State.READY, "activate", invalid)

    def test_mutable_image_tag_rejected(self):
        invalid = replace(
            self.plan,
            candidate=ImagePair(
                "ghcr.io/devnechi/fbwebltd-app:latest",
                self.plan.candidate.web,
            ),
        )
        with self.assertRaises(ValueError):
            invalid.validate_preconditions()

    def test_app_web_image_swap_rejected(self):
        invalid = replace(
            self.plan,
            candidate=ImagePair(
                self.plan.candidate.web,
                self.plan.candidate.app,
            ),
        )
        with self.assertRaises(ValueError):
            invalid.validate_preconditions()

    def test_identical_candidate_rejected(self):
        invalid = replace(
            self.plan, candidate=self.plan.previous
        )
        with self.assertRaises(ValueError):
            invalid.validate_preconditions()

    def test_terminal_state_cannot_reactivate(self):
        with self.assertRaises(ValueError):
            next_state(State.SUCCEEDED, "activate", self.plan)

    def test_unapproved_transition_rejected(self):
        with self.assertRaises(ValueError):
            next_state(State.PRECHECK, "activate", self.plan)

    def test_database_excluded_from_execution_policy(self):
        policy = execution_policy()
        self.assertEqual(
            policy["allowed_services"], ("app", "web")
        )
        self.assertIn("db", policy["forbidden_services"])
        self.assertFalse(policy["automatic_migrations"])
        self.assertFalse(policy["unrestricted_compose_up"])
        self.assertFalse(policy["production_execution_enabled"])


if __name__ == "__main__":
    unittest.main()
