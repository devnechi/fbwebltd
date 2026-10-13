#!/usr/bin/env python3
"""Versioned attempt binding and integrated eligibility tests."""

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
from lab_rollback_command import LAB_PROJECT, PREVIOUS
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import AttemptStatus
from rollback_attempt_store import (
    RollbackAttemptStore,
    validate_attempt_record,
)
from rollback_attempt_view import read_attempts_locked
from rollback_planner import ImagePair, ReleasePlan


class BoundAttemptTests(unittest.TestCase):

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        base = Path(temporary.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-bound-attempt-001"
        self.db_id = "e" * 64

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(
            self.release_id,
            self.candidate,
            PREVIOUS,
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

        self.identity = VerifiedIdentity(
            project=LAB_PROJECT,
            app_reference=self.candidate.app,
            web_reference=self.candidate.web,
            db_container_id=self.db_id,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=True,
            web_healthy=True,
        )

    def begin_bound(self):
        with patch(
            "rollback_operation_gate.collect_allowed_snapshot",
            return_value=self.identity,
        ):
            with deployment_lock(self.sim.lock_dir) as lease:
                return self.store.begin_bound_locked(
                    self.release_id,
                    LAB_PROJECT,
                    lease,
                )

    def test_bound_attempt_contains_operation_identity(self):
        record = self.begin_bound()

        self.assertEqual(record["schema_version"], 2)
        self.assertEqual(record["status"], "STARTED")
        self.assertEqual(record["project"], LAB_PROJECT)
        self.assertEqual(record["previous_app"], PREVIOUS.app)
        self.assertEqual(record["previous_web"], PREVIOUS.web)
        self.assertEqual(record["database_identity"], self.db_id)
        self.assertEqual(len(record["execution_id"]), 32)
        self.assertEqual(len(record["operation_fingerprint"]), 64)

    def test_bound_record_survives_reopening_store(self):
        original = self.begin_bound()
        reopened = RollbackAttemptStore(self.sim)

        self.assertEqual(
            reopened.read(self.release_id)[0],
            original,
        )

    def test_unfinished_attempt_blocks_second_operation(self):
        self.begin_bound()

        with self.assertRaises(ValueError):
            self.begin_bound()

        self.assertEqual(len(self.store.read(self.release_id)), 1)

    def test_wrong_database_observation_blocks_persistence(self):
        self.identity = VerifiedIdentity(
            project=LAB_PROJECT,
            app_reference=self.candidate.app,
            web_reference=self.candidate.web,
            db_container_id="f" * 64,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=True,
            web_healthy=True,
        )

        with self.assertRaises(ValueError):
            self.begin_bound()

        self.assertEqual(self.store.read(self.release_id), [])

    def test_wrong_project_blocks_persistence(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            with self.assertRaises(ValueError):
                self.store.begin_bound_locked(
                    self.release_id,
                    "fbweb",
                    lease,
                )

        self.assertEqual(self.store.read(self.release_id), [])

    def test_expired_lease_blocks_persistence(self):
        with deployment_lock(self.sim.lock_dir) as lease:
            pass

        with self.assertRaises(RuntimeError):
            self.store.begin_bound_locked(
                self.release_id,
                LAB_PROJECT,
                lease,
            )

    def test_versioned_attempt_status_updates_preserve_binding(self):
        started = self.begin_bound()

        updated = self.store.finish(
            self.release_id,
            started["attempt_id"],
            0,
            AttemptStatus.FAILED,
        )

        self.assertEqual(updated["status"], "FAILED")
        self.assertEqual(updated["revision"], 1)
        self.assertEqual(
            updated["operation_fingerprint"],
            started["operation_fingerprint"],
        )
        self.assertEqual(
            updated["execution_id"],
            started["execution_id"],
        )

    def test_read_only_view_accepts_bound_attempt(self):
        self.begin_bound()

        with deployment_lock(self.sim.lock_dir):
            attempts = read_attempts_locked(
                self.sim,
                self.release_id,
            )

        self.assertEqual(len(attempts), 1)
        self.assertEqual(
            attempts[0].status,
            AttemptStatus.STARTED,
        )

    def test_tampered_binding_is_rejected(self):
        record = self.begin_bound()
        changed = dict(record)
        changed["operation_fingerprint"] = "invalid"

        with self.assertRaises(ValueError):
            validate_attempt_record(changed)

    def test_legacy_attempt_records_remain_readable(self):
        legacy_id = "fbweb-bound-legacy-001"
        candidate = self.candidate

        self.sim.journal.create(
            legacy_id,
            candidate,
            PREVIOUS,
        )
        self.sim.create_checkpoint(legacy_id, "f" * 64)

        journal = self.sim.journal
        plan = ReleasePlan(
            candidate=candidate,
            previous=PREVIOUS,
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

        journal.advance(legacy_id, 0, "precheck_passed", plan)
        journal.advance(legacy_id, 1, "activate", plan)
        journal.advance(legacy_id, 2, "failed")

        record = self.store.begin(legacy_id)

        self.assertNotIn("schema_version", record)
        self.assertEqual(
            self.store.read(legacy_id)[0],
            record,
        )


if __name__ == "__main__":
    unittest.main()
