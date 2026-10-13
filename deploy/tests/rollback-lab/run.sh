#!/bin/sh
set -eu

PROJECT="fbweb-gate16g-lab"
FILE="deploy/tests/rollback-lab/compose.yml"

PREVIOUS_IMAGE="busybox:1.36"
CANDIDATE_IMAGE="busybox:1.35"

# Required for every Docker Compose invocation, including 'ps'.
export LAB_APP_IMAGE="$PREVIOUS_IMAGE"
export LAB_WEB_IMAGE="$PREVIOUS_IMAGE"
export LAB_APP_HEALTH="good"

compose() {
  docker compose -p "$PROJECT" -f "$FILE" "$@"
}

container_id() {
  compose ps -q "$1"
}

image_id() {
  docker inspect -f '{{.Image}}' "$1"
}

cleanup() {
  echo "Cleaning isolated laboratory..."
  LAB_APP_IMAGE="$PREVIOUS_IMAGE"
  LAB_WEB_IMAGE="$PREVIOUS_IMAGE"
  LAB_APP_HEALTH="good"
  export LAB_APP_IMAGE LAB_WEB_IMAGE LAB_APP_HEALTH

  compose down --volumes --remove-orphans
}

if [ -n "$(docker ps -aq \
  --filter "label=com.docker.compose.project=$PROJECT")" ]; then
  echo "FAIL: Existing laboratory containers detected"
  exit 1
fi

if docker volume inspect "${PROJECT}_lab_database" \
  >/dev/null 2>&1; then
  echo "FAIL: Existing laboratory volume detected"
  exit 1
fi

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "Preparing images..."
docker pull "$PREVIOUS_IMAGE"
docker pull "$CANDIDATE_IMAGE"

echo "Starting known-good release..."
compose up -d

DB_BEFORE=$(container_id db)
APP_BEFORE=$(container_id app)
WEB_BEFORE=$(container_id web)

test -n "$DB_BEFORE"
test -n "$APP_BEFORE"
test -n "$WEB_BEFORE"

PREVIOUS_APP_ID=$(image_id "$APP_BEFORE")
PREVIOUS_WEB_ID=$(image_id "$WEB_BEFORE")

docker exec "$DB_BEFORE" sh -c \
  'echo rollback-data-preserved > /data/marker.txt'

echo "Activating deliberately unhealthy candidate..."

export LAB_APP_IMAGE="$CANDIDATE_IMAGE"
export LAB_WEB_IMAGE="$CANDIDATE_IMAGE"
export LAB_APP_HEALTH="bad"

compose up -d \
  --no-deps \
  --no-build \
  --pull never \
  --force-recreate \
  app web

APP_CANDIDATE=$(container_id app)
WEB_CANDIDATE=$(container_id web)

CANDIDATE_APP_ID=$(image_id "$APP_CANDIDATE")
CANDIDATE_WEB_ID=$(image_id "$WEB_CANDIDATE")

test "$PREVIOUS_APP_ID" != "$CANDIDATE_APP_ID" || {
  echo "FAIL: Application image did not change"
  exit 1
}

test "$PREVIOUS_WEB_ID" != "$CANDIDATE_WEB_ID" || {
  echo "FAIL: Web image did not change"
  exit 1
}

echo "Checking unhealthy candidate..."

HEALTH="unknown"
ATTEMPT=0

while [ "$ATTEMPT" -lt 15 ]; do
  HEALTH=$(docker inspect -f \
    '{{.State.Health.Status}}' "$APP_CANDIDATE")

  if [ "$HEALTH" = "unhealthy" ]; then
    break
  fi

  ATTEMPT=$((ATTEMPT + 1))
  sleep 2
done

if [ "$HEALTH" != "unhealthy" ]; then
  echo "FAIL: Candidate health did not become unhealthy: $HEALTH"
  exit 1
fi

echo "PASS: Unhealthy candidate detected"

echo "Restoring recorded previous image pair..."

export LAB_APP_IMAGE="$PREVIOUS_IMAGE"
export LAB_WEB_IMAGE="$PREVIOUS_IMAGE"
export LAB_APP_HEALTH="good"

compose up -d \
  --no-deps \
  --no-build \
  --pull never \
  --force-recreate \
  app web

DB_AFTER=$(container_id db)
APP_AFTER=$(container_id app)
WEB_AFTER=$(container_id web)

test "$DB_BEFORE" = "$DB_AFTER" || {
  echo "FAIL: Database container identity changed"
  exit 1
}

test "$(image_id "$APP_AFTER")" = "$PREVIOUS_APP_ID" || {
  echo "FAIL: Previous application image was not restored"
  exit 1
}

test "$(image_id "$WEB_AFTER")" = "$PREVIOUS_WEB_ID" || {
  echo "FAIL: Previous web image was not restored"
  exit 1
}

echo "Waiting for restored application health..."

RESTORED_HEALTH="unknown"
ATTEMPT=0

while [ "$ATTEMPT" -lt 15 ]; do
  RESTORED_HEALTH=$(docker inspect -f \
    '{{.State.Health.Status}}' "$APP_AFTER")

  if [ "$RESTORED_HEALTH" = "healthy" ]; then
    break
  fi

  ATTEMPT=$((ATTEMPT + 1))
  sleep 2
done

test "$RESTORED_HEALTH" = "healthy" || {
  echo "FAIL: Restored application unhealthy: $RESTORED_HEALTH"
  exit 1
}

MARKER=$(docker exec "$DB_AFTER" cat /data/marker.txt)

test "$MARKER" = "rollback-data-preserved" || {
  echo "FAIL: Database data marker lost"
  exit 1
}

echo "PASS: Previous application image restored"
echo "PASS: Previous web image restored"
echo "PASS: Restored application healthy"
echo "PASS: Database container unchanged"
echo "PASS: Database data preserved"
echo "PASS: Isolated image rollback simulation"
