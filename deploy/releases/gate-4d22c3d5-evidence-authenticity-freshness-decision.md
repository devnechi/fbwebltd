# Gate 4D.22C.3D.5 — Evidence Authenticity and Freshness

Status: DESIGN PROPOSED — IMPLEMENTATION NOT AUTHORIZED
Date: 2026-10-13

Production deployment: DISABLED
Laboratory Docker execution: DENIED
Automatic retry: DENIED
Runtime isolation: NOT INDEPENDENTLY VERIFIED

## 1. Objective

Define the security architecture for authenticating laboratory
runtime evidence, validating its freshness and preventing replay.

This decision extends Gate 4D.22C.3D.4 without modifying its
existing versioned declaration validator.

No cryptographic authority, runtime collector, signing key,
Docker access or execution authorization is introduced.

## 2. Existing Evidence Boundary

lab_runtime_evidence_schema.py validates:

- Evidence schema version.
- VM and daemon identifiers.
- Declared Docker socket and data root.
- Collection identifiers and UTC timestamp format.
- SHA-256 digest format.
- Declared isolation control consistency.

The existing validator does not independently establish:

- Collector authenticity.
- Source-digest integrity.
- Trusted collection time.
- Runtime identity ownership.
- Evidence freshness.
- Replay resistance.
- Actual runtime isolation.

All existing execution-denial outcomes must be preserved.

## 3. Security Decision

### A1 — Independent Trust Anchor

Evidence authenticity must be verified against a trust anchor
approved independently of the evidence being evaluated.

A collector name or identifier inside the evidence must not
authorize that collector.

Trusted collector identities and verification keys must be
distributed through a separately reviewed mechanism.

An evidence record must not supply its own trusted key.

Key provisioning, rotation, revocation and compromise handling
require a separate implementation and operational review.

### A2 — Cryptographic Evidence Binding

A future authentication envelope must bind:

- The exact versioned evidence payload.
- Evidence schema and authentication-envelope versions.
- Collector identity and trusted key identifier.
- VM and daemon subject identities.
- Evidence and collection identifiers.
- The assessment-specific challenge.
- Collection and expiry timestamps.
- The intended laboratory verification purpose.

The signed bytes must use one documented canonical encoding.

Verification must reject modified, ambiguous, unsupported or
noncanonical payload representations.

A valid signature establishes authenticated origin and payload
integrity only when the signing key is independently trusted.

It does not prove the underlying observations are true.

### A3 — Algorithm and Key Policy

The implementation must use an approved, well-reviewed
cryptographic library and a fixed algorithm policy.

Algorithm negotiation must not be controlled by untrusted evidence.

Unknown algorithms, unexpected keys, revoked keys and invalid
signatures must fail closed.

Secrets and private keys must not be included in evidence records,
repository fixtures or diagnostic output.

### A4 — Trusted Assessment Time

Freshness evaluation must use a time source supplied by the
trusted verifier.

The evidence's own collected_at value cannot establish
the current time.

The future policy must explicitly define:

- Maximum evidence age.
- Permitted clock skew.
- Expiration requirements.
- Handling of future-dated evidence.
- Handling of missing or unreliable trusted time.

Timestamp comparisons must use timezone-aware UTC values.

No timestamp supplied by the evidence may extend the approved
freshness window.

### A5 — Replay Prevention

A fresh assessment must use a verifier-issued,
unpredictable challenge bound to the expected subject.

The verifier must bind the challenge to:

- The intended verification purpose.
- Expected VM identity.
- Expected daemon identity.
- Collection session.
- An explicit validity window.

A challenge must be accepted at most once.

Replay protection requires trusted durable state or another
separately reviewed atomic single-use mechanism.

An in-memory set is insufficient for replay resistance across
verifier restarts.

On persistence failure or uncertain challenge consumption,
verification must fail closed.

### A6 — Subject Continuity

Evidence must be rejected if authenticated subjects disagree
with the verifier's independently supplied expectations.

The following must be correlated:

- VM identity.
- Daemon identity.
- Process identity and kernel start time where relevant.
- Collection session.
- Challenge identity.
- Authenticated collector identity.

Evidence from different sessions must not be silently merged.

Daemon restarts, PID reuse or socket replacement invalidate
continuity unless independently resolved.

### A7 — Evidence Source Integrity

A source_digest field is only a declaration unless the verifier
has access to the source bytes or an independently authenticated
digest commitment.

Any later digest verification must use an approved canonical
representation and the actual authenticated source material.

Digest-format validation alone must never be reported as
evidence authentication.

### A8 — Authorization Separation

The authenticity verifier must not:

- Grant Docker execution.
- Grant production deployment.
- Permit automatic retry.
- Trigger rollback.
- Start a VM or daemon.
- Connect to a Docker socket.
- Execute subprocesses.
- Change runtime configuration.

Even fully authenticated and fresh evidence is not sufficient
to prove VM or daemon isolation.

Execution authorization remains an independent security gate.

## 4. Proposed Verification Sequence

A future verifier must:

1. Validate the evidence schema.
2. Validate the authentication-envelope schema.
3. Resolve collector trust independently.
4. Validate the approved algorithm and key status.
5. Verify the cryptographic evidence binding.
6. Validate the verifier-issued challenge.
7. Check expected subject and purpose binding.
8. Evaluate timestamps using trusted verifier time.
9. Atomically enforce single-use replay protection.
10. Produce a bounded authenticity assessment.

The implementation must specify the ordering and failure
semantics of durable challenge consumption.

Failures after a challenge is consumed must not permit
uncontrolled reuse.

Successful authentication must not automatically change
the runtime isolation assessment.

## 5. Required Assessment Separation

Future assessments must distinguish:

- Schema validity.
- Payload integrity.
- Collector authenticity.
- Trusted subject binding.
- Evidence freshness.
- Replay protection.
- Independent runtime verification.
- Execution authorization.

These are separate security conclusions.

For this gate, the following remain false:

- runtime_evidence_verified
- vm_identity_proven
- daemon_identity_proven
- daemon_isolation_proven
- isolation_proven
- docker_execution_permitted
- production_execution_enabled
- automatic_retry_permitted

manual_verification_required remains true.

## 6. Adversarial Test Requirements

A subsequent implementation must test:

- Unknown or revoked collector keys.
- Invalid or modified signatures.
- Algorithm substitution.
- Noncanonical signed payloads.
- Evidence signed for another purpose.
- VM or daemon subject substitution.
- Wrong collection session.
- Expired evidence.
- Future-dated evidence.
- Untrusted assessment time.
- Repeated challenge submission.
- Concurrent replay attempts.
- Verifier restart after challenge consumption.
- Replay-store corruption or unavailability.
- Daemon restart between evidence collection and review.
- Missing authenticated source material.
- Valid signatures over false isolation declarations.
- Malformed authentication envelopes.

All ambiguous conditions must fail closed.

## 7. Implementation Boundaries

This architecture decision does not implement:

- Signing or cryptographic verification.
- Collector key provisioning.
- Key rotation or revocation.
- Trusted clock integration.
- Durable replay storage.
- Runtime attestation.
- Docker inspection or execution.
- VM or hypervisor integration.
- Production authorization.

These require separately reviewed changes.

## 8. Acceptance Criteria

Gate 4D.22C.3D.5 may be accepted as a design when:

1. Collector trust is independent of submitted evidence.
2. Cryptographic binding requirements are explicit.
3. Freshness relies on trusted verifier time.
4. Replay protection requires atomic single-use state.
5. Subject and session continuity are defined.
6. Signed false claims cannot become isolation proof.
7. Existing execution restrictions remain unchanged.
8. Repository validation and review are completed.

Passing these criteria approves the design only.

## 9. Final Decision

The versioned runtime evidence schema remains an untrusted
declaration format.

A future authentication mechanism must independently establish
collector trust, integrity, freshness and replay resistance.

Authenticated evidence must not be confused with independently
verified runtime isolation.

Docker execution, automatic retry and production deployment
remain blocked.
