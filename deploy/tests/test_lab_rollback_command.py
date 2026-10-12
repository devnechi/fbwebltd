#!/usr/bin/env python3
"""Tests for the non-executing laboratory restoration command."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_rollback_command import (
    LAB_PROJECT,
    PREVIOUS,
    execution_enabled,
    plan_lab_rollback,
    validate_lab_compose_file,
)
from rollback_planner import ImagePair


class LabRollbackCommandTests(unittest.TestCase):

    def test_previous_pair_produces_valid_command(self):
        command = plan_lab_rollback(PREVIOUS)
        self.assertTrue(command.validate())

    def test_project_must_be_exact_lab_name(self):
        with self.assertRaises(ValueError):
            plan_lab_rollback(PREVIOUS, project="fbweb")

    def test_other_lab_project_rejected(self):
        with self.assertRaises(ValueError):
            plan_lab_rollback(
                PREVIOUS,
                project="fbweb-gate16ad-lab",
            )

    def test_candidate_image_pair_rejected(self):
        candidate = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        with self.assertRaises(ValueError):
            plan_lab_rollback(candidate)

    def test_database_service_cannot_be_added(self):
        command = plan_lab_rollback(PREVIOUS)

        changed = replace(
            command,
            argv=command.argv + ("db",),
        )

        with self.assertRaises(ValueError):
            changed.validate()

    def test_volume_removal_rejected(self):
        command = plan_lab_rollback(PREVIOUS)

        changed = replace(
            command,
            argv=command.argv + ("--volumes",),
        )

        with self.assertRaises(ValueError):
            changed.validate()

    def test_image_build_option_rejected(self):
        command = plan_lab_rollback(PREVIOUS)

        changed = replace(
            command,
            argv=command.argv + ("--build",),
        )

        with self.assertRaises(ValueError):
            changed.validate()

    def test_image_environment_cannot_be_changed(self):
        command = plan_lab_rollback(PREVIOUS)

        changed = replace(
            command,
            environment=(
                ("LAB_APP_IMAGE", "latest"),
                ("LAB_WEB_IMAGE", PREVIOUS.web),
            ),
        )

        with self.assertRaises(ValueError):
            changed.validate()

    def test_command_cannot_be_mutated(self):
        command = plan_lab_rollback(PREVIOUS)

        with self.assertRaises(AttributeError):
            command.project = "fbweb"

    def test_existing_lab_compose_file(self):
        root = Path(__file__).resolve().parents[2]
        path = validate_lab_compose_file(root)
        self.assertTrue(path.is_file())

    def test_execution_remains_disabled(self):
        self.assertFalse(execution_enabled())


if __name__ == "__main__":
    unittest.main()
