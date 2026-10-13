#!/usr/bin/env python3
"""Read-only daemon identity evidence regression tests."""

import os
from pathlib import Path
import socket
import sys
import tempfile
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from lab_daemon_identity import (
    assess_lab_daemon_identity,
    find_socket_holders,
    parse_unix_table,
)


HEADER = "Num RefCount Protocol Flags Type St Inode Path\n"


class DaemonIdentityTests(unittest.TestCase):

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

        self.proc = self.root / "proc"
        (self.proc / "net").mkdir(parents=True)

        self.inode = 1234567
        self.table = (
            HEADER
            + "00000001: 00000002 00000000 00010000 "
            + "0001 01 "
            + str(self.inode)
            + " "
            + str(self.endpoint)
            + "\n"
        )

    def add_holder(self, pid=9876, fd=7):
        folder = self.proc / str(pid) / "fd"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / str(fd)).symlink_to(
            "socket:[" + str(self.inode) + "]"
        )

    def assess(self, table=None):
        return assess_lab_daemon_identity(
            self.endpoint,
            proc_root=self.proc,
            unix_table_content=(
                self.table if table is None else table
            ),
        )

    def test_single_record_and_holder_are_observable(self):
        self.add_holder()
        result = self.assess()

        self.assertTrue(result.evidence_consistent)
        self.assertEqual(result.socket_inode, self.inode)
        self.assertEqual(result.holders[0].pid, 9876)

    def test_evidence_never_authorizes_docker(self):
        self.add_holder()
        result = self.assess()

        self.assertFalse(result.daemon_identity_proven)
        self.assertFalse(result.daemon_isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_missing_kernel_record_fails_closed(self):
        result = self.assess(table=HEADER)

        self.assertFalse(result.evidence_consistent)
        self.assertEqual(result.socket_record_count, 0)

    def test_duplicate_kernel_record_fails_closed(self):
        self.add_holder()
        result = self.assess(
            table=self.table + self.table.splitlines()[1] + "\n"
        )

        self.assertFalse(result.evidence_consistent)
        self.assertEqual(result.socket_record_count, 2)

    def test_no_visible_holder_fails_closed(self):
        result = self.assess()
        self.assertFalse(result.evidence_consistent)

    def test_multiple_holders_remain_visible(self):
        self.add_holder(pid=9876, fd=7)
        self.add_holder(pid=9877, fd=8)

        result = self.assess()
        self.assertEqual(len(result.holders), 2)
        self.assertFalse(result.docker_execution_permitted)

    def test_mismatched_inode_not_accepted(self):
        folder = self.proc / "9876" / "fd"
        folder.mkdir(parents=True)
        (folder / "7").symlink_to("socket:[999999]")

        result = self.assess()
        self.assertFalse(result.evidence_consistent)

    def test_invalid_socket_permissions_rejected(self):
        self.endpoint.chmod(0o666)

        with self.assertRaises(ValueError):
            self.assess()

    def test_non_socket_endpoint_rejected(self):
        self.listener.close()
        self.endpoint.unlink()
        self.endpoint.write_text("not a socket")

        with self.assertRaises(ValueError):
            self.assess()

    def test_invalid_kernel_table_rejected(self):
        with self.assertRaises(ValueError):
            parse_unix_table("not a valid header", str(self.endpoint))

    def test_fd_scan_reports_unreadable_processes(self):
        self.add_holder()
        # A proc entry without an fd directory cannot establish
        # complete descriptor visibility.
        (self.proc / "9999").mkdir()

        holders, incomplete = find_socket_holders(
            self.proc, self.inode
        )

        self.assertTrue(incomplete)
        self.assertEqual(len(holders), 1)


if __name__ == "__main__":
    unittest.main()
