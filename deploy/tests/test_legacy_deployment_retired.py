#!/usr/bin/env python3
"""Prevent reintroduction of unsafe legacy deployment mechanisms."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LegacyDeploymentRetirementTests(unittest.TestCase):

    def test_legacy_deployment_script_absent(self):
        self.assertFalse(
            (ROOT / "deploy/fbweb-deploy").exists(),
            "Legacy deployment script must remain retired",
        )

    def test_production_workflow_deployment_disabled(self):
        workflow = (
            ROOT / ".github/workflows/deploy.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("if: ${{ false }}", workflow)
        self.assertNotIn("rsync --delete", workflow)

    def test_dry_run_wrapper_has_no_docker_commands(self):
        wrapper = (
            ROOT / "deploy/releases/fbweb-dry-run"
        ).read_text(encoding="utf-8")

        self.assertNotIn("/usr/bin/docker", wrapper)
        self.assertNotIn("docker compose", wrapper)


if __name__ == "__main__":
    unittest.main()
