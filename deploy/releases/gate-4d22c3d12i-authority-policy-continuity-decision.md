# Gate 4D.22C.3D.12I - Authority Trust Policy Continuity

Status: LABORATORY CONTRACTS ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Independently provisioned trust anchors: NOT IMPLEMENTED
Trusted policy approval: NOT IMPLEMENTED
Protected policy-state persistence: NOT IMPLEMENTED
Independent rollback resistance: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Define bounded, pure continuity contracts for the caller-supplied
STATE, WITNESS and ADMIN response-signing key policy.

This follows Gate 3D.12H, which verifies Ed25519 signatures
against caller-provided AuthorityResponseKeyPolicy records.

The gate does not turn that supplied key policy into an
independently authenticated source of authority.

## 2. Authority Trust Domains

Maintain distinct role labels for STATE, WITNESS and ADMIN.
Their identifiers are pinned within an ordinary policy chain.

A structurally distinct label is not proof of separate key
custody, administration, hosting or independent control.

The ADMIN response cannot authorize its own root or replace
its own signing key solely by claiming a later policy epoch.

No real root-provisioning ceremony occurs in this gate.

## 3. Policy Snapshot

The immutable AuthorityPolicySnapshot declares:

- Registry and existing authority-key policy identifiers.
- Policy epoch and local policy generation.
- Recovery epoch.
- Previous snapshot commitment.
- Transition identifier.
- Three fixed, distinct authority-role identifiers.
- Existing AuthorityResponseKeyPolicy.

Epoch and generation are positive safe integers. A declared
genesis snapshot starts at epoch 1, generation 1 and a zero
previous commitment.

Genesis validity is a shape check only, never independent
proof that bootstrap was authorized.

## 4. Key Records and History

Reuse Gate 3D.12H AuthorityResponseKey validation and its
role-separated Ed25519 signing purposes.

Within a policy snapshot, signer records must be sorted by
(role, authority_id, key_id) and confined to the pinned role.

Every role must retain at least one declared active key.
This does not independently prove that any key is currently
usable at a trustworthy time.

Historical records are retained in the candidate snapshot,
including disabled or revoked keys. The laboratory contract
rejects deletion of old key identities.

New keys must start active and carry fresh key identity and
public-key material. No existing public key may be reused
for a newly introduced signer.

## 5. Allowed Lifecycle Changes

- active -> active, disabled or revoked
- disabled -> disabled or revoked
- revoked -> revoked only

A retired key may not return to active in an ordinary policy
rotation. Its public key, key identifier, role, authority,
algorithm, purpose and declared validity interval remain fixed.

Key material replacement under the same key identifier is
forbidden. A replacement receives a new key identifier.

Old keys cannot silently disappear from the retained history.
The 32-key laboratory bound is not an operational retention
architecture; scaling and compaction require future review.

## 6. Chain Continuity

An ordinary proposed transition must:

1. Validate both caller-supplied snapshots.
2. Advance policy epoch by exactly one.
3. Advance local policy generation by exactly one.
4. Keep the recovery epoch unchanged.
5. Keep all three authority-role bindings unchanged.
6. Use a new transition identifier.
7. Bind the new snapshot to the SHA-256 commitment of the old.
8. Preserve all historical key identities and retirement state.
9. Actually enroll or retire at least one key.

Domain-separated SHA-256 commitments provide deterministic
logical chaining, not authenticated provenance or protected
rollback resistance.

A malicious caller can fabricate a self-consistent chain.
The contract must never equate a valid chain with approved
key rotation or an independently trusted administrative root.

## 7. Policy and Registry Position Alignment

A pure helper may check that a supplied request's role labels
and a supplied ProtectedPosition.policy_epoch match the
caller-supplied authority policy snapshot.

It does not alter ProtectedPosition or commit any state.

Gate 3D.12C does not currently provide a trusted, atomic
policy-epoch update with the separate state and witness.
Future integration must reconcile these authorities before
any policy can be accepted operationally.

## 8. Bootstrap, Rotation and Recovery

The first policy and every subsequent root change require an
independently controlled enrollment and authorization process.

No key may approve its own enrollment merely by appearing
inside the candidate policy. No ADMIN response may bootstrap
its own trust anchor.

An ordinary rotation cannot change pinned authority identity
or recovery epoch. Emergency root replacement, key compromise,
new administrative domains and protected backup restoration
must use a separate reviewed recovery protocol.

No automated recovery, policy write or retry is introduced.

## 9. Adversarial Acceptance Tests

Tests must cover valid additions and retirement, policy-chain
gaps, replayed transition IDs, key disappearance, key-material
rebinding, disabled/revoked reactivation, invalid role binding,
absence of an active key, malformed bootstrap, digest forgery,
policy-epoch disagreement and immutable non-authorizing results.

Tests must demonstrate that apparently valid caller-created
snapshots and commitments still have no independent provenance.

## 10. Deferred Operational Dependencies

- Independently provisioned and protected trust anchors.
- Authorization of key enrollment, rotation and revocation.
- Protected policy epoch and monotonic rollback witness.
- Durable, atomic or reconciled security-state transitions.
- Verified trust-policy issuer and key-compromise response.
- Trusted time, nonce tracking and freshness controls.
- Authenticated service adapters and runtime isolation.

## 11. Final Decision

Gate 3D.12I accepts only pure policy-continuity analysis.
A positive result is a logical proposal, not an approval,
commit, authentication or operational acceptance decision.

Docker execution, automatic retries and production
deployment remain blocked.
