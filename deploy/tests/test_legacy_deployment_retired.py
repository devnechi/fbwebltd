#!/usr/bin/env python3
"""Prevent unsafe legacy deployment methods and unrestricted production CD."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LegacyDeploymentRetirementTests(unittest.TestCase):

    def test_legacy_deployment_script_absent(self):
        self.assertFalse(
            (ROOT / "deploy/fbweb-deploy").exists(),
            "Legacy deployment script must remain retired",
        )

    def test_production_deployment_requires_manual_master_trigger(self):
        workflow = (
            ROOT / ".github/workflows/deploy.yml"
        ).read_text(encoding="utf-8")

        self.assertNotIn("rsync --delete", workflow)

        self.assertIn(
            "\n  deploy:\n",
            workflow,
            "A separate production deployment job is required",
        )

        deployment = workflow.split("\n  deploy:\n", 1)[1]

        self.assertIn(
            "github.event_name == 'workflow_dispatch'",
            deployment,
            "Production deployment must require manual triggering",
        )

        self.assertIn(
            "github.ref == 'refs/heads/master'",
            deployment,
            "Production deployment must be restricted to master",
        )

        self.assertIn(
            "environment: production",
            deployment,
            "Deployment must use the protected production environment",
        )

        self.assertIn(
            "needs:",
            deployment,
            "Deployment must depend on earlier workflow jobs",
        )

        self.assertIn(
            "needs.publish.outputs.app_digest",
            deployment,
            "Deployment must use the published Laravel image digest",
        )

        self.assertIn(
            "needs.publish.outputs.web_digest",
            deployment,
            "Deployment must use the published Caddy image digest",
        )

        self.assertIn(
            "StrictHostKeyChecking=yes",
            deployment,
            "SSH host-key verification must remain enabled",
        )

        self.assertNotIn(
            "docker compose up",
            deployment,
            "GitHub Actions must use the restricted server deployment command",
        )

    def test_dry_run_wrapper_has_no_docker_commands(self):
        wrapper = (
            ROOT / "deploy/releases/fbweb-dry-run"
        ).read_text(encoding="utf-8")

        self.assertNotIn("/usr/bin/docker", wrapper)
        self.assertNotIn("docker compose", wrapper)


if __name__ == "__main__":
    unittest.main()
