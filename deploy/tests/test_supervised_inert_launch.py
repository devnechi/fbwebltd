#!/usr/bin/env python3
"""Gate 4D.22C.3A supervised inert launch regression tests."""

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
)
from locked_durable_barrier import LockedEvidenceStore
from supervised_inert_launch import execute_supervised_inert
from test_docker_execution_evidence import attempt


class SupervisedInertLaunchTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.locks = self.root / "locks"
        self.evidence = self.root / "evidence"
        self.marker = str(self.root / "marker")

        self.locks.mkdir(mode=0o700)
        self.evidence.mkdir(mode=0o700)

    def test_supervised_launch_persists_exit(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            result = execute_supervised_inert(
                store, attempt(), self.marker
            )

            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.evidence_phase, EXIT_OBSERVED)
            self.assertFalse(result.automatic_retry_permitted)
            self.assertFalse(result.docker_operation_settled)
            self.assertTrue(result.manual_reconciliation_required)
            self.assertFalse(result.production_execution_enabled)

        self.assertEqual(
            Path(self.marker).read_bytes(),
            b"RELEASED\n",
        )

        persisted = DockerExecutionEvidenceStore(
            self.evidence
        ).read("gate22b-lab")

        self.assertEqual(persisted["phase"], EXIT_OBSERVED)
        self.assertEqual(persisted["pid"], result.pid)
        self.assertEqual(
            persisted["start_ticks"], result.start_ticks
        )

    def test_read_only_store_cannot_launch(self):
        store = DockerExecutionEvidenceStore(self.evidence)

        with self.assertRaises(RuntimeError):
            execute_supervised_inert(
                store, attempt(), self.marker
            )

        self.assertFalse(Path(self.marker).exists())

    def test_expired_lease_rejects_launch(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

        with self.assertRaises(RuntimeError):
            execute_supervised_inert(
                store, attempt(), self.marker
            )

        self.assertFalse(Path(self.marker).exists())

    def test_unbound_attempt_rejected(self):
        value = attempt()
        value.pop("schema_version")

        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            with self.assertRaises(ValueError):
                execute_supervised_inert(
                    store, value, self.marker
                )

        self.assertFalse(Path(self.marker).exists())

    def test_duplicate_execution_refused(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            first = execute_supervised_inert(
                store, attempt(), self.marker
            )

            self.assertEqual(first.exit_code, 0)

            with self.assertRaises(FileExistsError):
                execute_supervised_inert(
                    store, attempt(), self.marker
                )

        self.assertEqual(
            Path(self.marker).read_bytes(),
            b"RELEASED\n",
        )

        record = DockerExecutionEvidenceStore(
            self.evidence
        ).read("gate22b-lab")

        self.assertEqual(record["phase"], EXIT_OBSERVED)

    def test_non_started_attempt_rejected(self):
        value = attempt()
        value["status"] = "FAILED"

        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            with self.assertRaises(ValueError):
                execute_supervised_inert(
                    store, value, self.marker
                )

        self.assertFalse(Path(self.marker).exists())


if __name__ == "__main__":
    unittest.main()
