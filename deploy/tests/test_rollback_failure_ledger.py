#!/usr/bin/env python3
"""Failure evidence persistence and isolation tests."""

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
from rollback_failure_ledger import RollbackFailureLedger
from rollback_planner import ImagePair, ReleasePlan


class FailureLedgerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)

        base = Path(temp.name)
        journals = base / "journals"
        locks = base / "locks"

        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)
        (journals / "failure-events").mkdir(mode=0o700)

        self.sim = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-failure-001"

        previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.sim.journal.create(self.release_id, candidate, previous)
        self.sim.create_checkpoint(self.release_id, "e" * 64)

        plan = ReleasePlan(
            candidate=candidate,
            previous=previous,
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

        journal = self.sim.journal
        journal.advance(self.release_id, 0, "precheck_passed", plan)
        journal.advance(self.release_id, 1, "activate", plan)
        journal.advance(self.release_id, 2, "failed")

        self.ledger = RollbackFailureLedger(self.sim)

    def record(self, kind="RESTORATION_COMMAND_FAILED"):
        return self.ledger.record(
            self.release_id,
            kind,
            "Isolated laboratory restoration did not complete",
        )

    def test_first_failure_persisted(self):
        event = self.record()
        self.assertEqual(event["sequence"], 1)
        self.assertEqual(len(self.ledger.read(self.release_id)), 1)

    def test_second_failure_has_new_sequence(self):
        self.record()
        second = self.record("HEALTH_CHECK_FAILED")
        self.assertEqual(second["sequence"], 2)
        self.assertEqual(len(self.ledger.read(self.release_id)), 2)

    def test_reopen_preserves_events(self):
        self.record()
        reopened = RollbackFailureLedger(self.sim)
        self.assertEqual(
            reopened.read(self.release_id),
            self.ledger.read(self.release_id),
        )

    def test_invalid_kind_rejected(self):
        with self.assertRaises(ValueError):
            self.record("DEPLOY_PRODUCTION")

    def test_empty_reason_rejected(self):
        with self.assertRaises(ValueError):
            self.ledger.record(
                self.release_id,
                "INSPECTION_FAILED",
                "",
            )

    def test_finalized_journal_rejects_new_failure(self):
        self.sim.journal.advance(self.release_id, 3, "restored")
        with self.assertRaises(ValueError):
            self.record()

    def test_lock_contention_rejected(self):
        with deployment_lock(self.sim.lock_dir):
            with self.assertRaises(RuntimeError):
                self.record()

    def test_journal_unchanged_by_failure_record(self):
        before = self.sim.journal.read(self.release_id)
        self.record()
        after = self.sim.journal.read(self.release_id)
        self.assertEqual(before, after)

    def test_existing_event_not_overwritten(self):
        first = self.record()
        self.record()
        events = self.ledger.read(self.release_id)
        self.assertEqual(events[0], first)

    def test_database_checkpoint_unchanged(self):
        before = self.sim.read_checkpoint(
            self.release_id,
            self.sim.journal.read(self.release_id),
        )
        self.record()
        after = self.sim.read_checkpoint(
            self.release_id,
            self.sim.journal.read(self.release_id),
        )
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
