#!/bin/sh
set -eu

PROJECT=fbweb-gate16ab-lab
RELEASE_ID=fbweb-gate16ab-001
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

for image in "$PREV_APP" "$PREV_WEB" "$NEXT_APP" "$NEXT_WEB"; do
    if ! docker image inspect "$image" >/dev/null 2>&1; then
        echo "FAIL: Required image is not available locally: $image"
        echo "Pull this immutable image before running the laboratory."
        exit 1
    fi
done

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

echo "===== 1. START PREVIOUS RELEASE ====="

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

for attempt in range(30):
    try:
        identity = collect_snapshot(project, previous)
        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError("Previous release did not become healthy")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# Fixtures only: these are not genuine production approvals.
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

print("PASS: Previous images verified")
print("PASS: Database identity checkpointed")
print("PASS: Journal entered ACTIVATING")
PY

echo "===== 2. ACTIVATE CANDIDATE PAIR ====="

LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

echo "===== 3. ENTER ROLLING_BACK ====="

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

for attempt in range(30):
    try:
        identity = collect_snapshot(os.environ["PROJECT"], candidate)
        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError("Candidate images were not verified")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

record = sim.journal.advance(
    os.environ["RELEASE_ID"],
    2,
    "failed",
)

assert record["state"] == "ROLLING_BACK"
assert record["revision"] == 3

checkpoint = sim.read_checkpoint(
    os.environ["RELEASE_ID"],
    record,
)
assert identity.db_container_id == checkpoint["db_identity"]

print("PASS: Candidate images verified")
print("PASS: ROLLING_BACK persisted before restoration")
PY

verify_retry() {
    EXPECT_ACTION="$1" PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from locked_rollback_retry import decide_retry_from_docker
from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]
project = os.environ["PROJECT"]
expected = os.environ["EXPECT_ACTION"]

before = sim.journal.read(release_id)
assert before["state"] == "ROLLING_BACK"
assert before["revision"] == 3

last = None

for attempt in range(30):
    try:
        last = decide_retry_from_docker(sim, release_id, project)

        if (
            last["action"] == expected
            and last["database_identity_matched"]
            and (
                expected != "VERIFY_AND_FINALIZE"
                or (last["app_healthy"] and last["web_healthy"])
            )
        ):
            break
    except ValueError:
        pass

    time.sleep(1)
else:
    raise AssertionError(
        f"Expected {expected}; last result: {last}"
    )

assert last["docker_mutation_performed"] is False
assert last["journal_mutation_performed"] is False
assert last["production_execution_enabled"] is False

after = sim.journal.read(release_id)
assert after == before, "Retry decision modified journal"

print("PASS: Locked retry action:", expected)
print("PASS: Journal remains unchanged")
print("PASS: Database identity matches checkpoint")
PY
}

echo "===== 4. INSPECT FULLY ACTIVATED CANDIDATE ====="

verify_retry RESTORE_PREVIOUS

echo "===== 5. SIMULATE INTERRUPTED PARTIAL ROLLBACK ====="

# Restore only web. Application remains on the candidate digest.
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    web

verify_retry RESTORE_PREVIOUS

echo "===== 6. COMPLETE LABORATORY RESTORATION ====="

LAB_APP_IMAGE="$PREV_APP"
export LAB_APP_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app

verify_retry VERIFY_AND_FINALIZE

echo "===== 7. FINALIZE VERIFIED ROLLBACK ====="

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
project = os.environ["PROJECT"]

result = finalize_rollback(
    sim,
    release_id,
    project,
)

assert result["state"] == "ROLLED_BACK"
assert result["revision"] == 4
assert result["database_identity_matched"]

reopened = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

record = reopened.journal.read(release_id)

assert record["state"] == "ROLLED_BACK"
assert record["revision"] == 4
assert not reopened.journal.interrupted(release_id)

print("PASS: Real Docker finalization succeeded")
print("PASS: Journal persisted ROLLED_BACK")
print("PASS: Reopened journal is terminal")
PY

echo "===== 8. VERIFY DATABASE IDENTITY AND VOLUME ====="

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
        "/usr/bin/docker", "ps", "-q", "--no-trunc",
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
    "Database container was replaced"
)

marker = subprocess.run(
    ["/usr/bin/docker", "exec", db_id, "cat", "/data/marker"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

assert marker == "preserved", "Database volume marker changed"

print("PASS: Database container ID unchanged")
print("PASS: Persistent database data preserved")
PY

echo "===== GATE 4D.16AB.3 PASSED ====="
echo "Cleaning the isolated laboratory project"
