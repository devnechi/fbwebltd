# Gate 4D.16 — Controlled Release and Rollback Contract

## Status

DESIGN ONLY — NOT AUTHORIZED FOR PRODUCTION EXECUTION.

## Objective

Activate an independently approved pair of immutable Laravel
and Caddy images while preserving production database,
persistent storage, secrets and recovery capability.

## Trust requirements

1. The release manifest must be schema-valid.
2. Both images must be pinned by SHA-256 digest.
3. Authorization must come from a trusted issuer.
4. Signed image provenance must match the approved source.
5. The controller must reject pending or unverified approvals.
6. The executable controller must be root-owned and installed
   through an independently reviewed process.

## Services permitted to change

- app
- web

## Services and resources forbidden to change

- db
- MySQL data volumes
- Laravel persistent storage volumes
- Caddy persistent data and configuration volumes
- Production secrets and environment files
- Database schema through automatic migrations

## Pre-activation requirements

1. Acquire an exclusive deployment lock.
2. Verify approval and immutable image identities.
3. Verify current production health.
4. Record the actual running app and web image identities.
5. Confirm the previous images are available for recovery.
6. Confirm fresh backup and recovery prerequisites.
7. Persist a recovery record before any service changes.

If a prerequisite fails, abort without changing services.

## Activation rules

Only the app and web services may be recreated.

Never execute unrestricted:

    docker compose up -d
    docker compose up -d --build
    docker compose up -d --remove-orphans

The execution adapter must explicitly address permitted services.

Image activation must not recreate or upgrade MySQL.

## Health acceptance

A candidate is successful only if all required checks pass:

1. Laravel application container is healthy.
2. Caddy serves the expected site.
3. The production HTTPS readiness endpoint succeeds.
4. The running app and web image identities match the candidate.
5. Checks succeed within a configured timeout.

## Rollback

On failed or timed-out activation:

1. Preserve failure details in the release journal.
2. Restore the recorded previous app/web image pair.
3. Recheck application and HTTPS health.
4. Record rollback completion or rollback failure.
5. Release the deployment lock.

Do not substitute mutable image tags for recorded image identities.

## Failure behavior

Missing recovery state: abort before activation.

Unverified approval: abort before activation.

Unhealthy candidate: attempt rollback.

Rollback failure: stop automatic changes, retain diagnostic
evidence and require manual incident response.

An interrupted deployment must be recoverable using the
durable journal and the recorded image identities.

## Implementation stages

A. Design and pure planning tests.
B. Restricted execution adapter.
C. Durable journal and interrupted-run recovery.
D. Isolated fault-injection tests.
E. Production readiness review.

No stage enables production deployment automatically.
