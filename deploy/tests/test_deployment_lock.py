#!/usr/bin/env python3
"""Tests for deployment-wide exclusivity."""

import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from deployment_lock import deployment_lock


class DeploymentLockTests(unittest.TestCase):

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)

        self.root = Path(self.temporary.name) / "locks"
        self.root.mkdir(mode=0o700)

    def test_lock_can_be_acquired(self):
        with deployment_lock(self.root):
            self.assertTrue(
                (self.root / "deployment.lock").is_file()
            )

    def test_second_operation_is_rejected(self):
        with deployment_lock(self.root):
            with self.assertRaises(RuntimeError):
                with deployment_lock(self.root):
                    pass

    def test_lock_released_after_normal_exit(self):
        with deployment_lock(self.root):
            pass

        with deployment_lock(self.root):
            pass

    def test_lock_released_after_exception(self):
        with self.assertRaises(ValueError):
            with deployment_lock(self.root):
                raise ValueError("Simulated failure")

        with deployment_lock(self.root):
            pass

    def test_insecure_directory_rejected(self):
        self.root.chmod(0o755)

        with self.assertRaises(ValueError):
            with deployment_lock(self.root):
                pass

    def test_symlink_directory_rejected(self):
        link = self.root.parent / "linked-locks"
        link.symlink_to(self.root, target_is_directory=True)

        with self.assertRaises(ValueError):
            with deployment_lock(link):
                pass

    def test_lock_permissions(self):
        with deployment_lock(self.root):
            info = (self.root / "deployment.lock").stat()
            self.assertEqual(
                stat.S_IMODE(info.st_mode),
                0o600,
            )

    def test_symlink_lock_file_rejected(self):
        target = self.root / "target"
        target.write_text("unchanged", encoding="utf-8")

        (self.root / "deployment.lock").symlink_to(target)

        with self.assertRaises(OSError):
            with deployment_lock(self.root):
                pass

        self.assertEqual(
            target.read_text(encoding="utf-8"),
            "unchanged",
        )


if __name__ == "__main__":
    unittest.main()
