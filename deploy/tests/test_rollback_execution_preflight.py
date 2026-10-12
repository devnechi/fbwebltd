#!/usr/bin/env python3
"""Security tests for the laboratory rollback execution preflight."""

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
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import AttemptStatus
from rollback_attempt_store import RollbackAttemptStore
from rollback_execution_preflight import inspect_rollback_preflight
from rollback_planner import ImagePair, ReleasePlan


class RollbackExecutionPreflightTests(unittest.TestCase):

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)

        base = Path(self.temporary.name)
        journals = base / "journals"
        locks = base / "locks"

        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-preflight-001"
        self.project = "fbweb-gate16ad-lab"
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

        # Test fixtures, not actual authorization.
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

        self.store = RollbackAttemptStore(self.sim)
        self.observed = self.identity(self.candidate)
        self.inspections = 0

    def identity(self, pair, *, db=None, healthy=True, project=None):
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

    def collector(self, project, previous, candidate, runner=None):
        self.inspections += 1
        self.assertEqual(project, self.project)
        self.assertEqual(previous, self.previous)
        self.assertEqual(candidate, self.candidate)
        return self.observed

    def inspect(self):
        with patch(
            "rollback_execution_preflight.collect_allowed_snapshot",
            side_effect=self.collector,
        ):
            return inspect_rollback_preflight(
                self.sim,
                self.release_id,
                self.project,
            )

    def fail_attempt(self):
        started = self.store.begin(self.release_id)
        self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

    def test_candidate_pair_retry_candidate(self):
        result = self.inspect()

        self.assertEqual(result["retry_action"], "RESTORE_PREVIOUS")
        self.assertEqual(result["attempt_action"], "RETRY_ELIGIBLE")
        self.assertTrue(result["retry_candidate"])
        self.assertFalse(result["execution_authorized"])
        self.assertEqual(self.inspections, 1)

    def test_mixed_pair_retry_candidate(self):
        self.observed = self.identity(
            ImagePair(self.candidate.app, self.previous.web)
        )

        result = self.inspect()
        self.assertTrue(result["retry_candidate"])

    def test_previous_healthy_requires_finalization(self):
        self.observed = self.identity(self.previous)

        result = self.inspect()

        self.assertEqual(
            result["retry_action"],
            "VERIFY_AND_FINALIZE",
        )
        self.assertEqual(
            result["attempt_action"],
            "VERIFY_AND_FINALIZE",
        )
        self.assertFalse(result["retry_candidate"])

    def test_database_mismatch_blocks_retry(self):
        self.observed = self.identity(
            self.candidate,
            db="f" * 64,
        )

        result = self.inspect()

        self.assertFalse(result["database_identity_matched"])
        self.assertEqual(
            result["attempt_action"],
            "MANUAL_INTERVENTION",
        )
        self.assertFalse(result["retry_candidate"])

    def test_unfinished_attempt_blocks_retry(self):
        self.store.begin(self.release_id)

        result = self.inspect()

        self.assertEqual(
            result["attempt_action"],
            "INSPECT_REQUIRED",
        )
        self.assertFalse(result["retry_candidate"])

    def test_three_failed_attempts_block_retry(self):
        for _ in range(3):
            self.fail_attempt()

        result = self.inspect()

        self.assertEqual(result["attempt_count"], 3)
        self.assertEqual(
            result["attempt_action"],
            "MANUAL_INTERVENTION",
        )
        self.assertFalse(result["retry_candidate"])

    def test_unexpected_image_observation_rejected(self):
        self.observed = self.identity(
            ImagePair(
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "f" * 64,
                self.candidate.web,
            )
        )

        # The real collector enforces the image allowlist.
        # Simulate that collector's rejection explicitly.
        with patch(
            "rollback_execution_preflight.collect_allowed_snapshot",
            side_effect=ValueError("Unexpected image"),
        ):
            with self.assertRaises(ValueError):
                inspect_rollback_preflight(
                    self.sim,
                    self.release_id,
                    self.project,
                )

    def test_observation_project_mismatch_rejected(self):
        self.observed = self.identity(
            self.candidate,
            project="fbweb-gate-other-lab",
        )

        with self.assertRaises(ValueError):
            self.inspect()

    def test_production_project_rejected(self):
        with self.assertRaises(ValueError):
            inspect_rollback_preflight(
                self.sim,
                self.release_id,
                "fbweb",
            )

    def test_wrong_journal_state_rejected(self):
        self.sim.journal.advance(
            self.release_id,
            3,
            "restored",
        )

        with self.assertRaises(ValueError):
            self.inspect()

    def test_lock_contention_rejected(self):
        with deployment_lock(self.sim.lock_dir):
            with self.assertRaises(RuntimeError):
                self.inspect()

    def test_preflight_does_not_modify_journal_or_attempts(self):
        self.fail_attempt()

        before_journal = self.sim.journal.read(self.release_id)
        before_attempts = self.store.read(self.release_id)

        result = self.inspect()

        after_journal = self.sim.journal.read(self.release_id)
        after_attempts = self.store.read(self.release_id)

        self.assertEqual(before_journal, after_journal)
        self.assertEqual(before_attempts, after_attempts)
        self.assertFalse(result["docker_mutation_performed"])
        self.assertFalse(result["journal_mutation_performed"])
        self.assertFalse(result["production_execution_enabled"])


if __name__ == "__main__":
    unittest.main()
