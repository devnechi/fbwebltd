#!/usr/bin/env python3
"""Tests for the non-provisioning rollback attempt reader."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from deployment_lock import deployment_lock
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import AttemptStatus
from rollback_attempt_store import RollbackAttemptStore
from rollback_attempt_view import read_attempts_locked


class RollbackAttemptViewTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        base = Path(self.temp.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-attempt-view-001"

    def read_locked(self):
        with deployment_lock(self.sim.lock_dir):
            return read_attempts_locked(self.sim, self.release_id)

    def test_absent_directory_not_created(self):
        root = self.sim.journal.root / "rollback-attempts"
        self.assertFalse(root.exists())
        self.assertEqual(self.read_locked(), [])
        self.assertFalse(root.exists())

    def test_empty_store_returns_empty_history(self):
        RollbackAttemptStore(self.sim)
        self.assertEqual(self.read_locked(), [])

    def test_symlink_directory_rejected(self):
        root = self.sim.journal.root / "rollback-attempts"
        target = self.sim.journal.root / "target"
        target.mkdir(mode=0o700)
        root.symlink_to(target)

        with self.assertRaises(ValueError):
            self.read_locked()

    def test_insecure_directory_rejected(self):
        root = self.sim.journal.root / "rollback-attempts"
        root.mkdir(mode=0o755)

        with self.assertRaises(ValueError):
            self.read_locked()

    def test_nonsequential_attempt_rejected(self):
        root = self.sim.journal.root / "rollback-attempts"
        directory = root / self.release_id
        root.mkdir(mode=0o700)
        directory.mkdir(mode=0o700)

        bad = directory / "000002.json"
        bad.write_text("{}", encoding="utf-8")
        bad.chmod(0o600)

        with self.assertRaises(ValueError):
            self.read_locked()

    def test_unexpected_file_rejected(self):
        root = self.sim.journal.root / "rollback-attempts"
        directory = root / self.release_id
        root.mkdir(mode=0o700)
        directory.mkdir(mode=0o700)

        (directory / "unexpected.txt").write_text("invalid")

        with self.assertRaises(ValueError):
            self.read_locked()

    def test_cannot_mutate_attempt_history(self):
        root = self.sim.journal.root / "rollback-attempts"
        directory = root / self.release_id
        root.mkdir(mode=0o700)
        directory.mkdir(mode=0o700)

        before = set(directory.iterdir())
        self.assertEqual(self.read_locked(), [])
        after = set(directory.iterdir())

        self.assertEqual(before, after)

    def test_attempt_status_enum_remains_available(self):
        self.assertEqual(AttemptStatus.STARTED.value, "STARTED")


if __name__ == "__main__":
    unittest.main()
