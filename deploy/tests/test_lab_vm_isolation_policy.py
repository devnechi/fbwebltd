#!/usr/bin/env python3
"""Gate 4D.22C.3D.2 VM baseline policy tests."""

from dataclasses import replace
from pathlib import Path
import sys
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from lab_vm_isolation_policy import (
    LabVMBaseline,
    REQUIRED_CONTROLS,
    assess_vm_baseline,
)


class LabVMBaselineTests(unittest.TestCase):

    def setUp(self):
        self.baseline = LabVMBaseline(
            vm_name="fbweb-dedicated-lab",
            environment="isolated-laboratory",
            network_mode="internal-only",
            guest_address="192.0.2.10",
            docker_data_root="/var/lib/fbweb-lab-docker",
            docker_socket="/run/fbweb-lab/docker-lab.sock",
            host_socket_shared=False,
            host_paths_shared=False,
            production_credentials_present=False,
            production_network_reachable=False,
            snapshot_policy="snapshot-before-each-experiment",
            controls=tuple(sorted(REQUIRED_CONTROLS)),
        )

    def evaluate(self, **changes):
        return assess_vm_baseline(
            replace(self.baseline, **changes)
        )

    def test_complete_declaration_accepted(self):
        result = self.evaluate()
        self.assertTrue(result.declaration_valid)
        self.assertEqual(result.missing_controls, ())

    def test_declaration_does_not_authorize_docker(self):
        result = self.evaluate()
        self.assertFalse(result.runtime_evidence_verified)
        self.assertFalse(result.isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.production_execution_enabled)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_host_socket_sharing_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(host_socket_shared=True)

    def test_host_filesystem_sharing_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(host_paths_shared=True)

    def test_production_credentials_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(production_credentials_present=True)

    def test_production_network_access_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(production_network_reachable=True)

    def test_host_network_mode_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(network_mode="bridged")

    def test_nat_network_mode_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(network_mode="nat")

    def test_wrong_environment_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(environment="production")

    def test_wrong_vm_identity_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(vm_name="production-docker")

    def test_host_docker_storage_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(docker_data_root="/var/lib/docker")

    def test_host_docker_socket_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(docker_socket="/var/run/docker.sock")

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                docker_data_root="/var/lib/../lib/fbweb-lab-docker"
            )

    def test_missing_snapshot_policy_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(snapshot_policy="none")

    def test_missing_isolation_control_detected(self):
        controls = tuple(sorted(
            REQUIRED_CONTROLS - {"no_production_credentials"}
        ))
        result = self.evaluate(controls=controls)
        self.assertFalse(result.declaration_valid)
        self.assertIn(
            "no_production_credentials",
            result.missing_controls,
        )

    def test_unknown_control_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                controls=self.baseline.controls + (
                    "allow_production_access",
                )
            )

    def test_duplicate_control_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                controls=self.baseline.controls + (
                    "dedicated_vm",
                )
            )

    def test_invalid_network_address_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(guest_address="10.0.0.1")

    def test_invalid_boolean_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(host_socket_shared="false")


if __name__ == "__main__":
    unittest.main()
