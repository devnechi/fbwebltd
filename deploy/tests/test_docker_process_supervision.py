#!/usr/bin/env python3
"""Gate 4D.22A: process identity and fail-closed supervision tests."""

from pathlib import Path
import os
import sys
import tempfile
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(RELEASES))

from docker_process_supervision import (
    ProcessIdentity,
    ProcessStatus,
    assess_process,
    capture_linux_identity,
    observe_linux_process,
    parse_proc_stat,
)


def proc_stat(pid=456, ticks=98765, state="S"):
    # Linux /proc/PID/stat fields 3 through 22.
    fields = (
        [state]
        + ["1"] * 18
        + [str(ticks)]
        + ["0"] * 30
    )
    return f"{pid} (docker compose with spaces) " + " ".join(fields)


class DockerProcessSupervisionTests(unittest.TestCase):
    def setUp(self):
        self.identity = ProcessIdentity(456, 98765)

    def assert_fail_closed(self, assessment):
        self.assertFalse(assessment.docker_operation_settled)
        self.assertFalse(assessment.automatic_retry_permitted)
        self.assertTrue(assessment.manual_reconciliation_required)

    def test_valid_process_record(self):
        identity, state = parse_proc_stat(proc_stat())
        self.assertEqual(identity, self.identity)
        self.assertEqual(state, "S")

    def test_active_process_detected(self):
        result = assess_process(self.identity, proc_stat())
        self.assertEqual(result.status, ProcessStatus.ACTIVE)
        self.assertTrue(result.original_process_active)
        self.assert_fail_closed(result)

    def test_running_process_detected(self):
        result = assess_process(self.identity, proc_stat(state="R"))
        self.assertEqual(result.status, ProcessStatus.ACTIVE)
        self.assert_fail_closed(result)

    def test_zombie_process_detected(self):
        result = assess_process(self.identity, proc_stat(state="Z"))
        self.assertEqual(result.status, ProcessStatus.EXITED)
        self.assert_fail_closed(result)

    def test_dead_process_detected(self):
        result = assess_process(self.identity, proc_stat(state="X"))
        self.assertEqual(result.status, ProcessStatus.EXITED)
        self.assert_fail_closed(result)

    def test_missing_process_detected(self):
        result = assess_process(self.identity, None)
        self.assertEqual(result.status, ProcessStatus.MISSING)
        self.assert_fail_closed(result)

    def test_pid_reuse_detected(self):
        result = assess_process(self.identity, proc_stat(ticks=98766))
        self.assertEqual(result.status, ProcessStatus.PID_REUSED)
        self.assert_fail_closed(result)

    def test_unreadable_process_fails_closed(self):
        result = assess_process(self.identity, unreadable=True)
        self.assertEqual(result.status, ProcessStatus.UNKNOWN)
        self.assert_fail_closed(result)

    def test_malformed_process_record_fails_closed(self):
        result = assess_process(self.identity, "invalid")
        self.assertEqual(result.status, ProcessStatus.UNKNOWN)
        self.assert_fail_closed(result)

    def test_mismatched_pid_fails_closed(self):
        result = assess_process(self.identity, proc_stat(pid=457))
        self.assertEqual(result.status, ProcessStatus.UNKNOWN)
        self.assert_fail_closed(result)

    def test_invalid_pid_rejected(self):
        with self.assertRaises(ValueError):
            ProcessIdentity(0, 100).validate()

    def test_boolean_pid_rejected(self):
        with self.assertRaises(ValueError):
            ProcessIdentity(True, 100).validate()

    def test_invalid_start_ticks_rejected(self):
        with self.assertRaises(ValueError):
            ProcessIdentity(456, 0).validate()

    def test_invalid_process_state_rejected(self):
        with self.assertRaises(ValueError):
            parse_proc_stat(proc_stat(state="?"))

    def test_incomplete_stat_rejected(self):
        with self.assertRaises(ValueError):
            parse_proc_stat("456 (docker) S 1 2 3")

    def test_missing_proc_file_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = observe_linux_process(
                self.identity, proc_root=Path(directory)
            )
        self.assertEqual(result.status, ProcessStatus.MISSING)
        self.assert_fail_closed(result)

    @unittest.skipUnless(
        sys.platform.startswith("linux") and Path("/proc/self/stat").exists(),
        "Linux procfs required",
    )
    def test_current_python_process_identity(self):
        identity = capture_linux_identity(os.getpid())
        result = observe_linux_process(identity)
        self.assertEqual(result.status, ProcessStatus.ACTIVE)
        self.assert_fail_closed(result)

    def test_no_process_status_authorizes_retry(self):
        samples = [
            proc_stat(),
            proc_stat(state="Z"),
            proc_stat(ticks=11111),
            None,
            "malformed",
        ]

        for sample in samples:
            with self.subTest(sample=sample):
                result = assess_process(self.identity, sample)
                self.assert_fail_closed(result)


if __name__ == "__main__":
    unittest.main()
