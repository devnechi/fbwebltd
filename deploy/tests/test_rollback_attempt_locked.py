#!/usr/bin/env python3
"""Lock-aware rollback attempt persistence regression tests."""

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


class LockedAttemptTests(unittest.TestCase):

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        base = Path(temporary.name)
        journals = base / "journals"
        locks = base / "locks"

        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-locked-attempt-001"

        previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(
            self.release_id, candidate, previous
        )
        self.sim.create_checkpoint(
            self.release_id, "e" * 64
        )

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

    def test_locked_begin_and_finish_under_one_lease(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            started = self.store.begin_locked(
                self.release_id, lease
            )

            self.assertEqual(started["status"], "STARTED")

            finished = self.store.finish_locked(
                self.release_id,
                started["attempt_id"],
                0,
                AttemptStatus.FAILED,
                lease,
            )

            self.assertEqual(finished["status"], "FAILED")
            self.assertEqual(finished["revision"], 1)

            records = self.store.read_locked(
                self.release_id, lease
            )

            self.assertEqual(len(records), 1)

    def test_begin_without_lease_rejected(self):
        with self.assertRaises(RuntimeError):
            self.store.begin_locked(self.release_id, None)

    def test_expired_lease_rejected(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            self.assertTrue(lease.require(self.sim.lock_dir))

        with self.assertRaises(RuntimeError):
            self.store.begin_locked(self.release_id, lease)

    def test_wrong_lock_directory_rejected(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        other = Path(temporary.name) / "other-locks"
        other.mkdir(mode=0o700)

        with deployment_lock(other) as wrong_lease:
            with self.assertRaises(RuntimeError):
                self.store.begin_locked(
                    self.release_id, wrong_lease
                )

    def test_unfinished_attempt_still_rejected(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            self.store.begin_locked(self.release_id, lease)

            with self.assertRaises(ValueError):
                self.store.begin_locked(
                    self.release_id, lease
                )

    def test_stale_revision_still_rejected(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            started = self.store.begin_locked(
                self.release_id, lease
            )

            with self.assertRaises(ValueError):
                self.store.finish_locked(
                    self.release_id,
                    started["attempt_id"],
                    9,
                    AttemptStatus.FAILED,
                    lease,
                )

    def test_unverified_success_still_forbidden(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            started = self.store.begin_locked(
                self.release_id, lease
            )

            with self.assertRaises(ValueError):
                self.store.finish_locked(
                    self.release_id,
                    started["attempt_id"],
                    0,
                    AttemptStatus.SUCCEEDED,
                    lease,
                )

    def test_public_methods_remain_compatible(self):
        started = self.store.begin(self.release_id)

        finished = self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        self.assertEqual(finished["status"], "FAILED")
        self.assertEqual(
            self.store.read(self.release_id)[0],
            finished,
        )


if __name__ == "__main__":
    unittest.main()
