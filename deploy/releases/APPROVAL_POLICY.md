# Future Basics — Production Release Approval Policy

## Status

Gate 4D.15 — approval-control design.

This document defines required controls. It does not grant
approval for any existing release.

## 1. Separation of duties

The deployment staging account (fbdeploy) is not authorized
to issue, install, modify, or revoke production approvals.

Production approval must be recorded through a separate
administrative process.

A GitHub Actions build, successful test, or valid signature
does not automatically authorize production deployment.

## 2. Required evidence

Before approval, the reviewer must verify:

- Release ID and repository.
- Exact Git commit and intended release branch.
- Successful CI test results.
- Laravel and Caddy immutable image digests.
- Cryptographically verified image attestations.
- Approved signing workflow and runner environment.
- Changes introduced by the proposed release.
- Production backup and recovery readiness.
- Rollback procedure and health-check criteria.

## 3. Authorization requirements

An approval record must contain:

- Release ID.
- Repository and source commit.
- Both immutable image references.
- Approval reference.
- Approver identity.
- Approval decision.
- Approval timestamp.
- Evidence references.

The authorization must originate from a trusted process
independent of the unprivileged staging account.

Approvals must be explicitly granted, not inferred from
a matching release manifest.

## 4. Protected storage

Trusted approvals belong under:

/etc/fbweb-deploy/approvals

Only an authorized administrator may install or modify them.

The directory must remain root-owned with restrictive
permissions.

Production controllers must not accept a caller-provided
approval directory.

## 5. Production activation

Approval does not itself execute deployment.

Activation also requires:

- Verified release images.
- A protected deployment controller.
- An available rollback image pair.
- Successful pre-deployment checks.
- A tested automatic rollback mechanism.
- Explicit authorization to activate the release.

MySQL data and persistent application volumes must remain
protected from application-image replacement operations.

## 6. Current release

Candidate: fbweb-23e0d1d-001

Status: PENDING REVIEW — NOT APPROVED.

No production activation is authorized by this document.
