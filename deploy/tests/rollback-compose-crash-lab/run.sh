#!/bin/sh
set -eu

cd "$(dirname "$0")/../../.."

SOURCE=deploy/tests/rollback-completion-lab/run.sh
PROJECT=fbweb-gate16ae-lab
VOLUME="${PROJECT}_db_data"

if [ ! -f "$SOURCE" ] || [ -L "$SOURCE" ]; then
    echo "FAIL: Reviewed completion laboratory missing"
    exit 1
fi

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory project already contains containers"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Laboratory database volume already exists"
    exit 1
fi

TEMP=$(mktemp "deploy/tests/rollback-completion-lab/.compose-crash-XXXXXXXX.sh")

cleanup_generated() {
    rm -f "$TEMP"
}

trap cleanup_generated EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

export CRASH_SOURCE="$SOURCE"
export CRASH_TARGET="$TEMP"

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
from pathlib import Path

source = Path(os.environ["CRASH_SOURCE"])
target = Path(os.environ["CRASH_TARGET"])

content = source.read_text(encoding="utf-8")
anchor = 'echo "===== EXECUTE REAL ROLLBACK ====="'

if content.count(anchor) != 1:
    raise SystemExit("FAIL: Reviewed laboratory structure changed")

prefix = content.split(anchor, 1)[0]

original_cleanup = """cleanup() {
    compose down -v >/dev/null 2>&1 || true
    rm -rf "$WORK"
}"""

guarded_cleanup = """cleanup() {
    if [ -f "$WORK/compose-active" ]; then
        echo "WARNING: Compose may still be active."
        echo "Laboratory preserved for manual investigation."
        echo "Journal directory: $WORK"
        return
    fi

    compose down -v >/dev/null 2>&1 || true
    rm -rf "$WORK"
}"""

if prefix.count(original_cleanup) != 1:
    raise SystemExit("FAIL: Source cleanup contract changed")

prefix = prefix.replace(original_cleanup, guarded_cleanup, 1)

suffix = r'''
echo "===== WAIT FOR CANDIDATE HEALTH ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PYHEALTH'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from lab_rollback_command import LAB_PROJECT
from rollback_planner import ImagePair

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

for _ in range(45):
    identity = collect_snapshot(LAB_PROJECT, candidate)

    if identity.app_healthy and identity.web_healthy:
        print("PASS: Candidate containers healthy")
        break

    time.sleep(1)
else:
    raise AssertionError("Candidate health deadline exceeded")
PYHEALTH

echo "===== KILL CONTROLLER WHILE COMPOSE IS ACTIVE ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PYCRASH'
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_allowed_snapshot
from lab_rollback_command import LAB_PROJECT, PREVIOUS
from lab_rollback_completion import complete_lab_rollback
from lab_rollback_executor import execute_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]
work = Path(os.environ["LAB_JOURNALS"]).parent
process_file = work / "compose-process.json"
active_file = work / "compose-active"

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

checkpoint = sim.read_checkpoint(
    release_id, sim.journal.read(release_id)
)


def linux_process_state(pid):
    """Get process state and kernel start ticks, or None if absent."""
    try:
        value = Path(f"/proc/{pid}/stat").read_text()
    except FileNotFoundError:
        return None

    fields = value.rsplit(")", 1)[1].split()
    return fields[0], fields[19]


def same_running_process(pid, start_ticks):
    info = linux_process_state(pid)
    return (
        info is not None
        and info[1] == start_ticks
        and info[0] not in ("Z", "X")
    )


worker = r"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "deploy/releases")

from lab_rollback_executor import execute_lab_rollback
from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

root = Path(os.environ["LAB_JOURNALS"]).parent


def restore(command):
    command.validate()

    environment = {
        "PATH": "/usr/bin:/bin",
        "HOME": os.path.expanduser("~"),
    }

    environment.update(dict(command.environment))

    child = subprocess.Popen(
        list(command.argv),
        cwd=os.getcwd(),
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Linux start ticks distinguish this process from a reused PID.
    stat = Path(f"/proc/{child.pid}/stat").read_text()
    ticks = stat.rsplit(")", 1)[1].split()[19]

    data = {"pid": child.pid, "start_ticks": ticks}

    process_path = root / "compose-process.json"
    process_path.write_text(
        json.dumps(data), encoding="utf-8"
    )

    # The parent uses this marker to prohibit unsafe teardown.
    (root / "compose-active").touch()

    return subprocess.CompletedProcess(
        command.argv, child.wait()
    )


execute_lab_rollback(
    sim,
    os.environ["RELEASE_ID"],
    command_runner=restore,
)
"""

controller = subprocess.Popen(
    [sys.executable, "-c", worker],
    env=os.environ.copy(),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.PIPE,
    text=True,
)

try:
    deadline = time.monotonic() + 45
    details = None

    while time.monotonic() < deadline:
        if process_file.exists() and active_file.exists():
            details = json.loads(
                process_file.read_text(encoding="utf-8")
            )
            break

        if controller.poll() is not None:
            error = controller.stderr.read()
            raise AssertionError(
                "Controller ended before Compose process was observed: "
                + error[-1500:]
            )

        time.sleep(0.1)

    if details is None:
        raise AssertionError("Compose launch was not observed")

    pid = details["pid"]
    start_ticks = details["start_ticks"]

    if not same_running_process(pid, start_ticks):
        raise AssertionError(
            "Compose finished before SIGKILL; experiment inconclusive"
        )

    # Confirm STARTED exists before terminating its owner.
    attempt_path = (
        sim.journal.root
        / "rollback-attempts"
        / release_id
        / "000001.json"
    )

    from rollback_attempt_store import validate_attempt_record

    record = validate_attempt_record(
        json.loads(attempt_path.read_text(encoding="utf-8"))
    )
    assert record["release_id"] == release_id
    assert record["schema_version"] == 2
    assert record["status"] == "STARTED"

    os.kill(controller.pid, signal.SIGKILL)
    controller.wait(timeout=15)

    assert controller.returncode == -signal.SIGKILL
    print("PASS: Controller received actual SIGKILL")

    # Do NOT assume Docker Compose stopped with its parent.
    observed_alive = same_running_process(pid, start_ticks)

    print(
        "OBSERVATION: Compose running after controller death:",
        observed_alive,
    )

    # The Compose subprocess may continue after losing its parent.
    # Wait for it to terminate; never start a replacement.
    deadline = time.monotonic() + 180

    while same_running_process(pid, start_ticks):
        if time.monotonic() >= deadline:
            raise RuntimeError(
                "Compose still active after observation deadline; "
                "laboratory must be preserved"
            )

        time.sleep(0.5)

    print("PASS: Original Compose process is no longer running")
    active_file.unlink()

    # A fresh inspection decides the outcome.
    deadline = time.monotonic() + 45
    identity = None

    while time.monotonic() < deadline:
        try:
            identity = collect_allowed_snapshot(
                LAB_PROJECT,
                PREVIOUS,
                candidate,
            )
            break
        except ValueError:
            time.sleep(0.5)

    if identity is None:
        raise AssertionError(
            "Docker state cannot be inspected; manual recovery required"
        )

    if identity.db_container_id != checkpoint["db_identity"]:
        raise AssertionError("Database identity changed")

    journal = sim.journal.read(release_id)
    attempts = RollbackAttemptStore(sim).read(release_id)

    assert journal["state"] == "ROLLING_BACK"
    assert len(attempts) == 1
    assert attempts[0]["status"] == "STARTED"

    print("PASS: Unresolved STARTED survived controller SIGKILL")
    print("PASS: Journal remains ROLLING_BACK")

    if (
        identity.app_reference == PREVIOUS.app
        and identity.web_reference == PREVIOUS.web
    ):
        # Docker may finish restoring containers after Compose exits.
        # Read-only health inspections are permitted.
        deadline = time.monotonic() + 60

        while not (identity.app_healthy and identity.web_healthy):
            if time.monotonic() >= deadline:
                break

            time.sleep(1)
            identity = collect_allowed_snapshot(
                LAB_PROJECT,
                PREVIOUS,
                candidate,
            )

            assert identity.db_container_id == checkpoint["db_identity"]

        if identity.app_healthy and identity.web_healthy:
            outcome = complete_lab_rollback(sim, release_id)

            assert outcome["journal_state"] == "ROLLED_BACK"
            assert outcome["attempt_status"] == "SUCCEEDED"

            print(
                "PASS: Previous images verified and journal finalized "
                "without re-execution"
            )
        else:
            print(
                "PASS: Previous images not healthy; "
                "manual intervention required"
            )
    else:
        print(
            "PASS: Candidate or mixed image state observed; "
            "manual intervention required"
        )

    # A restarted executor is forbidden from launching restoration.
    commands = []

    def forbidden_command(command):
        commands.append(command)
        raise AssertionError("Unexpected duplicate Docker execution")

    try:
        execute_lab_rollback(
            sim,
            release_id,
            command_runner=forbidden_command,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate restoration was accepted")

    assert commands == []
    assert len(RollbackAttemptStore(sim).read(release_id)) == 1

    print("PASS: Duplicate restoration prevented")

finally:
    if controller.poll() is None:
        controller.kill()
        controller.wait()

    # Do not clear the active marker if Compose might still run.
    if process_file.exists():
        details = json.loads(
            process_file.read_text(encoding="utf-8")
        )

        if not same_running_process(
            details["pid"], details["start_ticks"]
        ):
            active_file.unlink(missing_ok=True)
PYCRASH

if [ -f "$WORK/compose-active" ]; then
    echo "FAIL: Compose process still active; cleanup prohibited"
    exit 1
fi

DB_ID=$(docker ps -q --no-trunc \
    --filter "label=com.docker.compose.project=$PROJECT" \
    --filter "label=com.docker.compose.service=db")

[ -n "$DB_ID" ] || {
    echo "FAIL: Database container missing"
    exit 1
}

MARKER=$(docker exec "$DB_ID" cat /data/marker)

[ "$MARKER" = "preserved" ] || {
    echo "FAIL: Database volume marker changed"
    exit 1
}

echo "PASS: Database volume marker preserved"
echo "===== GATE 4D.16AE.12B PASSED ====="
'''

target.write_text(prefix + suffix, encoding="utf-8")
target.chmod(0o600)

print("PASS: During-Compose crash laboratory generated")
PY

sh -n "$TEMP"

echo "===== RUNNING DURING-COMPOSE SIGKILL EXPERIMENT ====="

sh "$TEMP"

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers remain"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Laboratory volume remains"
    exit 1
fi

echo "PASS: Laboratory cleanup verified"
echo "===== SIGKILL DURING COMPOSE TEST SUCCESSFUL ====="
