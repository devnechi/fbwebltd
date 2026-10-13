# Gate 4D.22C.3D.11A - Trusted Registry Provenance Architecture

Status: DESIGN PROPOSED - IMPLEMENTATION NOT AUTHORIZED
Date: 2026-10-13

Production deployment: DISABLED
Laboratory Docker execution: DENIED
Automatic retry: DENIED
Independent runtime isolation: NOT VERIFIED
Operational key provisioning: NOT AUTHORIZED

## 1. Objective

Define the security architecture for authenticating the laboratory
collector-key registry, controlling registry revisions, enforcing
key lifecycle changes and preventing registry rollback.

This decision builds upon Gates 4D.22C.3D.7 through 3D.10.

This gate introduces no operational trust anchors, registry
distribution mechanism, persistent revision store, collector
signing keys or Docker execution permission.

## 2. Current Security Boundary

The existing implementation provides:

- Strict laboratory evidence schema validation.
- Versioned authentication-envelope validation.
- Restricted canonical evidence signing bytes.
- Collector/key eligibility checks.
- Ed25519 evidence signature verification.

The collector registry is currently caller-supplied.

Consequently, a valid evidence signature proves only that
the supplied public key verifies the signed payload.

It does not independently establish:

- Registry issuer identity.
- Authorization of the registry issuer.
- Authentic registry distribution.
- Current registry revision.
- Protection against previously signed registry rollback.
- Current revocation status from an authoritative source.
- Trusted collector identity.
- Runtime observation truthfulness.
- Laboratory VM or Docker daemon isolation.

## 3. Security Decision

### R1 - Separate Administrative Trust Authority

The registry verification authority must be separate from
laboratory evidence collectors.

An independently authorized administrator or administrative
signing service must control registry issuance.

Collector signing keys must not be permitted to sign or approve
collector registries.

Registry administration and evidence collection must use
separate cryptographic purposes and trust policies.

### R2 - Independently Provisioned Trust Anchor

The verifier must receive approved administrative public keys
from a separately controlled trusted configuration.

The registry under verification must never:

- Supply its own trusted administrative public key.
- Enroll an administrative signing authority.
- Modify the accepted administrative trust anchors.
- Expand its permitted verification purpose.
- Disable registry signature verification.

An arbitrary caller-supplied public key is not independently
authenticated merely because a signature verifies.

Trust-anchor enrollment and removal require separately
authorized operational procedures.

### R3 - Versioned Signed Registry Format

A future signed registry must contain at least:

- Registry format version.
- Registry identity.
- Monotonically increasing registry revision.
- Issuing administrative key identifier.
- Issuance timestamp.
- Expiration timestamp.
- Collector key records.
- Registry signature.

Collector key records must preserve the existing policy fields:

- collector_id
- key_id
- algorithm
- public_key_hex
- purpose
- vm_id
- daemon_id
- valid_from
- valid_until
- status

The format must use a strictly defined canonical serialization
contract with explicit signed-byte domain separation.

The registry format must reject:

- Duplicate JSON keys.
- Duplicate collector/key identities.
- Ambiguous numeric encodings.
- Unsupported fields or format versions.
- Invalid character encodings.
- Noncanonical key ordering or record ordering.
- Unknown signature algorithms.
- Noncanonical signatures.

The existing evidence canonicalization contract does not
support arrays, while the registry model contains a tuple
of collector key records.

A separate versioned registry wire format must therefore
be specified and tested before implementation.

The evidence canonicalization module must not be silently
changed to accept new data types.

### R4 - Registry Signature Verification

The future registry verifier must:

1. Parse original registry bytes strictly.
2. Validate the registry format and all key records.
3. Validate the administrative signing purpose.
4. Resolve the administrator key from approved trust policy.
5. Reconstruct the exact canonical signed bytes.
6. Verify the administrative Ed25519 signature.
7. Validate issuer authorization and key lifecycle status.
8. Validate the registry validity period.
9. Evaluate registry revision continuity independently.
10. Return a bounded registry assessment.

Unknown issuers, invalid signatures and unsupported algorithms
must fail closed.

A valid registry signature alone does not establish that the
registry is the latest authorized revision.

### R5 - Monotonic Revision and Rollback Protection

The verifier must maintain an independently trusted record of
the highest accepted registry revision.

That state must associate a registry revision with the
digest of its approved signed content.

A registry with a lower revision must be rejected.

A registry with the same revision but a different content
digest must be rejected.

Identical content at the same revision may be recognized,
but recognition must not imply a new authorization decision.

Revision advances require a separately specified continuity
policy, including handling of missing intermediate revisions.

For a normal incremental update, the future format should
bind the previous accepted revision and digest.

Emergency replacement and recovery require separate
administrative authorization.

The registry itself must not define or reset the verifier's
trusted revision floor.

### R6 - Durable Revision State

Operational rollback protection requires a trusted durable
state mechanism with atomic update semantics.

The implementation must address:

- Concurrent verifier processes.
- Process crashes.
- Power loss.
- Storage corruption.
- Lost or uncertain commits.
- Filesystem rollback.
- Backup restoration.
- Replayed registry distribution messages.
- Multi-host verifier consistency.

Writing a revision number into an ordinary unprotected file
does not establish rollback protection against a host attacker.

The design must identify the protected storage and trust model
before operational deployment.

Failure to read or update trusted revision state must
fail closed.

### R7 - Registry Freshness

Registry timestamps must be evaluated against verifier-controlled
trusted time.

A signed but expired registry must not be accepted for new
operational assessments.

A future-dated registry must not become valid merely because
it carries an authentic signature.

Trusted clock failure or uncertainty must block acceptance.

Registry freshness is separate from evidence freshness.

Both must be evaluated independently.

### R8 - Collector Key Revocation

The registry must preserve key states:

- active
- disabled
- revoked

For live verification, revoked or disabled collector keys
must not be accepted even when a historical signature is
cryptographically valid.

A key compromised before revocation may have produced
fraudulent historical evidence.

Forensic verification of historical signatures must be
separate from current authorization or evidence acceptance.

The lifecycle design must specify:

- Revocation publication.
- Maximum permitted registry staleness.
- Collector deactivation.
- Expiration.
- Rotation.
- Compromise response.
- Recovery of stale verifiers.

No evidence assessment may override an authoritative
revocation decision.

### R9 - Administrative Key Rotation

Administrative key rotation must not be self-authorized
by untrusted registry content.

A new administrative trust anchor requires independently
authorized enrollment.

A compromised administrative key requires a defined
emergency recovery procedure.

A valid signature from a revoked administrative authority
must not authorize a new registry revision.

Historical registry acceptance records require separate
retention and audit rules.

### R10 - Registry Distribution

Registry transport and signature validity are distinct.

A registry may be delivered through an untrusted transport
only when the verifier independently establishes:

- Approved administrative signing authority.
- Authentic signed content.
- Approved verification purpose.
- Valid revision continuity.
- Trusted registry freshness.
- Current key lifecycle state.

Transport security must not replace content authentication
or trusted rollback protection.

The registry must not fetch or install trust anchors from
URLs embedded in untrusted content.

### R11 - Trust and Authentication Conclusions

The future assessments must distinguish:

- registry_structure_valid
- registry_signature_verified
- administrative_key_policy_valid
- registry_revision_current
- registry_freshness_verified
- registry_provenance_authenticated
- collector_key_policy_eligible
- evidence_signature_verified
- collector_authenticated
- evidence_replay_prevention_verified
- runtime_isolation_proven
- docker_execution_permitted

No result may infer registry provenance solely from
a caller-supplied administrative public key.

No result may infer replay prevention from signature validity.

No result may infer runtime isolation from authenticated
registry or collector evidence.

### R12 - Authorization Separation

Registry authentication must never directly:

- Start or stop Docker.
- Connect to a Docker socket.
- Start or modify a virtual machine.
- Launch subprocesses.
- Enable automatic retries.
- Perform rollback.
- Enable image publishing.
- Authorize production deployment.
- Modify unrelated release authorization policy.

Runtime isolation and execution authorization remain
independent security gates.

## 4. Proposed Implementation Stages

### Gate 3D.11B - Offline Registry Verification

Implement and test:

- A versioned registry wire contract.
- Strict canonical registry parsing.
- Registry-specific domain separation.
- Administrative Ed25519 signature verification.
- Explicit external trust-anchor inputs.
- Signature and issuer-policy failure handling.
- Non-authorizing verification assessments.

Use ephemeral test-only administrative keys.

Do not provision operational signing authorities.

Do not claim trusted registry provenance when the
administrative trust anchor is merely caller-supplied.

### Gate 3D.11C - Revision and Revocation State

Define and independently review:

- Revision continuity.
- Current revision and signed-content digest binding.
- Atomic durable updates.
- Concurrent verification semantics.
- Key revocation publication and enforcement.
- Failure recovery.
- Bootstrap and emergency restoration.
- Trusted time requirements.

Operational persistent storage must not be introduced
without a separately approved threat model.

### Future Operational Integration

Independently review:

- Trust-anchor custody.
- Administrative approval controls.
- Registry distribution.
- Trusted state persistence.
- Collector onboarding.
- Key rotation.
- Compromise recovery.
- Operational logging.
- Change-management responsibilities.

Do not enable runtime execution through this process.

## 5. Required Adversarial Tests

Future implementations must reject or safely handle:

1. Unsigned registry.
2. Invalid administrative signature.
3. Unknown administrative key.
4. Revoked administrative key.
5. Collector key used as a registry signing authority.
6. Algorithm substitution.
7. Registry purpose substitution.
8. Modified signed registry.
9. Duplicate collector/key identity.
10. Duplicate or malformed JSON keys.
11. Ambiguous canonical serialization.
12. Lower registry revision.
13. Conflicting content at the same revision.
14. Missing or invalid revision continuity.
15. Concurrent revision replacement.
16. Revision-state corruption.
17. Storage write failure.
18. Restoration of stale trusted state.
19. Expired registry.
20. Future-dated registry.
21. Collector key reactivation after revocation.
22. Untrusted trust-anchor replacement.
23. Administrative key compromise.
24. Registry distribution replay.
25. Valid registry signature with false isolation claims.

All uncertain trust states must fail closed.

## 6. Gate 3D.11A Acceptance Criteria

The architecture may be accepted when:

1. Registry issuance authority is separated from collectors.
2. Administrative trust anchors are independently controlled.
3. The registry signing format is clearly separated from
   laboratory evidence signing.
4. Canonical serialization requirements are defined.
5. Revision rollback and equivocation risks are addressed.
6. Revocation and administrative rotation rules are defined.
7. Trusted time and freshness are treated independently.
8. Operational integration remains deferred.
9. Existing execution-denial guarantees are preserved.
10. Repository tests and security review are completed.

Acceptance approves architecture only.

## 7. Final Decision

Future Basics laboratory collector registries require
independently authorized administrative signatures,
strictly canonical signed bytes, trusted key lifecycle
controls and independently protected revision continuity.

No combination of registry signature validity and evidence
signature validity can independently prove runtime isolation.

Gate 3D.11A does not introduce operational trust anchors,
trusted persistence, collector authentication guarantees
or execution authorization.

Laboratory Docker execution, automatic retries and
production deployment remain blocked.
