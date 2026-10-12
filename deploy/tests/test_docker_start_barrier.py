#!/usr/bin/env python3
"""Gate 4D.22B.2: inert start barrier and controller SIGKILL."""

import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from docker_start_barrier import spawn_blocked_child
from docker_process_supervision import (
    ProcessIdentity,
    ProcessStatus,
    observe_linux_process,
)


@unittest.skipUnless(
    sys.platform.startswith("linux"),
    "Linux process supervision required",
)
class StartBarrierTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.marker = str(Path(self.temp.name) / "marker")

    def test_child_starts_blocked(self):
        child = spawn_blocked_child(self.marker)
        try:
            time.sleep(0.1)
            self.assertIsNone(child.process.poll())
            self.assertFalse(Path(self.marker).exists())
        finally:
            child.close_without_release()
            child.wait()

    def test_release_executes_inert_action(self):
        child = spawn_blocked_child(self.marker)
        try:
            self.assertFalse(Path(self.marker).exists())
            child.release()
            self.assertEqual(child.wait(), 0)
            self.assertEqual(
                Path(self.marker).read_bytes(),
                b"RELEASED\n",
            )
        finally:
            child.close_without_release()

    def test_close_without_release_prevents_action(self):
        child = spawn_blocked_child(self.marker)
        child.close_without_release()
        self.assertEqual(child.wait(), 76)
        self.assertFalse(Path(self.marker).exists())

    def test_duplicate_release_rejected(self):
        child = spawn_blocked_child(self.marker)
        try:
            child.release()
            with self.assertRaises(ValueError):
                child.release()
            self.assertEqual(child.wait(), 0)
        finally:
            child.close_without_release()

    def test_release_after_close_rejected(self):
        child = spawn_blocked_child(self.marker)
        child.close_without_release()
        with self.assertRaises(ValueError):
            child.release()
        self.assertEqual(child.wait(), 76)

    def test_process_identity_captured(self):
        child = spawn_blocked_child(self.marker)
        try:
            self.assertIsInstance(child.identity, ProcessIdentity)
            self.assertEqual(child.identity.pid, child.process.pid)

            observed = observe_linux_process(child.identity)
            self.assertEqual(observed.status, ProcessStatus.ACTIVE)
        finally:
            child.close_without_release()
            child.wait()

    def test_invalid_marker_rejected(self):
        with self.assertRaises(ValueError):
            spawn_blocked_child("")

    def test_controller_sigkill_before_release(self):
        """Kill controller; orphaned child must see EOF and do nothing."""
        child_script = r"""
import os
import sys

sys.path.insert(0, "deploy/releases")
from docker_start_barrier import spawn_blocked_child

child = spawn_blocked_child(os.environ["BARRIER_MARKER"])

with open(os.environ["BARRIER_INFO"], "w") as handle:
    handle.write(
        f"{child.identity.pid} {child.identity.start_ticks}\n"
    )
    handle.flush()
    os.fsync(handle.fileno())

# Remain alive, holding the release write-end.
import time
time.sleep(120)
"""

        info = Path(self.temp.name) / "identity.txt"

        env = dict(os.environ)
        env["BARRIER_MARKER"] = self.marker
        env["BARRIER_INFO"] = str(info)

        controller = subprocess.Popen(
            [sys.executable, "-c", child_script],
            cwd=str(RELEASES.parents[1]),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        try:
            deadline = time.monotonic() + 10

            while not info.exists():
                if controller.poll() is not None:
                    self.fail("Controller exited before identity capture")

                if time.monotonic() > deadline:
                    self.fail("Controller identity capture timed out")

                time.sleep(0.02)

            pid_text, ticks_text = info.read_text().strip().split()
            identity = ProcessIdentity(
                int(pid_text), int(ticks_text)
            )

            self.assertEqual(
                observe_linux_process(identity).status,
                ProcessStatus.ACTIVE,
            )

            os.kill(controller.pid, signal.SIGKILL)
            controller.wait(timeout=10)
            self.assertEqual(
                controller.returncode,
                -signal.SIGKILL,
            )

            deadline = time.monotonic() + 10

            while time.monotonic() < deadline:
                state = observe_linux_process(identity).status

                if state in (
                    ProcessStatus.EXITED,
                    ProcessStatus.MISSING,
                ):
                    break

                time.sleep(0.05)
            else:
                self.fail(
                    "Blocked child did not exit after controller death"
                )

            self.assertFalse(Path(self.marker).exists())

        finally:
            if controller.poll() is None:
                controller.kill()
                controller.wait()

    def test_no_marker_without_explicit_release(self):
        child = spawn_blocked_child(self.marker)
        try:
            time.sleep(0.2)
            self.assertFalse(Path(self.marker).exists())
            self.assertFalse(child.released)
        finally:
            child.close_without_release()
            child.wait()


if __name__ == "__main__":
    unittest.main()
