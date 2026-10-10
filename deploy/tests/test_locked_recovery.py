#!/usr/bin/env python3
"""Tests for a single Docker observation under the deployment lock."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from locked_recovery import decide_from_docker
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan


class LockedRecoveryTests(unittest.TestCase):

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)

        base = Path(self.temporary.name)
        journals = base / "journals"
        locks = base / "locks"
        journals.mkdir(mode=0o700)
        locks.mkdir(mode=0o700)

        self.simulator = RecoverySimulator(journals, locks)
        self.release_id = "fbweb-locked-001"
        self.project = "fbweb-gate16w-lab"
        self.db_id = "c" * 64

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
        self.simulator.create_checkpoint(self.release_id, self.db_id)

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

        self.calls = []
        self.running = self.candidate
        self.observed_db_id = self.db_id

    def container(self, service, container_id, image_id, reference):
        return {
            "Id": container_id,
            "Image": image_id,
            "Config": {
                "Image": reference,
                "Labels": {
                    "com.docker.compose.project": self.project,
                    "com.docker.compose.service": service,
                },
            },
            "State": {
                "Running": True,
                "Health": {"Status": "healthy"},
            },
        }

    def runner(self, argv, **kwargs):
        self.calls.append(argv)

        app_image_id = "sha256:" + "1" * 64
        web_image_id = "sha256:" + "2" * 64
        db_image_id = "sha256:" + "3" * 64

        containers = [
            self.container(
                "app", "a" * 64, app_image_id, self.running.app
            ),
            self.container(
                "web", "b" * 64, web_image_id, self.running.web
            ),
            self.container(
                "db", self.observed_db_id, db_image_id, "busybox:1.36"
            ),
        ]

        images = [
            {
                "Id": app_image_id,
                "RepoDigests": [self.running.app],
            },
            {
                "Id": web_image_id,
                "RepoDigests": [self.running.web],
            },
            {
                "Id": db_image_id,
                "RepoDigests": ["busybox@sha256:" + "f" * 64],
            },
        ]

        if argv[1] == "ps":
            output = "\n".join(
                item["Id"][:12] for item in containers
            ) + "\n"
        elif argv[1:3] == ["inspect", "--type"]:
            output = json.dumps(containers)
        elif argv[1:3] == ["image", "inspect"]:
            output = json.dumps(images)
        else:
            raise AssertionError("Unexpected command: " + str(argv))

        return SimpleNamespace(stdout=output)

    def decide(self):
        return decide_from_docker(
            self.simulator,
            self.release_id,
            self.project,
            runner=self.runner,
        )

    def test_candidate_requests_rollback(self):
        result = self.decide()
        self.assertEqual(result["action"], "RESTORE_PREVIOUS")
        self.assertFalse(result["docker_mutation_performed"])

    def test_mixed_images_request_rollback(self):
        self.running = ImagePair(
            self.candidate.app, self.previous.web
        )
        result = self.decide()
        self.assertEqual(result["action"], "RESTORE_PREVIOUS")

    def test_previous_images_need_no_action(self):
        self.running = self.previous
        result = self.decide()
        self.assertEqual(result["action"], "NO_ACTION")

    def test_database_change_requires_intervention(self):
        self.observed_db_id = "9" * 64
        result = self.decide()
        self.assertEqual(
            result["action"], "MANUAL_INTERVENTION"
        )
        self.assertFalse(result["database_identity_matched"])

    def test_single_docker_collection(self):
        self.decide()
        self.assertEqual(
            [call[1] for call in self.calls],
            ["ps", "inspect", "image"],
        )

    def test_production_project_rejected_without_docker(self):
        with self.assertRaises(ValueError):
            decide_from_docker(
                self.simulator,
                self.release_id,
                "fbweb",
                runner=self.runner,
            )
        self.assertEqual(self.calls, [])

    def test_journal_unchanged(self):
        before = self.simulator.journal.read(self.release_id)
        self.decide()
        after = self.simulator.journal.read(self.release_id)
        self.assertEqual(after, before)

    def test_lock_blocks_concurrent_operation(self):
        from deployment_lock import deployment_lock

        with deployment_lock(self.simulator.lock_dir):
            with self.assertRaises(RuntimeError):
                self.decide()

        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
