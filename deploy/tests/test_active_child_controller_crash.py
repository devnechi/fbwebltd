#!/usr/bin/env python3
"""Gate 4D.22B.5: active inert child survives controller SIGKILL.

No Docker execution, production access, or automatic retry.
"""

import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


TESTS = Path(__file__).resolve().parent
RELEASES = TESTS.parent / "releases"
REPO = TESTS.parents[1]

sys.path.insert(0, str(RELEASES))
sys.path.insert(0, str(TESTS))

from deployment_lock import deployment_lock
from docker_execution_evidence import (
    DockerExecutionEvidenceStore,
    OBSERVED,
)
from docker_process_supervision import (
    ProcessIdentity,
    ProcessStatus,
    observe_linux_process,
)


CHILD_SCRIPT = r"""
import os
from pathlib import Path
import sys
import time

fd = int(sys.argv[1])
root = Path(sys.argv[2])

try:
    permission = os.read(fd, 1)
finally:
    os.close(fd)

if permission != b"R":
    sys.exit(76)

(root / "child-started").write_text("STARTED\n")

# Continue independently while the parent controller is killed.
time.sleep(3)

(root / "child-finished").write_text("FINISHED\n")
sys.exit(0)
"""


CONTROLLER_SCRIPT = r"""
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(os.environ["TEST_ROOT"])

sys.path.insert(0, os.environ["TEST_RELEASES"])
sys.path.insert(0, os.environ["TEST_TESTS"])

from deployment_lock import deployment_lock
from docker_process_supervision import capture_linux_identity
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from locked_durable_barrier import LockedEvidenceStore
from test_docker_execution_evidence import attempt

child_script = os.environ["TEST_CHILD_SCRIPT"]

with deployment_lock(root / "locks") as lease:
    store = LockedEvidenceStore(
        root / "evidence", root / "locks", lease
    )

    prepared = store.prepare(
        attempt(), plan_lab_rollback(PREVIOUS)
    )

    if prepared["phase"] != "PREPARED":
        raise RuntimeError("Missing durable PREPARED evidence")

    read_fd, write_fd = os.pipe()

    try:
        child = subprocess.Popen(
            [
                sys.executable,
                "-c",
                child_script,
                str(read_fd),
                str(root),
            ],
            pass_fds=(read_fd,),
            close_fds=True,
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except BaseException:
        os.close(read_fd)
        os.close(write_fd)
        raise

    os.close(read_fd)

    try:
        identity = capture_linux_identity(child.pid)

        observed = store.observe(
            attempt()["release_id"], identity
        )

        if (
            observed["phase"] != "OBSERVED"
            or observed["pid"] != identity.pid
            or observed["start_ticks"] != identity.start_ticks
        ):
            raise RuntimeError("Durable process binding failed")

        # Revalidate the exact process before release.
        from docker_process_supervision import (
            observe_linux_process,
            ProcessStatus,
        )

        if (
            observe_linux_process(identity).status
            != ProcessStatus.ACTIVE
        ):
            raise RuntimeError("Original child is not active")

        if os.write(write_fd, b"R") != 1:
            raise RuntimeError("Child release failed")

    finally:
        os.close(write_fd)

    deadline = time.monotonic() + 10

    while not (root / "child-started").exists():
        if child.poll() is not None:
            raise RuntimeError(
                "Child exited before active-work confirmation"
            )

        if time.monotonic() >= deadline:
            raise RuntimeError("Child-start confirmation timed out")

        time.sleep(0.01)

    if child.poll() is not None:
        raise RuntimeError("Child finished too early")

    with open(root / "controller-ready", "w") as handle:
        handle.write(
            f"{identity.pid} {identity.start_ticks}\n"
        )
        handle.flush()
        os.fsync(handle.fileno())

    # Hold the lock until externally killed.
    time.sleep(120)
"""


REPLACEMENT_SCRIPT = r"""
import os
from pathlib import Path
import sys

sys.path.insert(0, os.environ["TEST_RELEASES"])
sys.path.insert(0, os.environ["TEST_TESTS"])

from deployment_lock import deployment_lock
from locked_durable_barrier import LockedEvidenceStore
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from test_docker_execution_evidence import attempt

root = Path(os.environ["TEST_ROOT"])

with deployment_lock(root / "locks") as lease:
    store = LockedEvidenceStore(
        root / "evidence", root / "locks", lease
    )

    record = store.read("gate22b-lab")

    if record["phase"] != "OBSERVED":
        raise RuntimeError("Durable observation missing")

    if store.assess("gate22b-lab").automatic_retry_permitted:
        raise RuntimeError("Automatic retry unexpectedly allowed")

    try:
        store.prepare(
            attempt(), plan_lab_rollback(PREVIOUS)
        )
    except FileExistsError:
        print("PASS: Replacement controller rejected duplicate")
    else:
        raise RuntimeError("Duplicate execution preparation accepted")
"""


@unittest.skipUnless(
    sys.platform.startswith("linux"),
    "Linux required",
)
class ActiveChildCrashTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)
        (self.root / "locks").mkdir(mode=0o700)
        (self.root / "evidence").mkdir(mode=0o700)

        self.env = dict(os.environ)
        self.env.update({
            "TEST_ROOT": str(self.root),
            "TEST_RELEASES": str(RELEASES),
            "TEST_TESTS": str(TESTS),
            "TEST_CHILD_SCRIPT": CHILD_SCRIPT,
            "PYTHONDONTWRITEBYTECODE": "1",
        })

    def test_active_child_survives_and_duplicate_is_blocked(self):
        controller = subprocess.Popen(
            [sys.executable, "-c", CONTROLLER_SCRIPT],
            cwd=str(REPO),
            env=self.env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )

        child_identity = None
        ready = self.root / "controller-ready"
        finished = self.root / "child-finished"

        try:
            deadline = time.monotonic() + 15

            while not ready.exists():
                if controller.poll() is not None:
                    error = controller.stderr.read()
                    self.fail(
                        "Controller exited before child release: "
                        + error[-3000:]
                    )

                if time.monotonic() >= deadline:
                    self.fail("Controller readiness timed out")

                time.sleep(0.01)

            pid, ticks = ready.read_text().strip().split()

            child_identity = ProcessIdentity(
                int(pid), int(ticks)
            )

            self.assertEqual(
                observe_linux_process(child_identity).status,
                ProcessStatus.ACTIVE,
            )

            self.assertTrue(
                (self.root / "child-started").exists()
            )

            self.assertFalse(finished.exists())

            os.kill(controller.pid, signal.SIGKILL)
            controller.wait(timeout=10)

            self.assertEqual(
                controller.returncode,
                -signal.SIGKILL,
            )

            # Original child remains alive immediately after
            # controller SIGKILL, while its work is unfinished.
            self.assertFalse(finished.exists())

            self.assertEqual(
                observe_linux_process(child_identity).status,
                ProcessStatus.ACTIVE,
            )

            replacement = subprocess.run(
                [sys.executable, "-c", REPLACEMENT_SCRIPT],
                cwd=str(REPO),
                env=self.env,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            self.assertEqual(
                replacement.returncode,
                0,
                msg=replacement.stdout + replacement.stderr,
            )

            self.assertIn(
                "rejected duplicate",
                replacement.stdout,
            )

            deadline = time.monotonic() + 10

            while not finished.exists():
                if time.monotonic() >= deadline:
                    self.fail(
                        "Original child did not complete after SIGKILL"
                    )

                time.sleep(0.05)

            self.assertEqual(
                finished.read_text(),
                "FINISHED\n",
            )

            store = DockerExecutionEvidenceStore(
                self.root / "evidence"
            )

            record = store.read("gate22b-lab")

            self.assertEqual(record["phase"], OBSERVED)
            self.assertEqual(record["pid"], child_identity.pid)
            self.assertEqual(
                record["start_ticks"], child_identity.start_ticks
            )

            assessment = store.assess("gate22b-lab")

            self.assertFalse(
                assessment.docker_operation_settled
            )
            self.assertFalse(
                assessment.automatic_retry_permitted
            )
            self.assertTrue(
                assessment.manual_reconciliation_required
            )

        finally:
            if controller.poll() is None:
                controller.kill()
                controller.wait(timeout=10)

            if controller.stderr is not None:
                controller.stderr.close()

            # Do not leave the inert child active after a failed test.
            # Kill only the specific verified test process.
            if child_identity is not None:
                assessment = observe_linux_process(child_identity)

                if assessment.status == ProcessStatus.ACTIVE:
                    try:
                        os.kill(child_identity.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass


if __name__ == "__main__":
    unittest.main()
