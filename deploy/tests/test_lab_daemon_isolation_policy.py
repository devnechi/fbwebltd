#!/usr/bin/env python3
"""Gate 4D.22C.3C.4 isolation declaration regression tests."""

from dataclasses import replace
from pathlib import Path
import sys
import tempfile
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from lab_daemon_isolation_policy import (
    LabIsolationDeclaration,
    REQUIRED_CONTROLS,
    assess_lab_isolation,
    inspect_private_lab_directory,
)


class LabDaemonIsolationPolicyTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        root = Path(self.temp.name)
        self.runtime = root / "runtime"
        self.data = root / "data"

        self.runtime.mkdir(mode=0o700)
        self.data.mkdir(mode=0o700)

        self.declaration = LabIsolationDeclaration(
            daemon_name="fbweb-dedicated-lab",
            socket_path=str(
                self.runtime / "docker-lab.sock"
            ),
            runtime_dir=str(self.runtime),
            data_root=str(self.data),
            controls=tuple(sorted(REQUIRED_CONTROLS)),
        )

    def evaluate(self, **changes):
        value = replace(self.declaration, **changes)
        return assess_lab_isolation(value)

    def test_complete_declaration_is_recognized(self):
        result = self.evaluate()
        self.assertTrue(result.declaration_valid)
        self.assertEqual(result.missing_controls, ())

    def test_complete_declaration_does_not_prove_isolation(self):
        result = self.evaluate()
        self.assertFalse(result.independent_evidence_verified)
        self.assertFalse(result.daemon_identity_proven)
        self.assertFalse(result.daemon_isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_missing_network_isolation_is_reported(self):
        controls = tuple(sorted(
            REQUIRED_CONTROLS - {
                "production_networks_inaccessible"
            }
        ))
        result = self.evaluate(controls=controls)
        self.assertFalse(result.declaration_valid)
        self.assertIn(
            "production_networks_inaccessible",
            result.missing_controls,
        )

    def test_missing_credentials_control_reported(self):
        controls = tuple(sorted(
            REQUIRED_CONTROLS - {
                "production_credentials_absent"
            }
        ))
        result = self.evaluate(controls=controls)
        self.assertFalse(result.declaration_valid)

    def test_host_docker_socket_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                socket_path="/var/run/docker.sock"
            )

    def test_host_docker_data_root_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                data_root="/var/lib/docker"
            )

    def test_nested_host_docker_data_root_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                data_root="/var/lib/docker/volumes/lab"
            )

    def test_runtime_data_overlap_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                data_root=str(self.runtime / "data")
            )

    def test_wrong_daemon_identity_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(
                daemon_name="production-dockerd"
            )

    def test_unknown_control_rejected(self):
        controls = self.declaration.controls + (
            "production_access_allowed",
        )
        with self.assertRaises(ValueError):
            self.evaluate(controls=controls)

    def test_duplicate_control_rejected(self):
        controls = self.declaration.controls + (
            "dedicated_daemon",
        )
        with self.assertRaises(ValueError):
            self.evaluate(controls=controls)

    def test_relative_runtime_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(runtime_dir="runtime")

    def test_private_directory_inspection_passes(self):
        self.assertTrue(
            inspect_private_lab_directory(self.runtime)
        )

    def test_world_accessible_directory_rejected(self):
        self.runtime.chmod(0o755)
        with self.assertRaises(ValueError):
            inspect_private_lab_directory(self.runtime)

    def test_directory_symlink_rejected(self):
        link = Path(self.temp.name) / "linked"
        link.symlink_to(
            self.runtime, target_is_directory=True
        )
        with self.assertRaises(ValueError):
            inspect_private_lab_directory(link)


if __name__ == "__main__":
    unittest.main()
