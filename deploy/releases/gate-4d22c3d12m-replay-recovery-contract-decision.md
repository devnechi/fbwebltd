# Gate 4D.22C.3D.12M - Pure Protected Replay-State and Recovery Contracts

Status: LABORATORY CONTRACTS ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retries: DENIED
Production deployment: DISABLED
Operational replay-state authority: NOT IMPLEMENTED
Independently controlled replay witness: NOT IMPLEMENTED
Durable transactional state: NOT IMPLEMENTED
Independently provisioned trust anchors: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Translate Gate 3D.12L protected replay-state architecture
into immutable Python contracts and adversarial tests.

All inputs are caller-supplied.

All assessments are offline and non-authorizing.

The gate implements no persistence, external authority
adapters, database transactions, cryptographic signing,
network communication or operational recovery.

## 2. Existing Contracts

Gate 3D.12K defines ReplayLedgerSnapshot,
ChallengeRecord, RoleReceipt and their logical lifecycle.

Gate 3D.12M reuses their canonical untrusted checksum
and validation logic.

It must not alter the existing lifecycle module,
cryptographic verifier or authority trust-policy module.

## 3. Protected Replay Position

ReplayProtectedPosition contains:

- Registry identity.
- Replay-ledger identity.
- Format version.
- Ledger generation.
- Replay-ledger commitment.
- Policy epoch.
- Recovery epoch.
- Transition identifier.
- Previous protected-position commitment.

A generation-zero genesis declaration is permitted for
laboratory construction only.

An ordinary later generation must bind a nonzero
previous-position digest.

No caller-created genesis declaration is authenticated.

## 4. Witness Checkpoint

ReplayWitnessCheckpoint holds one protected position.

ReplayProtectedReadBundle contains the supplied ledger,
primary position and witness checkpoint.

Logical read validation compares their generations,
registry identities, ledger commitments and positions.

Equality is not evidence that the primary authority
and witness were independently controlled.

It does not establish an authenticated read.

## 5. Commitments

Replay-ledger commitments reuse the canonical Gate
3D.12K checksum format.

Protected-position and conditional-operation commitments
have separate SHA-256 domain prefixes.

The operation commitment binds:

- Expected protected-position digest.
- Candidate ledger commitment.
- Requested operation.
- Request identifier.
- Transition identifier.

These checksums are neither signatures nor MACs.

An attacker can fabricate matching records and hashes.

## 6. Conditional Transition Intent

ReplayConditionalTransitionIntent binds:

- Expected protected replay position.
- Expected witness checkpoint.
- Candidate replay ledger.
- Lifecycle operation.
- Request identifier.
- Transition identifier.
- Operation commitment.

It must reject stale expected positions, witness conflicts,
unchanged transition identifiers and generation gaps.

The candidate ledger must advance by exactly one
generation for an ordinary operation.

The policy and recovery epochs remain unchanged.

Key-policy rotations and emergency recovery require
separate approved protocols.

## 7. Request History Preservation

Ordinary transitions must preserve all unrelated requests.

The original request's challenge, purpose, policy epoch
and state generation must not be silently rebound.

RESERVE may add exactly one previously absent request.

ISSUE may transition RESERVED to ISSUED.

CONSUME may append exactly one new role receipt without
changing an earlier receipt.

COMPLETE requires all three expected role receipts.

EXPIRE, ABORT and UNCERTAIN may close an open request.

Ordinary transitions must never reactivate terminal requests.

This is logical validation, not authenticated response
verification or durable replay protection.

## 8. Split-Commit Reconciliation

A separate pure classifier evaluates supplied observations:

BOTH_PREVIOUS_UNTRUSTED
STATE_AHEAD_OF_WITNESS
WITNESS_AHEAD_OF_STATE
BOTH_PROPOSED_UNTRUSTED
CONFLICTING_OR_UNEXPECTED_POSITIONS
REPLAY_STATE_ROLLBACK_SUSPECTED
REPLAY_WITNESS_ROLLBACK_SUSPECTED
REPLAY_AUTHORITY_UNAVAILABLE
REPLAY_WITNESS_UNAVAILABLE
BOTH_AUTHORITIES_UNAVAILABLE

A positive structural match remains untrusted.

The classifier cannot authorize witness advancement,
recovery, automatic retries or application execution.

## 9. Crash and Recovery Boundary

A lost acknowledgement does not prove a failed commit.

A primary state ahead of its witness must fail closed.

A witness ahead of primary state must also fail closed.

A restored older database cannot establish currentness
using its own local hash history.

This implementation performs no automatic reconciliation
or replay-ledger repair.

## 10. Tests

Adversarial tests must verify:

- Valid and malformed protected positions.
- Genesis and non-genesis digest constraints.
- Ledger and witness agreement.
- Tampered ledger commitments.
- Conditional generation advancement.
- Stale expected positions.
- Incorrect operation commitments.
- Reused transition identifiers.
- Request-history preservation.
- Duplicate role-consumption rejection.
- Terminal request immutability.
- Split-commit classifications.
- Unavailable authority handling.
- Rolled-back position detection.
- Frozen non-authorizing assessments.

## 11. Deferred Operational Dependencies

Actual security guarantees require independently
provisioned authority identities, protected transactional
state, durable conditional commits, an independently
controlled forward-only witness, trusted time and
reviewed recovery authorizations.

The existing offline Ed25519 verifier and policy
continuity contracts do not satisfy those requirements.

## 12. Final Decision

Gate 3D.12M implements pure replay-state and recovery
contracts only.

It does not create a protected replay authority.

Docker execution, automatic retries and production
deployment remain blocked.
