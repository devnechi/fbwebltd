#!/usr/bin/env python3
"""Tests for the non-executing, lease-bound rollback operation gate."""

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from deployment_lock import deployment_lock
from docker_identity import VerifiedIdentity
from lab_rollback_command import LAB_PROJECT, PREVIOUS
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import AttemptStatus
from rollback_attempt_store import RollbackAttemptStore
from rollback_operation_gate import evaluate_rollback_operation_locked
from rollback_planner import ImagePair, ReleasePlan


class RollbackOperationGateTests(unittest.TestCase):

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        root = Path(temporary.name)
        journals = root / "journals"
        locks = root / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-operation-gate-001"
        self.db_id = "e" * 64
        self.previous = PREVIOUS

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(
            self.release_id,
            self.candidate,
            self.previous,
        )

        self.sim.create_checkpoint(self.release_id, self.db_id)

        # Synthetic fixture flags; not approval or provenance evidence.
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

    def identity(self, pair, db=None):
        return VerifiedIdentity(
            project=LAB_PROJECT,
            app_reference=pair.app,
            web_reference=pair.web,
            db_container_id=self.db_id if db is None else db,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=True,
            web_healthy=True,
        )

    def evaluate(self):
        with patch(
            "rollback_operation_gate.collect_allowed_snapshot",
            return_value=self.observed,
        ):
            with deployment_lock(self.sim.lock_dir) as lease:
                return evaluate_rollback_operation_locked(
                    self.sim,
                    self.release_id,
                    LAB_PROJECT,
                    lease,
                )

    def test_candidate_pair_produces_bound_operation(self):
        before = self.sim.journal.read(self.release_id)

        operation = self.evaluate()

        self.assertTrue(operation.validate_fingerprint())
        self.assertEqual(operation.project, LAB_PROJECT)
        self.assertEqual(operation.previous_app, PREVIOUS.app)
        self.assertEqual(operation.previous_web, PREVIOUS.web)
        self.assertEqual(operation.database_identity, self.db_id)
        self.assertEqual(len(operation.fingerprint), 64)
        self.assertFalse(operation.execution_authorized)

        self.assertEqual(
            self.sim.journal.read(self.release_id),
            before,
        )

    def test_operation_tampering_rejected(self):
        operation = self.evaluate()

        altered = replace(operation, database_identity="f" * 64)

        with self.assertRaises(ValueError):
            altered.validate_fingerprint()

    def test_wrong_database_identity_rejected(self):
        self.observed = self.identity(
            self.candidate,
            db="f" * 64,
        )

        with self.assertRaises(ValueError):
            self.evaluate()

    def test_healthy_previous_pair_not_retry_eligible(self):
        self.observed = self.identity(self.previous)

        with self.assertRaises(ValueError):
            self.evaluate()

    def test_unfinished_attempt_blocks_operation(self):
        store = RollbackAttemptStore(self.sim)
        store.begin(self.release_id)

        with self.assertRaises(ValueError):
            self.evaluate()

    def test_three_failed_attempts_block_operation(self):
        store = RollbackAttemptStore(self.sim)

        for _ in range(3):
            started = store.begin(self.release_id)
            store.finish(
                self.release_id,
                started["attempt_id"],
                started["revision"],
                AttemptStatus.FAILED,
            )

        with self.assertRaises(ValueError):
            self.evaluate()

    def test_invalid_project_rejected(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            with self.assertRaises(ValueError):
                evaluate_rollback_operation_locked(
                    self.sim,
                    self.release_id,
                    "fbweb",
                    lease,
                )

    def test_missing_and_expired_lease_rejected(self):
        with self.assertRaises(RuntimeError):
            evaluate_rollback_operation_locked(
                self.sim,
                self.release_id,
                LAB_PROJECT,
                None,
            )

        with deployment_lock(self.sim.lock_dir) as lease:
            pass

        with self.assertRaises(RuntimeError):
            evaluate_rollback_operation_locked(
                self.sim,
                self.release_id,
                LAB_PROJECT,
                lease,
            )


if __name__ == "__main__":
    unittest.main()
