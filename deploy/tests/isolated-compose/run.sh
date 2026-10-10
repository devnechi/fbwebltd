#!/bin/sh
set -eu

PROJECT="fbweb-gate16f-lab"
FILE="deploy/tests/isolated-compose/compose.yml"

if [ -n "$(docker ps -aq \
  --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Existing lab containers detected"
    exit 1
fi

if docker volume inspect "${PROJECT}_lab_database" \
  >/dev/null 2>&1; then
    echo "FAIL: Existing lab volume detected"
    exit 1
fi

cleanup() {
  docker compose -p "$PROJECT" -f "$FILE" \
    down --volumes --remove-orphans
}

trap cleanup EXIT HUP INT TERM

echo "Starting isolated laboratory..."
docker compose -p "$PROJECT" -f "$FILE" \
  up -d

DB_BEFORE=$(docker compose -p "$PROJECT" -f "$FILE" ps -q db)
APP_BEFORE=$(docker compose -p "$PROJECT" -f "$FILE" ps -q app)
WEB_BEFORE=$(docker compose -p "$PROJECT" -f "$FILE" ps -q web)

test -n "$DB_BEFORE"
test -n "$APP_BEFORE"
test -n "$WEB_BEFORE"

docker exec "$DB_BEFORE" sh -c \
  'echo persistent-test-marker > /data/gate16f.txt'

echo "Recreating app and web only..."
docker compose -p "$PROJECT" -f "$FILE" \
  up --detach --no-deps --no-build \
  --pull never --force-recreate app web

DB_AFTER=$(docker compose -p "$PROJECT" -f "$FILE" ps -q db)
APP_AFTER=$(docker compose -p "$PROJECT" -f "$FILE" ps -q app)
WEB_AFTER=$(docker compose -p "$PROJECT" -f "$FILE" ps -q web)

test "$DB_BEFORE" = "$DB_AFTER" || {
  echo "FAIL: Database container changed"
  exit 1
}

test "$APP_BEFORE" != "$APP_AFTER" || {
  echo "FAIL: Application was not recreated"
  exit 1
}

test "$WEB_BEFORE" != "$WEB_AFTER" || {
  echo "FAIL: Web container was not recreated"
  exit 1
}

MARKER=$(docker exec "$DB_AFTER" \
  cat /data/gate16f.txt)

test "$MARKER" = "persistent-test-marker" || {
  echo "FAIL: Database volume marker lost"
  exit 1
}

echo "PASS: Database container identity unchanged"
echo "PASS: Application container recreated"
echo "PASS: Web container recreated"
echo "PASS: Database volume data preserved"
echo "PASS: Isolated Compose service-boundary test"
