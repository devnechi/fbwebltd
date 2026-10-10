#!/bin/sh
set -eu

PROJECT=fbweb-gate16x-lab
COMPOSE=deploy/tests/recovery-integration-lab/compose.yml
RELEASE_ID=fbweb-gate16x-001

PREV_APP='ghcr.io/devnechi/fbwebltd-app@sha256:5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a'
PREV_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4'

NEXT_APP='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
NEXT_WEB='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export PROJECT RELEASE_ID PREV_APP PREV_WEB NEXT_APP NEXT_WEB

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory project already has containers"
    exit 1
fi

WORK=$(mktemp -d)
mkdir -m 700 "$WORK/journals" "$WORK/locks"
export LAB_JOURNALS="$WORK/journals"
export LAB_LOCKS="$WORK/locks"

LAB_APP_IMAGE="$PREV_APP"
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

cleanup() {
    docker compose -p "$PROJECT" -f "$COMPOSE" down -v \
        >/dev/null 2>&1 || true
    rm -rf "$WORK"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

compose() {
    docker compose -p "$PROJECT" -f "$COMPOSE" "$@"
}

echo "Pulling verified previous images into local laboratory"
docker pull --platform linux/amd64 "$PREV_APP"
docker pull --platform linux/amd64 "$PREV_WEB"

echo "Starting previous release in isolated containers"
compose up -d --pull never --no-build

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, ReleasePlan

project = os.environ["PROJECT"]
previous = ImagePair(os.environ["PREV_APP"], os.environ["PREV_WEB"])
candidate = ImagePair(os.environ["NEXT_APP"], os.environ["NEXT_WEB"])

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
    raise SystemExit("FAIL: Previous release did not become healthy")

sim = RecoverySimulator(
    Path(os.environ["LAB_JOURNALS"]),
    Path(os.environ["LAB_LOCKS"]),
)

release_id = os.environ["RELEASE_ID"]
sim.journal.create(release_id, candidate, previous)
sim.create_checkpoint(release_id, identity.db_container_id)

# The following flags are laboratory fixtures only.
# They are NOT evidence of production authorization.
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

Path(os.environ["LAB_JOURNALS"], "db-id.txt").write_text(
    identity.db_container_id,
    encoding="utf-8",
)

print("PASS: Real database container ID recorded before activation")
print("PASS: Journal advanced to ACTIVATING")
PY

verify() {
    EXPECT_ACTION="$1" PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
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

expected = os.environ["EXPECT_ACTION"]
result = None

for _ in range(30):
    try:
        result = decide_from_docker(
            sim,
            os.environ["RELEASE_ID"],
            os.environ["PROJECT"],
        )
        if result["action"] == expected:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise SystemExit(
        f"FAIL: Expected {expected}; last result: {result}"
    )

assert result["database_identity_matched"]
assert result["docker_mutation_performed"] is False
assert result["journal_mutation_performed"] is False
assert result["production_execution_enabled"] is False

print("PASS: Live recovery decision:", expected)
PY
}

echo "Verifying interrupted activation before any container change"
verify NO_ACTION

echo "Switching only application and web to candidate images"
LAB_APP_IMAGE="$NEXT_APP"
LAB_WEB_IMAGE="$NEXT_WEB"
export LAB_APP_IMAGE LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    app web

verify RESTORE_PREVIOUS

echo "Testing partial application/web activation"
LAB_WEB_IMAGE="$PREV_WEB"
export LAB_WEB_IMAGE

compose up -d \
    --no-deps \
    --no-build \
    --pull never \
    --force-recreate \
    web

verify RESTORE_PREVIOUS

echo "Confirming database identity and persistent marker"
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import subprocess
from pathlib import Path

project = os.environ["PROJECT"]
expected_id = Path(
    os.environ["LAB_JOURNALS"], "db-id.txt"
).read_text(encoding="utf-8")

observed = subprocess.run(
    [
        "/usr/bin/docker", "ps", "-q",
        "--filter", f"label=com.docker.compose.project={project}",
        "--filter", "label=com.docker.compose.service=db",
        "--no-trunc",
    ],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

assert observed == expected_id, "Database container was replaced"

marker = subprocess.run(
    ["/usr/bin/docker", "exec", observed, "cat", "/data/marker"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

assert marker == "preserved", "Database volume marker changed"

print("PASS: Database container unchanged")
print("PASS: Database volume data preserved")
PY

echo "PASS: Real Docker recovery decision laboratory"
echo "Cleaning only the isolated laboratory project"
