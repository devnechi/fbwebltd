#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

REPO="devnechi/fbwebltd"
ENVIRONMENT="production"

if [[ $# -ne 1 ]]; then
    echo "Usage: bash $0 RELEASE_FINGERPRINT" >&2
    exit 2
fi

FINGERPRINT="$1"

if [[ ! "$FINGERPRINT" =~ ^[0-9a-f]{64}$ ]]; then
    echo "BLOCKED: Invalid release fingerprint"
    exit 1
fi

command -v gh >/dev/null || {
    echo "BLOCKED: GitHub CLI missing"
    exit 1
}

command -v python3 >/dev/null || {
    echo "BLOCKED: Python 3 missing"
    exit 1
}

echo "===== LIVE GITHUB ENVIRONMENT INSPECTION ====="

if ! RESPONSE=$(gh api "repos/$REPO/environments/$ENVIRONMENT"); then
    echo "BLOCKED: Cannot fetch trusted environment metadata"
    exit 1
fi

echo "===== RELEASE AUTHORIZATION ASSESSMENT ====="

printf '%s' "$RESPONSE" |
    PYTHONDONTWRITEBYTECODE=1 python3 \
      deploy/releases/approval_authority_policy.py \
      --fingerprint "$FINGERPRINT"
