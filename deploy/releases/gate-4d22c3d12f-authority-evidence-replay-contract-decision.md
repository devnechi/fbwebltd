# Gate 4D.22C.3D.12F - Independent Authority Evidence Contracts

Status: LABORATORY CONTRACT ONLY - AUTHORITY UNVERIFIED
Date: 2026-10-13

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Authority authentication: NOT IMPLEMENTED
Trusted administrative policy: NOT ESTABLISHED
Trusted time: NOT IMPLEMENTED
Replay prevention: NOT IMPLEMENTED
Protected state and witness: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Specify and test how future responses from a transactional
state authority, independent rollback witness and administrative
trust authority bind to one verifier-initiated read request.

This gate extends Gates 3D.12C-3D.12E with offline data contracts.
It implements no network transport, digital signature, MAC, key,
credential, state persistence, nonce cache or authority adapter.

## 2. Requested Authorities

One AuthorityReadChallenge declares a registry identity,
request identifier, challenge and three DISTINCT expected
role-specific authority identifiers.

The labels are caller-supplied. This contract cannot prove
those labels were independently enrolled or approved.

Operational use would require a separately provisioned,
verified trust configuration independent of registry content.

## 3. Response Binding

Every AuthorityReadEvidence must bind:

- Its exact role: STATE, WITNESS or ADMIN.
- Its expected authority identifier.
- The requested registry identity.
- The request identifier.
- The challenge.
- A deterministic digest of the typed response body.
- A deterministic digest of the complete declared envelope.

A mismatching response must fail closed.
Cross-role substitution must fail closed.

The body and envelope digests are unkeyed SHA-256 checksums.
They DO NOT authenticate an authority or protect against a
malicious caller capable of recomputing them.

## 4. Role-Specific Payloads

STATE responses contain a ProtectedPosition and its bound
RevocationHistorySnapshot. Their revocation commitment and
revision/generation references must match.

WITNESS responses contain a WitnessCheckpoint referencing
the same protected position.

ADMIN responses contain an AdministrativeKeyPolicy declaration
and its declared policy epoch, which must match the protected
position. No administrator is thereby authorized.

The existing validators are reused rather than weakened.

## 5. Challenge and Replay Boundary

The contract compares a response to the supplied request ID
and challenge. It rejects an older response when those fields
are changed for a new request.

It CANNOT detect a response replayed with the same request ID
and challenge, or a coordinated attacker forging both sides.

Operational anti-replay requires independently generated
unpredictable challenges, uniqueness tracking across restarts,
explicit expiry/freshness guarantees and authenticated responses.
A challenge echo alone does not establish state currentness.

This gate creates no random challenge generator or nonce store.

## 6. Authority Independence

Distinct role labels and matching content are necessary
structural constraints, but not evidence of genuine separation.

Operational authority identity verification must consider:

- Independent enrollment and key custody.
- Service credential lifecycle and revocation.
- Channel and/or message authentication.
- Registry scope and purpose binding.
- Credential and policy epoch restrictions.
- Stale reply and rollback detection.
- Independent audit evidence.

The verifier must not accept an authority selected merely
by untrusted input or the registry being assessed.

## 7. Failure Behavior

Invalid role, challenge, identifier, payload, digest,
revision, revocation commitment, state/witness pair or
policy epoch must raise ValueError.

No partially positive assessment is returned on failure.

A locally consistent assessment retains all operational
trust and execution claims as false.

## 8. Adversarial Acceptance

Tests must include wrong IDs, swapped roles, malformed
challenges, altered payloads, wrong digests, state/witness
conflict, policy-epoch conflict, stale response under a new
challenge, coordinated forged declarations and replay with
an identical caller-provided challenge.

Those positive demonstrations must explicitly preserve
false authentication and replay-protection claims.

## 9. Later Integration

Operational work is separate and requires reviewed:

- Administrative trust-anchor provisioning.
- Authenticated state, witness and policy service adapters.
- Cryptographic response/channel verification.
- Trusted challenge generation and replay tracking.
- State/witness crash consistency and recovery.
- Trusted time and freshness rules.
- Verified runtime isolation and independent execution approval.

## 10. Final Decision

Gate 3D.12F provides response-binding analysis only.
It does not establish independent provenance, authoritative
currentness, rollback resistance or durable state acceptance.

Docker execution, automatic retries and production
deployment remain blocked.
