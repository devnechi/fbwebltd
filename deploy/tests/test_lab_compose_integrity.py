#!/usr/bin/env python3
"""Tests for exact laboratory Compose configuration integrity."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_compose_integrity import (
    APPROVED_COMPOSE,
    LAB_COMPOSE,
    validate_lab_compose_integrity,
)


class LabComposeIntegrityTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.path = self.root / LAB_COMPOSE
        self.path.parent.mkdir(parents=True)
        self.path.write_text(
            APPROVED_COMPOSE,
            encoding="utf-8",
        )

    def test_approved_compose_passes(self):
        self.assertEqual(
            validate_lab_compose_integrity(self.root),
            self.path,
        )

    def test_extra_privileged_setting_rejected(self):
        text = APPROVED_COMPOSE.replace(
            "read_only: true",
            "read_only: true\n    privileged: true",
            1,
        )
        self.path.write_text(text, encoding="utf-8")

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(self.root)

    def test_extra_volume_rejected(self):
        self.path.write_text(
            APPROVED_COMPOSE + "\nvolumes_extra:\n",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(self.root)

    def test_image_reference_change_rejected(self):
        self.path.write_text(
            APPROVED_COMPOSE.replace(
                "${LAB_APP_IMAGE:?Required}",
                "some-image:latest",
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(self.root)

    def test_healthcheck_change_rejected(self):
        self.path.write_text(
            APPROVED_COMPOSE.replace(
                'test: ["CMD-SHELL", "true"]',
                'test: ["CMD-SHELL", "false"]',
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(self.root)

    def test_missing_file_rejected(self):
        self.path.unlink()

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(self.root)

    def test_symlink_file_rejected(self):
        target = self.root / "alternative.yml"
        target.write_text(APPROVED_COMPOSE, encoding="utf-8")
        self.path.unlink()
        self.path.symlink_to(target)

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(self.root)

    def test_symlink_parent_rejected(self):
        new_root = self.root / "alternate"
        new_root.mkdir()

        link = self.root / "linked"
        link.symlink_to(new_root, target_is_directory=True)

        with self.assertRaises(ValueError):
            validate_lab_compose_integrity(link)

    def test_validation_does_not_modify_file(self):
        before = self.path.read_bytes()
        validate_lab_compose_integrity(self.root)
        self.assertEqual(self.path.read_bytes(), before)

    def test_actual_repository_compose_matches_baseline(self):
        repository_root = Path(__file__).resolve().parents[2]

        validated = validate_lab_compose_integrity(
            repository_root
        )

        self.assertTrue(validated.is_file())


if __name__ == "__main__":
    unittest.main()
