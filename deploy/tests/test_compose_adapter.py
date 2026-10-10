#!/usr/bin/env python3
"""Tests for the restricted, non-executing Compose planner."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from compose_adapter import (
    activation_command,
    compose_environment,
    execution_enabled,
    inspect_compose_file,
)

from rollback_planner import ImagePair


ROOT = Path(__file__).resolve().parents[2]


class ComposeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.images = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

    def test_fixed_service_targets(self):
        command = activation_command(self.images)
        self.assertEqual(command.argv[-2:], ("app", "web"))

    def test_database_not_targeted(self):
        command = activation_command(self.images)
        self.assertNotIn("db", command.argv)

    def test_no_dependency_recreation(self):
        command = activation_command(self.images)
        self.assertIn("--no-deps", command.argv)

    def test_no_build(self):
        command = activation_command(self.images)
        self.assertIn("--no-build", command.argv)
        self.assertNotIn("--build", command.argv)

    def test_no_orphan_removal(self):
        command = activation_command(self.images)
        self.assertNotIn("--remove-orphans", command.argv)

    def test_no_mutable_image_tag(self):
        images = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app:latest",
            self.images.web,
        )
        with self.assertRaises(ValueError):
            activation_command(images)

    def test_tampered_command_rejected(self):
        command = activation_command(self.images)
        altered = replace(
            command,
            argv=command.argv[:-1] + ("db",),
        )
        with self.assertRaises(ValueError):
            altered.validate()

    def test_image_environment(self):
        command = activation_command(self.images)
        environment = compose_environment(command)

        self.assertEqual(
            environment["FBWEB_APP_IMAGE"],
            self.images.app,
        )
        self.assertEqual(
            environment["FBWEB_WEB_IMAGE"],
            self.images.web,
        )

    def test_expected_compose_file(self):
        self.assertTrue(
            inspect_compose_file(ROOT / "compose.release.yml")
        )

    def test_wrong_compose_file_rejected(self):
        with self.assertRaises(ValueError):
            inspect_compose_file(ROOT / "compose.prod.yml")

    def test_execution_disabled(self):
        self.assertFalse(execution_enabled())


if __name__ == "__main__":
    unittest.main()
