#!/usr/bin/env python3
"""Integration tests for simulation-only recovery coordination."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from recovery_simulator import RecoverySimulator
from recovery_reconciler import ContainerSnapshot
from recovery_journal import RecoveryJournal
from rollback_planner import ImagePair, ReleasePlan


class RecoverySimulatorTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        base = Path(self.temp.name)
        self.journals = base / "journals"
        self.locks = base / "locks"

        self.journals.mkdir(mode=0o700)
        self.locks.mkdir(mode=0o700)

        self.simulator = RecoverySimulator(
            self.journals, self.locks
        )

        self.release_id = "fbweb-sim-001"
        self.db_identity = "db-container-before-activation"

        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.journal = RecoveryJournal(self.journals)

        self.journal.create(
            self.release_id, self.candidate, self.previous
        )

    def snapshot(self, pair, db_identity=None):
        return ContainerSnapshot(
            app_image=pair.app,
            web_image=pair.web,
            db_identity=db_identity or self.db_identity,
            app_healthy=True,
            web_healthy=True,
        )

    def advance_to_activation(self):
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

    def test_interrupted_candidate_requires_restoration(self):
        self.simulator.create_checkpoint(
            self.release_id, self.db_identity
        )
        self.advance_to_activation()

        result = self.simulator.decide(
            self.release_id,
            self.snapshot(self.candidate),
        )

        self.assertEqual(result["action"], "RESTORE_PREVIOUS")
        self.assertFalse(result["docker_executed"])

    def test_partial_activation_requires_restoration(self):
        self.simulator.create_checkpoint(
            self.release_id, self.db_identity
        )
        self.advance_to_activation()

        mixed = ImagePair(
            self.candidate.app, self.previous.web
        )

        result = self.simulator.decide(
            self.release_id, self.snapshot(mixed)
        )

        self.assertEqual(result["action"], "RESTORE_PREVIOUS")

    def test_changed_database_requires_manual_intervention(self):
        self.simulator.create_checkpoint(
            self.release_id, self.db_identity
        )
        self.advance_to_activation()

        result = self.simulator.decide(
            self.release_id,
            self.snapshot(self.candidate, "unexpected-db"),
        )

        self.assertEqual(
            result["action"], "MANUAL_INTERVENTION"
        )

    def test_missing_checkpoint_blocks_decision(self):
        with self.assertRaises(FileNotFoundError):
            self.simulator.decide(
                self.release_id,
                self.snapshot(self.previous),
            )

    def test_duplicate_checkpoint_rejected(self):
        self.simulator.create_checkpoint(
            self.release_id, self.db_identity
        )

        with self.assertRaises(FileExistsError):
            self.simulator.create_checkpoint(
                self.release_id, self.db_identity
            )

    def test_corrupted_checkpoint_blocks_decision(self):
        self.simulator.create_checkpoint(
            self.release_id, self.db_identity
        )

        path = self.simulator.checkpoint_path(self.release_id)
        path.write_text('{"invalid":true}', encoding="utf-8")

        with self.assertRaises(ValueError):
            self.simulator.decide(
                self.release_id,
                self.snapshot(self.candidate),
            )

    def test_checkpoint_cannot_be_created_after_activation(self):
        self.advance_to_activation()

        with self.assertRaises(ValueError):
            self.simulator.create_checkpoint(
                self.release_id, self.db_identity
            )


if __name__ == "__main__":
    unittest.main()
