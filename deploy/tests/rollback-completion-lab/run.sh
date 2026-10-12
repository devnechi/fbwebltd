#!/bin/sh
set -eu

PROJECT=fbweb-gate16ae-lab
COMPOSE=deploy/tests/recovery-integration-lab/compose.yml
RELEASE_ID=fbweb-gate16ae-completion-001

PREV_APP='ghcr.io/devnechi/fbwebltd-app@sha256:5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a'
PREV_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4'
NEXT_APP='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
NEXT_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export PROJECT RELEASE_ID PREV_APP PREV_WEB NEXT_APP NEXT_WEB

cd "$(dirname "$0")/../../.."

# Never use this script against a pre-existing Docker project.
if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers already exist"
    exit 1
fi

if docker volume inspect "${PROJECT}_db_data" >/dev/null 2>&1; then
    echo "FAIL: Laboratory database volume already exists"
    exit 1
fi

for IMAGE in "$PREV_APP" "$PREV_WEB" "$NEXT_APP" "$NEXT_WEB"; do
    docker image inspect "$IMAGE" >/dev/null || {
        echo "FAIL: Required image unavailable: $IMAGE"
        exit 1
    }
done

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, "deploy/releases")
from lab_compose_integrity import validate_lab_compose_integrity

validate_lab_compose_integrity(Path.cwd())
print("PASS: Laboratory Compose integrity")
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

echo "===== START PREVIOUS RELEASE ====="

export LAB_APP_IMAGE="$PREV_APP"
export LAB_WEB_IMAGE="$PREV_WEB"

compose up -d --pull never --no-build

echo "===== CREATE RECOVERY CHECKPOINT ====="

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
    os.environ["PREV_APP"], os.environ["PREV_WEB"]
)
candidate = ImagePair(
    os.environ["NEXT_APP"], os.environ["NEXT_WEB"]
)

for _ in range(30):
    try:
        identity = collect_snapshot(project, previous)
        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError("Previous images did not become healthy")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# Synthetic laboratory flags; not actual deployment approvals.
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
print("PASS: Journal and database checkpoint prepared")
PY

echo "===== ACTIVATE CANDIDATE ====="

export LAB_APP_IMAGE="$NEXT_APP"
export LAB_WEB_IMAGE="$NEXT_WEB"

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

echo "===== EXECUTE REAL ROLLBACK ====="

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
    raise AssertionError("Candidate images did not become healthy")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)
release_id = os.environ["RELEASE_ID"]

result = execute_lab_rollback(sim, release_id, LAB_PROJECT)

assert result["restoration_verified"] is True
assert result["journal_finalized"] is False
assert result["attempt_status"] == "STARTED"

record = RollbackAttemptStore(sim).read(release_id)[0]
assert record["schema_version"] == 2
assert record["status"] == "STARTED"

restored = collect_snapshot(LAB_PROJECT, PREVIOUS)
assert restored.app_healthy and restored.web_healthy

checkpoint = sim.read_checkpoint(
    release_id,
    sim.journal.read(release_id),
)
assert restored.db_container_id == checkpoint["db_identity"]

print("PASS: Actual restricted restoration completed")
print("PASS: Bound STARTED attempt persisted")
PY

# Capture full container identities before any completion operation.
container_ids() {
    docker ps -aq --no-trunc \
      --filter "label=com.docker.compose.project=$PROJECT" \
      | sort
}

BEFORE_IDS=$(container_ids)

if [ "$(printf '%s\n' "$BEFORE_IDS" | grep -c .)" -ne 3 ]; then
    echo "FAIL: Expected exactly three laboratory containers"
    exit 1
fi

echo "===== SIMULATE INTERRUPTED COMPLETION ====="

# Run completion in a separate Python process.
# Inject failure after the attempt is durably marked SUCCEEDED
# but before the journal finalizer executes.
if PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
from unittest.mock import patch

sys.path.insert(0, "deploy/releases")

from lab_rollback_completion import complete_lab_rollback
from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

def injected_failure(*args, **kwargs):
    raise RuntimeError("injected completion interruption")

with patch(
    "lab_rollback_completion.finalize_rollback_locked",
    side_effect=injected_failure,
):
    complete_lab_rollback(
        sim,
        os.environ["RELEASE_ID"],
    )
PY
then
    echo "FAIL: Injected interruption was not triggered"
    exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys

sys.path.insert(0, "deploy/releases")

from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)
release_id = os.environ["RELEASE_ID"]

record = RollbackAttemptStore(sim).read(release_id)[0]
journal = sim.journal.read(release_id)

assert record["status"] == "SUCCEEDED"
assert record["revision"] == 1
assert journal["state"] == "ROLLING_BACK"
assert journal["revision"] == 3

print("PASS: SUCCEEDED persisted before journal finalization")
print("PASS: Journal remains ROLLING_BACK after interruption")
PY

AFTER_INTERRUPTION_IDS=$(container_ids)
[ "$BEFORE_IDS" = "$AFTER_INTERRUPTION_IDS" ] || {
    echo "FAIL: Containers changed during interrupted completion"
    exit 1
}

echo "===== RESTART COMPLETION CONTROLLER ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys

sys.path.insert(0, "deploy/releases")

from lab_rollback_completion import complete_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)
release_id = os.environ["RELEASE_ID"]

resumed = complete_lab_rollback(sim, release_id)

assert resumed["attempt_status"] == "SUCCEEDED"
assert resumed["journal_state"] == "ROLLED_BACK"
assert resumed["already_complete"] is False
assert resumed["docker_mutation_performed"] is False

again = complete_lab_rollback(sim, release_id)

assert again["already_complete"] is True
assert again["journal_state"] == "ROLLED_BACK"
assert again["docker_mutation_performed"] is False

attempts = RollbackAttemptStore(sim).read(release_id)
journal = sim.journal.read(release_id)

assert len(attempts) == 1
assert attempts[0]["status"] == "SUCCEEDED"
assert attempts[0]["revision"] == 1
assert journal["state"] == "ROLLED_BACK"
assert journal["revision"] == 4

print("PASS: Restarted controller finalized journal")
print("PASS: Repeated completion is idempotent")
print("PASS: Exactly one successful attempt recorded")
PY

AFTER_COMPLETION_IDS=$(container_ids)
[ "$BEFORE_IDS" = "$AFTER_COMPLETION_IDS" ] || {
    echo "FAIL: Containers were recreated during completion"
    exit 1
}

echo "PASS: App/web/db container IDs unchanged during completion"

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
echo "===== GATE 4D.16AE.10 PASSED ====="
