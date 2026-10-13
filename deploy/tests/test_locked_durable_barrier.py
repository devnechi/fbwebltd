#!/usr/bin/env python3
"""Gate 4D.22B.4: lease rejection and post-release SIGKILL."""

import os
from pathlib import Path
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

from deployment_lock import deployment_lock
from docker_execution_evidence import (
    DockerExecutionEvidenceStore,
    OBSERVED,
)
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from locked_durable_barrier import (
    LockedEvidenceStore,
    prepare_locked_barrier,
)
from test_docker_execution_evidence import attempt


@unittest.skipUnless(
    sys.platform.startswith("linux"),
    "Linux required",
)
class LockedDurableBarrierTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.evidence = self.root / "evidence"
        self.locks = self.root / "locks"
        self.marker = str(self.root / "marker")

        self.evidence.mkdir(mode=0o700)
        self.locks.mkdir(mode=0o700)

    def test_missing_lease_rejected(self):
        with self.assertRaises(RuntimeError):
            LockedEvidenceStore(
                self.evidence, self.locks, None
            )

    def test_wrong_lock_directory_rejected(self):
        other = self.root / "other-lock"
        other.mkdir(mode=0o700)

        with deployment_lock(self.locks) as lease:
            with self.assertRaises(RuntimeError):
                LockedEvidenceStore(
                    self.evidence, other, lease
                )

    def test_expired_lease_blocks_prepare(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

        with self.assertRaises(RuntimeError):
            store.prepare(
                attempt(), plan_lab_rollback(PREVIOUS)
            )

        self.assertFalse(
            store.path("gate22b-lab").exists()
        )

    def test_active_lease_allows_inert_release(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            binding = prepare_locked_barrier(
                store, attempt(), self.marker
            )

            try:
                self.assertTrue(binding.verify())
                self.assertFalse(Path(self.marker).exists())

                binding.release()
                self.assertEqual(binding.wait(), 0)

                self.assertEqual(
                    Path(self.marker).read_bytes(),
                    b"RELEASED\n",
                )
            finally:
                binding.close_without_release()

        reopened = DockerExecutionEvidenceStore(
            self.evidence
        )

        self.assertEqual(
            reopened.read("gate22b-lab")["phase"],
            OBSERVED,
        )

        self.assertFalse(
            reopened.assess(
                "gate22b-lab"
            ).automatic_retry_permitted
        )

    def test_expired_lease_blocks_release(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            binding = prepare_locked_barrier(
                store, attempt(), self.marker
            )

        try:
            with self.assertRaises(RuntimeError):
                binding.release()

            self.assertEqual(binding.wait(), 76)
            self.assertFalse(Path(self.marker).exists())
        finally:
            binding.close_without_release()

    def test_competing_lock_is_rejected(self):
        with deployment_lock(self.locks):
            with self.assertRaises(RuntimeError):
                with deployment_lock(self.locks):
                    pass

    def test_duplicate_preparation_is_rejected(self):
        with deployment_lock(self.locks) as lease:
            store = LockedEvidenceStore(
                self.evidence, self.locks, lease
            )

            binding = prepare_locked_barrier(
                store, attempt(), self.marker
            )

            try:
                with self.assertRaises(FileExistsError):
                    prepare_locked_barrier(
                        store, attempt(), self.marker
                    )
            finally:
                binding.close_without_release()
                binding.wait()

    def test_post_release_sigkill_remains_unresolved(self):
        """A released child may finish after controller SIGKILL."""

        worker = r"""
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, os.environ["TEST_RELEASES"])
sys.path.insert(0, os.environ["TEST_TESTS"])

from deployment_lock import deployment_lock
from locked_durable_barrier import (
    LockedEvidenceStore,
    prepare_locked_barrier,
)
from test_docker_execution_evidence import attempt

root = Path(os.environ["TEST_ROOT"])

with deployment_lock(root / "locks") as lease:
    store = LockedEvidenceStore(
        root / "evidence",
        root / "locks",
        lease,
    )

    binding = prepare_locked_barrier(
        store,
        attempt(),
        str(root / "marker"),
    )

    binding.release()

    # Parent will kill this controller after the inert action
    # has completed. The evidence must still be unresolved.
    binding.wait(timeout=10)

    with open(root / "released", "w") as handle:
        handle.write("RELEASED\n")
        handle.flush()
        os.fsync(handle.fileno())

    time.sleep(120)
"""

        env = dict(os.environ)
        env.update({
            "TEST_RELEASES": str(RELEASES),
            "TEST_TESTS": str(TESTS),
            "TEST_ROOT": str(self.root),
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
            ready = self.root / "released"
            deadline = time.monotonic() + 15

            while not ready.exists():
                if controller.poll() is not None:
                    error = controller.stderr.read()
                    self.fail(
                        "Controller exited early: "
                        + error[-3000:]
                    )

                if time.monotonic() >= deadline:
                    self.fail("Post-release setup timed out")

                time.sleep(0.02)

            self.assertEqual(
                Path(self.marker).read_bytes(),
                b"RELEASED\n",
            )

            # While controller owns the lease, a competing
            # controller must not acquire the lock.
            with self.assertRaises(RuntimeError):
                with deployment_lock(self.locks):
                    pass

            os.kill(controller.pid, signal.SIGKILL)
            controller.wait(timeout=10)

            self.assertEqual(
                controller.returncode,
                -signal.SIGKILL,
            )

            # Kernel releases the dead controller's flock.
            # The durable execution record must still block
            # a repeat of the same bound operation.
            with deployment_lock(self.locks) as lease:
                store = LockedEvidenceStore(
                    self.evidence, self.locks, lease
                )

                self.assertEqual(
                    store.read("gate22b-lab")["phase"],
                    OBSERVED,
                )

                with self.assertRaises(FileExistsError):
                    prepare_locked_barrier(
                        store, attempt(), self.marker
                    )

            assessment = DockerExecutionEvidenceStore(
                self.evidence
            ).assess("gate22b-lab")

            self.assertFalse(
                assessment.automatic_retry_permitted
            )
            self.assertFalse(
                assessment.docker_operation_settled
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
