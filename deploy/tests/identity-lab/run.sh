#!/bin/sh
set -eu

PROJECT=fbweb-gate16s-lab
COMPOSE=deploy/tests/identity-lab/compose.yml

cleanup() {
    docker compose -p "$PROJECT" -f "$COMPOSE" down \
        --remove-orphans >/dev/null 2>&1 || true
}

trap cleanup EXIT HUP INT TERM

echo "Starting isolated identity laboratory"

docker compose -p "$PROJECT" -f "$COMPOSE" \
    up -d --pull never --no-build

echo "Checking real Docker inspection responses"

PROJECT="$PROJECT" PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, "deploy/releases")

from docker_snapshot_reader import collect_snapshot
from rollback_planner import ImagePair

project = os.environ["PROJECT"]

def docker(*args):
    result = subprocess.run(
        ["/usr/bin/docker", *args],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )
    return result.stdout

ids = docker(
    "ps",
    "--all",
    "--filter",
    "label=com.docker.compose.project=" + project,
    "--format",
    "{{.ID}}",
).splitlines()

assert len(ids) == 3, "Expected exactly three lab containers"

containers = json.loads(
    docker("inspect", "--type", "container", *ids)
)

services = {}

for item in containers:
    labels = item["Config"]["Labels"]
    assert labels["com.docker.compose.project"] == project
    service = labels["com.docker.compose.service"]
    assert service not in services
    services[service] = item

assert set(services) == {"app", "web", "db"}

for _ in range(15):
    containers = json.loads(
        docker("inspect", "--type", "container", *ids)
    )
    services = {
        item["Config"]["Labels"]["com.docker.compose.service"]: item
        for item in containers
    }
    if all(
        services[name]["State"].get("Health", {}).get("Status")
        == "healthy"
        for name in ("app", "web")
    ):
        break
    time.sleep(1)
else:
    raise AssertionError("Laboratory health checks did not pass")

for name in ("app", "web", "db"):
    item = services[name]
    assert item["State"]["Running"] is True
    assert len(item["Id"]) == 64

    metadata = json.loads(
        docker("image", "inspect", item["Image"])
    )
    assert len(metadata) == 1
    assert metadata[0]["Id"] == item["Image"]

    configured = item["Config"]["Image"]
    assert configured in metadata[0]["RepoDigests"]

    print(
        "PASS:", name,
        "container identity, local image ID and registry digest"
    )

# The existing policy specifically permits only the application's
# GHCR image references. BusyBox must never pass as an approved image.
unrelated = ImagePair(
    "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
    "ghcr.io/devnechi/fbwebltd-web@sha256:" + "b" * 64,
)

try:
    collect_snapshot(project, unrelated)
except ValueError:
    print("PASS: Unrelated BusyBox images rejected by GHCR policy")
else:
    raise AssertionError("FAIL: Unrelated images were accepted")

print("PASS: Live Docker inspection laboratory")
PY

echo "Laboratory finished; cleanup will remove only $PROJECT"
