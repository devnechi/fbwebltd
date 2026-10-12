#!/usr/bin/env python3
"""Tests for lease-aware rollback journal finalization."""

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
from rollback_finalizer import (
    finalize_rollback,
    finalize_rollback_locked,
)
from rollback_planner import ImagePair, ReleasePlan


class LockedFinalizerTests(unittest.TestCase):

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        base = Path(temporary.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-finalizer-locked-001"
        self.project = "fbweb-gate16ae-lab"
        self.db_id = "e" * 64

        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(
            self.release_id, self.candidate, self.previous
        )
        self.sim.create_checkpoint(self.release_id, self.db_id)

        # Synthetic laboratory flags, not production approval.
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

    def identity(self, pair=None, db=None, healthy=True):
        pair = pair or self.previous

        return VerifiedIdentity(
            project=self.project,
            app_reference=pair.app,
            web_reference=pair.web,
            db_container_id=self.db_id if db is None else db,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=healthy,
            web_healthy=healthy,
        )

    def finalize_locked(self, observed):
        with patch(
            "rollback_finalizer.collect_allowed_snapshot",
            return_value=observed,
        ) as collector:
            with deployment_lock(self.sim.lock_dir) as lease:
                result = finalize_rollback_locked(
                    self.sim,
                    self.release_id,
                    self.project,
                    lease,
                )
            self.assertEqual(collector.call_count, 1)
            return result

    def test_valid_lease_finalizes_healthy_previous_pair(self):
        result = self.finalize_locked(self.identity())

        self.assertEqual(result["state"], "ROLLED_BACK")
        self.assertTrue(result["database_identity_matched"])
        self.assertFalse(result["docker_mutation_performed"])

    def test_missing_lease_rejected(self):
        with self.assertRaises(RuntimeError):
            finalize_rollback_locked(
                self.sim, self.release_id, self.project, None
            )

    def test_expired_lease_rejected(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            pass

        with self.assertRaises(RuntimeError):
            finalize_rollback_locked(
                self.sim, self.release_id, self.project, lease
            )

    def test_wrong_project_rejected(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            with self.assertRaises(ValueError):
                finalize_rollback_locked(
                    self.sim, self.release_id, "fbweb", lease
                )

    def test_changed_database_rejected_without_transition(self):
        before = self.sim.journal.read(self.release_id)

        with self.assertRaises(ValueError):
            self.finalize_locked(
                self.identity(db="f" * 64)
            )

        self.assertEqual(
            self.sim.journal.read(self.release_id), before
        )

    def test_candidate_images_rejected(self):
        with self.assertRaises(ValueError):
            self.finalize_locked(
                self.identity(pair=self.candidate)
            )

        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_unhealthy_previous_images_rejected(self):
        with self.assertRaises(ValueError):
            self.finalize_locked(
                self.identity(healthy=False)
            )

        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_public_wrapper_remains_compatible(self):
        with patch(
            "rollback_finalizer.collect_allowed_snapshot",
            return_value=self.identity(),
        ):
            result = finalize_rollback(
                self.sim, self.release_id, self.project
            )

        self.assertEqual(result["state"], "ROLLED_BACK")

    def test_nested_public_wrapper_rejected(self):
        with deployment_lock(self.sim.lock_dir):
            with self.assertRaises(RuntimeError):
                finalize_rollback(
                    self.sim, self.release_id, self.project
                )

    def test_cannot_finalize_twice(self):
        self.finalize_locked(self.identity())

        with self.assertRaises(ValueError):
            self.finalize_locked(self.identity())


if __name__ == "__main__":
    unittest.main()
