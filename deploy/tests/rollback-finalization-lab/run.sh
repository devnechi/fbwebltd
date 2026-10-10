#!/bin/sh
set -eu

PROJECT=fbweb-gate16aa-lab
RELEASE_ID=fbweb-gate16aa-001
COMPOSE=deploy/tests/recovery-integration-lab/compose.yml

PREV_APP='ghcr.io/devnechi/fbwebltd-app@sha256:5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a'
PREV_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4'

NEXT_APP='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
NEXT_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export PROJECT RELEASE_ID PREV_APP PREV_WEB NEXT_APP NEXT_WEB

VOLUME="${PROJECT}_db_data"

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers already exist"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Laboratory volume already exists"
    exit 1
fi

WORK=$(mktemp -d)
mkdir -m 700 "$WORK/journals" "$WORK/locks"

export LAB_JOURNALS="$WORK/journals"
export LAB_LOCKS="$WORK/locks"

LAB_APP_IMAGE="$PREV_APP"
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose() {
    docker compose -p "$PROJECT" -f "$COMPOSE" "$@"
}

cleanup() {
    compose down -v >/dev/null 2>&1 || true
    rm -rf "$WORK"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "===== STEP 1: START PREVIOUS RELEASE ====="

compose up -d --pull never --no-build

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan

project = os.environ["PROJECT"]
release_id = os.environ["RELEASE_ID"]

previous = ImagePair(
    os.environ["PREV_APP"],
    os.environ["PREV_WEB"],
)

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

identity = None

for _ in range(30):
    try:
        identity = collect_snapshot(project, previous)

        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass

    time.sleep(1)
else:
    raise SystemExit("FAIL: Previous release not healthy")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# Laboratory fixtures, not authentic production approvals.
plan = ReleasePlan(
    candidate=candidate,
    previous=previous,
    approval_verified=True,
    provenance_verified=True,
    recovery_record_persisted=True,
    backup_verified=True,
    deployment_lock_acquired=True,
    current_health_verified=True,
)

sim.journal.advance(release_id, 0, "precheck_passed", plan)
sim.journal.advance(release_id, 1, "activate", plan)

record = sim.journal.read(release_id)

assert record["state"] == "ACTIVATING"
assert record["revision"] == 2

print("PASS: Previous application and web verified")
print("PASS: Real database container ID checkpointed")
print("PASS: Journal persisted at ACTIVATING")
PY

echo "===== STEP 2: ACTIVATE CANDIDATE IMAGES ====="

LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

echo "===== STEP 3: RECORD ROLLING_BACK ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

for _ in range(30):
    try:
        identity = collect_snapshot(os.environ["PROJECT"], candidate)
        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise SystemExit("FAIL: Candidate image pair not verified")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]

record = sim.journal.advance(
    release_id,
    2,
    "failed",
)

assert record["state"] == "ROLLING_BACK"
assert record["revision"] == 3

checkpoint = sim.read_checkpoint(release_id, record)

assert identity.db_container_id == checkpoint["db_identity"]

print("PASS: Candidate release observed")
print("PASS: Journal persisted at ROLLING_BACK")
print("PASS: Database identity unchanged")
PY

echo "===== STEP 4: REJECT PREMATURE FINALIZATION ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys

sys.path.insert(0, "deploy/releases")

from rollback_finalizer import finalize_rollback
from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]
before = sim.journal.read(release_id)

try:
    finalize_rollback(
        sim,
        release_id,
        os.environ["PROJECT"],
    )
except ValueError:
    print("PASS: Finalization rejected with candidate images")
else:
    raise AssertionError(
        "FAIL: Candidate images were incorrectly finalized"
    )

after = sim.journal.read(release_id)

assert after == before, "Journal changed after rejected finalization"
assert after["state"] == "ROLLING_BACK"

print("PASS: Journal remains ROLLING_BACK")
print("PASS: Journal revision unchanged")
PY

echo "===== STEP 5: RESTORE PREVIOUS IMAGES ====="

LAB_APP_IMAGE="$PREV_APP"
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

echo "===== STEP 6: VERIFY AND FINALIZE ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from recovery_simulator import RecoverySimulator
from rollback_finalizer import finalize_rollback
from rollback_planner import ImagePair

project = os.environ["PROJECT"]
release_id = os.environ["RELEASE_ID"]

previous = ImagePair(
    os.environ["PREV_APP"],
    os.environ["PREV_WEB"],
)

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

record = sim.journal.read(release_id)
checkpoint = sim.read_checkpoint(release_id, record)

for _ in range(30):
    try:
        identity = collect_snapshot(project, previous)

        if (
            identity.app_healthy
            and identity.web_healthy
            and identity.db_container_id == checkpoint["db_identity"]
        ):
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError("FAIL: Previous images not restored and healthy")

print("PASS: Previous app image restored")
print("PASS: Previous web image restored")
print("PASS: Restored services healthy")
print("PASS: Database container ID unchanged")

result = finalize_rollback(
    sim,
    release_id,
    project,
)

assert result["state"] == "ROLLED_BACK"
assert result["revision"] == 4
assert result["database_identity_matched"]
assert result["docker_mutation_performed"] is False
assert result["production_execution_enabled"] is False

reopened = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

final_record = reopened.journal.read(release_id)

assert final_record["state"] == "ROLLED_BACK"
assert final_record["revision"] == 4
assert not reopened.journal.interrupted(release_id)

print("PASS: Journal finalized at ROLLED_BACK")
print("PASS: Final revision persisted as 4")
print("PASS: Journal remains finalized after reopening")
print("PASS: Finalizer performed no Docker mutation")
PY

echo "===== STEP 7: VERIFY DATABASE VOLUME ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import subprocess
import sys

sys.path.insert(0, "deploy/releases")

from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]
record = sim.journal.read(release_id)
checkpoint = sim.read_checkpoint(release_id, record)

db_id = subprocess.run(
    [
        "/usr/bin/docker",
        "ps",
        "-q",
        "--no-trunc",
        "--filter",
        "label=com.docker.compose.project=" + os.environ["PROJECT"],
        "--filter",
        "label=com.docker.compose.service=db",
    ],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

assert db_id == checkpoint["db_identity"], (
    "Database container was recreated"
)

marker = subprocess.run(
    ["/usr/bin/docker", "exec", db_id, "cat", "/data/marker"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

assert marker == "preserved", "Database marker changed"

print("PASS: Database container preserved")
print("PASS: Persistent database volume data preserved")
PY

echo "===== GATE 4D.16AA PASSED ====="
echo "Cleanup of isolated laboratory follows"
