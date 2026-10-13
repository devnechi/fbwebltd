#!/usr/bin/env python3
"""Tests for fresh locked rollback retry classification."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from deployment_lock import deployment_lock
from docker_identity import VerifiedIdentity
from locked_rollback_retry import decide_retry_from_docker
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan


class LockedRollbackRetryTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        root = Path(self.temp.name)
        journals = root / "journals"
        locks = root / "locks"

        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-retry-live-001"
        self.project = "fbweb-gate16ab-lab"
        self.db_id = "c" * 64

        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "d" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "e" * 64,
        )

        self.sim.journal.create(
            self.release_id,
            self.candidate,
            self.previous,
        )

        self.sim.create_checkpoint(
            self.release_id,
            self.db_id,
        )

        # Test-only simulated preconditions, not real approvals.
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

        journal = self.sim.journal
        journal.advance(self.release_id, 0, "precheck_passed", plan)
        journal.advance(self.release_id, 1, "activate", plan)
        journal.advance(self.release_id, 2, "failed")

        self.observed = self.identity(self.candidate)

    def identity(self, pair, healthy=True, db=None, project=None):
        return VerifiedIdentity(
            project=self.project if project is None else project,
            app_reference=pair.app,
            web_reference=pair.web,
            db_container_id=self.db_id if db is None else db,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=healthy,
            web_healthy=healthy,
        )

    def decide(self):
        with patch(
            "locked_rollback_retry.collect_allowed_snapshot",
            return_value=self.observed,
        ):
            return decide_retry_from_docker(
                self.sim,
                self.release_id,
                self.project,
            )

    def test_candidate_requires_restoration(self):
        result = self.decide()
        self.assertEqual(result["action"], "RESTORE_PREVIOUS")

    def test_mixed_pair_requires_restoration(self):
        self.observed = self.identity(
            ImagePair(self.previous.app, self.candidate.web)
        )
        self.assertEqual(
            self.decide()["action"],
            "RESTORE_PREVIOUS",
        )

    def test_previous_pair_requires_finalization(self):
        self.observed = self.identity(self.previous)
        result = self.decide()
        self.assertEqual(
            result["action"],
            "VERIFY_AND_FINALIZE",
        )
        self.assertFalse(result["journal_mutation_performed"])

    def test_unhealthy_previous_requires_intervention(self):
        self.observed = self.identity(self.previous, healthy=False)
        self.assertEqual(
            self.decide()["action"],
            "MANUAL_INTERVENTION",
        )

    def test_database_change_requires_intervention(self):
        self.observed = self.identity(
            self.candidate,
            db="f" * 64,
        )
        result = self.decide()
        self.assertEqual(
            result["action"],
            "MANUAL_INTERVENTION",
        )
        self.assertFalse(result["database_identity_matched"])

    def test_production_project_is_rejected(self):
        with self.assertRaises(ValueError):
            decide_retry_from_docker(
                self.sim,
                self.release_id,
                "fbweb",
            )

    def test_observation_project_mismatch_rejected(self):
        self.observed = self.identity(
            self.candidate,
            project="fbweb-gate-other-lab",
        )
        with self.assertRaises(ValueError):
            self.decide()

    def test_concurrent_lock_blocks_retry(self):
        with deployment_lock(self.sim.lock_dir):
            with self.assertRaises(RuntimeError):
                self.decide()

    def test_wrong_journal_state_rejected(self):
        self.sim.journal.advance(
            self.release_id,
            3,
            "restored",
        )
        with self.assertRaises(ValueError):
            self.decide()

    def test_decision_preserves_journal(self):
        before = self.sim.journal.read(self.release_id)
        self.decide()
        after = self.sim.journal.read(self.release_id)

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
