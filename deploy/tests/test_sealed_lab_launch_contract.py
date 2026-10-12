#!/usr/bin/env python3
"""Gate 4D.22C.3C.1: non-executing sealed contract tests."""

from pathlib import Path
import socket
import sys
import tempfile
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from lab_compose_integrity import APPROVED_COMPOSE, LAB_COMPOSE
from lab_rollback_command import LAB_PROJECT, PREVIOUS
from sealed_lab_launch_contract import (
    seal_lab_launch,
    validate_private_lab_socket,
)


class SealedLabLaunchContractTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.repo = self.root / "repository"
        self.repo.mkdir(mode=0o700)

        self.compose = self.repo / LAB_COMPOSE
        self.compose.parent.mkdir(parents=True)
        self.compose.write_text(
            APPROVED_COMPOSE, encoding="utf-8"
        )

        self.runtime = self.root / "runtime"
        self.runtime.mkdir(mode=0o700)

        self.endpoint = self.runtime / "docker-lab.sock"
        self.listener = socket.socket(
            socket.AF_UNIX, socket.SOCK_STREAM
        )
        self.listener.bind(str(self.endpoint))
        self.endpoint.chmod(0o600)
        self.addCleanup(self.listener.close)

    def seal(self, ambient=None):
        return seal_lab_launch(
            self.repo,
            self.runtime,
            self.endpoint,
            ambient_environment=(
                {} if ambient is None else ambient
            ),
        )

    def test_exact_lab_command_and_images(self):
        sealed = self.seal()

        self.assertEqual(
            sealed.argv[0:2],
            ("/usr/bin/docker", "compose"),
        )
        self.assertIn(LAB_PROJECT, sealed.argv)
        self.assertIn("--no-build", sealed.argv)
        self.assertIn("--force-recreate", sealed.argv)

        env = dict(sealed.environment)
        self.assertEqual(env["LAB_APP_IMAGE"], PREVIOUS.app)
        self.assertEqual(env["LAB_WEB_IMAGE"], PREVIOUS.web)
        self.assertEqual(
            env["DOCKER_HOST"],
            "unix://" + str(self.endpoint),
        )

    def test_result_never_authorizes_execution(self):
        sealed = self.seal()
        self.assertFalse(sealed.production_execution_enabled)
        self.assertFalse(sealed.automatic_retry_permitted)

    def test_default_host_socket_rejected(self):
        with self.assertRaises(ValueError):
            validate_private_lab_socket(
                "/var/run/docker.sock", self.runtime
            )

    def test_tcp_endpoint_rejected(self):
        with self.assertRaises(ValueError):
            validate_private_lab_socket(
                "tcp://127.0.0.1:2375", self.runtime
            )

    def test_wrong_socket_name_rejected(self):
        with self.assertRaises(ValueError):
            validate_private_lab_socket(
                self.runtime / "other.sock",
                self.runtime,
            )

    def test_regular_file_endpoint_rejected(self):
        self.listener.close()
        self.endpoint.unlink()
        self.endpoint.write_text("not a socket")

        with self.assertRaises(ValueError):
            self.seal()

    def test_world_accessible_socket_rejected(self):
        self.endpoint.chmod(0o666)

        with self.assertRaises(ValueError):
            self.seal()

    def test_world_accessible_runtime_rejected(self):
        self.runtime.chmod(0o755)

        with self.assertRaises(ValueError):
            self.seal()

    def test_symlink_endpoint_rejected(self):
        other = self.runtime / "other.sock"
        self.endpoint.rename(other)
        self.endpoint.symlink_to(other)

        with self.assertRaises(ValueError):
            self.seal()

    def test_ambient_docker_host_rejected(self):
        with self.assertRaises(ValueError):
            self.seal({
                "DOCKER_HOST": "unix:///var/run/docker.sock"
            })

    def test_ambient_compose_override_rejected(self):
        with self.assertRaises(ValueError):
            self.seal({
                "COMPOSE_FILE": "/tmp/untrusted.yml"
            })

    def test_ambient_image_override_rejected(self):
        with self.assertRaises(ValueError):
            self.seal({
                "LAB_APP_IMAGE": "untrusted:latest"
            })

    def test_ambient_loader_override_rejected(self):
        with self.assertRaises(ValueError):
            self.seal({
                "LD_PRELOAD": "/tmp/untrusted.so"
            })

    def test_compose_content_mutation_rejected(self):
        self.compose.write_text(
            APPROVED_COMPOSE + "\n# unauthorized change\n",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            self.seal()

    def test_missing_compose_rejected(self):
        self.compose.unlink()

        with self.assertRaises(ValueError):
            self.seal()

    def test_validation_does_not_connect_to_socket(self):
        # Socket is bound but not listening. A connection attempt
        # would fail; structural inspection must still succeed.
        self.assertFalse(self.seal().production_execution_enabled)


if __name__ == "__main__":
    unittest.main()
