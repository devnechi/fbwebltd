# Gate 4D.22C.3D.12K - Pure Challenge Lifecycle and Replay Classification

Status: LABORATORY CONTRACT ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Operational random challenge generation: NOT IMPLEMENTED
Protected replay-state service: NOT IMPLEMENTED
Durable challenge reservation: NOT IMPLEMENTED
Independent trust anchors: NOT PROVISIONED
Trusted time: NOT IMPLEMENTED
Operational replay prevention: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Implement the pure, offline request-lifecycle and replay
classification contracts defined by Gate 3D.12J.

The new functions operate exclusively on caller-supplied
immutable snapshots. They never read, write, reserve or
commit authoritative replay records.

No filesystem, network, database, random generator,
clock, service adapter or Docker operation is introduced.

## 2. Existing Dependencies

Gate 3D.12F provides the AuthorityReadChallenge and
AuthorityReadEvidence contracts.

Gate 3D.12H provides laboratory authority-signature
verification under caller-supplied public keys.

Gate 3D.12I provides logical authority trust-policy
continuity.

Gate 3D.12J defines the replay lifecycle architecture.

Gate 3D.12K remains independent of actual signing,
protected persistence, trusted time and operational trust.

## 3. Immutable Records

ReplayLedgerSnapshot contains a registry identifier,
a caller-supplied ledger generation and bounded request
records.

ChallengeRecord binds:

- AuthorityReadChallenge and purpose.
- Declared policy epoch and state generation.
- Request lifecycle state and local generation.
- Role-specific response receipts.

RoleReceipt records the declared role, response body
commitment and response envelope commitment.

These records are not signatures or authenticated logs.

## 4. Lifecycle

The logical lifecycle supports:

RESERVED -> ISSUED -> COLLECTING -> COMPLETE

A reserved, issued or collecting request may also become:

EXPIRED
ABORTED
UNCERTAIN

All three are terminal for ordinary processing.

The CREATED state exists as a caller-side request proposal.
No durable CREATED record is assumed.

An operational request would require independently durable
reservation before issuance.

## 5. Reservation

A pure assessment rejects reuse of request identifiers and
challenge values retained in the supplied ledger.

A successful assessment proposes a new immutable snapshot.

It does not reserve the request in real storage.

The challenge is caller-provided. Its unpredictability,
uniqueness outside the supplied ledger and secure generation
are not established.

## 6. Role-Specific Consumption

STATE, WITNESS and ADMIN receipts are tracked separately.

Each supplied response must match the expected request,
challenge, registry and authority label.

Its existing Gate 3D.12F body and envelope commitments
are recomputed.

The declared protected policy epoch and state generation
must agree with the request.

A repeated role response is classified as a duplicate.
Different content for an already consumed role is classified
as a conflicting role response.

The signatures and independent identities are not verified
by this pure lifecycle function.

## 7. Completion

Completion requires exactly the three role receipts.

A matching receipt set does not establish trusted freshness,
signature validity, independent authority provenance,
durable replay resistance or operational acceptance.

The completion assessment remains non-authorizing.

## 8. Concurrency

Every simulated reservation or request transition receives
the expected ledger generation.

Request transitions also receive the expected record
generation.

A mismatch is classified as a concurrency or stale-request
conflict rather than silently advancing a proposal.

This is not a real atomic compare-and-swap implementation.

Without protected storage, two callers may independently
produce conflicting snapshots from the same starting state.

## 9. Rollback Observation

A pure comparison identifies:

- Unavailable observed replay state.
- An observed lower ledger generation.
- Conflicting content at the same generation.
- Unverified forward movement.
- An unchanged, untrusted observation.

Both inputs are caller-supplied.

This classification does not provide a real monotonic
rollback witness.

## 10. Limits and Recovery

The laboratory snapshot is bounded to 128 request records.

Closed request identities remain recorded to prevent
logical reuse within that supplied snapshot.

A future operational design must separately address
retention, protected compaction, crash consistency,
persistent state, recovery and scaling.

No automatic retry or recovery is implemented.

Expiry is an explicitly requested simulated transition.
It is not calculated from a trusted clock.

## 11. Adversarial Tests

Tests must cover:

- Reservation before issue.
- Reused request identifiers and challenges.
- Missing reservation or unexpected issue.
- Correct receipt collection and completion.
- Wrong role, authority, registry, challenge or request.
- Invalid body and envelope commitments.
- Duplicate and conflicting role receipts.
- Policy epoch and state generation conflicts.
- Concurrent ledger and request-generation conflicts.
- Expired, aborted and uncertain terminal requests.
- Rolled-back, unavailable or conflicting ledger snapshots.
- Malformed caller-supplied snapshots.
- Immutable output and false operational trust claims.

## 12. Required Future Work

Operational replay prevention requires:

- Reviewed cryptographically secure challenge generation.
- Durable atomic challenge reservation.
- Authenticated authority-response verification.
- Independently trusted authority public keys.
- Protected role-consumption state.
- Crash-safe reconciliation.
- An independent anti-rollback mechanism.
- Trusted time or another approved freshness control.
- Separate runtime-isolation and execution approvals.

## 13. Final Decision

Gate 3D.12K authorizes only pure logical replay analysis.

Every successful lifecycle operation returns a proposed
snapshot, never a durable or authoritative state change.

Docker execution, automatic retries and production
deployment remain blocked.
