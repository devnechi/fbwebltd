#!/bin/sh
set -eu

cd "$(dirname "$0")/../../.."

SOURCE="deploy/tests/rollback-completion-lab/run.sh"
PROJECT="fbweb-gate16ae-lab"
VOLUME="${PROJECT}_db_data"

if [ ! -f "$SOURCE" ] || [ -L "$SOURCE" ]; then
    echo "FAIL: Reviewed completion laboratory missing"
    exit 1
fi

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Existing laboratory containers detected"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Existing laboratory volume detected"
    exit 1
fi

TEMP=$(mktemp "deploy/tests/rollback-completion-lab/.execution-crash-XXXXXXXX.sh")

cleanup() {
    rm -f "$TEMP"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

export CRASH_LAB_SOURCE="$SOURCE"
export CRASH_LAB_TEMP="$TEMP"

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
from pathlib import Path

source = Path(os.environ["CRASH_LAB_SOURCE"])
target = Path(os.environ["CRASH_LAB_TEMP"])

content = source.read_text(encoding="utf-8")

anchor = 'echo "===== EXECUTE REAL ROLLBACK ====="'

if content.count(anchor) != 1:
    raise SystemExit(
        "FAIL: Source laboratory structure changed"
    )

# Reuse only the reviewed lab's initialization, checkpoint creation,
# and candidate activation. Do not run its successful rollback path.
prefix = content.split(anchor, 1)[0]

suffix = r'''
echo "===== SIGKILL AFTER DURABLE STARTED ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PYWORKER'
import os
import signal
import subprocess
import sys

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from lab_rollback_command import LAB_PROJECT
from lab_rollback_executor import execute_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

before = collect_snapshot(LAB_PROJECT, candidate)
assert before.app_healthy and before.web_healthy

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]


def kill_before_compose(command):
    command.validate()

    # The executor has already persisted STARTED.
    # No restoration command has been issued.
    os.kill(os.getpid(), signal.SIGKILL)

    raise AssertionError("SIGKILL unexpectedly returned")


worker = r"""
import os
import signal
import sys

sys.path.insert(0, "deploy/releases")

from lab_rollback_executor import execute_lab_rollback
from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

def kill_before_compose(command):
    command.validate()
    os.kill(os.getpid(), signal.SIGKILL)
    raise AssertionError("SIGKILL returned")

execute_lab_rollback(
    sim,
    os.environ["RELEASE_ID"],
    command_runner=kill_before_compose,
)
"""

result = subprocess.run(
    [sys.executable, "-c", worker],
    env=os.environ.copy(),
    check=False,
    timeout=60,
)

if result.returncode != -signal.SIGKILL:
    raise AssertionError(
        f"Expected SIGKILL (-9), got {result.returncode}"
    )

print("PASS: Actual SIGKILL terminated only the controller worker")

from rollback_attempt_store import RollbackAttemptStore

store = RollbackAttemptStore(sim)
attempts = store.read(release_id)
journal = sim.journal.read(release_id)

assert len(attempts) == 1
assert attempts[0]["schema_version"] == 2
assert attempts[0]["status"] == "STARTED"
assert journal["state"] == "ROLLING_BACK"

after = collect_snapshot(LAB_PROJECT, candidate)

assert before.app_container_id == after.app_container_id
assert before.web_container_id == after.web_container_id
assert before.db_container_id == after.db_container_id

print("PASS: STARTED survived SIGKILL")
print("PASS: Journal remains ROLLING_BACK")
print("PASS: Candidate container identities unchanged")

try:
    execute_lab_rollback(
        sim,
        release_id,
        command_runner=lambda command: (
            (_ for _ in ()).throw(
                AssertionError("Duplicate restoration command invoked")
            )
        ),
    )
except ValueError:
    print("PASS: Restarted executor rejected duplicate execution")
else:
    raise AssertionError("Duplicate execution was accepted")

assert len(store.read(release_id)) == 1

print("PASS: Exactly one unresolved attempt remains")
PYWORKER

DB_ID=$(docker ps -q --no-trunc \
    --filter "label=com.docker.compose.project=$PROJECT" \
    --filter "label=com.docker.compose.service=db")

[ -n "$DB_ID" ] || {
    echo "FAIL: Database container missing"
    exit 1
}

MARKER=$(docker exec "$DB_ID" cat /data/marker)

[ "$MARKER" = "preserved" ] || {
    echo "FAIL: Database marker changed"
    exit 1
}

echo "PASS: Database volume marker preserved"
echo "===== PRE-EXECUTION SIGKILL LAB PASSED ====="
'''

target.write_text(prefix + suffix, encoding="utf-8")
target.chmod(0o600)

print("PASS: Pre-execution crash laboratory generated")
PY

sh -n "$TEMP"

echo "===== RUNNING ISOLATED SIGKILL EXPERIMENT ====="

sh "$TEMP"

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers remain"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Laboratory database volume remains"
    exit 1
fi

echo "PASS: Laboratory resources cleaned"
echo "===== GATE 4D.16AE.12A PASSED ====="
