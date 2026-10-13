# Gate 4D.22C.3D.12C - Protected-State Contract Interfaces

Status: LABORATORY CONTRACT ONLY - NO OPERATIONAL AUTHORITY
Date: 2026-10-13

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Protected state service: NOT IMPLEMENTED
Rollback witness: NOT IMPLEMENTED
Independent administrative trust: NOT PROVISIONED
Trusted time: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Define typed, pure, non-authorizing interfaces to model protected
registry-state reads and proposed conditional transitions.

The selected Gate 3D.12B architecture prefers an independent
transactional authority and separately protected rollback witness.
Neither authority is implemented or authenticated by this gate.

## 2. State and Witness Records

ProtectedPosition includes the registry identity, wire version,
accepted revision, domain-separated registry signing digest,
generation, administrative policy epoch, recovery epoch,
revocation commitment and transition identifier.

WitnessCheckpoint refers to a protected position. In this gate,
its contents are caller-created data and are not trusted merely
because they match a state record.

RevocationHistorySnapshot retains the Gate 3D.11E tombstone format.
The revocation commitment uses the specified, separately domain-
separated SHA-256 digest of canonical sorted tombstone fields.

The digest proves neither completeness nor independent provenance.

## 3. Read Contract

A structurally valid ProtectedReadBundle must contain:

- A strictly validated protected position.
- A strictly validated witness position matching that position.
- Revocation history bound to the position's revision, signing
  digest and generation.
- A matching computed revocation-history commitment.

A consistent response is NOT an authenticated state read.
A coordinated attacker can forge mutually matching records.

Future state and witness adapters require separate authenticated
connections, identities, freshness guarantees and protected reads.

## 4. Transition Contract

ProtectedTransitionIntent supplies the observed expected position,
the immediately consecutive candidate revision, candidate signing
digest, proposed revocation history and a new transition identifier.

The evaluator rejects stale expected positions, skipped revisions,
malformed proposals, missing historical tombstones and status
regressions. Administrative policy and recovery epochs cannot be
changed through this ordinary proposal path.

The result is a frozen ProtectedTransitionAssessment with an
uncommitted next-position proposal and linked history snapshot.

The result does NOT mutate the caller's state or any authority.

## 5. Split Authority and Commit Semantics

Future transactional-state and rollback-witness provider protocols
are independent. The interface shapes do NOT prove that either
provider is genuine or securely administered.

A transactional state update and witness update are not assumed
to be atomic across two separate authorities.

The following conditions must deny operational acceptance:

- State advanced while witness remained stale.
- Witness advanced while transactional state remained stale.
- Competing updates expecting the same old generation.
- Lost commit response or indeterminate commit status.
- Authority unavailability or unverified state provenance.
- A state/witness match sourced from untrusted callers.

Future integration must define a recovery/reconciliation protocol
before any operational state-acceptance semantics are introduced.

## 6. Relationship to Existing Gates

Gate 3D.11B provides canonical signatures under caller-supplied
administrative keys. Gate 3D.11D enforces logical revision
continuity. Gate 3D.11E evaluates revocation history. Gate 3D.11F
combines those checks but does not authenticate state provenance.

This gate adds pure state-boundary data contracts only.
It does not replace or loosen any existing verification gate.

## 7. Adversarial Tests

Tests must include: malformed positions, boolean revision and epoch
values, stale expected positions, wrong digests, witness mismatch,
missing and regressed tombstones, forged matching records, competing
updates, state-only advancement, witness-only advancement, generation
exhaustion, immutable proposals and no execution claims.

In-memory simulations are not evidence of actual distributed
atomicity, authenticated reads, rollback resistance or durability.

## 8. Future Integration Requirements

A future operational adapter must separately establish:

- Independently verified administrative trust anchors.
- Genuine identity and provenance of both state and witness.
- Transactional conditional update semantics and strong consistency.
- A rollback-resistant witness with independently reviewed custody.
- Crash-safe coordination, reconciliation and disaster recovery.
- Trusted time and revocation publication guarantees.
- Protected audit and formal execution-authorization boundaries.

No operational adapter, credentials, database, network access,
Docker permission or production release is approved in this gate.
