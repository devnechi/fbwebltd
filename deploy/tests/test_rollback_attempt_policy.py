#!/usr/bin/env python3
"""Conservative attempt lifecycle classification tests."""

import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from rollback_attempt_policy import (
    Attempt,
    AttemptDecision,
    AttemptStatus,
    classify_attempts,
)


class RollbackAttemptPolicyTests(unittest.TestCase):

    def classify(self, attempts, **kwargs):
        options = {
            "fresh_inspection": True,
            "previous_pair_healthy": False,
            "database_identity_matched": True,
        }
        options.update(kwargs)
        return classify_attempts(
            "ROLLING_BACK",
            attempts,
            **options,
        )

    def attempt(self, number, status):
        return Attempt("attempt-" + str(number), status)

    def test_new_attempt_eligible_after_inspection(self):
        self.assertEqual(
            self.classify([]),
            AttemptDecision.RETRY_ELIGIBLE,
        )

    def test_started_requires_reconciliation(self):
        attempts = [self.attempt(1, AttemptStatus.STARTED)]
        self.assertEqual(
            self.classify(attempts),
            AttemptDecision.INSPECT_REQUIRED,
        )

    def test_interrupted_requires_reconciliation(self):
        attempts = [self.attempt(1, AttemptStatus.INTERRUPTED)]
        self.assertEqual(
            self.classify(attempts),
            AttemptDecision.INSPECT_REQUIRED,
        )

    def test_one_failed_attempt_allows_reviewed_retry(self):
        attempts = [self.attempt(1, AttemptStatus.FAILED)]
        self.assertEqual(
            self.classify(attempts),
            AttemptDecision.RETRY_ELIGIBLE,
        )

    def test_two_failed_attempts_still_eligible(self):
        attempts = [
            self.attempt(1, AttemptStatus.FAILED),
            self.attempt(2, AttemptStatus.FAILED),
        ]
        self.assertEqual(
            self.classify(attempts),
            AttemptDecision.RETRY_ELIGIBLE,
        )

    def test_three_failures_require_manual_intervention(self):
        attempts = [
            self.attempt(i, AttemptStatus.FAILED)
            for i in range(1, 4)
        ]
        self.assertEqual(
            self.classify(attempts),
            AttemptDecision.MANUAL_INTERVENTION,
        )

    def test_database_mismatch_blocks_retry(self):
        self.assertEqual(
            self.classify(
                [],
                database_identity_matched=False,
            ),
            AttemptDecision.MANUAL_INTERVENTION,
        )

    def test_restored_healthy_pair_needs_finalizer(self):
        self.assertEqual(
            self.classify(
                [self.attempt(1, AttemptStatus.INTERRUPTED)],
                previous_pair_healthy=True,
            ),
            AttemptDecision.VERIFY_AND_FINALIZE,
        )

    def test_no_fresh_inspection_blocks_retry(self):
        self.assertEqual(
            self.classify([], fresh_inspection=False),
            AttemptDecision.INSPECT_REQUIRED,
        )

    def test_success_without_healthy_previous_needs_manual_review(self):
        self.assertEqual(
            self.classify(
                [self.attempt(1, AttemptStatus.SUCCEEDED)]
            ),
            AttemptDecision.MANUAL_INTERVENTION,
        )

    def test_duplicate_attempt_rejected(self):
        attempt = self.attempt(1, AttemptStatus.FAILED)
        with self.assertRaises(ValueError):
            self.classify([attempt, attempt])

    def test_wrong_journal_state_rejected(self):
        with self.assertRaises(ValueError):
            classify_attempts(
                "ACTIVATING",
                [],
                fresh_inspection=True,
                database_identity_matched=True,
            )

    def test_invalid_boolean_rejected(self):
        with self.assertRaises(ValueError):
            self.classify([], fresh_inspection="yes")

    def test_bad_attempt_id_rejected(self):
        with self.assertRaises(ValueError):
            self.classify([
                Attempt("../invalid", AttemptStatus.FAILED)
            ])


if __name__ == "__main__":
    unittest.main()
