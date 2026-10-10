#!/usr/bin/env python3
"""Security tests for the read-only Docker snapshot collector."""

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from docker_snapshot_reader import collect_snapshot
from rollback_planner import ImagePair


class DockerSnapshotReaderTests(unittest.TestCase):

    def setUp(self):
        self.project = "fbweb-gate16q-lab"
        self.expected = ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
            "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
        )

        self.calls = []

        self.containers = [
            self.container("app", "a", "1", self.expected.app),
            self.container("web", "b", "2", self.expected.web),
            self.container("db", "c", "3", "mysql:8.0"),
        ]

        self.images = [
            {
                "Id": "sha256:" + "1" * 64,
                "RepoDigests": [self.expected.app],
            },
            {
                "Id": "sha256:" + "2" * 64,
                "RepoDigests": [self.expected.web],
            },
            {
                "Id": "sha256:" + "3" * 64,
                "RepoDigests": ["mysql@sha256:" + "d" * 64],
            },
        ]

    def container(self, service, container_char, image_char, ref):
        return {
            "Id": container_char * 64,
            "Image": "sha256:" + image_char * 64,
            "Config": {
                "Image": ref,
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

    def runner(self, argv, **kwargs):
        self.calls.append(argv)

        if argv[1] == "ps":
            output = "\n".join(
                item["Id"][:12] for item in self.containers
            ) + "\n"
        elif argv[1:3] == ["inspect", "--type"]:
            output = json.dumps(self.containers)
        elif argv[1:3] == ["image", "inspect"]:
            output = json.dumps(self.images)
        else:
            raise AssertionError("Unexpected Docker command")

        return SimpleNamespace(stdout=output)

    def test_valid_laboratory_snapshot(self):
        result = collect_snapshot(
            self.project, self.expected, runner=self.runner
        )

        self.assertEqual(
            result.db_container_id,
            "c" * 64,
        )
        self.assertTrue(result.app_healthy)

    def test_production_project_prohibited(self):
        with self.assertRaises(ValueError):
            collect_snapshot(
                "fbweb", self.expected, runner=self.runner
            )

        self.assertEqual(self.calls, [])

    def test_invalid_project_prohibited(self):
        with self.assertRaises(ValueError):
            collect_snapshot(
                "../fbweb", self.expected, runner=self.runner
            )

        self.assertEqual(self.calls, [])

    def test_only_read_only_docker_commands(self):
        collect_snapshot(
            self.project, self.expected, runner=self.runner
        )

        self.assertEqual(len(self.calls), 3)

        self.assertEqual(
            [call[1] for call in self.calls],
            ["ps", "inspect", "image"],
        )

        forbidden = {
            "run", "up", "stop", "rm", "pull",
            "push", "exec", "start", "restart",
        }

        for call in self.calls:
            self.assertFalse(
                any(part in forbidden for part in call[1:])
            )

    def test_duplicate_container_rejected(self):
        self.containers[2]["Id"] = self.containers[0]["Id"]

        with self.assertRaises(ValueError):
            collect_snapshot(
                self.project, self.expected, runner=self.runner
            )

    def test_missing_container_rejected(self):
        self.containers.pop()

        with self.assertRaises(ValueError):
            collect_snapshot(
                self.project, self.expected, runner=self.runner
            )

    def test_wrong_registry_digest_rejected(self):
        self.images[0]["RepoDigests"] = [
            "ghcr.io/devnechi/fbwebltd-app@sha256:" + "f" * 64
        ]

        with self.assertRaises(ValueError):
            collect_snapshot(
                self.project, self.expected, runner=self.runner
            )


if __name__ == "__main__":
    unittest.main()
