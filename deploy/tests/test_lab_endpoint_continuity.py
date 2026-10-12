#!/usr/bin/env python3
"""Gate 4D.22C.3C.3 endpoint continuity tests."""

from pathlib import Path
import socket
import sys
import tempfile
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from lab_endpoint_continuity import (
    EndpointSnapshot,
    assess_endpoint_continuity,
    capture_endpoint_snapshot,
    inspect_endpoint_continuity,
)


class EndpointContinuityTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        self.runtime = self.root / "runtime"
        self.runtime.mkdir(mode=0o700)

        self.endpoint = self.runtime / "docker-lab.sock"

        self.listener = socket.socket(
            socket.AF_UNIX, socket.SOCK_STREAM
        )
        self.listener.bind(str(self.endpoint))
        self.endpoint.chmod(0o600)
        self.addCleanup(self.listener.close)

    def capture(self):
        return capture_endpoint_snapshot(
            self.endpoint, self.runtime
        )

    def replace_socket(self):
        self.listener.close()
        self.endpoint.unlink()

        replacement = socket.socket(
            socket.AF_UNIX, socket.SOCK_STREAM
        )
        replacement.bind(str(self.endpoint))
        self.endpoint.chmod(0o600)
        self.addCleanup(replacement.close)

    def test_initial_snapshot_captured(self):
        result = self.capture()
        self.assertGreater(result.socket_inode, 0)
        self.assertEqual(result.socket_mode, 0o600)
        self.assertEqual(result.runtime_mode, 0o700)

    def test_unchanged_endpoint_detected(self):
        previous = self.capture()

        result = inspect_endpoint_continuity(
            previous, self.endpoint, self.runtime
        )

        self.assertTrue(result.unchanged)

    def test_unchanged_endpoint_never_authorizes(self):
        previous = self.capture()

        result = inspect_endpoint_continuity(
            previous, self.endpoint, self.runtime
        )

        self.assertFalse(result.daemon_identity_proven)
        self.assertFalse(result.daemon_isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_socket_replacement_detected(self):
        previous = self.capture()
        self.replace_socket()

        result = inspect_endpoint_continuity(
            previous, self.endpoint, self.runtime
        )

        self.assertFalse(result.unchanged)
        self.assertFalse(result.docker_execution_permitted)

    def test_socket_permissions_changed_rejected(self):
        previous = self.capture()
        self.endpoint.chmod(0o666)

        with self.assertRaises(ValueError):
            inspect_endpoint_continuity(
                previous, self.endpoint, self.runtime
            )

    def test_runtime_permissions_changed_rejected(self):
        previous = self.capture()
        self.runtime.chmod(0o755)

        with self.assertRaises(ValueError):
            inspect_endpoint_continuity(
                previous, self.endpoint, self.runtime
            )

    def test_symlink_substitution_rejected(self):
        previous = self.capture()

        other = self.runtime / "other.sock"
        self.endpoint.rename(other)
        self.endpoint.symlink_to(other)

        with self.assertRaises(ValueError):
            inspect_endpoint_continuity(
                previous, self.endpoint, self.runtime
            )

    def test_missing_socket_rejected(self):
        previous = self.capture()
        self.listener.close()
        self.endpoint.unlink()

        with self.assertRaises(OSError):
            inspect_endpoint_continuity(
                previous, self.endpoint, self.runtime
            )

    def test_incorrect_snapshot_type_rejected(self):
        with self.assertRaises(ValueError):
            assess_endpoint_continuity({}, {})

    def test_runtime_directory_replacement_detected(self):
        previous = self.capture()

        original = self.root / "old-runtime"
        self.runtime.rename(original)

        new_runtime = self.root / "runtime"
        new_runtime.mkdir(mode=0o700)

        new_endpoint = new_runtime / "docker-lab.sock"
        replacement = socket.socket(
            socket.AF_UNIX, socket.SOCK_STREAM
        )
        replacement.bind(str(new_endpoint))
        new_endpoint.chmod(0o600)
        self.addCleanup(replacement.close)

        result = inspect_endpoint_continuity(
            previous, new_endpoint, new_runtime
        )

        self.assertFalse(result.unchanged)

    def test_snapshot_comparison_is_fail_closed(self):
        previous = self.capture()

        different = EndpointSnapshot(
            **{
                **previous.__dict__,
                "socket_inode": previous.socket_inode + 1,
            }
        )

        result = assess_endpoint_continuity(
            previous, different
        )

        self.assertFalse(result.unchanged)
        self.assertTrue(result.manual_verification_required)


if __name__ == "__main__":
    unittest.main()
