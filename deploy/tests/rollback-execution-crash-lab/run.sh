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
    raise SystemExit("FAIL: Source laboratory structure changed")

prefix = content.split(anchor, 1)[0]

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

for attempt in range(40):
    identity = collect_snapshot(LAB_PROJECT, candidate)

    if identity.app_healthy and identity.web_healthy:
        print("PASS: Candidate images healthy")
        break

    time.sleep(1)
else:
    raise AssertionError(
        "Candidate containers did not become healthy"
    )
PYHEALTH

echo "===== SIGKILL AFTER DURABLE STARTED ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PYWORKER'
import os
import signal
import subprocess
import sys

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from lab_rollback_command import LAB_PROJECT
from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

before = collect_snapshot(LAB_PROJECT, candidate)

assert before.app_healthy and before.web_healthy

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
    raise AssertionError("SIGKILL unexpectedly returned")

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
    timeout=90,
)

if result.returncode != -signal.SIGKILL:
    raise AssertionError(
        f"Expected controller SIGKILL (-9), got {result.returncode}"
    )

print("PASS: Actual SIGKILL terminated controller worker")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]
store = RollbackAttemptStore(sim)

attempts = store.read(release_id)
journal = sim.journal.read(release_id)

assert len(attempts) == 1
assert attempts[0]["schema_version"] == 2
assert attempts[0]["status"] == "STARTED"
assert journal["state"] == "ROLLING_BACK"

print("PASS: Durable STARTED survived SIGKILL")
print("PASS: Journal remains ROLLING_BACK")

after = collect_snapshot(LAB_PROJECT, candidate)

assert before.app_container_id == after.app_container_id
assert before.web_container_id == after.web_container_id
assert before.db_container_id == after.db_container_id

print("PASS: Candidate container identities unchanged")

commands = []

def forbidden_command(command):
    commands.append(command)
    raise AssertionError("Duplicate restoration executed")

from lab_rollback_executor import execute_lab_rollback

try:
    execute_lab_rollback(
        sim,
        release_id,
        command_runner=forbidden_command,
    )
except ValueError:
    assert commands == []
    print("PASS: Restarted executor rejected duplicate execution")
else:
    raise AssertionError("Duplicate execution accepted")

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
    echo "FAIL: Database volume marker changed"
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
    echo "FAIL: Laboratory volume remains"
    exit 1
fi

echo "PASS: Laboratory resources cleaned"
echo "===== GATE 4D.16AE.12A PASSED ====="
