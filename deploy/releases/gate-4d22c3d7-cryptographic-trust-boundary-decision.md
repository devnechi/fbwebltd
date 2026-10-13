# Gate 4D.22C.3D.7 — Cryptographic Verification Trust Boundary

Status: DESIGN PROPOSED — VERIFICATION NOT IMPLEMENTED
Date: 2026-10-13

Laboratory Docker execution: DENIED
Production deployment: DISABLED
Automatic retry: DENIED
Runtime isolation: NOT INDEPENDENTLY VERIFIED

## 1. Objective

Define the trust boundaries required to verify Ed25519 signatures
over Future Basics laboratory runtime evidence.

This decision extends Gates 4D.22C.3D.5 and 4D.22C.3D.6.

It does not implement cryptographic verification, generate keys,
provision collectors, connect to Docker or authorize execution.

## 2. Existing Implementation

lab_runtime_evidence_schema.py validates untrusted runtime
evidence declarations.

lab_runtime_auth_envelope.py validates envelope structure,
expected identity bindings, signature encoding and declared
timestamp windows.

The current signing_payload function generates a provisional
deterministic JSON representation.

The existing implementation does not authenticate collectors,
verify signatures, consume replay challenges or establish
independent runtime isolation.

## 3. Trust Boundaries

### T1 — Independent Collector Trust

Trusted collector identities must be established through a
verifier-controlled trust registry.

The registry must bind:

- Collector identity.
- Approved verification key identifier.
- Ed25519 public key.
- Permitted verification purpose.
- Key lifecycle status.
- Key validity period.
- Approved subject scope, where applicable.

Evidence must never establish its own trusted collector or key.

An unknown, disabled, revoked or mismatched key must be rejected.

### T2 — Cryptographic Algorithm

Ed25519 is the proposed fixed signature algorithm for
laboratory evidence authentication.

The verifier must not negotiate an alternative algorithm
based on untrusted envelope data.

The future implementation must use a maintained cryptographic
library with documented Ed25519 verification semantics.

Private keys and signing operations are outside this gate.

### T3 — Canonical Signed Bytes

The complete signing format must be specified before
cryptographic verification is implemented.

The contract must define:

- Character encoding.
- JSON parsing requirements.
- Duplicate-key rejection.
- Permitted JSON value types.
- Unicode normalization policy.
- Numeric representation restrictions.
- Key ordering and whitespace rules.
- Envelope version handling.
- Signature-field exclusion.
- Domain separation and purpose binding.

The current signing_payload representation is provisional.

It must not be treated as an independently approved
interoperable canonicalization standard.

The verifier must reject any payload whose signed bytes
cannot be reconstructed unambiguously.

### T4 — Trusted Key Resolution

The key identifier in an envelope is untrusted input.

A verifier must resolve that identifier only within its
independently approved collector trust policy.

A matching identifier without a matching trusted public key
and authorized collector relationship is insufficient.

Submitted public keys, embedded certificates or external
key locations must not be trusted automatically.

### T5 — Signature Verification

A future verification mechanism must:

1. Validate the evidence and envelope structures.
2. Resolve the collector and key from trusted policy.
3. Reject unsupported algorithms and key states.
4. Construct the approved canonical signed bytes.
5. Verify the Ed25519 signature using the trusted public key.
6. Confirm verifier-controlled expected subject bindings.
7. Preserve separate freshness and replay conclusions.
8. Return a bounded authentication assessment.

Verification failure must not fall back to format-only
validation or an alternative verification algorithm.

A successful signature check must not authorize execution.

### T6 — Key Lifecycle

The trust architecture must explicitly support:

- Key enrollment under independent authorization.
- Key rotation.
- Key expiration.
- Immediate key revocation.
- Collector deactivation.
- Response to suspected key compromise.
- Audit records for trust-policy changes.

The behavior of historical evidence after key revocation
must be defined before implementation.

No private signing keys may be committed to the repository.

### T7 — Trusted Time and Replay Protection

Cryptographic verification does not establish freshness.

Freshness requires verifier-controlled trusted time and
approved validity limits.

Replay resistance requires verifier-issued challenges and
durable atomic single-use enforcement.

Signature verification must remain distinct from durable
challenge consumption.

Failure or uncertainty in replay-state persistence must
fail closed.

### T8 — Runtime Isolation and Execution

An authentic signature establishes integrity and authenticated
origin under the approved key policy.

It does not prove that:

- The laboratory VM is isolated.
- The claimed daemon is the observed daemon.
- The socket belongs to the intended daemon.
- Production resources are inaccessible.
- Network or filesystem isolation is effective.
- A Docker operation is safe to execute.

These conditions require independent runtime verification.

Docker execution authorization requires a further separate
review and cannot be inferred from signature verification.

## 4. Required Assessment Separation

The future system must distinguish:

- schema_valid
- envelope_structure_valid
- signature_verified
- collector_authenticated
- subject_binding_verified
- freshness_verified
- replay_prevention_verified
- runtime_evidence_verified
- isolation_proven
- docker_execution_permitted

For this gate, cryptographic verification is not implemented.

Runtime evidence remains independently unverified.

The following safety outcomes remain mandatory:

- runtime_evidence_verified = false
- isolation_proven = false
- docker_execution_permitted = false
- production_execution_enabled = false
- automatic_retry_permitted = false
- manual_verification_required = true

## 5. Adversarial Acceptance Tests

A future implementation must cover:

1. Unknown collector.
2. Unknown or revoked key.
3. Collector and key mismatch.
4. Invalid Ed25519 signature.
5. Modified signed evidence.
6. Modified challenge or verification purpose.
7. Algorithm substitution.
8. Duplicate JSON object keys.
9. Ambiguous numeric and Unicode representations.
10. Noncanonical signed payload.
11. Key rotation and expired keys.
12. Concurrent trust-policy changes.
13. Compromised collector key.
14. Valid signatures over false isolation claims.
15. Expired or replayed evidence.
16. Verifier restart and replay-state recovery.
17. Signature-verification library failure.
18. Subject or collection-session substitution.

All ambiguous conditions must fail closed.

## 6. Implementation Exclusions

This gate does not:

- Generate or store private keys.
- Provision a collector.
- Install cryptographic dependencies.
- Implement signature verification.
- Implement key rotation or revocation.
- Implement replay storage.
- Connect to Docker.
- Launch subprocesses.
- Create or start virtual machines.
- Enable laboratory execution.
- Enable automatic recovery.
- Authorize production deployment.

## 7. Acceptance Criteria

This decision may be accepted when:

1. Collector trust is independent of submitted evidence.
2. The Ed25519 policy is fixed.
3. Canonicalization requirements are documented.
4. Key lifecycle and revocation requirements are defined.
5. Verification failures are fail-closed.
6. Freshness and replay remain separate trust conclusions.
7. Authentication cannot establish runtime isolation.
8. Execution and production restrictions are preserved.
9. Repository validation and review are completed.

Acceptance approves the architecture only.

## 8. Final Decision

A verifier-controlled collector trust registry and a formally
reviewed canonical signing format are prerequisites for
cryptographic laboratory evidence authentication.

Actual verification must be implemented and tested under
a subsequent gate.

No laboratory Docker execution, automatic retry or production
deployment is authorized by this decision.
