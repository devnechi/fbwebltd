#!/usr/bin/env python3
"""Rollback finalization must require observed restoration."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from docker_identity import VerifiedIdentity
from recovery_simulator import RecoverySimulator
from rollback_finalizer import finalize_rollback
from rollback_planner import ImagePair, ReleasePlan


class RollbackFinalizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        base = Path(self.temp.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-finalize-001"
        self.project = "fbweb-gate16z-lab"
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
            self.release_id, self.candidate, self.previous
        )
        self.sim.create_checkpoint(self.release_id, self.db_id)

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

        self.observed = self.identity(self.previous)

    def identity(self, pair, db=None, healthy=True):
        return VerifiedIdentity(
            project=self.project,
            app_reference=pair.app,
            web_reference=pair.web,
            db_container_id=db or self.db_id,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=healthy,
            web_healthy=healthy,
        )

    def finalize(self):
        with patch(
            "rollback_finalizer.collect_allowed_snapshot",
            return_value=self.observed,
        ):
            return finalize_rollback(
                self.sim,
                self.release_id,
                self.project,
            )

    def test_healthy_previous_finalizes(self):
        result = self.finalize()
        self.assertEqual(result["state"], "ROLLED_BACK")
        self.assertEqual(result["revision"], 4)

    def test_candidate_cannot_finalize(self):
        self.observed = self.identity(self.candidate)
        with self.assertRaises(ValueError):
            self.finalize()
        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_database_change_blocks_finalization(self):
        self.observed = self.identity(
            self.previous, db="f" * 64
        )
        with self.assertRaises(ValueError):
            self.finalize()

    def test_unhealthy_previous_blocks_finalization(self):
        self.observed = self.identity(
            self.previous, healthy=False
        )
        with self.assertRaises(ValueError):
            self.finalize()

    def test_cannot_finalize_twice(self):
        self.finalize()
        with self.assertRaises(ValueError):
            self.finalize()

    def test_production_project_rejected(self):
        with self.assertRaises(ValueError):
            finalize_rollback(
                self.sim, self.release_id, "fbweb"
            )

    def test_global_lock_contention_blocks_finalization(self):
        from deployment_lock import deployment_lock

        with deployment_lock(self.sim.lock_dir):
            with self.assertRaises(RuntimeError):
                self.finalize()

    def test_failure_preserves_journal_revision(self):
        before = self.sim.journal.read(self.release_id)
        self.observed = self.identity(self.candidate)

        with self.assertRaises(ValueError):
            self.finalize()

        self.assertEqual(
            self.sim.journal.read(self.release_id), before
        )


if __name__ == "__main__":
    unittest.main()
