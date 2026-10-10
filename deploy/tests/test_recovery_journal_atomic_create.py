#!/usr/bin/env python3
"""Atomic journal-creation regression tests."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from recovery_journal import RecoveryJournal
from rollback_planner import ImagePair


class AtomicCreateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)

        self.root = Path(self.temporary.name) / "journals"
        self.root.mkdir(mode=0o700)

        self.journal = RecoveryJournal(self.root)
        self.release_id = "fbweb-atomic-001"

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

    def test_complete_record_created(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )

        record = self.journal.read(self.release_id)
        self.assertEqual(record["revision"], 0)
        self.assertEqual(record["state"], "PRECHECK")

    def test_publication_failure_leaves_no_journal(self):
        with patch(
            "recovery_journal.os.link",
            side_effect=OSError("Simulated publication failure"),
        ):
            with self.assertRaises(OSError):
                self.journal.create(
                    self.release_id, self.candidate, self.previous
                )

        self.assertFalse(
            self.journal.path(self.release_id).exists()
        )
        self.assertEqual(
            list(self.root.glob(".journal-*")), []
        )

    def test_existing_journal_is_not_overwritten(self):
        original = self.journal.create(
            self.release_id, self.candidate, self.previous
        )

        with self.assertRaises(FileExistsError):
            self.journal.create(
                self.release_id, self.candidate, self.previous
            )

        self.assertEqual(
            self.journal.read(self.release_id), original
        )


if __name__ == "__main__":
    unittest.main()
