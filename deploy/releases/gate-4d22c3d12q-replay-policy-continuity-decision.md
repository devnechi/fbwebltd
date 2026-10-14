# Gate 4D.22C.3D.12Q - Pure Replay Trust-Policy Continuity and Revocation

Status: OFFLINE LABORATORY ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retries: DENIED
Production deployment: DISABLED
Independent replay trust roots: NOT PROVISIONED
Independent policy issuer authentication: NOT IMPLEMENTED
Protected policy storage: NOT IMPLEMENTED
Independent policy rollback witness: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Durable replay-state service: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Implement pure, immutable replay trust-policy continuity and revocation
contracts following Gate 3D.12P. All policy snapshots, key records,
approval references, authority labels and witness positions are caller
supplied. Structural consistency alone cannot create trust.

## 2. Existing Contracts

Gate 3D.12I provides the analogous offline registry-role policy model.
Gate 3D.12O supplies ReplayResponseKey, ReplayResponseKeyPolicy,
ReplayReadChallenge and the role-separated Ed25519 response verifier.
Gate 3D.12P defines the architecture for independently approved replay
trust roots, protected policy history and recovery.

This gate does not modify existing modules or provision trust roots.

## 3. Snapshot Schema

ReplayPolicySnapshot contains the registry and replay-ledger identities,
format and policy versions, policy epoch, protected policy generation,
recovery epoch, prior snapshot checksum, transition identifier, pinned
policy issuer, declared approval reference, two pinned replay authority
identities and the complete ReplayResponseKeyPolicy.

The embedded ReplayResponseKeyPolicy epoch must equal the snapshot epoch.
The issuer ID and approval reference are labels, NOT verified approvals.

## 4. Genesis Boundary

The logical genesis is epoch 1, generation 1, recovery epoch at least 1,
with an all-zero previous commitment. A non-genesis snapshot cannot use
the all-zero predecessor digest.

Valid genesis shape is NOT authorization to bootstrap trust roots.
No automatic trust-on-first-use mechanism is implemented.

## 5. Canonical Key Policy

The key tuple must be sorted by (role, authority_id, key_id). Both
REPLAY_STATE and REPLAY_WITNESS must have at least one declared active
key. Every key must retain its pinned authority identity and the signing
purpose defined in Gate 3D.12O.

Duplicate signing-key IDs and reused key material are rejected. The
32-record bound is a laboratory limit, not operational retention policy.

## 6. Ordinary Policy Transitions

A permitted ordinary transition:

1. Advances both policy epoch and generation by exactly one.
2. Preserves registry, ledger, format, policy ID and recovery epoch.
3. Preserves both replay authority role identities and the issuer ID.
4. Uses a new transition identifier and approval reference.
5. Commits to the complete previous policy snapshot checksum.
6. Preserves all earlier key identities and immutable key metadata.
7. Adds at least one key or changes an existing key lifecycle state.
8. Does not claim to authenticate the issuer or approve the transition.

A declared approval reference cannot replace independent approval proof.

## 7. Key Lifecycle and History

The ordinary lifecycle permits:

- active -> active, disabled, revoked
- disabled -> disabled, revoked
- revoked -> revoked only

Existing role, authority, key ID, public key, algorithm, purpose and
validity interval may not change. A replacement requires a new key ID
and new public key material. History cannot be deleted or reactivated.
New keys must begin in the active state.

A future operational system must preserve revocation history across
compaction, backup restoration and recovery.

## 8. Local Commitments

Policy snapshot commitments use domain-separated SHA-256 over deterministic
canonical JSON encoding. The previous digest forms a logical chain only.

An attacker may create a consistent forged chain and corresponding digest.
No checksum in this gate authenticates policy provenance or currentness.

## 9. Replay Binding

A pure helper compares a supplied policy snapshot with a supplied
ReplayReadChallenge and ReplayProtectedPosition. Registry, ledger, policy
and recovery epochs and the two replay authority identifiers must agree.

Matching declarations do not prove independently trusted authorities,
proper challenge reservation, secure randomness or protected state.

## 10. Untrusted Policy Witness

ReplayPolicyCheckpoint contains the policy identity, policy epoch,
generation, recovery epoch and policy commitment. It is a caller-created
logical checkpoint, not an independently controlled rollback witness.

The classifier considers previous, proposed, primary and witness
observations without performing any writes or retries.

## 11. Reconciliation Outcomes

BOTH_PREVIOUS_UNTRUSTED
POLICY_STATE_AHEAD_OF_WITNESS
POLICY_WITNESS_AHEAD_OF_STATE
BOTH_PROPOSED_UNTRUSTED
POLICY_STATE_ROLLBACK_SUSPECTED
POLICY_WITNESS_ROLLBACK_SUSPECTED
CONFLICTING_OR_UNEXPECTED_POLICY_POSITIONS
POLICY_STATE_UNAVAILABLE
POLICY_WITNESS_UNAVAILABLE
BOTH_POLICY_AUTHORITIES_UNAVAILABLE

Even BOTH_PROPOSED_UNTRUSTED does not prove a committed policy change.
An unavailable or split witness fails closed. No witness catch-up or
automatic rollback repair is approved.

## 12. Recovery Boundary

Ordinary policy rotation cannot change the recovery epoch, issuer ID or
pinned replay authority identities. Emergency root replacement and
policy recovery require a separate architecture and independently
approved authorization procedure.

A compromised key or issuer must never authorize its own replacement
solely through self-signed or caller-supplied declarations.

## 13. Adversarial Tests

Tests cover ordinary rotations, validity-window and key-material
rebinding, forbidden reactivation, key-history deletion, duplicate
material, invalid snapshot and genesis shapes, stale policy epochs,
pinned issuer/role identity changes, checkpoint mismatch, rollback,
split-commit observations and immutable non-authorizing assessments.

No fixture represents independent authority approval or protected time.

## 14. Deferred Operational Dependencies

Operational acceptance still requires independently provisioned trust
roots, authenticated policy issuer identity, protected policy storage,
independent rollback-resistant witness, actual transaction semantics,
trusted time, revocation enforcement and audited recovery authority.

Existing signature verification remains under caller-supplied key policy.

## 15. Acceptance Criteria

The gate requires: strict shape checks, exact ordinary epoch advances,
immutable role bindings, irreversible revocation, preserved history,
deterministic untrusted commitments, fail-closed observation classifications,
and passing complete Python security tests.

## 16. Final Decision

Gate 3D.12Q implements OFFLINE, NON-AUTHORIZING policy continuity only.
It does not enroll, activate, revoke or recover any operational key.
Docker execution, automatic retries and production deployment remain
blocked.
