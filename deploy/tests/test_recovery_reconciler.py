#!/usr/bin/env python3
"""Interrupted-release recovery decision tests."""

import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from recovery_reconciler import (
    ContainerSnapshot,
    RecoveryAction,
    reconcile,
)
from recovery_journal import timestamp
from rollback_planner import ImagePair


class RecoveryReconcilerTests(unittest.TestCase):

    def setUp(self):
        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        )

        self.record = {
            "schema_version": 1,
            "release_id": "fbweb-test-001",
            "revision": 2,
            "state": "ACTIVATING",
            "candidate": vars(self.candidate),
            "previous": vars(self.previous),
            "updated_at": timestamp(),
        }

        self.db_identity = "known-db-container-id"

    def snapshot(self, pair, healthy=True):
        return ContainerSnapshot(
            app_image=pair.app,
            web_image=pair.web,
            db_identity=self.db_identity,
            app_healthy=healthy,
            web_healthy=healthy,
        )

    def test_candidate_requires_rollback(self):
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(self.candidate),
                self.db_identity,
            ),
            RecoveryAction.RESTORE_PREVIOUS,
        )

    def test_partial_activation_requires_rollback(self):
        mixed = ImagePair(self.candidate.app, self.previous.web)
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(mixed),
                self.db_identity,
            ),
            RecoveryAction.RESTORE_PREVIOUS,
        )

    def test_previous_healthy_requires_no_change(self):
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(self.previous),
                self.db_identity,
            ),
            RecoveryAction.NO_ACTION,
        )

    def test_previous_unhealthy_requires_intervention(self):
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(self.previous, healthy=False),
                self.db_identity,
            ),
            RecoveryAction.MANUAL_INTERVENTION,
        )

    def test_changed_database_identity_blocks_recovery(self):
        snapshot = self.snapshot(self.candidate)
        snapshot = ContainerSnapshot(
            snapshot.app_image,
            snapshot.web_image,
            "unexpected-database-id",
            True,
            True,
        )
        self.assertEqual(
            reconcile(self.record, snapshot, self.db_identity),
            RecoveryAction.MANUAL_INTERVENTION,
        )

    def test_ready_state_aborts_without_changes(self):
        self.record["state"] = "READY"
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(self.previous),
                self.db_identity,
            ),
            RecoveryAction.ABORT_BEFORE_ACTIVATION,
        )

    def test_unknown_images_require_manual_intervention(self):
        unexpected = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "e" * 64,
            self.previous.web,
        )
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(unexpected),
                self.db_identity,
            ),
            RecoveryAction.MANUAL_INTERVENTION,
        )

    def test_recovery_failed_remains_manual(self):
        self.record["state"] = "RECOVERY_FAILED"
        self.assertEqual(
            reconcile(
                self.record,
                self.snapshot(self.candidate),
                self.db_identity,
            ),
            RecoveryAction.MANUAL_INTERVENTION,
        )


if __name__ == "__main__":
    unittest.main()
