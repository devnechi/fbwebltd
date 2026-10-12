#!/bin/sh
set -eu

cd "$(dirname "$0")/../../.."

PROJECT=fbweb-gate18-lab
COMPOSE=deploy/tests/application-readiness-lab/compose.yml
APP_IMAGE='ghcr.io/devnechi/fbwebltd-app@sha256:cfea548abd17b2dd096bd896ab57d0bc5e9629344537e49e51fa0040d3feddcc'
WEB_IMAGE='ghcr.io/devnechi/fbwebltd-web@sha256:4f1b087069eafd9c6b95101a89143a4078e7f70cf7ed60d00fe02f4dbd9119fe'

compose() {
    docker compose -p "$PROJECT" -f "$COMPOSE" "$@"
}

echo "===== PREFLIGHT ====="

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory project already exists"
    exit 1
fi

if docker volume inspect "${PROJECT}_db_data" >/dev/null 2>&1; then
    echo "FAIL: Laboratory database volume already exists"
    exit 1
fi

if docker network inspect "${PROJECT}_internal" >/dev/null 2>&1; then
    echo "FAIL: Laboratory network already exists"
    exit 1
fi

for image in "$APP_IMAGE" "$WEB_IMAGE"; do
    docker image inspect "$image" >/dev/null || {
        echo "FAIL: Required application image missing"
        exit 1
    }
done

# Validate that the lab exposes no host ports.
if grep -Eq '^[[:space:]]+(ports:|network_mode:|privileged:)' "$COMPOSE"; then
    echo "FAIL: Forbidden laboratory Compose setting"
    exit 1
fi

# Confirm the existing application readiness implementation.
docker run --rm \
    --network none \
    --entrypoint /bin/sh \
    "$APP_IMAGE" \
    -c 'test -f deploy/health/check.sh && test -f deploy/health/readiness.php' \
    || {
        echo "FAIL: Published application image lacks readiness scripts"
        exit 1
    }

compose config -q

echo "PASS: Isolated Compose configuration"
echo "PASS: Published Laravel image contains readiness scripts"

cleanup() {
    echo "===== LABORATORY CLEANUP ====="
    if ! compose down --volumes --remove-orphans; then
        echo "WARNING: Cleanup encountered an error"
    fi
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "===== START MYSQL, LARAVEL AND CADDY ====="

compose up -d --pull missing --no-build --wait --wait-timeout 180

echo "===== VERIFY LARAVEL READINESS ====="

ready=0
attempt=0

while [ "$attempt" -lt 40 ]; do
    if compose exec -T app sh deploy/health/check.sh >/dev/null 2>&1; then
        ready=1
        break
    fi

    attempt=$((attempt + 1))
    sleep 2
done

if [ "$ready" -ne 1 ]; then
    echo "FAIL: Laravel/PHP-FPM/MySQL readiness"
    compose logs --tail 35 app db
    exit 1
fi

echo "PASS: PHP-FPM accepts connections"
echo "PASS: Laravel bootstrap and MySQL SELECT 1"

echo "===== VERIFY CADDY HTTP CONNECTIVITY ====="

# These tests run inside the private container, with no host port.
compose exec -T web \
    wget -q -O /dev/null http://127.0.0.1:8080/ \
    || {
        echo "FAIL: Public homepage HTTP request"
        compose logs --tail 40 web app
        exit 1
    }

echo "PASS: Real HTTP homepage request through Caddy and Laravel"

compose exec -T web \
    wget -q -O /dev/null http://127.0.0.1:8080/about \
    || {
        echo "FAIL: Public /about route"
        compose logs --tail 40 web app
        exit 1
    }

echo "PASS: Public /about route"

echo "===== NEGATIVE TEST: STOP DATABASE ====="

compose stop db

# The readiness probe must fail while MySQL is unavailable.
if compose exec -T app sh deploy/health/check.sh >/dev/null 2>&1; then
    echo "FAIL: Laravel falsely reported ready without MySQL"
    exit 1
fi

echo "PASS: Laravel readiness rejects unavailable MySQL"

echo "===== RESTORE DATABASE CONNECTIVITY ====="

compose start db

attempt=0
recovered=0

while [ "$attempt" -lt 40 ]; do
    if compose exec -T app sh deploy/health/check.sh >/dev/null 2>&1; then
        recovered=1
        break
    fi

    attempt=$((attempt + 1))
    sleep 2
done

if [ "$recovered" -ne 1 ]; then
    echo "FAIL: Laravel readiness did not recover"
    exit 1
fi

echo "PASS: Laravel readiness recovered after MySQL restart"

echo "===== VERIFY REAL HTTP AFTER DATABASE RECOVERY ====="

compose exec -T web \
    wget -q -O /dev/null http://127.0.0.1:8080/ \
    || {
        echo "FAIL: Homepage after database recovery"
        exit 1
    }

echo "PASS: Caddy-to-Laravel HTTP response after recovery"

echo "===== VERIFY LABORATORY BOUNDARIES ====="

if [ "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT" | grep -c .)" -ne 3 ]; then
    echo "FAIL: Unexpected laboratory container count"
    exit 1
fi

published=$(docker ps \
    --filter "label=com.docker.compose.project=$PROJECT" \
    --format '{{.Ports}}')

if printf '%s\n' "$published" | grep -Eq '(^|, | )([0-9.]+:)?[0-9]+->'; then
    echo "FAIL: Laboratory unexpectedly published host ports"
    exit 1
fi

echo "PASS: Exactly three isolated laboratory containers"
echo "PASS: No host ports published"
echo "===== GATE 4D.18 PASSED ====="
