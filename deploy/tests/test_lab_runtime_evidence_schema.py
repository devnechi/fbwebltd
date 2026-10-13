#!/usr/bin/env python3
"""Gate 4D.22C.3D.4 evidence schema security tests."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_runtime_evidence_schema import (
    LAB_DATA_ROOT,
    LAB_NAME,
    LAB_SOCKET,
    REQUIRED_CONTROLS,
    validate_evidence,
)


def sample_evidence():
    return {
        "schema_version": 1,
        "evidence_id": "evidence-001",
        "subject": {
            "vm_id": "vm-001",
            "daemon_id": "daemon-001",
        },
        "provenance": {
            "collector_id": "offline-collector",
            "collection_id": "collection-001",
            "collected_at": "2026-10-13T07:00:00Z",
            "source_type": "offline-record",
            "source_digest": "a" * 64,
        },
        "vm": {
            "vm_id": "vm-001",
            "vm_name": LAB_NAME,
            "configuration_digest": "b" * 64,
            "lifecycle": "declared-isolated",
        },
        "daemon": {
            "vm_id": "vm-001",
            "daemon_id": "daemon-001",
            "daemon_name": LAB_NAME,
            "pid": 1234,
            "start_ticks": 100,
            "socket_path": LAB_SOCKET,
            "data_root": LAB_DATA_ROOT,
        },
        "isolation": {
            "vm_id": "vm-001",
            "daemon_id": "daemon-001",
            "controls": {
                key: True for key in REQUIRED_CONTROLS
            },
        },
    }


class RuntimeEvidenceSchemaTests(unittest.TestCase):

    def test_consistent_declaration_never_authorizes_execution(self):
        result = validate_evidence(sample_evidence())

        self.assertTrue(result.schema_valid)
        self.assertTrue(result.declaration_consistent)
        self.assertFalse(result.runtime_evidence_verified)
        self.assertFalse(result.vm_identity_proven)
        self.assertFalse(result.daemon_identity_proven)
        self.assertFalse(result.daemon_isolation_proven)
        self.assertFalse(result.isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.production_execution_enabled)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_rejects_unknown_schema_version(self):
        data = sample_evidence()
        data["schema_version"] = 2

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_boolean_schema_version(self):
        data = sample_evidence()
        data["schema_version"] = True

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_missing_root_field(self):
        data = sample_evidence()
        del data["provenance"]

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_unexpected_root_field(self):
        data = sample_evidence()
        data["execution_permitted"] = True

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_vm_subject_mismatch(self):
        data = sample_evidence()
        data["vm"]["vm_id"] = "different-vm"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_daemon_subject_mismatch(self):
        data = sample_evidence()
        data["daemon"]["daemon_id"] = "different-daemon"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_isolation_subject_mismatch(self):
        data = sample_evidence()
        data["isolation"]["vm_id"] = "different-vm"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_host_docker_socket(self):
        data = sample_evidence()
        data["daemon"]["socket_path"] = "/run/docker.sock"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_host_docker_data_root(self):
        data = sample_evidence()
        data["daemon"]["data_root"] = "/var/lib/docker"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_boolean_pid(self):
        data = sample_evidence()
        data["daemon"]["pid"] = True

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_invalid_start_ticks(self):
        data = sample_evidence()
        data["daemon"]["start_ticks"] = 0

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_invalid_timestamp(self):
        data = sample_evidence()
        data["provenance"]["collected_at"] = "2026-02-30T07:00:00Z"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_noncanonical_timestamp(self):
        data = sample_evidence()
        data["provenance"]["collected_at"] = "2026-10-13T10:00:00+03:00"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_invalid_source_digest(self):
        data = sample_evidence()
        data["provenance"]["source_digest"] = "not-a-sha256-digest"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_unknown_source_type(self):
        data = sample_evidence()
        data["provenance"]["source_type"] = "verified"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_missing_isolation_control(self):
        data = sample_evidence()
        del data["isolation"]["controls"]["dedicated_vm"]

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_false_isolation_control(self):
        data = sample_evidence()
        data["isolation"]["controls"]["no_production_credentials"] = False

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_string_isolation_control(self):
        data = sample_evidence()
        data["isolation"]["controls"]["dedicated_vm"] = "true"

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_unknown_isolation_control(self):
        data = sample_evidence()
        data["isolation"]["controls"]["allow_production"] = True

        with self.assertRaises(ValueError):
            validate_evidence(data)

    def test_rejects_malformed_evidence(self):
        with self.assertRaises(ValueError):
            validate_evidence([])

    def test_input_is_not_mutated(self):
        data = sample_evidence()
        original = deepcopy(data)

        validate_evidence(data)

        self.assertEqual(data, original)


if __name__ == "__main__":
    unittest.main()
