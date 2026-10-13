# Gate 4D.22C.3D.12E - Pure Reconciliation Evaluator

Status: LABORATORY ONLY - NON-AUTHORIZING
Date: 2026-10-13

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Trusted state authority: NOT IMPLEMENTED
Independent rollback witness: NOT IMPLEMENTED
Trusted administrative provenance: NOT ESTABLISHED
Trusted time: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Implement a pure classifier for the failure and split-commit
scenarios defined by Gate 4D.22C.3D.12D.

The classifier compares caller-supplied observed transactional
state and rollback-witness positions against:

- The previous logical protected-state position.
- A proposed next position recomputed by Gate 3D.12C.
- Caller-reported transactional and witness outcomes.

No service is contacted and no state is committed.

## 2. Security Boundary

Observations and reported acknowledgements are untrusted.

The classifier cannot establish that the observations came
from genuine independent authorities.

Matching observations cannot prove durable state acceptance,
freshness, rollback resistance or execution authorization.

An acknowledged transaction is not necessarily durable.

An unknown or contradictory result must not be accepted.

## 3. Classification Contract

The supported classifications are:

BOTH_PREVIOUS:
Both observed authorities remain at the previous position.

STATE_AHEAD:
Transactional state reports the proposed position but
the witness remains at the previous position.

WITNESS_AHEAD:
The witness reports the proposed position but transactional
state remains at the previous position.

BOTH_PROPOSED_UNTRUSTED:
Both supplied observations match the proposed position.
This establishes logical agreement only.

AUTHORITY_UNAVAILABLE:
At least one required authority observation is absent,
unless an observed rollback or conflict has higher priority.

CONFLICTING_POSITION:
An observed position differs from both the previous
and proposed positions.

ROLLBACK_SUSPECTED:
An observed revision, generation, administrative-policy
epoch or recovery epoch is below the previous baseline.

TRANSITION_ID_CONFLICT:
An observed position reuses the proposed transition
identifier while binding different state content.

No classification means ACCEPTED or COMMITTED.

## 4. Validation

The implementation must reuse the existing pure protected
transition contract to recompute the proposed next state.

Observed state/history pairs must be complete and internally
consistent.

The revocation-history digest must match the observed state.

Witness positions must satisfy the protected-position schema.

Malformed supplied data must fail closed.

## 5. Report Handling

Caller-reported outcomes may be:

- NOT_ATTEMPTED
- ACKNOWLEDGED
- REJECTED
- UNKNOWN

Reports are only diagnostic hints.

An acknowledgement inconsistent with observed state is
flagged as a contradiction.

A rejected or unattempted operation observed at the
proposed position is also flagged as a contradiction.

UNKNOWN reports remain visibly uncertain.

Reports never override the position classification.

## 6. Failure and Recovery

The classifier must not automatically:

- Retry either operation.
- Advance a rollback witness.
- Roll back a witness.
- Commit transactional state.
- Restore a database backup.
- Perform bootstrap or emergency recovery.
- Authenticate authority identities.
- Grant execution or deployment permissions.

All operational decisions require future independently
authenticated and protected authority integrations.

## 7. Adversarial Testing

Tests must cover:

- Both authorities at previous and proposed positions.
- Each split-commit direction.
- Missing or malformed observations.
- Forged matching observations.
- Contradictory acknowledgements.
- Unknown outcomes.
- Stale generation and rollback indicators.
- Concurrent competing proposals.
- Transition identifier collisions.
- Revocation-history commitment mismatch.
- Immutable and mutation-free results.
- Explicit absence of authorization claims.

## 8. Acceptance

Gate 3D.12E may be reviewed when:

- The pure classifier is implemented.
- Existing protected-state contracts are reused.
- All new adversarial tests pass.
- The full repository security suite passes.
- No operational state service is introduced.
- Existing Docker and production restrictions remain.

Success authorizes an offline classification result only.

## 9. Final Decision

The classifier is a laboratory security-analysis component.

Even a BOTH_PROPOSED_UNTRUSTED result cannot be used
to authorize registry acceptance or runtime execution.

Independently authenticated reads, durability, freshness,
recovery and state/witness coordination remain future work.

Docker execution, automatic retries and production
deployment remain blocked.
