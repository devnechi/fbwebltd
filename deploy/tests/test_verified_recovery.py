#!/usr/bin/env python3
"""Tests for verified-identity recovery decisions."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from docker_identity import VerifiedIdentity
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan
from verified_recovery import decide_verified


class VerifiedRecoveryTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        root = Path(self.temp.name)
        journal_dir = root / "journals"
        lock_dir = root / "locks"
        journal_dir.mkdir(mode=0o700)
        lock_dir.mkdir(mode=0o700)

        self.simulator = RecoverySimulator(journal_dir, lock_dir)
        self.release_id = "fbweb-verified-001"
        self.database_id = "c" * 64

        self.previous = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )
        self.candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "d" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "e" * 64,
        )

        self.simulator.journal.create(
            self.release_id, self.candidate, self.previous
        )
        self.simulator.create_checkpoint(
            self.release_id, self.database_id
        )

        plan = ReleasePlan(
            candidate=self.candidate,
            previous=self.previous,
            approval_verified=True,
            provenance_verified=True,
            recovery_record_persisted=True,
            backup_verified=True,
            deployment_lock_acquired=True,
            current_health_verified=True,
        )

        self.simulator.journal.advance(
            self.release_id, 0, "precheck_passed", plan
        )
        self.simulator.journal.advance(
            self.release_id, 1, "activate", plan
        )

    def identity(self, app, web, db=None, project=None):
        return VerifiedIdentity(
            project=project or "fbweb-gate16v-lab",
            app_reference=app,
            web_reference=web,
            db_container_id=db or self.database_id,
            app_container_id="1" * 64,
            web_container_id="2" * 64,
            app_healthy=True,
            web_healthy=True,
        )

    def test_candidate_requests_restore(self):
        result = decide_verified(
            self.simulator,
            self.release_id,
            self.identity(
                self.candidate.app,
                self.candidate.web,
            ),
        )
        self.assertEqual(result["action"], "RESTORE_PREVIOUS")
        self.assertFalse(result["docker_executed"])

    def test_mixed_images_request_restore(self):
        result = decide_verified(
            self.simulator,
            self.release_id,
            self.identity(
                self.candidate.app,
                self.previous.web,
            ),
        )
        self.assertEqual(result["action"], "RESTORE_PREVIOUS")

    def test_healthy_previous_requires_no_action(self):
        result = decide_verified(
            self.simulator,
            self.release_id,
            self.identity(
                self.previous.app,
                self.previous.web,
            ),
        )
        self.assertEqual(result["action"], "NO_ACTION")

    def test_database_change_requires_intervention(self):
        result = decide_verified(
            self.simulator,
            self.release_id,
            self.identity(
                self.candidate.app,
                self.candidate.web,
                db="f" * 64,
            ),
        )
        self.assertEqual(
            result["action"], "MANUAL_INTERVENTION"
        )
        self.assertFalse(result["database_identity_matched"])

    def test_unknown_image_rejected(self):
        unknown = (
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "f" * 64
        )
        with self.assertRaises(ValueError):
            decide_verified(
                self.simulator,
                self.release_id,
                self.identity(unknown, self.candidate.web),
            )

    def test_production_project_rejected(self):
        with self.assertRaises(ValueError):
            decide_verified(
                self.simulator,
                self.release_id,
                self.identity(
                    self.candidate.app,
                    self.candidate.web,
                    project="fbweb",
                ),
            )

    def test_missing_checkpoint_rejected(self):
        path = self.simulator.checkpoint_path(self.release_id)
        path.unlink()

        with self.assertRaises(FileNotFoundError):
            decide_verified(
                self.simulator,
                self.release_id,
                self.identity(
                    self.candidate.app,
                    self.candidate.web,
                ),
            )

    def test_journal_does_not_change(self):
        before = self.simulator.journal.read(self.release_id)

        decide_verified(
            self.simulator,
            self.release_id,
            self.identity(
                self.candidate.app,
                self.candidate.web,
            ),
        )

        after = self.simulator.journal.read(self.release_id)
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
