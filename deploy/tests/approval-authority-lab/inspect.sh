#!/usr/bin/env bash
set -euo pipefail

REPO="devnechi/fbwebltd"
ENVIRONMENT="production"

echo "===== GATE 4D.21B: READ-ONLY AUTHORITY INSPECTION ====="

command -v gh >/dev/null || {
    echo "FAIL: GitHub CLI unavailable"
    exit 1
}

command -v python3 >/dev/null || {
    echo "FAIL: Python 3 unavailable"
    exit 1
}

echo "===== AUTHENTICATED ACCOUNT ====="
gh api user --jq '{login: .login, id: .id}'

echo "===== REPOSITORY IDENTITY ====="
gh api "repos/$REPO" \
    --jq '{
        full_name: .full_name,
        id: .id,
        private: .private,
        default_branch: .default_branch
    }'

echo "===== PRODUCTION ENVIRONMENT PROTECTION ====="

if ! ENV_JSON=$(gh api "repos/$REPO/environments/$ENVIRONMENT"); then
    echo "BLOCKED: Cannot independently inspect production environment"
    exit 1
fi

printf '%s' "$ENV_JSON" | python3 -c '
import json
import sys

data = json.load(sys.stdin)
rules = data.get("protection_rules") or []

print("Environment:", data.get("name"))
print("Prevent self-review:", data.get("prevent_self_review"))
print("Can admins bypass:", data.get("can_admins_bypass"))
print("Deployment branch policy:", json.dumps(
    data.get("deployment_branch_policy"), sort_keys=True
))

reviewers_found = False

for rule in rules:
    rule_type = rule.get("type")
    print("Protection rule:", rule_type)

    if rule_type == "required_reviewers":
        reviewers_found = True

        for reviewer in rule.get("reviewers") or []:
            entity = reviewer.get("reviewer") or {}

            print(
                "Required reviewer:",
                reviewer.get("type"),
                entity.get("login")
                or entity.get("slug")
                or entity.get("id")
            )

if not reviewers_found:
    print("WARNING: Required reviewer rule not established")

if data.get("prevent_self_review") is not True:
    print("WARNING: Self-review prevention not established")

if data.get("can_admins_bypass") is not False:
    print("WARNING: Administrator bypass restriction not established")
'

echo "===== PRODUCTION DEPLOYMENT RECORDS ====="

gh api "repos/$REPO/deployments?environment=$ENVIRONMENT&per_page=10" \
    --jq '[.[] | {
        id,
        ref,
        sha,
        creator: .creator.login,
        created_at,
        environment
    }]'

echo "===== DRAFT PULL REQUEST ====="

gh pr view 1 --repo "$REPO" \
    --json number,isDraft,state,baseRefName,headRefName \
    --jq '{
        number,
        isDraft,
        state,
        baseRefName,
        headRefName
    }'

echo "===== COMPLETED INSPECTION ====="
echo "No environment, deployment, or repository settings were modified."
echo "This report does not grant deployment authorization."
