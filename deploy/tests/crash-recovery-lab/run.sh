#!/bin/sh
set -eu

PROJECT=fbweb-gate16y-lab
RELEASE_ID=fbweb-gate16y-001
COMPOSE=deploy/tests/recovery-integration-lab/compose.yml

PREV_APP='ghcr.io/devnechi/fbwebltd-app@sha256:5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a'
PREV_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4'

NEXT_APP='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
NEXT_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export PROJECT RELEASE_ID PREV_APP PREV_WEB NEXT_APP NEXT_WEB

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers already exist"
    exit 1
fi

WORK=$(mktemp -d)
mkdir -m 700 "$WORK/journals" "$WORK/locks"

export LAB_JOURNALS="$WORK/journals"
export LAB_LOCKS="$WORK/locks"
export LAB_READY="$WORK/controller-ready"

LAB_APP_IMAGE="$PREV_APP"
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

HOLDER_PID=

compose() {
    docker compose -p "$PROJECT" -f "$COMPOSE" "$@"
}

cleanup() {
    if [ -n "$HOLDER_PID" ]; then
        kill "$HOLDER_PID" 2>/dev/null || true
        wait "$HOLDER_PID" 2>/dev/null || true
    fi

    compose down -v >/dev/null 2>&1 || true
    rm -rf "$WORK"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "Starting previous release in isolated laboratory"
compose up -d --pull never --no-build

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan

previous = ImagePair(os.environ["PREV_APP"], os.environ["PREV_WEB"])
candidate = ImagePair(os.environ["NEXT_APP"], os.environ["NEXT_WEB"])

identity = None

for _ in range(30):
    try:
        identity = collect_snapshot(os.environ["PROJECT"], previous)
        if identity.app_healthy and identity.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise SystemExit("FAIL: Previous containers did not become healthy")

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]

sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# Laboratory-only simulation flags. Not production approval.
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

print("PASS: Recovery journal persisted at ACTIVATING")
print("PASS: Actual database identity checkpointed")
PY

echo "Activating candidate images in laboratory only"

LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

echo "Launching a controller process holding the deployment lock"

PYTHONDONTWRITEBYTECODE=1 python3 -u - <<'PY' &
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, "deploy/releases")

from deployment_lock import deployment_lock

with deployment_lock(os.environ["LAB_LOCKS"]):
    Path(os.environ["LAB_READY"]).write_text(
        "locked", encoding="utf-8"
    )
    time.sleep(300)
PY

HOLDER_PID=$!

READY=0

for attempt in 1 2 3 4 5 6 7 8 9 10; do
    if [ -f "$LAB_READY" ]; then
        READY=1
        break
    fi

    if ! kill -0 "$HOLDER_PID" 2>/dev/null; then
        echo "FAIL: Controller exited before acquiring lock"
        exit 1
    fi

    sleep 1
done

if [ "$READY" -ne 1 ]; then
    echo "FAIL: Controller failed to acquire lock"
    exit 1
fi

echo "PASS: Controller acquired global lock"

echo "Simulating abrupt controller termination"

kill -9 "$HOLDER_PID"
wait "$HOLDER_PID" 2>/dev/null || true
HOLDER_PID=

echo "Restarting recovery decision process"

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from locked_recovery import decide_from_docker
from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"],
    os.environ["LAB_LOCKS"],
)

release_id = os.environ["RELEASE_ID"]
project = os.environ["PROJECT"]

record = sim.journal.read(release_id)

assert record["state"] == "ACTIVATING"
assert record["revision"] == 2

print("PASS: Interrupted journal recovered after process termination")

result = None

for _ in range(30):
    try:
        result = decide_from_docker(
            sim,
            release_id,
            project,
        )
        if result["action"] == "RESTORE_PREVIOUS":
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError(
        "FAIL: Restarted recovery did not request restoration: "
        + str(result)
    )

assert result["database_identity_matched"]
assert result["docker_mutation_performed"] is False
assert result["journal_mutation_performed"] is False
assert result["production_execution_enabled"] is False

after = sim.journal.read(release_id)

assert after == record, "Recovery decision unexpectedly changed journal"

print("PASS: Global lock reacquired after controller crash")
print("PASS: Fresh Docker inspection completed")
print("PASS: Restarted controller requests RESTORE_PREVIOUS")
print("PASS: Database container identity preserved")
print("PASS: Recovery decision did not mutate Docker or journal")
PY

echo "PASS: Crash-and-restart recovery decision laboratory"
echo "Cleaning isolated laboratory"
