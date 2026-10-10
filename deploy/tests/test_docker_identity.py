#!/usr/bin/env python3
"""Tests for read-only Docker identity validation."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from docker_identity import validate_inspection
from rollback_planner import ImagePair


class DockerIdentityTests(unittest.TestCase):

    def setUp(self):
        self.project = "fbweb-gate16p-lab"

        self.expected = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        self.app_id = "sha256:" + "1" * 64
        self.web_id = "sha256:" + "2" * 64
        self.db_id = "sha256:" + "3" * 64

        self.containers = [
            self.container(
                "app", "a", self.app_id, self.expected.app
            ),
            self.container(
                "web", "b", self.web_id, self.expected.web
            ),
            self.container(
                "db", "c", self.db_id, "mysql:8.0"
            ),
        ]

        self.images = [
            {
                "Id": self.app_id,
                "RepoDigests": [self.expected.app],
            },
            {
                "Id": self.web_id,
                "RepoDigests": [self.expected.web],
            },
        ]

    def container(self, service, character, image_id, reference):
        return {
            "Id": character * 64,
            "Image": image_id,
            "Config": {
                "Image": reference,
                "Labels": {
                    "com.docker.compose.project": self.project,
                    "com.docker.compose.service": service,
                },
            },
            "State": {
                "Running": True,
                "Health": {"Status": "healthy"},
            },
        }

    def validate(self):
        return validate_inspection(
            self.containers,
            self.images,
            self.project,
            self.expected,
        )

    def test_valid_identity_mapping(self):
        result = self.validate()
        self.assertEqual(result.app_reference, self.expected.app)
        self.assertEqual(result.web_reference, self.expected.web)
        self.assertEqual(result.db_container_id, "c" * 64)

    def test_wrong_compose_project_rejected(self):
        self.containers[0]["Config"]["Labels"][
            "com.docker.compose.project"
        ] = "other-project"

        with self.assertRaises(ValueError):
            self.validate()

    def test_duplicate_service_rejected(self):
        self.containers.append(copy.deepcopy(self.containers[0]))

        with self.assertRaises(ValueError):
            self.validate()

    def test_mutable_container_reference_rejected(self):
        self.containers[0]["Config"]["Image"] = "latest"

        with self.assertRaises(ValueError):
            self.validate()

    def test_wrong_registry_digest_rejected(self):
        self.images[0]["RepoDigests"] = [
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "f" * 64
        ]

        with self.assertRaises(ValueError):
            self.validate()

    def test_wrong_local_image_id_rejected(self):
        self.containers[0]["Image"] = "sha256:" + "9" * 64

        with self.assertRaises(ValueError):
            self.validate()

    def test_stopped_container_rejected(self):
        self.containers[1]["State"]["Running"] = False

        with self.assertRaises(ValueError):
            self.validate()

    def test_unhealthy_container_reported(self):
        self.containers[0]["State"]["Health"]["Status"] = "unhealthy"

        result = self.validate()

        self.assertFalse(result.app_healthy)
        self.assertTrue(result.web_healthy)


if __name__ == "__main__":
    unittest.main()
