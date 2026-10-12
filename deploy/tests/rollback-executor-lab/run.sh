#!/bin/sh
set -eu

PROJECT=fbweb-gate16ae-lab
COMPOSE=deploy/tests/recovery-integration-lab/compose.yml
RELEASE_ID=fbweb-gate16ae-executor-001

PREV_APP='ghcr.io/devnechi/fbwebltd-app@sha256:5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a'
PREV_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4'

NEXT_APP='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
NEXT_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export PROJECT RELEASE_ID PREV_APP PREV_WEB NEXT_APP NEXT_WEB

cd "$(dirname "$0")/../../.."

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Existing laboratory containers detected"
    exit 1
fi

if docker volume inspect "${PROJECT}_db_data" >/dev/null 2>&1; then
    echo "FAIL: Existing laboratory database volume detected"
    exit 1
fi

for IMAGE in "$PREV_APP" "$PREV_WEB" "$NEXT_APP" "$NEXT_WEB"; do
    docker image inspect "$IMAGE" >/dev/null || {
        echo "FAIL: Required pinned image missing"
        exit 1
    }
done

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, "deploy/releases")

from lab_compose_integrity import validate_lab_compose_integrity

validate_lab_compose_integrity(Path.cwd())
print("PASS: Laboratory Compose configuration approved")
PY

WORK=$(mktemp -d)
mkdir -m 700 "$WORK/journals" "$WORK/locks"

export LAB_JOURNALS="$WORK/journals"
export LAB_LOCKS="$WORK/locks"

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

echo "===== STARTING PREVIOUS RELEASE ====="

LAB_APP_IMAGE="$PREV_APP"
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d --pull never --no-build

echo "===== PREPARING RECOVERY JOURNAL ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan

previous = ImagePair(
    os.environ["PREV_APP"],
    os.environ["PREV_WEB"],
)
candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

for _ in range(30):
    try:
        identity = collect_snapshot(os.environ["PROJECT"], previous)
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

release_id = os.environ["RELEASE_ID"]

sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# Laboratory-only fixtures, not production authorization.
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
sim.journal.advance(release_id, 2, "failed")

assert sim.journal.read(release_id)["state"] == "ROLLING_BACK"

print("PASS: Real database identity checkpointed")
print("PASS: Recovery journal entered ROLLING_BACK")
PY

echo "===== ACTIVATING CANDIDATE IMAGES ====="

LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

echo "===== RUNNING ACTUAL RESTRICTED EXECUTOR ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from lab_rollback_command import LAB_PROJECT, PREVIOUS
from lab_rollback_executor import execute_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair

release_id = os.environ["RELEASE_ID"]

candidate = ImagePair(
    os.environ["NEXT_APP"],
    os.environ["NEXT_WEB"],
)

for _ in range(30):
    try:
        identity = collect_snapshot(LAB_PROJECT, candidate)
        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError("Candidate release did not become healthy")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

before = sim.journal.read(release_id)
checkpoint = sim.read_checkpoint(release_id, before)

result = execute_lab_rollback(
    sim,
    release_id,
    LAB_PROJECT,
)

assert result["restoration_verified"] is True
assert result["database_identity_matched"] is True
assert result["attempt_status"] == "STARTED"
assert result["journal_finalized"] is False
assert result["production_execution_enabled"] is False

after = sim.journal.read(release_id)
assert after == before
assert after["state"] == "ROLLING_BACK"

store = RollbackAttemptStore(sim)
attempts = store.read(release_id)

assert len(attempts) == 1
assert attempts[0]["schema_version"] == 2
assert attempts[0]["status"] == "STARTED"
assert attempts[0]["execution_id"] == result["execution_id"]
assert attempts[0]["previous_app"] == PREVIOUS.app
assert attempts[0]["previous_web"] == PREVIOUS.web
assert attempts[0]["database_identity"] == checkpoint["db_identity"]

restored = collect_snapshot(LAB_PROJECT, PREVIOUS)

assert restored.db_container_id == checkpoint["db_identity"]
assert restored.app_healthy and restored.web_healthy

print("PASS: Real Docker app/web restoration verified")
print("PASS: Previous immutable images restored")
print("PASS: Database container identity unchanged")
print("PASS: Bound attempt remains STARTED")
print("PASS: Recovery journal remains ROLLING_BACK")

try:
    execute_lab_rollback(sim, release_id, LAB_PROJECT)
except ValueError:
    print("PASS: Second executor invocation blocked")
else:
    raise AssertionError("Second restoration was not blocked")

assert len(store.read(release_id)) == 1
PY

echo "===== VERIFY DATABASE MARKER ====="

DB_ID=$(docker ps -q --no-trunc \
    --filter "label=com.docker.compose.project=$PROJECT" \
    --filter "label=com.docker.compose.service=db")

if [ -z "$DB_ID" ]; then
    echo "FAIL: Database container missing"
    exit 1
fi

MARKER=$(docker exec "$DB_ID" cat /data/marker)

if [ "$MARKER" != "preserved" ]; then
    echo "FAIL: Database volume marker changed"
    exit 1
fi

echo "PASS: Database volume marker preserved"
echo "===== GATE 4D.16AE.8 PASSED ====="
