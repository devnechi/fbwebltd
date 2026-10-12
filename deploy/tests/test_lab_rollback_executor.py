#!/usr/bin/env python3
"""Tests for the restricted laboratory rollback executor."""

import subprocess
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
from lab_rollback_executor import execute_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan
from rollback_attempt_store import RollbackAttemptStore


class LaboratoryExecutorTests(unittest.TestCase):

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)

        base = Path(temporary.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-executor-001"
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

        self.observed = self.identity(self.candidate)
        self.commands = []

    def identity(self, pair, db=None, healthy=True):
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

    def collector(self, *args, **kwargs):
        return self.observed

    def successful_command(self, command):
        command.validate()
        self.commands.append(command)
        self.observed = self.identity(PREVIOUS)
        return subprocess.CompletedProcess(command.argv, 0)

    def failed_command(self, command):
        command.validate()
        self.commands.append(command)
        return subprocess.CompletedProcess(command.argv, 1)

    def run_executor(self, command_runner):
        with patch(
            "rollback_operation_gate.collect_allowed_snapshot",
            side_effect=self.collector,
        ), patch(
            "lab_rollback_executor.collect_allowed_snapshot",
            side_effect=self.collector,
        ):
            return execute_lab_rollback(
                self.sim,
                self.release_id,
                command_runner=command_runner,
            )

    def test_successful_restoration_remains_unfinalized(self):
        before = self.sim.journal.read(self.release_id)

        result = self.run_executor(self.successful_command)

        self.assertTrue(result["restoration_verified"])
        self.assertFalse(result["journal_finalized"])
        self.assertEqual(result["attempt_status"], "STARTED")
        self.assertEqual(result["journal_state"], "ROLLING_BACK")
        self.assertEqual(len(self.commands), 1)

        self.assertEqual(
            self.sim.journal.read(self.release_id), before
        )

        records = RollbackAttemptStore(self.sim).read(
            self.release_id
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], "STARTED")

    def test_command_failure_preserves_unresolved_attempt(self):
        with self.assertRaises(RuntimeError):
            self.run_executor(self.failed_command)

        records = RollbackAttemptStore(self.sim).read(
            self.release_id
        )
        self.assertEqual(records[0]["status"], "STARTED")
        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_second_execution_rejected(self):
        self.run_executor(self.successful_command)

        with self.assertRaises(ValueError):
            self.run_executor(self.successful_command)

        self.assertEqual(len(self.commands), 1)

    def test_production_project_rejected(self):
        with self.assertRaises(ValueError):
            execute_lab_rollback(
                self.sim,
                self.release_id,
                project="fbweb",
            )

        self.assertEqual(
            RollbackAttemptStore(self.sim).read(self.release_id),
            [],
        )

    def test_database_change_blocks_success(self):
        def changed_db(command):
            command.validate()
            self.commands.append(command)
            self.observed = self.identity(
                PREVIOUS, db="f" * 64
            )
            return subprocess.CompletedProcess(command.argv, 0)

        with self.assertRaises(ValueError):
            self.run_executor(changed_db)

        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_unhealthy_previous_pair_blocks_success(self):
        def unhealthy(command):
            command.validate()
            self.commands.append(command)
            self.observed = self.identity(
                PREVIOUS, healthy=False
            )
            return subprocess.CompletedProcess(command.argv, 0)

        with self.assertRaises(ValueError):
            self.run_executor(unhealthy)

        self.assertEqual(
            self.sim.journal.read(self.release_id)["state"],
            "ROLLING_BACK",
        )

    def test_no_execution_when_journal_is_finalized(self):
        self.sim.journal.advance(
            self.release_id, 3, "restored"
        )

        with self.assertRaises(ValueError):
            self.run_executor(self.successful_command)

        self.assertEqual(self.commands, [])


if __name__ == "__main__":
    unittest.main()
