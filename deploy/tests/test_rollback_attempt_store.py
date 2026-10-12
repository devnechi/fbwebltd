#!/usr/bin/env python3
"""Durable rollback attempt lifecycle tests."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from deployment_lock import deployment_lock
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import AttemptStatus
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair, ReleasePlan


class RollbackAttemptStoreTests(unittest.TestCase):

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)

        base = Path(temp.name)
        journals = base / "journals"
        locks = base / "locks"

        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-attempt-store-001"

        previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(
            self.release_id,
            candidate,
            previous,
        )

        self.sim.create_checkpoint(
            self.release_id,
            "e" * 64,
        )

        # Test fixtures only, not production approval.
        plan = ReleasePlan(
            candidate=candidate,
            previous=previous,
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

    def test_begin_persists_started(self):
        record = self.store.begin(self.release_id)
        self.assertEqual(record["status"], "STARTED")
        self.assertEqual(record["revision"], 0)
        self.assertEqual(len(self.store.read(self.release_id)), 1)

    def test_restart_observes_unfinished_attempt(self):
        started = self.store.begin(self.release_id)

        reopened = RollbackAttemptStore(self.sim)
        records = reopened.read(self.release_id)

        self.assertEqual(records[0], started)

    def test_second_active_attempt_rejected(self):
        self.store.begin(self.release_id)

        with self.assertRaises(ValueError):
            self.store.begin(self.release_id)

    def test_failed_attempt_persisted(self):
        started = self.store.begin(self.release_id)

        result = self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["revision"], 1)

    def test_interrupted_attempt_persisted(self):
        started = self.store.begin(self.release_id)

        result = self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.INTERRUPTED,
        )

        self.assertEqual(result["status"], "INTERRUPTED")

    def test_next_attempt_receives_unique_id(self):
        first = self.store.begin(self.release_id)

        self.store.finish(
            self.release_id,
            first["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        second = self.store.begin(self.release_id)

        self.assertNotEqual(
            first["attempt_id"],
            second["attempt_id"],
        )
        self.assertEqual(second["attempt_id"], "attempt-000002")

    def test_stale_revision_rejected(self):
        started = self.store.begin(self.release_id)

        with self.assertRaises(ValueError):
            self.store.finish(
                self.release_id,
                started["attempt_id"],
                4,
                AttemptStatus.FAILED,
            )

    def test_completed_attempt_cannot_be_updated_twice(self):
        started = self.store.begin(self.release_id)

        self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        with self.assertRaises(ValueError):
            self.store.finish(
                self.release_id,
                started["attempt_id"],
                1,
                AttemptStatus.INTERRUPTED,
            )

    def test_unverified_success_forbidden(self):
        started = self.store.begin(self.release_id)

        with self.assertRaises(ValueError):
            self.store.finish(
                self.release_id,
                started["attempt_id"],
                0,
                AttemptStatus.SUCCEEDED,
            )

    def test_lock_contention_blocks_begin(self):
        with deployment_lock(self.sim.lock_dir):
            with self.assertRaises(RuntimeError):
                self.store.begin(self.release_id)

    def test_attempt_storage_does_not_change_journal(self):
        before = self.sim.journal.read(self.release_id)

        started = self.store.begin(self.release_id)
        self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        after = self.sim.journal.read(self.release_id)
        self.assertEqual(before, after)

    def test_finalized_journal_blocks_new_attempt(self):
        self.sim.journal.advance(
            self.release_id,
            3,
            "restored",
        )

        with self.assertRaises(ValueError):
            self.store.begin(self.release_id)

    def test_policy_projection_uses_persisted_records(self):
        first = self.store.begin(self.release_id)

        self.store.finish(
            self.release_id,
            first["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        attempts = self.store.policy_attempts(self.release_id)

        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0].status, AttemptStatus.FAILED)

    def test_missing_attempt_cannot_be_finished(self):
        with self.assertRaises(ValueError):
            self.store.finish(
                self.release_id,
                "attempt-000001",
                0,
                AttemptStatus.FAILED,
            )


if __name__ == "__main__":
    unittest.main()
