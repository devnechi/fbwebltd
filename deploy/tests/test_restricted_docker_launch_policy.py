#!/usr/bin/env python3
"""Gate 4D.22C.3B.1: restricted Docker launch policy tests."""

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
from docker_execution_evidence import DockerExecutionEvidenceStore
from docker_process_supervision import (
    ProcessAssessment,
    ProcessIdentity,
    ProcessStatus,
)
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from locked_durable_barrier import LockedEvidenceStore
from restricted_docker_launch_policy import validate_launch_binding
from test_docker_execution_evidence import attempt


class RestrictedDockerLaunchPolicyTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        root = Path(self.temp.name)
        self.evidence = root / "evidence"
        self.locks = root / "locks"

        self.evidence.mkdir(mode=0o700)
        self.locks.mkdir(mode=0o700)

        self.lock_context = deployment_lock(self.locks)
        self.lease = self.lock_context.__enter__()
        self.addCleanup(
            self.lock_context.__exit__, None, None, None
        )

        self.store = LockedEvidenceStore(
            self.evidence, self.locks, self.lease
        )

        self.attempt = attempt()
        self.command = plan_lab_rollback(PREVIOUS)
        self.identity = ProcessIdentity(4321, 98765)

        self.store.prepare(self.attempt, self.command)
        self.store.observe(
            self.attempt["release_id"],
            self.identity,
        )

    def observer(self, identity):
        return ProcessAssessment(
            status=ProcessStatus.ACTIVE,
            original_process_active=True,
            docker_operation_settled=False,
            automatic_retry_permitted=False,
            manual_reconciliation_required=True,
            reason="Simulated active Linux process",
        )

    def evaluate(self, **changes):
        return validate_launch_binding(
            changes.get("store", self.store),
            changes.get("attempt", self.attempt),
            changes.get("command", self.command),
            changes.get("identity", self.identity),
            process_observer=changes.get(
                "observer", self.observer
            ),
        )

    def test_exact_binding_is_valid_precondition_only(self):
        result = self.evaluate()

        self.assertTrue(result.eligible_for_barrier_release)
        self.assertFalse(result.docker_operation_settled)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertFalse(result.production_execution_enabled)

    def test_unleased_store_rejected(self):
        readonly = DockerExecutionEvidenceStore(self.evidence)

        with self.assertRaises(RuntimeError):
            self.evaluate(store=readonly)

    def test_wrong_execution_id_rejected(self):
        value = dict(self.attempt)
        value["execution_id"] = "f" * 32

        with self.assertRaises(ValueError):
            self.evaluate(attempt=value)

    def test_wrong_operation_fingerprint_rejected(self):
        value = dict(self.attempt)
        value["operation_fingerprint"] = "f" * 64

        with self.assertRaises(ValueError):
            self.evaluate(attempt=value)

    def test_different_pid_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                identity=ProcessIdentity(9999, 98765)
            )

    def test_different_kernel_start_ticks_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                identity=ProcessIdentity(4321, 99999)
            )

    def test_mutated_docker_command_rejected(self):
        mutated = replace(
            self.command,
            argv=self.command.argv + ("--remove-orphans",),
        )

        with self.assertRaises(ValueError):
            self.evaluate(command=mutated)

    def test_mutable_image_tag_rejected(self):
        mutated = replace(
            self.command,
            argv=(
                "/usr/bin/docker",
                "compose",
                "up",
                "-d",
            ),
        )

        with self.assertRaises(ValueError):
            self.evaluate(command=mutated)

    def test_wrong_project_rejected(self):
        value = dict(self.attempt)
        value["project"] = "production"

        with self.assertRaises(ValueError):
            self.evaluate(attempt=value)

    def test_completed_process_rejected(self):
        def exited(_identity):
            return ProcessAssessment(
                status=ProcessStatus.EXITED,
                original_process_active=False,
                docker_operation_settled=False,
                automatic_retry_permitted=False,
                manual_reconciliation_required=True,
                reason="Original process exited",
            )

        with self.assertRaises(ValueError):
            self.evaluate(observer=exited)

    def test_pid_reuse_rejected(self):
        def reused(_identity):
            return ProcessAssessment(
                status=ProcessStatus.PID_REUSED,
                original_process_active=False,
                docker_operation_settled=False,
                automatic_retry_permitted=False,
                manual_reconciliation_required=True,
                reason="PID reused",
            )

        with self.assertRaises(ValueError):
            self.evaluate(observer=reused)

    def test_prepared_without_observation_rejected(self):
        self.assertEqual(
            self.store.read("gate22b-lab")["phase"],
            "OBSERVED",
        )

        self.store.record_exit("gate22b-lab", 0)

        with self.assertRaises(ValueError):
            self.evaluate()

    def test_expired_lease_rejected(self):
        other = Path(self.temp.name) / "other-locks"
        other.mkdir(mode=0o700)

        with deployment_lock(other) as lease:
            expired = LockedEvidenceStore(
                self.evidence, other, lease
            )

        with self.assertRaises(RuntimeError):
            self.evaluate(store=expired)


if __name__ == "__main__":
    unittest.main()
