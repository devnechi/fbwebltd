# Future Basics CI/CD — Production Readiness Assessment

**Gate:** 4D.17
**Date:** 2026-10-12
**Branch:** feature/docker-cicd-deployment
**Production status:** BLOCKED
**Production deployment workflow:** Intentionally disabled
**Pull request #1:** Must remain draft and unmerged

## 1. Executive Decision

The CI/CD pipeline and restricted laboratory rollback mechanism have
successfully demonstrated image publication, bounded rollback execution,
durable attempt persistence, database container preservation and recovery
from several abrupt controller-interruption scenarios.

These results establish laboratory recovery behavior, not authorization
or sufficient evidence for production deployment.

Production deployment MUST remain disabled until all mandatory release
gates below are completed, independently reviewed and approved.

## 2. Verified Evidence

### 2.1 CI and Image Publication

Current GitHub Actions workflow:

- Validates PHP syntax.
- Installs locked Composer dependencies.
- Executes Laravel tests against isolated SQLite.
- Runs Python recovery security tests.
- Builds and publishes application and web images to GHCR.
- Generates image attestations.
- Records immutable image references.
- Leaves the production deploy job disabled.

Independent consumption and verification of the exact release
attestations is not yet integrated into a production deployment gate.

### 2.2 Laboratory Rollback

Demonstrated laboratory behaviors:

- Restoration of pinned previous application and web images.
- Database container identity preservation.
- Laboratory volume marker preservation.
- Durable bound STARTED attempts.
- SUCCEEDED persistence and ROLLED_BACK journal completion.
- Idempotent completion.
- Duplicate restoration prevention.
- Recovery after actual controller SIGKILL.
- Observation of Compose continuing after controller SIGKILL.

These tests use restricted laboratory containers with synthetic
health checks and a simulated database marker.

They do not prove MySQL data recovery or application-level correctness.

### 2.3 Current Application Health Components

Existing:

- deploy/health/check.sh
- deploy/health/readiness.php
- deploy/Caddyfile

The Laravel readiness implementation checks:

1. PHP-FPM connectivity.
2. Laravel bootstrap.
3. Database connectivity using SELECT 1.

These checks should be tested in a production-like environment.

A read-only HTTPS smoke test and real Caddy-to-Laravel request test
are still required.

## 3. Mandatory Production Blockers

### P0-01: Real Application Readiness

Required evidence:

- PHP-FPM responds.
- Laravel bootstrap succeeds.
- Database connection works.
- Caddy can proxy a real HTTP request to PHP-FPM.
- HTTPS response is valid.
- Critical public routes work.
- Error logs do not reveal sensitive information.
- Readiness failure blocks release completion.

Testing must use the actual application entrypoint, not a shell
command that always returns success.

### P0-02: Database Backup and Restore

Required evidence:

- Consistent MySQL backup from an isolated test environment.
- Backup integrity verification.
- Actual restore into a disposable database instance.
- Tables and representative data verified after restoration.
- Documented recovery-point and recovery-time measurements.
- Explicit handling of schema compatibility and migrations.
- Database volume never destroyed by an application rollback.

Existing database-marker tests do not satisfy this requirement.

### P0-03: Image Provenance Verification

Required evidence:

- Immutable app and web image digests.
- Attestation subject-digest match.
- Expected repository and workflow identity.
- Expected Git commit and protected release source.
- Verified provenance before deployment authorization.
- Rejection of unsigned or mismatched image pairs.

A successful CI build is not itself release approval.

### P0-04: Independent Release Approval

Required evidence:

- Named authorized approver.
- Recorded decision bound to the immutable release pair.
- Approved maintenance window.
- Approved rollback destination.
- Independent authorization separate from a Python fixture flag.
- Audit trail for authorization and execution.

Laboratory ReleasePlan booleans do not constitute production approval.

### P0-05: Crash and In-flight Operation Supervision

Required evidence:

- Tracking of restoration subprocesses and relevant process groups.
- Safe recovery when Compose exits but Docker operations remain pending.
- No concurrent conflicting deployment activity.
- Durable attempt-to-operation binding.
- No blind retry after controller termination.
- Defined operator escalation on ambiguous container state.

A terminated Compose PID alone does not prove that all Docker
daemon-side activity has finished.

### P0-06: Runtime and Dependency Support

Current repository includes a PHP 8.1-based container and Laravel 8.

Required evidence:

- Supported runtime and framework upgrade plan.
- Dependency vulnerability assessment.
- Verified compatibility and regression testing.
- Defined security exception process for any temporary legacy runtime.

Legacy runtime risk is not resolved by containerization alone.

### P0-07: Production Configuration and Secrets

Required evidence:

- Production secrets never committed to Git.
- No secret values included in image layers or CI logs.
- Environment variables validated.
- Correct trusted proxy and TLS configuration.
- Secure storage and restricted access for database credentials.
- Appropriate application-key backup and recovery.
- Production-specific volume, filesystem and permission review.

The production.env.example file is a template, not proof that live
configuration is secure.

## 4. Deployment Decision Matrix

| Gate | Mandatory | Current decision |
| --- | --- | --- |
| CI and image publication | Yes | Laboratory/CI verified |
| Real application readiness | Yes | OPEN |
| Actual database restore | Yes | OPEN |
| Independent provenance verification | Yes | OPEN |
| Independent release approval | Yes | OPEN |
| Crash supervision hardening | Yes | OPEN |
| Runtime and dependency security | Yes | OPEN |
| Production configuration review | Yes | OPEN |

**Production release authorization: DENIED pending completion of the
mandatory open gates.**

## 5. Recommended Implementation Sequence

1. Validate the existing Laravel/PHP-FPM readiness probe.
2. Build a disposable Caddy-to-Laravel smoke-test environment.
3. Add application-level failure-injection tests.
4. Rehearse actual MySQL backup and restoration.
5. Implement independent image-attestation verification.
6. Harden in-flight Docker operation supervision.
7. Resolve or formally assess legacy framework/runtime risks.
8. Review production configuration, secrets and permissions.
9. Produce an independently approved release and rollback runbook.
10. Reassess production readiness before any change to the disabled
    GitHub Actions deploy job.

## 6. Explicitly Prohibited Actions

Until a separate approval is recorded:

- Do not enable the production deploy job.
- Do not merge draft pull request #1.
- Do not invoke the recovery executor against production.
- Do not alter production MySQL volumes.
- Do not run unreviewed production migrations.
- Do not substitute laboratory mock health checks for readiness.
- Do not treat image signatures as deployment authorization.

## 7. Closure Criteria

This assessment may be closed only when every mandatory gate has:

- Reproducible test evidence.
- An immutable source-code revision.
- Recorded test outcome.
- Security review.
- Explicit independent approval where required.

Successful laboratory tests alone cannot close production readiness.
