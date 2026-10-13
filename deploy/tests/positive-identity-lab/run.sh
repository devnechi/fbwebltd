#!/bin/sh
set -eu

PROJECT=fbweb-gate16u-lab
COMPOSE=deploy/tests/positive-identity-lab/compose.yml

LAB_APP_IMAGE='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
LAB_WEB_IMAGE='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

export LAB_APP_IMAGE LAB_WEB_IMAGE

cleanup() {
    docker compose -p "$PROJECT" -f "$COMPOSE" down >/dev/null 2>&1 || true
}

trap cleanup EXIT

echo "Checking that laboratory containers do not already exist"

EXISTING=$(docker ps -aq \
    --filter "label=com.docker.compose.project=$PROJECT")

if [ -n "$EXISTING" ]; then
    echo "FAIL: Existing laboratory containers detected"
    exit 1
fi

echo "Starting isolated digest-pinned containers"

docker compose -p "$PROJECT" -f "$COMPOSE" \
    up -d --pull never --no-build

PROJECT="$PROJECT" PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from rollback_planner import ImagePair

project = os.environ["PROJECT"]

expected = ImagePair(
    os.environ["LAB_APP_IMAGE"],
    os.environ["LAB_WEB_IMAGE"],
)

verified = None

for attempt in range(20):
    try:
        verified = collect_snapshot(project, expected)
        if verified.app_healthy and verified.web_healthy:
            break
    except ValueError:
        pass
    time.sleep(1)
else:
    raise AssertionError(
        "FAIL: Positive identity verification did not become healthy"
    )

assert verified.project == project
assert verified.app_reference == expected.app
assert verified.web_reference == expected.web

assert len({
    verified.app_container_id,
    verified.web_container_id,
    verified.db_container_id,
}) == 3

print("PASS: Genuine application digest accepted")
print("PASS: Genuine web digest accepted")
print("PASS: Application container healthy")
print("PASS: Web container healthy")
print("PASS: Database container identity recorded")

incorrect = ImagePair(
    "ghcr.io/devnechi/fbwebltd-app@sha256:" + "f" * 64,
    expected.web,
)

try:
    collect_snapshot(project, incorrect)
except ValueError:
    print("PASS: Incorrect application digest rejected")
else:
    raise AssertionError(
        "FAIL: Incorrect application digest was accepted"
    )

print("PASS: Positive Docker identity integration")
PY

echo "PASS: Laboratory completed; cleanup follows"
