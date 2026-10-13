#!/usr/bin/env python3
"""Independent-process deployment lock and crash-release tests."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RELEASES = Path(__file__).resolve().parents[1] / "releases"

HOLDER = """
import sys
import time
from deployment_lock import deployment_lock

with deployment_lock(sys.argv[1]):
    print("LOCK_ACQUIRED", flush=True)
    time.sleep(300)
"""

CONTENDER = """
import sys
from deployment_lock import deployment_lock

try:
    with deployment_lock(sys.argv[1]):
        print("ACQUIRED")
except RuntimeError:
    print("BUSY")
    sys.exit(3)
"""


class CrossProcessLockTests(unittest.TestCase):

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)

        self.root = Path(self.temporary.name) / "locks"
        self.root.mkdir(mode=0o700)

        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = str(RELEASES)
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def start_holder(self):
        process = subprocess.Popen(
            [sys.executable, "-c", HOLDER, str(self.root)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.env,
        )

        try:
            ready = process.stdout.readline().strip()
            self.assertEqual(ready, "LOCK_ACQUIRED")
        except BaseException:
            process.kill()
            process.communicate(timeout=5)
            raise

        self.addCleanup(self.stop_holder, process)
        return process

    @staticmethod
    def stop_holder(process):
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=5)

    def contend(self):
        return subprocess.run(
            [sys.executable, "-c", CONTENDER, str(self.root)],
            capture_output=True,
            text=True,
            timeout=10,
            env=self.env,
            check=False,
        )

    def test_second_process_cannot_acquire_lock(self):
        holder = self.start_holder()
        self.assertIsNone(holder.poll())

        result = self.contend()

        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(result.stdout.strip(), "BUSY")

    def test_lock_released_after_process_killed(self):
        holder = self.start_holder()

        holder.kill()
        holder.wait(timeout=5)

        result = self.contend()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "ACQUIRED")


if __name__ == "__main__":
    unittest.main()
