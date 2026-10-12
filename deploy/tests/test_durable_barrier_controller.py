#!/usr/bin/env python3
"""Gate 4D.22B.3: inert durable barrier integration tests."""

from pathlib import Path
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest


TESTS = Path(__file__).resolve().parent
RELEASES = TESTS.parent / "releases"
REPO = TESTS.parents[1]

sys.path.insert(0, str(RELEASES))
sys.path.insert(0, str(TESTS))

from docker_execution_evidence import (
    DockerExecutionEvidenceStore,
    PREPARED,
    OBSERVED,
)
from docker_process_supervision import (
    ProcessIdentity,
    ProcessStatus,
    observe_linux_process,
)
from durable_barrier_controller import prepare_bound_barrier
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from test_docker_execution_evidence import attempt


@unittest.skipUnless(
    sys.platform.startswith("linux"),
    "Linux required",
)
class DurableBarrierTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.evidence = self.root / "evidence"
        self.evidence.mkdir(mode=0o700)

        self.marker = str(self.root / "action-marker")
        self.store = DockerExecutionEvidenceStore(self.evidence)

    def assert_denied(self, release_id="gate22b-lab"):
        result = self.store.assess(release_id)
        self.assertFalse(result.docker_operation_settled)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_reconciliation_required)

    def test_prepared_then_observed_before_release(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        try:
            record = self.store.read("gate22b-lab")
            self.assertEqual(record["phase"], OBSERVED)
            self.assertEqual(record["pid"], binding.child.identity.pid)
            self.assertFalse(Path(self.marker).exists())
            self.assertTrue(binding.verify())
            self.assert_denied()
        finally:
            binding.close_without_release()
            self.assertEqual(binding.wait(), 76)

    def test_release_after_durable_observation(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        try:
            binding.release()
            self.assertEqual(binding.wait(), 0)
            self.assertEqual(
                Path(self.marker).read_bytes(),
                b"RELEASED\n",
            )
            self.assertEqual(
                self.store.read("gate22b-lab")["phase"],
                OBSERVED,
            )
            self.assert_denied()
        finally:
            binding.close_without_release()

    def test_closed_barrier_cannot_be_released(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        binding.close_without_release()
        with self.assertRaises(ValueError):
            binding.release()
        self.assertEqual(binding.wait(), 76)
        self.assertFalse(Path(self.marker).exists())

    def test_duplicate_release_rejected(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        try:
            binding.release()
            self.assertEqual(binding.wait(), 0)
            with self.assertRaises(ValueError):
                binding.release()
            self.assert_denied()
        finally:
            binding.close_without_release()

    def test_fingerprint_mismatch_blocks_release(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        try:
            binding.operation_fingerprint = "f" * 64
            with self.assertRaises(ValueError):
                binding.release()
            self.assertEqual(binding.wait(), 76)
            self.assertFalse(Path(self.marker).exists())
        finally:
            binding.close_without_release()

    def test_pid_mismatch_blocks_release(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        try:
            binding.child.identity = ProcessIdentity(
                binding.child.identity.pid,
                binding.child.identity.start_ticks + 1,
            )
            with self.assertRaises(ValueError):
                binding.release()
            self.assertEqual(binding.wait(), 76)
            self.assertFalse(Path(self.marker).exists())
        finally:
            binding.close_without_release()

    def test_duplicate_prepare_fails_closed(self):
        binding = prepare_bound_barrier(
            self.store, attempt(), self.marker
        )
        try:
            with self.assertRaises(FileExistsError):
                prepare_bound_barrier(
                    self.store, attempt(), self.marker
                )
            self.assertFalse(Path(self.marker).exists())
        finally:
            binding.close_without_release()
            binding.wait()

    def test_crash_before_and_after_observation(self):
        for phase in ("before", "after"):
            with self.subTest(phase=phase):
                self._test_controller_crash(phase)

    def _test_controller_crash(self, phase):
        root = self.root / phase
        root.mkdir()

        evidence = root / "evidence"
        evidence.mkdir(mode=0o700)

        marker = root / "marker"
        ready = root / "ready"
        child_info = root / "child-info"

        worker = r"""
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, os.environ["TEST_RELEASES"])
sys.path.insert(0, os.environ["TEST_TESTS"])

from docker_execution_evidence import DockerExecutionEvidenceStore
from durable_barrier_controller import prepare_bound_barrier
from docker_start_barrier import spawn_blocked_child
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from test_docker_execution_evidence import attempt

root = Path(os.environ["TEST_ROOT"])
store = DockerExecutionEvidenceStore(root / "evidence")
phase = os.environ["TEST_PHASE"]

if phase == "before":
    store.prepare(attempt(), plan_lab_rollback(PREVIOUS))
    child = spawn_blocked_child(str(root / "marker"))
else:
    binding = prepare_bound_barrier(
        store, attempt(), str(root / "marker")
    )
    child = binding.child

with open(root / "child-info", "w") as handle:
    handle.write(
        f"{child.identity.pid} "
        f"{child.identity.start_ticks}\n"
    )
    handle.flush()
    os.fsync(handle.fileno())

(root / "ready").write_text("READY\n")
time.sleep(120)
"""

        env = dict(os.environ)
        env.update({
            "TEST_RELEASES": str(RELEASES),
            "TEST_TESTS": str(TESTS),
            "TEST_ROOT": str(root),
            "TEST_PHASE": phase,
            "PYTHONDONTWRITEBYTECODE": "1",
        })

        controller = subprocess.Popen(
            [sys.executable, "-c", worker],
            cwd=str(REPO),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            deadline = time.monotonic() + 15

            while not ready.exists():
                if controller.poll() is not None:
                    diagnostic = controller.stderr.read()
                    self.fail(
                        f"Controller exited in {phase}: "
                        f"{diagnostic[-3000:]}"
                    )

                if time.monotonic() >= deadline:
                    self.fail("Crash setup timed out")

                time.sleep(0.02)

            pid, ticks = child_info.read_text().strip().split()
            identity = ProcessIdentity(int(pid), int(ticks))

            current = DockerExecutionEvidenceStore(evidence).read(
                "gate22b-lab"
            )

            self.assertEqual(
                current["phase"],
                PREPARED if phase == "before" else OBSERVED,
            )

            self.assertEqual(
                observe_linux_process(identity).status,
                ProcessStatus.ACTIVE,
            )

            self.assertFalse(marker.exists())

            os.kill(controller.pid, signal.SIGKILL)
            controller.wait(timeout=10)

            self.assertEqual(
                controller.returncode,
                -signal.SIGKILL,
            )

            deadline = time.monotonic() + 15

            while time.monotonic() < deadline:
                status = observe_linux_process(identity).status

                if status in (
                    ProcessStatus.EXITED,
                    ProcessStatus.MISSING,
                ):
                    break

                time.sleep(0.05)
            else:
                self.fail(
                    "Orphaned blocked child did not exit"
                )

            self.assertFalse(marker.exists())

            reopened = DockerExecutionEvidenceStore(evidence)
            persisted = reopened.read("gate22b-lab")

            self.assertEqual(
                persisted["phase"],
                PREPARED if phase == "before" else OBSERVED,
            )

            assessment = reopened.assess("gate22b-lab")
            self.assertFalse(
                assessment.automatic_retry_permitted
            )
            self.assertTrue(
                assessment.manual_reconciliation_required
            )

        finally:
            if controller.poll() is None:
                controller.kill()
                controller.wait(timeout=10)

            if controller.stderr is not None:
                controller.stderr.close()


if __name__ == "__main__":
    unittest.main()
