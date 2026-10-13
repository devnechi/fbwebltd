#!/usr/bin/env python3
"""Durable recovery journal tests."""

import json
import os
import stat
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from recovery_journal import RecoveryJournal
from rollback_planner import ImagePair, ReleasePlan, State


class RecoveryJournalTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "rollback"
        self.root.mkdir(mode=0o700)
        self.journal = RecoveryJournal(self.root)
        self.release_id = "fbweb-test-001"

        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )
        self.plan = ReleasePlan(
            candidate=self.candidate,
            previous=self.previous,
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

    def test_create_and_read(self):
        record = self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        self.assertEqual(record["state"], "PRECHECK")
        self.assertEqual(
            self.journal.read(self.release_id)["previous"]["app"],
            self.previous.app,
        )

    def test_file_permissions(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        mode = stat.S_IMODE(
            self.journal.path(self.release_id).stat().st_mode
        )
        self.assertEqual(mode, 0o600)

    def test_duplicate_release_rejected(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        with self.assertRaises(FileExistsError):
            self.journal.create(
                self.release_id, self.candidate, self.previous
            )

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            self.journal.read("../secrets")

    def test_unprotected_directory_rejected(self):
        self.root.chmod(0o755)
        with self.assertRaises(ValueError):
            RecoveryJournal(self.root)

    def test_symlink_directory_rejected(self):
        link = self.root.parent / "link"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            RecoveryJournal(link)

    def test_malformed_record_rejected(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        path = self.journal.path(self.release_id)
        path.write_text('{"invalid":true}', encoding="utf-8")
        with self.assertRaises(ValueError):
            self.journal.read(self.release_id)

    def test_journal_symlink_rejected(self):
        target = self.root / "target.txt"
        target.write_text("do not overwrite", encoding="utf-8")
        self.journal.path(self.release_id).symlink_to(target)
        with self.assertRaises(OSError):
            self.journal.read(self.release_id)
        self.assertEqual(target.read_text(), "do not overwrite")

    def test_successful_state_persistence(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        first = self.journal.advance(
            self.release_id, 0, "precheck_passed", self.plan
        )
        self.assertEqual(first["state"], State.READY.value)

        second = self.journal.advance(
            self.release_id, 1, "activate", self.plan
        )
        self.assertEqual(second["state"], State.ACTIVATING.value)

        reopened = RecoveryJournal(self.root)
        self.assertEqual(
            reopened.read(self.release_id)["state"],
            State.ACTIVATING.value,
        )
        self.assertTrue(reopened.interrupted(self.release_id))

    def test_stale_revision_rejected(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        with self.assertRaises(ValueError):
            self.journal.advance(
                self.release_id, 5, "precheck_passed", self.plan
            )

    def test_mismatched_image_pair_rejected(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        wrong_plan = replace(
            self.plan, candidate=self.previous
        )
        with self.assertRaises(ValueError):
            self.journal.advance(
                self.release_id, 0, "precheck_passed", wrong_plan
            )

    def test_missing_approval_rejected(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        invalid = replace(self.plan, approval_verified=False)
        with self.assertRaises(ValueError):
            self.journal.advance(
                self.release_id, 0, "precheck_passed", invalid
            )

    def test_rollback_state_persistence(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        self.journal.advance(
            self.release_id, 0, "precheck_passed", self.plan
        )
        self.journal.advance(
            self.release_id, 1, "activate", self.plan
        )
        self.journal.advance(self.release_id, 2, "failed")
        self.journal.advance(self.release_id, 3, "restored")
        self.assertFalse(self.journal.interrupted(self.release_id))
        self.assertEqual(
            self.journal.read(self.release_id)["state"],
            State.ROLLED_BACK.value,
        )

    def test_unknown_event_rejected(self):
        self.journal.create(
            self.release_id, self.candidate, self.previous
        )
        with self.assertRaises(ValueError):
            self.journal.advance(
                self.release_id, 0, "deploy_everything", self.plan
            )


if __name__ == "__main__":
    unittest.main()
