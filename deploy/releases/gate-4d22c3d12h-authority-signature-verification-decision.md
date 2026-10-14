# Gate 4D.22C.3D.12H - Pure Authority Signature Verification

Status: LABORATORY VERIFICATION ONLY
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Independent trust anchors: NOT PROVISIONED
Operational authority services: NOT IMPLEMENTED
Replay prevention: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Rollback-resistant storage: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Implement strict, offline Ed25519 signature verification
for STATE, WITNESS and ADMIN authority-response records.

This gate implements the laboratory cryptographic
verification design approved for review in Gate 3D.12G.

It extends the existing Gate 3D.12F response-binding
contracts without modifying their non-authorizing claims.

## 2. Security Boundary

The authority-key policy is supplied by the caller.

Verification proves that response bytes match a signature
under a specified public key.

It does not prove that the public key belongs to an
independently authorized security authority.

The verifier does not provision or discover trusted roots.

The administrative policy returned in an ADMIN response
cannot authorize its own authority-response verification.

## 3. Signature Roles

STATE, WITNESS and ADMIN each use a different
domain-separated signing message.

The signing purpose and approved authority identity
must match the selected key-policy record.

Duplicate key material across authority roles is rejected.

Registry administrative signing keys remain a separate
cryptographic purpose and verification protocol.

## 4. Signed Response Format

SignedAuthorityResponse binds:

- Role and authority identifier.
- Authority signing-key identifier.
- Registry identifier.
- Request identifier and challenge.
- Typed response body commitment.
- Response envelope commitment.
- Declared administrative policy epoch.
- Algorithm and role-specific signing purpose.
- Ed25519 signature.

The signature is excluded from its own signing message.

The exact signing bytes are:

ROLE_DOMAIN_PREFIX + CANONICAL_UNSIGNED_JSON

The signing domain differs for each authority role.

## 5. Strict Wire Requirements

A signed response wrapper must reject:

- Unknown fields.
- Duplicate JSON keys.
- Invalid field types.
- Floats or unsupported numeric encodings.
- Noncanonical JSON.
- Oversized messages.
- Invalid signature lengths.
- Noncanonical base64url signatures.
- Unsupported signing algorithms.
- Incorrect role or signing purpose.

The complete typed response body is validated through
the existing Gate 3D.12F contract before signature
verification.

This gate does not introduce a general-purpose
network response parser or operational transport.

## 6. Caller-Supplied Key Policy

The key policy declares:

- Role.
- Authority identifier.
- Signing-key identifier.
- Public-key material.
- Algorithm and purpose.
- Lifecycle state.
- Declared validity interval.

Only active keys inside their declared validity interval
may verify a response.

The assessment time is explicitly caller-supplied.

Passing the declared validity check does not prove
that an independent trusted time source was used.

## 7. Cryptographic Verification

The verifier must:

1. Validate all three response-binding declarations.
2. Validate the caller-supplied authority-key policy.
3. Validate the supplied assessment time.
4. Bind each signed header to its response declaration.
5. Select the exact role-specific signing-key record.
6. Enforce key lifecycle and declared validity.
7. Reconstruct the canonical signing message.
8. Verify the Ed25519 signature.
9. Return an immutable non-authorizing assessment.

No private key is created or required in the verifier.

Test fixtures may generate temporary private keys in memory.

## 8. Replay Limitations

A valid signed response can be replayed when the
same request identifier and challenge are reused.

This gate does not independently generate challenges,
track consumed challenges or maintain protected replay state.

Cryptographic signature verification must not be
reported as replay prevention or currentness.

## 9. Failure Behavior

Invalid headers, signatures, purposes, key-policy records,
key lifecycle states or evidence bindings must fail closed.

The verifier must not perform recovery, retry, commits,
network requests, Docker operations or deployment actions.

## 10. Adversarial Acceptance Tests

The tests must cover valid signatures, altered signatures,
wrong public keys, disabled and revoked keys, role
substitution, signing-purpose confusion, challenge changes,
wrong request IDs, noncanonical wire bytes, duplicate
fields, policy substitution and replay limitations.

Every positive test must preserve false operational
authentication, freshness, rollback and execution claims.

## 11. Next Security Gate

Gate 3D.12I should define independently provisioned
authority trust-policy contracts, policy epoch continuity,
key rotation and trust-root replacement constraints.

Even after Gate 3D.12I, operational trust requires
independent provisioning and protected enforcement.

## 12. Final Decision

Gate 3D.12H implements offline Ed25519 verification
against explicitly caller-supplied authority public keys.

No independently trusted authority identity or
operational state currentness is established.

Docker execution, automatic retries and production
deployment remain blocked.
