#!/usr/bin/env python3
"""Gate 4D.22C.3B.2: restricted inert release regression."""

from dataclasses import replace
from pathlib import Path
import sys
import tempfile
import unittest


TESTS = Path(__file__).resolve().parent
RELEASES = TESTS.parent / "releases"

sys.path.insert(0, str(RELEASES))
sys.path.insert(0, str(TESTS))

from deployment_lock import deployment_lock
from docker_execution_evidence import (
    DockerExecutionEvidenceStore,
    EXIT_OBSERVED,
    OBSERVED,
)
from docker_process_supervision import (
    ProcessAssessment,
    ProcessStatus,
)
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from locked_durable_barrier import LockedEvidenceStore
from restricted_barrier_release import execute_restricted_inert
from test_docker_execution_evidence import attempt


class RestrictedBarrierReleaseTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.locks = self.root / "locks"
        self.evidence = self.root / "evidence"
        self.marker = str(self.root / "marker")

        self.locks.mkdir(mode=0o700)
        self.evidence.mkdir(mode=0o700)

    def store_under_lease(self, lease):
        return LockedEvidenceStore(
            self.evidence,
            self.locks,
            lease,
        )

    def test_valid_restricted_inert_release(self):
        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

            result = execute_restricted_inert(
                store, attempt(), self.marker
            )

            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.evidence_phase, EXIT_OBSERVED)
            self.assertFalse(result.docker_executed)
            self.assertFalse(result.docker_operation_settled)
            self.assertFalse(result.automatic_retry_permitted)
            self.assertTrue(result.manual_reconciliation_required)
            self.assertFalse(result.production_execution_enabled)

        self.assertEqual(
            Path(self.marker).read_bytes(),
            b"RELEASED\n",
        )

    def test_duplicate_launch_rejected(self):
        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

            execute_restricted_inert(
                store, attempt(), self.marker
            )

            with self.assertRaises(FileExistsError):
                execute_restricted_inert(
                    store, attempt(), self.marker
                )

    def test_mutated_command_rejected_before_prepared(self):
        command = plan_lab_rollback(PREVIOUS)

        mutated = replace(
            command,
            argv=command.argv + ("--remove-orphans",),
        )

        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

            with self.assertRaises(ValueError):
                execute_restricted_inert(
                    store,
                    attempt(),
                    self.marker,
                    command=mutated,
                )

        self.assertFalse(Path(self.marker).exists())
        self.assertFalse(
            (self.evidence / "gate22b-lab.json").exists()
        )

    def test_wrong_attempt_rejected_before_spawn(self):
        value = attempt()
        value["status"] = "FAILED"

        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

            with self.assertRaises(ValueError):
                execute_restricted_inert(
                    store, value, self.marker
                )

        self.assertFalse(Path(self.marker).exists())

    def test_unleased_store_rejected(self):
        readonly = DockerExecutionEvidenceStore(
            self.evidence
        )

        with self.assertRaises(RuntimeError):
            execute_restricted_inert(
                readonly, attempt(), self.marker
            )

        self.assertFalse(Path(self.marker).exists())

    def test_expired_lease_rejected(self):
        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

        with self.assertRaises(RuntimeError):
            execute_restricted_inert(
                store, attempt(), self.marker
            )

        self.assertFalse(Path(self.marker).exists())

    def test_process_policy_rejection_blocks_release(self):
        def rejected_observer(_identity):
            return ProcessAssessment(
                status=ProcessStatus.PID_REUSED,
                original_process_active=False,
                docker_operation_settled=False,
                automatic_retry_permitted=False,
                manual_reconciliation_required=True,
                reason="Simulated PID reuse",
            )

        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

            with self.assertRaises(ValueError):
                execute_restricted_inert(
                    store,
                    attempt(),
                    self.marker,
                    process_observer=rejected_observer,
                )

            record = store.read("gate22b-lab")
            self.assertEqual(record["phase"], OBSERVED)

        self.assertFalse(Path(self.marker).exists())

    def test_success_still_requires_reconciliation(self):
        with deployment_lock(self.locks) as lease:
            store = self.store_under_lease(lease)

            execute_restricted_inert(
                store, attempt(), self.marker
            )

        readonly = DockerExecutionEvidenceStore(
            self.evidence
        )

        assessment = readonly.assess("gate22b-lab")

        self.assertFalse(assessment.docker_operation_settled)
        self.assertFalse(assessment.automatic_retry_permitted)
        self.assertTrue(assessment.manual_reconciliation_required)


if __name__ == "__main__":
    unittest.main()
