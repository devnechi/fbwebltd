#!/bin/sh
set -eu

PROJECT=fbweb-gate16ad-lab
COMPOSE=deploy/tests/recovery-integration-lab/compose.yml
RELEASE_ID=fbweb-gate16ad-001

PREV_APP='ghcr.io/devnechi/fbwebltd-app@sha256:5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a'
PREV_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4'

NEXT_APP='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
NEXT_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export PROJECT RELEASE_ID PREV_APP PREV_WEB NEXT_APP NEXT_WEB

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers already exist"
    exit 1
fi

if docker volume inspect "${PROJECT}_db_data" >/dev/null 2>&1; then
    echo "FAIL: Laboratory volume already exists"
    exit 1
fi

for IMAGE in "$PREV_APP" "$PREV_WEB" "$NEXT_APP" "$NEXT_WEB"; do
    docker image inspect "$IMAGE" >/dev/null || {
        echo "FAIL: Required immutable image not available: $IMAGE"
        exit 1
    }
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

echo "===== STARTING PREVIOUS RELEASE ====="
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
    os.environ["LAB_JOURNALS"], os.environ["LAB_LOCKS"]
)
release_id = os.environ["RELEASE_ID"]

sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# Laboratory fixtures only; these are not production authorization.
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

print("PASS: Actual DB identity checkpointed")
print("PASS: ROLLING_BACK persisted")
PY

check_preflight() {
    EXPECT_ACTION="$1" EXPECT_RETRY="$2" \
    PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from recovery_simulator import RecoverySimulator
from rollback_execution_preflight import inspect_rollback_preflight

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"], os.environ["LAB_LOCKS"]
)
release_id = os.environ["RELEASE_ID"]

before = sim.journal.read(release_id)
expected = os.environ["EXPECT_ACTION"]
retry_expected = os.environ["EXPECT_RETRY"] == "true"

result = None
for _ in range(30):
    try:
        result = inspect_rollback_preflight(
            sim, release_id, os.environ["PROJECT"]
        )
        if (
            result["attempt_action"] == expected
            and result["retry_candidate"] == retry_expected
            and (
                expected != "VERIFY_AND_FINALIZE"
                or result["previous_pair_healthy"]
            )
        ):
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError(
        f"Expected {expected}, retry={retry_expected}; got {result}"
    )

assert result["database_identity_matched"]
assert result["execution_authorized"] is False
assert result["docker_mutation_performed"] is False
assert result["journal_mutation_performed"] is False
assert result["production_execution_enabled"] is False
assert sim.journal.read(release_id) == before

print(f"PASS: {expected}; retry_candidate={retry_expected}")
print("PASS: Preflight did not mutate journal or Docker")
PY
}

attempt_operation() {
    OPERATION="$1" PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys

sys.path.insert(0, "deploy/releases")

from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore
from rollback_attempt_policy import AttemptStatus

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"], os.environ["LAB_LOCKS"]
)
store = RollbackAttemptStore(sim)
release_id = os.environ["RELEASE_ID"]
operation = os.environ["OPERATION"]

if operation == "START":
    record = store.begin(release_id)
    assert record["status"] == "STARTED"
    print("PASS: STARTED attempt persisted")

elif operation == "FAIL_LATEST":
    records = store.read(release_id)
    latest = records[-1]
    assert latest["status"] == "STARTED"
    updated = store.finish(
        release_id,
        latest["attempt_id"],
        latest["revision"],
        AttemptStatus.FAILED,
    )
    assert updated["status"] == "FAILED"
    print("PASS: Failed attempt persisted")

else:
    raise ValueError("Unknown lab attempt operation")
PY
}

echo "===== CANDIDATE RELEASE ====="

LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d --no-deps --no-build --pull never \
    --force-recreate app web

check_preflight RETRY_ELIGIBLE true

echo "===== MIXED IMAGE PAIR ====="

LAB_WEB_IMAGE="$PREV_WEB"
export LAB_WEB_IMAGE

compose up -d --no-deps --no-build --pull never \
    --force-recreate web

check_preflight RETRY_ELIGIBLE true

echo "===== HEALTHY PREVIOUS PAIR ====="

LAB_APP_IMAGE="$PREV_APP"
export LAB_APP_IMAGE

compose up -d --no-deps --no-build --pull never \
    --force-recreate app

check_preflight VERIFY_AND_FINALIZE false

echo "===== RESTORE CANDIDATE PAIR FOR ATTEMPT TESTS ====="

LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d --no-deps --no-build --pull never \
    --force-recreate app web

echo "===== UNFINISHED ATTEMPT ====="

attempt_operation START
check_preflight INSPECT_REQUIRED false

echo "===== THREE FAILED ATTEMPTS ====="

attempt_operation FAIL_LATEST

attempt_operation START
attempt_operation FAIL_LATEST

attempt_operation START
attempt_operation FAIL_LATEST

check_preflight MANUAL_INTERVENTION false

echo "===== VERIFY DATABASE PRESERVATION ====="

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import subprocess
import sys

sys.path.insert(0, "deploy/releases")

from recovery_simulator import RecoverySimulator

sim = RecoverySimulator(
    os.environ["LAB_JOURNALS"], os.environ["LAB_LOCKS"]
)
release_id = os.environ["RELEASE_ID"]
record = sim.journal.read(release_id)
checkpoint = sim.read_checkpoint(release_id, record)

result = subprocess.run(
    [
        "/usr/bin/docker", "ps", "-q", "--no-trunc",
        "--filter",
        "label=com.docker.compose.project=" + os.environ["PROJECT"],
        "--filter", "label=com.docker.compose.service=db",
    ],
    capture_output=True,
    text=True,
    check=True,
    timeout=15,
)

db_id = result.stdout.strip()
assert db_id == checkpoint["db_identity"], "DB container replaced"

marker = subprocess.run(
    ["/usr/bin/docker", "exec", db_id, "cat", "/data/marker"],
    capture_output=True,
    text=True,
    check=True,
    timeout=15,
).stdout.strip()

assert marker == "preserved", "DB volume data changed"

attempts_root = (
    sim.journal.root / "rollback-attempts" / release_id
)
assert len(list(attempts_root.glob("[0-9]" * 6 + ".json"))) == 3

print("PASS: Database container unchanged")
print("PASS: Database volume marker preserved")
print("PASS: Three persisted attempt records")
PY

echo "===== GATE 4D.16AD.3 PASSED ====="
echo "Cleaning isolated laboratory"
