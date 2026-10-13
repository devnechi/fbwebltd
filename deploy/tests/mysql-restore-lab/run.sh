#!/bin/sh
set -eu

cd "$(dirname "$0")/../../.."

PROJECT=fbweb-gate19-lab
COMPOSE=deploy/tests/mysql-restore-lab/compose.yml
WORK=$(mktemp -d)

compose() {
    docker compose -p "$PROJECT" -f "$COMPOSE" "$@"
}

OWNED=0

cleanup() {
    echo "===== CLEANUP ====="
    if [ "$OWNED" -eq 1 ]; then
        compose down --volumes --remove-orphans >/dev/null 2>&1 || \
            echo "WARNING: Docker cleanup failed"
    fi
    rm -rf "$WORK"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

fail() {
    echo "FAIL: $1"
    exit 1
}

query() {
    service=$1
    sql=$2

    compose exec -T "$service" sh -c \
        'MYSQL_PWD="$MYSQL_PASSWORD" exec mysql -h 127.0.0.1 -u"$MYSQL_USER" -D "$MYSQL_DATABASE" -N -B -e "$1"' \
        sh "$sql"
}

wait_for_mysql() {
    service=$1
    count=0

    echo "===== WAIT FOR $service MYSQL ====="

    while [ "$count" -lt 90 ]; do
        if query "$service" 'SELECT 1' >/dev/null 2>&1; then
            echo "PASS: $service MySQL accepts SQL connections"
            return 0
        fi

        count=$((count + 1))
        sleep 5
    done

    compose logs --tail 60 "$service"
    fail "$service MySQL startup deadline exceeded"
}

snapshot() {
    service=$1
    destination=$2

    {
        echo "CLIENTS"
        query "$service" \
            'SELECT id, client_code, full_name, status FROM clients ORDER BY id'

        echo "PAYMENTS"
        query "$service" \
            'SELECT id, client_id, amount, reference_code FROM payments ORDER BY id'
    } > "$destination"
}

echo "===== PREFLIGHT ====="

command -v docker >/dev/null 2>&1 || fail "Docker unavailable"
command -v sha256sum >/dev/null 2>&1 || fail "sha256sum unavailable"

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    fail "Existing laboratory containers detected"
fi

for volume in "${PROJECT}_source_data" "${PROJECT}_restore_data"; do
    if docker volume inspect "$volume" >/dev/null 2>&1; then
        fail "Existing laboratory volume detected: $volume"
    fi
done

if docker network inspect "${PROJECT}_internal" >/dev/null 2>&1; then
    fail "Existing laboratory network detected"
fi

if grep -Eq '^[[:space:]]+(ports:|network_mode:|privileged:)' "$COMPOSE"; then
    fail "Forbidden Compose setting"
fi

compose config -q

echo "PASS: Disposable MySQL laboratory validated"

echo "===== START SOURCE DATABASE ====="

OWNED=1
compose up -d --no-deps --pull missing source
wait_for_mysql source

echo "===== CREATE REPRESENTATIVE TEST DATA ====="

compose exec -T source sh -c \
    'MYSQL_PWD="$MYSQL_PASSWORD" exec mysql -h 127.0.0.1 -u"$MYSQL_USER" -D "$MYSQL_DATABASE"' \
    <<'SQL'
CREATE TABLE clients (
    id INT NOT NULL PRIMARY KEY,
    client_code VARCHAR(30) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE payments (
    id INT NOT NULL PRIMARY KEY,
    client_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    reference_code VARCHAR(30) NOT NULL UNIQUE,
    CONSTRAINT fk_payment_client
        FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB;

START TRANSACTION;

INSERT INTO clients
    (id, client_code, full_name, status)
VALUES
    (1, 'FB-001', 'Amani Testing', 'ACTIVE'),
    (2, 'FB-002', 'Neema Example', 'ACTIVE'),
    (3, 'FB-003', 'Juma Rehearsal', 'INACTIVE');

INSERT INTO payments
    (id, client_id, amount, reference_code)
VALUES
    (1, 1, 150000.50, 'PAY-001'),
    (2, 1, 82500.00, 'PAY-002'),
    (3, 2, 400000.75, 'PAY-003'),
    (4, 3, 10000.00, 'PAY-004');

COMMIT;
SQL

client_count=$(query source 'SELECT COUNT(*) FROM clients')
payment_count=$(query source 'SELECT COUNT(*) FROM payments')

[ "$client_count" = "3" ] || fail "Unexpected source client count"
[ "$payment_count" = "4" ] || fail "Unexpected source payment count"

echo "PASS: Three client records and four payment records inserted"

echo "===== CREATE CONSISTENT MYSQL BACKUP ====="

compose exec -T source sh -c \
    'MYSQL_PWD="$MYSQL_PASSWORD" exec mysqldump \
      -h 127.0.0.1 \
      -u"$MYSQL_USER" \
      --single-transaction \
      --quick \
      --no-tablespaces \
      --set-gtid-purged=OFF \
      --default-character-set=utf8mb4 \
      "$MYSQL_DATABASE"' \
    > "$WORK/source.sql"

[ -s "$WORK/source.sql" ] || fail "SQL backup is empty"

grep -q 'CREATE TABLE `clients`' "$WORK/source.sql" || \
    fail "Clients table missing from backup"

grep -q 'CREATE TABLE `payments`' "$WORK/source.sql" || \
    fail "Payments table missing from backup"

backup_hash=$(sha256sum "$WORK/source.sql" | awk '{print $1}')

echo "PASS: Consistent logical SQL backup created"
echo "Backup SHA-256: $backup_hash"

snapshot source "$WORK/source-records.txt"

source_hash=$(sha256sum "$WORK/source-records.txt" | awk '{print $1}')

echo "PASS: Source records captured for comparison"

echo "===== START INDEPENDENT RESTORE DATABASE ====="

compose up -d --no-deps --pull missing restore
wait_for_mysql restore

echo "===== RESTORE THE SQL BACKUP ====="

compose exec -T restore sh -c \
    'MYSQL_PWD="$MYSQL_PASSWORD" exec mysql \
      -h 127.0.0.1 \
      -u"$MYSQL_USER" \
      -D "$MYSQL_DATABASE"' \
    < "$WORK/source.sql"

echo "PASS: SQL backup restored successfully"

echo "===== VERIFY RESTORED DATA ====="

snapshot restore "$WORK/restored-records.txt"

restore_hash=$(sha256sum "$WORK/restored-records.txt" | awk '{print $1}')

[ "$source_hash" = "$restore_hash" ] || \
    fail "Restored records do not match source"

cmp "$WORK/source-records.txt" "$WORK/restored-records.txt" || \
    fail "Canonical source and restored records differ"

restored_clients=$(query restore 'SELECT COUNT(*) FROM clients')
restored_payments=$(query restore 'SELECT COUNT(*) FROM payments')

[ "$restored_clients" = "3" ] || \
    fail "Incorrect restored client count"

[ "$restored_payments" = "4" ] || \
    fail "Incorrect restored payment count"

echo "PASS: Client record counts match"
echo "PASS: Payment record counts match"
echo "PASS: Restored records match source byte-for-byte"
echo "PASS: Source and restore SHA-256 checksums match"

echo "===== VERIFY FOREIGN KEY INTEGRITY ====="

orphans=$(query restore \
    'SELECT COUNT(*) FROM payments p LEFT JOIN clients c ON c.id = p.client_id WHERE c.id IS NULL')

[ "$orphans" = "0" ] || fail "Orphan payment records detected"

echo "PASS: Payment-to-client foreign key relationships preserved"

echo "===== CORRUPTED BACKUP NEGATIVE TEST ====="

cp "$WORK/source.sql" "$WORK/corrupt.sql"

# Append invalid SQL to guarantee that the file is rejected.
printf '\nINVALID_BACKUP_STATEMENT;\n' >> "$WORK/corrupt.sql"

# Use a separate throwaway schema. Never corrupt the verified restore.
compose exec -T restore sh -c \
    'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql \
      -h 127.0.0.1 -uroot \
      -e "CREATE DATABASE fbweb_corrupt_test"' \
    || fail "Could not create disposable negative-test database"

if compose exec -T restore sh -c \
    'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql \
      -h 127.0.0.1 -uroot \
      --database=fbweb_corrupt_test' \
    < "$WORK/corrupt.sql" > "$WORK/corrupt.stdout" 2> "$WORK/corrupt.stderr"
then
    fail "Corrupted SQL backup was incorrectly accepted"
fi

echo "PASS: Corrupted SQL restore returned a nonzero exit status"

# The previously verified restore must remain intact.
snapshot restore "$WORK/verified-after-negative-test.txt"

after_hash=$(sha256sum "$WORK/verified-after-negative-test.txt" | awk '{print $1}')

[ "$after_hash" = "$source_hash" ] || \
    fail "Negative test changed the verified restoration"

echo "PASS: Verified restore remains unchanged after negative test"

echo "===== VERIFY LABORATORY BOUNDARIES ====="

containers=$(docker ps -aq \
    --filter "label=com.docker.compose.project=$PROJECT" | grep -c .)

[ "$containers" -eq 2 ] || fail "Unexpected laboratory container count"

ports=$(docker ps \
    --filter "label=com.docker.compose.project=$PROJECT" \
    --format '{{.Ports}}')

if printf '%s\n' "$ports" | grep -q -- '->'; then
    fail "Laboratory published a host port"
fi

echo "PASS: Exactly two laboratory database containers"
echo "PASS: No host ports published"

echo "===== REMOVE LABORATORY RESOURCES ====="

compose down --volumes --remove-orphans || \
    fail "Docker Compose cleanup failed"

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    fail "Laboratory containers remain"
fi

for volume in "${PROJECT}_source_data" "${PROJECT}_restore_data"; do
    if docker volume inspect "$volume" >/dev/null 2>&1; then
        fail "Laboratory volume remains: $volume"
    fi
done

if docker network inspect "${PROJECT}_internal" >/dev/null 2>&1; then
    fail "Laboratory network remains"
fi

echo "PASS: Containers, network and database volumes cleaned"
echo "===== GATE 4D.19 PASSED ====="
