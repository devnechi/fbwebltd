#!/usr/bin/env python3
"""Read-only production approval policy. Always denies execution."""

from dataclasses import dataclass
import json
import re


REPOSITORY = "devnechi/fbwebltd"
ENVIRONMENT = "production"

FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ApprovalAssessment:
    environment_controls_valid: bool
    authorization_granted: bool
    reasons: tuple


def assess_environment(payload):
    """Inspect untrusted environment metadata without granting access."""
    reasons = []

    if not isinstance(payload, dict):
        raise ValueError("Environment response must be an object")

    if payload.get("name") != ENVIRONMENT:
        reasons.append("Unexpected environment identity")

    rules = payload.get("protection_rules")

    if not isinstance(rules, list):
        reasons.append("Environment protection rules unavailable")
        rules = []

    required_reviewers = [
        rule for rule in rules
        if isinstance(rule, dict)
        and rule.get("type") == "required_reviewers"
    ]

    if len(required_reviewers) != 1:
        reasons.append("Exactly one required-reviewers rule is required")
    else:
        rule = required_reviewers[0]
        reviewers = rule.get("reviewers")

        if not isinstance(reviewers, list) or not reviewers:
            reasons.append("Required reviewer identities unavailable")
        else:
            identities = []

            for entry in reviewers:
                if not isinstance(entry, dict):
                    reasons.append("Malformed reviewer entry")
                    continue

                reviewer_type = entry.get("type")
                reviewer = entry.get("reviewer")

                if reviewer_type not in ("User", "Team"):
                    reasons.append("Unrecognized reviewer type")
                    continue

                if not isinstance(reviewer, dict):
                    reasons.append("Reviewer identity missing")
                    continue

                identity = (
                    reviewer.get("login")
                    if reviewer_type == "User"
                    else reviewer.get("slug")
                )

                if not isinstance(identity, str) or not identity.strip():
                    reasons.append("Reviewer identity missing")
                    continue

                identities.append((reviewer_type, identity))

            if not identities:
                reasons.append("No usable reviewer identities")

            if len(identities) != len(set(identities)):
                reasons.append("Duplicate reviewer identities")

    if payload.get("prevent_self_review") is not True:
        reasons.append("Self-review prevention is not enforced")

    if payload.get("can_admins_bypass") is not False:
        reasons.append("Administrator bypass is not disabled")

    branch_policy = payload.get("deployment_branch_policy")

    if not isinstance(branch_policy, dict):
        reasons.append("Deployment branch policy unavailable")
    elif not (
        branch_policy.get("protected_branches") is True
        or branch_policy.get("custom_branch_policies") is True
    ):
        reasons.append("Deployment source restriction not established")

    return tuple(reasons)


def assess_release_authority(environment_payload, release_fingerprint):
    """Assess readiness; never transform metadata into authorization."""
    reasons = list(assess_environment(environment_payload))

    if (
        not isinstance(release_fingerprint, str)
        or FINGERPRINT_PATTERN.fullmatch(release_fingerprint) is None
    ):
        reasons.append("Invalid release intent fingerprint")

    controls_valid = len(reasons) == 0

    # No verified approval-evidence adapter exists yet.
    # In particular, environment metadata cannot prove an actual review.
    reasons.append(
        "No independently verified approval bound to this exact release"
    )

    return ApprovalAssessment(
        environment_controls_valid=controls_valid,
        authorization_granted=False,
        reasons=tuple(reasons),
    )


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--fingerprint", required=True)
    args = parser.parse_args()

    try:
        payload = json.load(sys.stdin)
        result = assess_release_authority(payload, args.fingerprint)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: Invalid authority evidence: {exc}")
        return 1

    print(f"Repository: {REPOSITORY}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Environment controls valid: {result.environment_controls_valid}")

    for reason in result.reasons:
        print(f"BLOCKED: {reason}")

    print("Authorization granted: false")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
