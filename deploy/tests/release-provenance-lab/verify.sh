#!/usr/bin/env bash
set -euo pipefail

REPO="devnechi/fbwebltd"
SOURCE_REF="refs/heads/master"
WORKFLOW="devnechi/fbwebltd/.github/workflows/deploy.yml"

APP_NAME="ghcr.io/devnechi/fbwebltd-app"
WEB_NAME="ghcr.io/devnechi/fbwebltd-web"

usage() {
    echo "Usage:"
    echo "  bash $0 COMMIT_SHA APP_DIGEST WEB_DIGEST"
    echo
    echo "All values must identify the same reviewed release."
    echo "COMMIT_SHA: full 40-character Git commit"
    echo "DIGEST: sha256:<64 lowercase hexadecimal characters>"
}

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

if [[ $# -ne 3 ]]; then
    usage
    exit 2
fi

COMMIT_SHA="$1"
APP_DIGEST="$2"
WEB_DIGEST="$3"

[[ "$COMMIT_SHA" =~ ^[0-9a-f]{40}$ ]] || \
    fail "Expected full 40-character commit SHA"

[[ "$APP_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]] || \
    fail "Invalid application image digest"

[[ "$WEB_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]] || \
    fail "Invalid web image digest"

command -v gh >/dev/null || fail "GitHub CLI unavailable"
command -v python3 >/dev/null || fail "Python 3 unavailable"

echo "===== FUTURE BASICS RELEASE PROVENANCE ====="
echo "Repository: $REPO"
echo "Commit: $COMMIT_SHA"
echo "Source ref: $SOURCE_REF"

REMOTE_SHA=$(
    gh api "repos/$REPO/commits/$COMMIT_SHA" --jq '.sha'
)

[[ "$REMOTE_SHA" == "$COMMIT_SHA" ]] || \
    fail "Expected commit does not exist in the trusted repository"

verify_image() {
    local name="$1"
    local digest="$2"
    local label="$3"
    local image="oci://${name}@${digest}"
    local result

    echo "===== VERIFY $label ====="

    if ! result=$(
        gh attestation verify "$image" \
          --repo "$REPO" \
          --signer-workflow "$WORKFLOW" \
          --source-ref "$SOURCE_REF" \
          --source-digest "$COMMIT_SHA" \
          --deny-self-hosted-runners \
          --format json
    ); then
        fail "$label attestation verification failed"
    fi

    if ! printf '%s' "$result" |
        python3 -c '
import json
import sys

try:
    data = json.load(sys.stdin)
except (ValueError, TypeError):
    sys.exit(1)

if not isinstance(data, list) or len(data) < 1:
    sys.exit(1)

expected_name, expected_digest = sys.argv[1:3]
found = False

for item in data:
    statement = (
        item.get("verificationResult", {})
        .get("statement", {})
    )

    for subject in statement.get("subject", []):
        digest = subject.get("digest", {})
        if (
            subject.get("name") == expected_name
            and digest.get("sha256") ==
                expected_digest.removeprefix("sha256:")
        ):
            found = True

if not found:
    sys.exit(1)
' "$name" "$digest"
    then
        fail "$label verified statement lacks exact subject digest"
    fi

    echo "PASS: $label attestation verified"
    echo "PASS: Expected workflow and master source verified"
    echo "PASS: Exact image digest verified"
}

verify_image "$APP_NAME" "$APP_DIGEST" "LARAVEL APPLICATION"
verify_image "$WEB_NAME" "$WEB_DIGEST" "CADDY WEB"

echo "===== RELEASE PAIR VERIFICATION ====="
echo "PASS: Both images match the required Git commit"
echo "PASS: Both image attestations were verified"
echo "PASS: Both immutable image digests were verified"
echo "Production deployment is not authorized by this verification."
