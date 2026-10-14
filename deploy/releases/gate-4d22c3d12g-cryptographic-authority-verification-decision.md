# Gate 4D.22C.3D.12G - Cryptographic Authority Verification Architecture

Status: ARCHITECTURE ONLY - OPERATIONAL TRUST NOT ESTABLISHED
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Authority response signatures: NOT IMPLEMENTED
Independently provisioned authority roots: NOT IMPLEMENTED
Authenticated authority transport: NOT IMPLEMENTED
Replay prevention: NOT IMPLEMENTED
Protected registry state: NOT IMPLEMENTED
Independent rollback witness: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Define a cryptographic verification architecture for responses
from the Future Basics laboratory registry security authorities.

This decision builds upon:

- Gate 3D.11B - Administrative registry signature verification.
- Gate 3D.11F - Non-authorizing registry assessment composition.
- Gate 3D.12A - Independent trust and protected-state architecture.
- Gate 3D.12B - Preferred trust-authority architecture.
- Gate 3D.12C - Protected-state interfaces.
- Gate 3D.12D - Authority authentication and reconciliation.
- Gate 3D.12E - Pure reconciliation evaluator.
- Gate 3D.12F - Authority-evidence response-binding contracts.

Gate 3D.12G is architecture-only.

No operational keys, services, credentials, persistent state,
cryptographic verifier implementation or execution authority
are created by this decision.

## 2. Existing Limitation

Gate 3D.12F verifies structural consistency of three
caller-supplied authority-evidence records.

The roles are:

STATE
WITNESS
ADMIN

The existing response-binding checks use unkeyed SHA-256
commitments.

Those commitments can identify accidental modifications
or inconsistent supplied records.

They do not prove response authorship.

A malicious caller can recompute a body commitment and
envelope commitment after replacing the contents.

The current authority identifiers are also caller-supplied.

A matching identifier does not establish independently
trusted authority identity.

## 3. Required Security Properties

The future verifier must distinguish between:

1. Structurally valid response.
2. Cryptographically valid response signature.
3. Signature verified under a provisionally supplied key.
4. Signer independently authorized for the expected role.
5. Response bound to the current verification request.
6. Response freshness independently established.
7. Protected state currentness independently established.
8. Operational acceptance independently authorized.

Passing an earlier property must not automatically
establish a later property.

A valid signature under an attacker-provided public key
must not establish authority authentication.

## 4. Independent Trust Bootstrap

Authority verification requires pre-established trust anchors.

Those anchors must not originate solely from:

- The authority response being checked.
- The candidate registry.
- Caller-controlled environment variables.
- Untrusted application configuration.
- Application database records.
- A previously unverified policy response.
- A test fixture.
- An unauthenticated network request.

The approved trust anchors must be provisioned through
a separately reviewed administrative process.

The implementation must distinguish trust-anchor
enrollment from ordinary response verification.

Bootstrap cannot silently occur when an anchor is absent.

## 5. Three Authority Roles

### 5.1 STATE Authority

Signs authenticated declarations of transactional
registry-state positions and their revocation history.

Its role purpose must be limited to the STATE authority.

A STATE signature cannot authorize an ADMIN policy
or represent the independent rollback witness.

### 5.2 WITNESS Authority

Signs independent declarations of rollback-witness
checkpoint positions.

The WITNESS authority must have separate key custody
and administration from the transactional STATE authority.

A STATE administrator must not be able to silently
replace the trusted WITNESS signing key.

### 5.3 ADMIN Authority

Signs independently authorized administrative
trust-policy declarations.

The ADMIN authority manages the approved registry
administrative signing policy.

It must not obtain its own trust solely from the
ADMIN response currently being assessed.

Authority-response keys and registry-administrator
signing keys serve distinct purposes.

## 6. Cryptographic Algorithm

The preferred laboratory verification algorithm is Ed25519.

The existing registry-signature verifier already uses
Ed25519 for a different domain and purpose.

Authority-response signatures must not reuse the
registry signature message format or purpose.

The future verifier must enforce:

- Explicit algorithm identifier.
- Exact public-key encoding.
- Exact signature length.
- Strict canonical message encoding.
- Role-specific signature purpose.
- Independently approved signer identity.
- No implicit algorithm fallback.
- No cross-role key substitution.

No private signing keys are required by this architecture gate.

Any operational algorithm change requires an explicit
reviewed version transition.

## 7. Domain Separation

Authority signatures must use purpose-separated messages.

Proposed domain identifiers:

FBWEB-LAB-STATE-RESPONSE-SIGNATURE-V1
FBWEB-LAB-WITNESS-RESPONSE-SIGNATURE-V1
FBWEB-LAB-ADMIN-RESPONSE-SIGNATURE-V1

The exact byte representation must be defined and
frozen before implementation.

A domain prefix must be included in the signed bytes.

Changing the role must change the signed message.

Registry administrative signatures must remain
cryptographically distinct from authority responses.

A correctly signed STATE response cannot be
reinterpreted as a WITNESS response.

## 8. Canonical Signed Message

The future signed authority response must bind:

- Signature-domain version.
- Authority role.
- Approved authority identifier.
- Approved signing-key identifier.
- Registry identity.
- Request identifier.
- Request challenge.
- Body commitment.
- Envelope commitment.
- Protected state or policy epoch.
- Declared signing algorithm.
- Declared signature purpose.

The typed response body must remain bound through
the validated body commitment.

For STATE and WITNESS, the body must also retain the
protected revision, signing digest, generation,
revocation commitment and transition identifier.

ADMIN responses must bind the declared administrative
policy and protected policy epoch.

No security-relevant response field may remain
outside the authenticated message binding.

## 9. Canonicalization

Future signed messages must use one exact canonical
byte representation.

The parser must reject:

- Duplicate JSON keys.
- Unknown signed fields.
- Unsupported numeric types.
- Noncanonical serialization.
- Unexpected field types.
- Oversized messages.
- Unsupported protocol versions.
- Noncanonical signature encoding.

The response verifier must verify the original
canonical signed content.

It must not interpret different representations
as equivalent security messages.

The signature field itself must not be included
within its own signed-message payload.

## 10. Trusted Authority-Key Policy

A future independent authority-key policy must bind:

- Authority identity.
- Authority role.
- Allowed registry scope.
- Signing-key identifier.
- Ed25519 public key.
- Signing purpose.
- Policy epoch or generation.
- Key lifecycle state.
- Validity and revocation restrictions.
- Authorized policy issuer.

The verifier must reject an authority key used
outside its assigned role or scope.

The same public-key material must not be silently
reused across independent authority domains.

An unauthorized key replacement must fail closed.

## 11. Administrative Root Circularity

The ADMIN authority creates a special trust-bootstrap risk.

The verifier must not accept a new administrative
trust root merely because the response is signed by
a key listed inside that same response.

A verified ADMIN response requires an independently
established authority root or an independently
authorized chain to that root.

A registry administrative signing policy may be
contained in the ADMIN response.

That does not make the policy independently trusted
until its ADMIN authority has been verified.

Trust cannot be established by circular self-reference.

## 12. Trust-Anchor Rotation

A future key-rotation procedure must separately address:

- Approved current authority root.
- Proposed replacement root.
- Independent administrative approval.
- Authorized transition evidence.
- Protected policy generation.
- Revocation of superseded credentials.
- Recovery after compromise.
- Prevention of older-root restoration.

A replacement root must not authorize its own enrollment.

A previously retired or compromised root must not
silently become current again.

The trust-policy epoch must be protected against rollback.

## 13. Response Verification Order

The preferred future verification sequence is:

Step 1:
Load an independently approved authority trust configuration.

Step 2:
Validate the current challenge and expected authority roles.

Step 3:
Parse the bounded canonical response.

Step 4:
Validate the response algorithm, purpose and role.

Step 5:
Resolve the signer against the independently approved
authority-key policy.

Step 6:
Validate the key's role, scope, lifecycle and policy binding.

Step 7:
Reconstruct the exact domain-separated signed bytes.

Step 8:
Cryptographically verify the Ed25519 signature.

Step 9:
Validate request identifier, challenge and response bindings.

Step 10:
Validate the typed authority-response body using existing
protected-state and authority-evidence contracts.

Step 11:
Verify response freshness and replay requirements using
separately approved operational controls.

Step 12:
Independently reconcile protected STATE and WITNESS positions.

Step 13:
Apply the existing non-authorizing security assessments.

No step grants Docker execution or production deployment.

Cryptographic verification and operational acceptance
remain separate security decisions.

## 14. Challenge and Replay Resistance

Gate 3D.12F checks that a response matches the supplied
request identifier and challenge.

This prevents some cross-request substitutions.

It does not establish:

- Challenge unpredictability.
- Challenge uniqueness.
- Nonce consumption.
- Replay rejection after a restart.
- Response freshness.
- Protection from paired authority rollback.

A valid signature on a previously used challenge
may still be replayable.

Operational anti-replay requires a reviewed challenge
generation and lifecycle mechanism.

It also requires explicit handling of repeated
request identifiers and replay-tracking state.

No nonce store or replay database is approved here.

## 15. Freshness and Trusted Time

An authentic signature does not prove that the
signed response represents the latest state.

A previously authentic response may become stale.

The future design must separately verify:

- Request binding.
- Challenge lifecycle.
- Authority freshness guarantees.
- Protected generation.
- Administrative policy epoch.
- Revocation freshness.
- Trusted time where time validity is required.

The current repository's offline verifier receives
time as a caller-provided input.

That does not establish a trusted time source.

Trusted time remains a separate operational dependency.

## 16. State and Witness Reconciliation

Authenticated STATE and WITNESS responses must be
evaluated through the existing reconciliation boundaries.

Signatures do not establish distributed transaction atomicity.

Both authorities may possess authentic but conflicting state.

The following cases remain fail closed:

- STATE ahead of WITNESS.
- WITNESS ahead of STATE.
- Different authenticated revisions.
- Different revocation-history commitments.
- Different protected generations.
- Conflicting transition identifiers.
- Unknown commit outcome.
- Unavailable authority.
- Stale authority response.

A matching pair cannot be considered current solely
because both signatures verify.

Protected monotonicity and independent rollback
resistance must also be established.

## 17. Compromised Authority Keys

The threat model must address compromise of:

- One STATE response-signing key.
- One WITNESS response-signing key.
- One ADMIN response-signing key.
- An authority trust-policy issuer.
- The application host.
- The authority-state storage service.

Key compromise response must not silently reset
the protected revision or revocation history.

The compromise of one authority must not automatically
permit an attacker to replace the other authorities'
trusted public keys.

Operational recovery requires independent approval.

## 18. Failure Handling

The future verification layer must fail closed on:

- Missing independently trusted authority key.
- Unapproved public-key substitution.
- Invalid signature.
- Unsupported algorithm.
- Incorrect signature purpose.
- Wrong role or registry scope.
- Wrong request challenge.
- Wrong request identifier.
- Noncanonical signed content.
- Retired or revoked authority key.
- Administrative trust-policy rollback.
- Stale authenticated response.
- Witness/state inconsistency.
- Uncertain commit outcome.
- Missing trusted time where required.
- Unverified authority provenance.

Failures must not trigger automatic permission escalation.

## 19. Required Adversarial Tests

The subsequent implementation gate must test:

1. Correct Ed25519 signature under a supplied key.
2. Invalid Ed25519 signature.
3. Modified response after signing.
4. Wrong authority role.
5. Wrong signature domain.
6. Wrong signing purpose.
7. Wrong registry identity.
8. Wrong request identifier.
9. Wrong challenge.
10. Wrong payload commitment.
11. Wrong authority identifier.
12. Unapproved signing-key identifier.
13. Wrong public key.
14. Cross-role public-key substitution.
15. Reused signing key across independent roles.
16. Noncanonical signed bytes.
17. Duplicate or unknown signed fields.
18. Unsupported algorithm.
19. Revoked authority key.
20. Disabled authority key.
21. Expired or not-yet-valid declared key.
22. Unapproved administrative root replacement.
23. Self-authorized ADMIN trust policy.
24. Replayed signed response.
25. Reused challenge.
26. Stale protected generation.
27. State/witness disagreement.
28. Policy-epoch disagreement.
29. Revocation-history commitment mismatch.
30. Missing independent trust configuration.
31. Authority response signed under attacker-provided key.
32. Duplicate signer identity or key material.
33. Missing trusted time.
34. Conflicting authenticated authority records.
35. Attempted Docker authorization after verification.

Tests must distinguish cryptographic signature validity
from independently established trusted provenance.

Offline test fixtures are not operationally trusted roots.

## 20. Integration Boundaries

The existing Gate 3D.12F module remains an unauthenticated
structural response-binding evaluator.

A future cryptographic verification module may build
above it without changing its existing trust claims.

No existing false operational-security flag may
be changed to true merely because a signature verifies.

In particular, the future implementation must not
equate signature verification with:

- Protected state currentness.
- Replay prevention.
- Durable commit confirmation.
- Rollback resistance.
- Runtime isolation.
- Docker execution permission.
- Production authorization.

## 21. Implementation Sequence

### Gate 3D.12H - Pure Cryptographic Verification

Implement a strict Ed25519 authority-response signature
verifier under caller-provided authority-key policies.

Add canonical message verification and adversarial tests.

Keep independent provenance and operational acceptance false.

### Gate 3D.12I - Independent Trust Policy Contracts

Define independently provisioned authority trust-policy
interfaces, protected policy epochs and rotation constraints.

Test unauthorized substitutions and bootstrap circularity.

### Gate 3D.12J - Replay and Freshness Architecture

Define trusted challenge generation, challenge lifecycle,
replay-state requirements and trusted-time dependencies.

Do not equate a nonce comparison with full freshness.

### Later Operational Gates

Evaluate and approve a real independently administered
trust service, transactional state service and witness.

Implement authenticated adapters only after a specific
technology and threat model have been reviewed.

## 22. Acceptance Criteria

This architecture decision can be reviewed when:

1. Authority roles and signing domains are separated.
2. Trust anchors are independent of responses.
3. The ADMIN bootstrap circularity is explicitly prohibited.
4. Canonical signed-message requirements are defined.
5. Authority-key rotation requirements are established.
6. Challenge matching and replay prevention are distinguished.
7. Signature validity and state currentness remain separate.
8. State/witness split-commit behavior remains fail closed.
9. No runtime or deployment permission is introduced.
10. The existing 921-test security suite remains passing.

## 23. Final Decision

Future Basics will adopt an independently anchored,
role-separated cryptographic verification architecture
for security-authority responses.

Ed25519 is the preferred laboratory response-signature
algorithm, with independent domain-separated signed bytes.

Actual authority-key provenance, durable replay protection,
trusted time, rollback prevention and operational acceptance
remain subject to later gates and independent approval.

Gate 3D.12G authorizes architecture review only.

Docker execution, automatic retries and production
deployment remain blocked.
