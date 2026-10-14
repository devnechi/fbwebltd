# Gate 4D.22C.3D.12O - Cryptographic Replay Authority Response Verification

Status: OFFLINE LABORATORY ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Independent replay trust roots: NOT PROVISIONED
Authenticated operational replay adapters: NOT IMPLEMENTED
Protected replay-ledger transactions: NOT IMPLEMENTED
Independent replay-witness service: NOT IMPLEMENTED
Secure operational challenge issuance: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Protected replay consumption: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Implement Gate 3D.12N's cryptographic read-response boundary for two
independent logical roles: REPLAY_STATE and REPLAY_WITNESS.

All public keys, key policy, expected authority labels, evidence and
assessment time are supplied by the caller. The verifier performs no I/O,
network calls, state writes, process execution or operational approvals.

## 2. Existing Dependencies

Gate 3D.12H defines Ed25519 verification for registry roles STATE,
WITNESS and ADMIN. Its signing keys and domains are NOT replay roles.

Gate 3D.12K supplies ReplayLedgerSnapshot and its non-authorizing checksum.

Gate 3D.12M supplies ReplayProtectedPosition, ReplayWitnessCheckpoint
and a domain-separated position checksum.

Gate 3D.12N specifies distinct replay response authentication rules.

No existing modules are changed by this gate.

## 3. Protocol Scope

Version 1 accepts POSITION_READ responses only. It does NOT interpret
signed messages as proofs of committed reservations, durable writes,
transition acknowledgements, witness advancement or authorized recovery.

Separate future gates must design and implement such acknowledgements.

## 4. Replay Read Challenge

A ReplayReadChallenge binds the registry, replay-ledger identifier,
request identity, 256-bit challenge representation, two expected replay
authority identities, policy and recovery epochs, and read purpose.

The supplied challenge's format is validated. Its unpredictability,
origin, reservation and one-time use are not established.

## 5. Separate Signing Domains

REPLAY_STATE and REPLAY_WITNESS use distinct versioned signature domains,
purposes and body-commitment domains.

Registry STATE, WITNESS and ADMIN signing contexts are incompatible with
replay authority signing contexts. Key-policy identifiers are separate.

Cryptographic domain separation prevents signature substitution but does
not prove independent operational key custody.

## 6. Evidence Bodies

REPLAY_STATE carries a ReplayStateReadBody with a replay ledger and its
protected-position declaration. The ledger checksum and generation
must match the position's declared values.

REPLAY_WITNESS carries a ReplayWitnessCheckpoint with its declared
protected position. A witness checkpoint is not independently trusted
merely because it is signed under a caller-provided key.

A role-specific body commitment covers the complete canonical body.

## 7. Signed Response Fields

Each SignedReplayResponse binds protocol version, signing role,
authority and key IDs, registry and ledger IDs, request and challenge,
read-only response status, body and protected-position commitments,
ledger digest, generation, policy epoch, recovery epoch, transition ID,
algorithm, purpose and Ed25519 signature.

The signing bytes exclude only the signature field.

## 8. Canonical Encoding

Signed objects use bounded UTF-8 canonical JSON: sorted object keys,
no insignificant whitespace, ASCII escaping, and deterministic numeric
fields. Duplicate keys, unknown fields, missing fields, invalid types,
unsupported algorithms, malformed signatures and noncanonical wire
bytes are rejected.

The canonical signature is 64 Ed25519 bytes represented as unpadded
base64url text.

## 9. Caller-Supplied Key Policy

The replay verification policy contains distinct role/purpose bindings,
public keys, key IDs, statuses and declared validity intervals.

The policy rejects duplicate key identities and reused key material
across replay roles. Revoked or disabled keys cannot verify responses.

The verifier uses caller-provided assessment time only to evaluate
the caller-provided key interval. It does NOT establish trusted time,
authenticated policy approval or currently authorized trust roots.

## 10. Verification Order

The pure verifier validates the challenge and supplied policy, checks
request and role-specific evidence, rechecks body and position
commitments, selects the declared key, checks its declared active
window, and verifies the Ed25519 signature under that key.

A mismatch raises ValueError. No execution decision is returned.

## 11. Reconciliation Output

Signed but untrusted primary/witness positions are classified as:

- MATCHING_UNTRUSTED
- REPLAY_STATE_AHEAD_UNTRUSTED
- REPLAY_WITNESS_AHEAD_UNTRUSTED
- CONFLICTING_UNTRUSTED

These are comparisons of caller-supplied observations, not proof of
currentness or of atomic two-authority commits.

## 12. Security Limitations

A valid signature under caller-supplied keys is insufficient to prove:

- Independent authority identity or key provenance.
- Current administrative approval or key-policy currentness.
- Protected challenge generation or replay prevention.
- Independently trusted time or expiry.
- Durable primary ledger commits or witness updates.
- Rollback-resistant storage or recovered state.
- Runtime isolation, Docker execution or production permission.

Every corresponding operational trust flag remains false.

## 13. Adversarial Validation

The tests cover valid signatures, corrupted signatures, role and
purpose substitution, registry/ledger/request/challenge binding,
position and ledger commitments, malformed canonical JSON, duplicate
keys, key revocation, declared time windows, stale positions and split
primary/witness reports.

Tests generate ephemeral Ed25519 key pairs solely in process memory.
They do not provision or operate real authority signing keys.

## 14. Deferred Gates

The next architecture review must cover independently provisioned replay
trust-policy roots, protected key rotation, freshness provenance and
authenticated read/commit acknowledgement semantics before any operational
replay-state service is introduced.

## 15. Final Decision

Gate 3D.12O authorizes offline cryptographic response analysis only.
Docker execution, automatic retries and production deployment remain
blocked. No protected replay-state authority has been implemented.
