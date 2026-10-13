#!/usr/bin/env python3
"""Tests for Gate 4D.22C.3D.1 read-only runtime preflight."""

import os
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

import lab_runtime_preflight as preflight


class RuntimePreflightTests(unittest.TestCase):

    def test_missing_path(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.sock"
            self.assertEqual(
                preflight.inspect_path(missing),
                {"exists": False},
            )

    def test_regular_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "example.txt"
            target.write_text("test", encoding="utf-8")

            result = preflight.inspect_path(target)

            self.assertTrue(result["exists"])
            self.assertEqual(result["kind"], "regular_file")

    def test_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = preflight.inspect_path(directory)

            self.assertTrue(result["exists"])
            self.assertEqual(result["kind"], "directory")

    def test_symlink_is_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.write_text("test", encoding="utf-8")

            link = root / "link"
            link.symlink_to(target)

            result = preflight.inspect_path(link)

            self.assertEqual(result["kind"], "symlink")

    @unittest.skipUnless(
        hasattr(socket, "AF_UNIX"),
        "Unix sockets are unavailable",
    )
    def test_unix_socket_metadata_only(self):
        with tempfile.TemporaryDirectory() as directory:
            endpoint = Path(directory) / "test.sock"

            listener = socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM,
            )

            try:
                listener.bind(str(endpoint))

                result = preflight.inspect_path(endpoint)

                self.assertTrue(result["exists"])
                self.assertEqual(result["kind"], "socket")
            finally:
                listener.close()

    def test_subordinate_ids_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "subuid"

            result = preflight.inspect_subordinate_ids(
                str(missing)
            )

            self.assertEqual(result, {"readable": False})

    def test_subordinate_ids_current_user(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "subuid"
            target.write_text(
                "otheruser:100000:65536\n"
                "testuser:200000:65536\n",
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"USER": "testuser"}):
                result = preflight.inspect_subordinate_ids(
                    str(target)
                )

            self.assertEqual(
                result,
                {
                    "readable": True,
                    "current_user_mapping_present": True,
                },
            )

    def test_collection_is_fail_closed(self):
        result = preflight.collect()

        self.assertEqual(result["gate"], "4D.22C.3D.1")
        self.assertEqual(result["mode"], "read-only")

        self.assertIs(
            result["docker_daemon_isolation_proven"],
            False,
        )
        self.assertIs(
            result["docker_execution_permitted"],
            False,
        )
        self.assertIs(
            result["production_execution_enabled"],
            False,
        )
        self.assertIs(
            result["automatic_retry_permitted"],
            False,
        )
        self.assertIs(
            result["manual_verification_required"],
            True,
        )

    def test_environment_values_are_not_exposed(self):
        secret = "test-secret-do-not-expose"

        with patch.dict(
            os.environ,
            {"DOCKER_HOST": secret},
        ):
            result = preflight.collect()

        self.assertTrue(
            result["environment_presence"]["DOCKER_HOST"]
        )
        self.assertNotIn(secret, str(result))

    def test_collection_does_not_invoke_docker(self):
        with patch(
            "subprocess.run",
            side_effect=AssertionError(
                "Subprocess execution prohibited"
            ),
        ), patch(
            "subprocess.Popen",
            side_effect=AssertionError(
                "Process creation prohibited"
            ),
        ), patch(
            "socket.socket",
            side_effect=AssertionError(
                "Socket creation prohibited"
            ),
        ):
            result = preflight.collect()

        self.assertFalse(
            result["docker_execution_permitted"]
        )


if __name__ == "__main__":
    unittest.main()
