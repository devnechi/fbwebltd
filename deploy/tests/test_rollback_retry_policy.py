#!/usr/bin/env python3
"""Tests for safe rollback retry decisions."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from recovery_journal import RecoveryJournal
from recovery_reconciler import ContainerSnapshot
from rollback_planner import ImagePair, ReleasePlan
from rollback_retry_policy import (
    RollbackRetryAction,
    decide_rollback_retry,
)


class RollbackRetryPolicyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        root = Path(temporary.name) / "journals"
        root.mkdir(mode=0o700)

        self.journal = RecoveryJournal(root)
        self.release_id = "fbweb-retry-001"
        self.db_id = "c" * 64

        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "d" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "e" * 64,
        )

        self.journal.create(
            self.release_id,
            self.candidate,
            self.previous,
        )

        plan = ReleasePlan(
            candidate=self.candidate,
            previous=self.previous,
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

        self.journal.advance(
            self.release_id, 0, "precheck_passed", plan
        )
        self.journal.advance(
            self.release_id, 1, "activate", plan
        )
        self.journal.advance(
            self.release_id, 2, "failed"
        )

    def snapshot(self, pair, healthy=True, db=None):
        return ContainerSnapshot(
            app_image=pair.app,
            web_image=pair.web,
            db_identity=self.db_id if db is None else db,
            app_healthy=healthy,
            web_healthy=healthy,
        )

    def decide(self, snapshot):
        return decide_rollback_retry(
            self.journal.read(self.release_id),
            snapshot,
            self.db_id,
        )

    def test_candidate_requires_restoration(self):
        self.assertEqual(
            self.decide(self.snapshot(self.candidate)),
            RollbackRetryAction.RESTORE_PREVIOUS,
        )

    def test_mixed_app_candidate_requires_restoration(self):
        pair = ImagePair(
            self.candidate.app,
            self.previous.web,
        )
        self.assertEqual(
            self.decide(self.snapshot(pair)),
            RollbackRetryAction.RESTORE_PREVIOUS,
        )

    def test_mixed_web_candidate_requires_restoration(self):
        pair = ImagePair(
            self.previous.app,
            self.candidate.web,
        )
        self.assertEqual(
            self.decide(self.snapshot(pair)),
            RollbackRetryAction.RESTORE_PREVIOUS,
        )

    def test_previous_healthy_requires_finalizer(self):
        self.assertEqual(
            self.decide(self.snapshot(self.previous)),
            RollbackRetryAction.VERIFY_AND_FINALIZE,
        )

    def test_previous_unhealthy_requires_intervention(self):
        self.assertEqual(
            self.decide(self.snapshot(self.previous, healthy=False)),
            RollbackRetryAction.MANUAL_INTERVENTION,
        )

    def test_database_identity_change_requires_intervention(self):
        self.assertEqual(
            self.decide(
                self.snapshot(self.candidate, db="f" * 64)
            ),
            RollbackRetryAction.MANUAL_INTERVENTION,
        )

    def test_wrong_state_rejected(self):
        self.journal.advance(
            self.release_id, 3, "restored"
        )

        with self.assertRaises(ValueError):
            self.decide(self.snapshot(self.previous))

    def test_decision_does_not_modify_journal(self):
        before = self.journal.read(self.release_id)

        self.decide(self.snapshot(self.candidate))

        after = self.journal.read(self.release_id)

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
