#!/usr/bin/env python3
"""Tests for evidence-bound laboratory rollback completion."""

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
from lab_rollback_command import LAB_PROJECT, PREVIOUS
from lab_rollback_completion import complete_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair, ReleasePlan


class CompletionTests(unittest.TestCase):

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        base = Path(temporary.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-completion-001"
        self.db_id = "e" * 64
        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(
            self.release_id, self.candidate, PREVIOUS
        )
        self.sim.create_checkpoint(self.release_id, self.db_id)

        plan = ReleasePlan(
            candidate=self.candidate,
            previous=PREVIOUS,
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
        self.identity = self.make_identity(PREVIOUS)

        candidate_identity = self.make_identity(self.candidate)

        # Establish an authentic v2 binding using the operation gate.
        with patch(
            "rollback_operation_gate.collect_allowed_snapshot",
            return_value=candidate_identity,
        ):
            from deployment_lock import deployment_lock

            with deployment_lock(self.sim.lock_dir) as lease:
                self.started = self.store.begin_bound_locked(
                    self.release_id, LAB_PROJECT, lease
                )

    def make_identity(self, pair, db=None, healthy=True):
        return VerifiedIdentity(
            project=LAB_PROJECT,
            app_reference=pair.app,
            web_reference=pair.web,
            db_container_id=self.db_id if db is None else db,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=healthy,
            web_healthy=healthy,
        )

    def complete(self):
        with patch(
            "lab_rollback_completion.collect_allowed_snapshot",
            return_value=self.identity,
        ), patch(
            "rollback_finalizer.collect_allowed_snapshot",
            return_value=self.identity,
        ):
            return complete_lab_rollback(
                self.sim,
                self.release_id,
            )

    def test_healthy_restoration_completes(self):
        result = self.complete()

        self.assertEqual(result["attempt_status"], "SUCCEEDED")
        self.assertEqual(result["journal_state"], "ROLLED_BACK")
        self.assertFalse(result["docker_mutation_performed"])

        self.assertEqual(
            self.store.read(self.release_id)[0]["status"],
            "SUCCEEDED",
        )

    def test_repeated_completion_is_idempotent(self):
        self.complete()
        result = self.complete()

        self.assertTrue(result["already_complete"])
        self.assertEqual(
            self.sim.journal.read(self.release_id)["revision"], 4
        )
        self.assertEqual(
            self.store.read(self.release_id)[0]["revision"], 1
        )

    def test_crash_between_attempt_and_journal_can_resume(self):
        with patch(
            "lab_rollback_completion.collect_allowed_snapshot",
            return_value=self.identity,
        ), patch(
            "rollback_finalizer.collect_allowed_snapshot",
            side_effect=RuntimeError("simulated crash"),
        ):
            with self.assertRaisesRegex(RuntimeError, "simulated crash"):
                complete_lab_rollback(self.sim, self.release_id)

        self.assertEqual(
            self.store.read(self.release_id)[0]["status"],
            "SUCCEEDED",
        )
        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

        result = self.complete()
        self.assertEqual(result["journal_state"], "ROLLED_BACK")

    def test_database_mismatch_blocks_completion(self):
        self.identity = self.make_identity(
            PREVIOUS, db="f" * 64
        )

        with self.assertRaises(ValueError):
            self.complete()

        self.assertEqual(
            self.store.read(self.release_id)[0]["status"],
            "STARTED",
        )

    def test_unhealthy_restoration_blocks_completion(self):
        self.identity = self.make_identity(
            PREVIOUS, healthy=False
        )

        with self.assertRaises(ValueError):
            self.complete()

        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_candidate_images_block_completion(self):
        self.identity = self.make_identity(self.candidate)

        with self.assertRaises(ValueError):
            self.complete()

    def test_tampered_fingerprint_blocks_completion(self):
        record = dict(self.started)
        record["operation_fingerprint"] = "a" * 64

        directory = self.store.directory(self.release_id)
        self.store._write(
            directory,
            directory / "000001.json",
            record,
            replace=True,
        )

        with self.assertRaises(ValueError):
            self.complete()

        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_production_project_blocked(self):
        with self.assertRaises(ValueError):
            complete_lab_rollback(
                self.sim,
                self.release_id,
                project="fbweb",
            )

    def test_no_attempt_cannot_finalize(self):
        release_id = "fbweb-completion-empty"
        self.sim.journal.create(
            release_id, self.candidate, PREVIOUS
        )
        self.sim.create_checkpoint(release_id, self.db_id)

        plan = ReleasePlan(
            candidate=self.candidate,
            previous=PREVIOUS,
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

        for revision, event in enumerate(
            ("precheck_passed", "activate", "failed")
        ):
            self.sim.journal.advance(
                release_id, revision, event, plan
                if event != "failed" else None
            )

        with self.assertRaises(ValueError):
            complete_lab_rollback(self.sim, release_id)


if __name__ == "__main__":
    unittest.main()
