#!/bin/sh
set -eu

PROJECT=fbweb-gate18-diagnostic
COMPOSE=deploy/tests/application-readiness-lab/compose.yml

cd "$(dirname "$0")/../../.."

compose() {
    docker compose -p "$PROJECT" -f "$COMPOSE" "$@"
}

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Diagnostic containers already exist"
    exit 1
fi

if docker volume inspect "${PROJECT}_db_data" >/dev/null 2>&1; then
    echo "FAIL: Diagnostic database volume already exists"
    exit 1
fi

cleanup() {
    compose down -v --remove-orphans >/dev/null 2>&1 || true
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "===== START MYSQL ONLY ====="

compose up -d --no-deps db

echo "===== MYSQL STARTUP OBSERVATION ====="

attempt=0

while [ "$attempt" -lt 20 ]; do
    attempt=$((attempt + 1))

    CID=$(compose ps -q db)

    if [ -z "$CID" ]; then
        echo "FAIL: MySQL container missing"
        break
    fi

    STATUS=$(docker inspect \
      --format '{{.State.Health.Status}}' "$CID")

    RUNNING=$(docker inspect \
      --format '{{.State.Running}}' "$CID")

    printf 'Observation %s: running=%s health=%s\n' \
      "$attempt" "$RUNNING" "$STATUS"

    if [ "$STATUS" = "healthy" ]; then
        echo "PASS: MySQL health check became healthy"
        break
    fi

    if [ "$RUNNING" != "true" ]; then
        echo "FAIL: MySQL process exited"
        break
    fi

    sleep 3
done

echo "===== MYSQL LOGS ====="
compose logs --tail 100 db

echo "===== HEALTH CHECK HISTORY ====="

CID=$(compose ps -q db)

if [ -n "$CID" ]; then
    docker inspect \
      --format '{{json .State.Health}}' \
      "$CID"

    echo
    echo "===== DIRECT DATABASE CONNECTIVITY ====="

    compose exec -T db \
      sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -h 127.0.0.1 -uroot -N -e "SELECT 1"' \
      || echo "FAIL: Direct MySQL authentication/connectivity"
fi

echo "===== DIAGNOSTIC FINISHED ====="
