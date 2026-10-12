#!/usr/bin/env python3
"""Gate 4D.22B.1: durable, fail-closed execution evidence."""

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(ROOT))

from docker_execution_evidence import (
    DockerExecutionEvidenceStore,
    PREPARED,
    OBSERVED,
    EXIT_OBSERVED,
    command_fingerprint,
)
from docker_process_supervision import ProcessIdentity
from lab_rollback_command import LAB_PROJECT, PREVIOUS, plan_lab_rollback


def attempt():
    stamp = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": 2,
        "attempt_id": "attempt-000001",
        "execution_id": "a" * 32,
        "release_id": "gate22b-lab",
        "status": "STARTED",
        "revision": 0,
        "journal_revision": 3,
        "operation_fingerprint": "b" * 64,
        "project": LAB_PROJECT,
        "previous_app": PREVIOUS.app,
        "previous_web": PREVIOUS.web,
        "candidate_app":
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "c" * 64,
        "candidate_web":
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "d" * 64,
        "database_identity": "e" * 64,
        "created_at": stamp,
        "updated_at": stamp,
    }


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "evidence"
        self.root.mkdir(mode=0o700)
        self.store = DockerExecutionEvidenceStore(self.root)
        self.command = plan_lab_rollback(PREVIOUS)

    def prepare(self):
        return self.store.prepare(attempt(), self.command)

    def test_prepared_durable_across_new_store(self):
        record = self.prepare()
        reopened = DockerExecutionEvidenceStore(self.root)
        self.assertEqual(reopened.read("gate22b-lab"), record)

    def test_prepared_does_not_invent_pid(self):
        record = self.prepare()
        self.assertEqual(record["phase"], PREPARED)
        self.assertIsNone(record["pid"])

    def test_duplicate_prepare_rejected(self):
        self.prepare()
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_wrong_project_rejected(self):
        value = attempt()
        value["project"] = "fbweb"
        with self.assertRaises(ValueError):
            self.store.prepare(value, self.command)

    def test_non_started_attempt_rejected(self):
        value = attempt()
        value["status"] = "FAILED"
        with self.assertRaises(ValueError):
            self.store.prepare(value, self.command)

    def test_wrong_previous_image_rejected(self):
        value = attempt()
        value["previous_app"] = value["candidate_app"]
        with self.assertRaises(ValueError):
            self.store.prepare(value, self.command)

    def test_command_fingerprint_stable(self):
        self.assertEqual(
            command_fingerprint(self.command),
            command_fingerprint(plan_lab_rollback(PREVIOUS)),
        )

    def test_observe_process_persists(self):
        self.prepare()
        identity = ProcessIdentity(1234, 56789)
        record = self.store.observe("gate22b-lab", identity)
        self.assertEqual(record["phase"], OBSERVED)
        self.assertEqual(record["pid"], 1234)
        self.assertEqual(
            DockerExecutionEvidenceStore(self.root)
            .read("gate22b-lab")["start_ticks"],
            56789,
        )

    def test_observe_before_prepare_rejected(self):
        with self.assertRaises(FileNotFoundError):
            self.store.observe(
                "gate22b-lab", ProcessIdentity(1234, 56789)
            )

    def test_duplicate_observation_rejected(self):
        self.prepare()
        self.store.observe(
            "gate22b-lab", ProcessIdentity(1234, 56789)
        )
        with self.assertRaises(ValueError):
            self.store.observe(
                "gate22b-lab", ProcessIdentity(9999, 99999)
            )

    def test_exit_before_observation_rejected(self):
        self.prepare()
        with self.assertRaises(ValueError):
            self.store.record_exit("gate22b-lab", 0)

    def test_exit_record_does_not_authorize_retry(self):
        self.prepare()
        self.store.observe(
            "gate22b-lab", ProcessIdentity(1234, 56789)
        )
        record = self.store.record_exit("gate22b-lab", 0)
        self.assertEqual(record["phase"], EXIT_OBSERVED)
        assessment = self.store.assess("gate22b-lab")
        self.assertFalse(assessment.docker_operation_settled)
        self.assertFalse(assessment.automatic_retry_permitted)
        self.assertTrue(assessment.manual_reconciliation_required)

    def test_failure_exit_does_not_authorize_retry(self):
        self.prepare()
        self.store.observe(
            "gate22b-lab", ProcessIdentity(1234, 56789)
        )
        self.store.record_exit("gate22b-lab", 1)
        self.assertFalse(
            self.store.assess("gate22b-lab").automatic_retry_permitted
        )

    def test_invalid_release_id_rejected(self):
        with self.assertRaises(ValueError):
            self.store.read("../production")

    def test_symlink_record_rejected(self):
        destination = self.store.path("gate22b-lab")
        destination.symlink_to("/etc/passwd")
        with self.assertRaises(ValueError):
            self.store.read("gate22b-lab")

    def test_unprivate_directory_rejected(self):
        self.root.chmod(0o755)
        with self.assertRaises(ValueError):
            DockerExecutionEvidenceStore(self.root)

    def test_prepared_is_not_authorization(self):
        self.prepare()
        assessment = self.store.assess("gate22b-lab")
        self.assertFalse(assessment.automatic_retry_permitted)
        self.assertFalse(assessment.docker_operation_settled)


if __name__ == "__main__":
    unittest.main()
