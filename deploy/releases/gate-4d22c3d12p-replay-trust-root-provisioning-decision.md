# Gate 4D.22C.3D.12P - Independent Replay Trust-Root Provisioning and Policy Authentication

Status: ARCHITECTURE ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retries: DENIED
Production deployment: DISABLED
Independent replay trust roots: NOT PROVISIONED
Operational policy authentication: NOT IMPLEMENTED
Protected replay policy storage: NOT IMPLEMENTED
Protected policy rollback witness: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Operational replay authority adapters: NOT IMPLEMENTED
Durable replay-state authority: NOT IMPLEMENTED
Independent replay-state witness: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Define how Future Basics will establish and maintain
independently trusted public keys for its replay-state
authority and independent replay rollback witness.

The design must address initial enrollment, authenticated
policy delivery, approved key rotation, key revocation,
policy rollback detection and emergency recovery.

Gate 3D.12P defines architecture requirements only.

It does not enroll keys, create credentials, authenticate
real services, change policy files or deploy infrastructure.

## 2. Existing Security Foundation

Gate 3D.12H:
Offline Ed25519 verification for registry STATE, WITNESS
and ADMIN responses under caller-supplied public keys.

Gate 3D.12I:
Pure authority key-policy continuity for registry roles.

Gate 3D.12J:
Challenge lifecycle and replay-resistance architecture.

Gate 3D.12K:
Pure challenge lifecycle and replay classification.

Gate 3D.12L:
Protected replay authority and recovery architecture.

Gate 3D.12M:
Pure replay positions, witness checkpoints and recovery
classifications.

Gate 3D.12N:
Replay authority authentication and signed-evidence
architecture.

Gate 3D.12O:
Offline Ed25519 verification for REPLAY_STATE and
REPLAY_WITNESS under caller-supplied key policies.

No previous gate establishes independent operational
trust-root provenance.

## 3. Fundamental Trust Problem

The Gate 3D.12O verifier can prove that a message was
signed by the private key corresponding to a supplied
public key.

It cannot determine whether that key belongs to the
approved replay authority.

An attacker may supply:

- An attacker-controlled public key.
- An internally consistent forged policy.
- A valid signature under the forged key.
- Matching replay-state and witness records.
- A fabricated policy history and checksum chain.

Cryptographic correctness under an untrusted key
does not create authority.

This problem must be resolved outside the response
whose authenticity is being evaluated.

## 4. Trust Domains

The future design distinguishes:

A. Application and replay verification runtime.

B. REPLAY_STATE operational signing identity.

C. REPLAY_WITNESS operational signing identity.

D. Replay trust-policy issuing authority.

E. Independent policy approval process.

F. Protected policy-state authority.

G. Independent policy rollback witness.

H. Emergency recovery authority.

I. Registry-state trust and administrative controls.

These are conceptual security boundaries.

Distinct class names, hostnames or key labels do not
establish separate administrative control.

The actual infrastructure and custody model require
an explicit independent review.

## 5. Replay Roles

The two replay signing roles are:

REPLAY_STATE
The transactional replay-state authority.

REPLAY_WITNESS
The separately controlled replay rollback witness.

They must not inherit the authority of registry:

STATE
WITNESS
ADMIN

Their keys must use the role-specific signing purposes
and cryptographic domains established in Gate 3D.12O.

A response from one role cannot authorize another role.

## 6. Approved Trust-Root Source

The verifier must obtain its expected replay authority
trust roots from an independently approved and protected
source.

A future approved source may be a protected configuration
store, trusted provisioning service or another reviewed
security mechanism.

This gate does not select a vendor or product.

The source must be administered outside the trust domain
of ordinary untrusted response payloads.

The source's integrity, availability, authorization
controls and rollback resistance must be evaluated.

Ordinary Git repository content is not automatically
an independently trusted root of authority.

## 7. No Trust on First Use

Receiving the first replay authority response does
not authorize its included public key.

A first successful Ed25519 signature does not establish
that the signer is the expected replay authority.

Automatic trust-on-first-use enrollment is prohibited.

A new public key must be approved through an independent
out-of-band identity and enrollment procedure.

The verifier must not silently accept a new root merely
because no previous root is configured.

## 8. Bootstrap Procedure

Initial replay trust-root enrollment must be an
explicitly authorized process.

The procedure must establish:

- The approved registry identity.
- The approved replay-ledger identity.
- Both replay authority identities.
- The role assigned to each authority.
- The approved signing-key fingerprints.
- The approved cryptographic algorithms.
- The approved verification purposes.
- The initial policy identifier and epoch.
- The initial recovery epoch.
- Administrative owners and separation of duties.
- Evidence of independent identity verification.
- The protected initial policy commitment.
- The initial independent rollback checkpoint.

The exact approval process must be reviewed before
the first operational enrollment.

A caller-created genesis manifest is not proof that
bootstrap was approved.

## 9. Independent Identity Verification

Before trusting a replay public key, the provisioning
process must verify the identity of the intended
authority through an independently established channel.

A public key carried in the response being verified
is not a valid independent channel.

The verification process must bind the key to:

- Authority role.
- Approved authority identifier.
- Registry scope.
- Replay-ledger scope.
- Signing purpose.
- Key identifier.
- Current policy epoch.
- Approved lifecycle status.

A matching key identifier alone is insufficient.

## 10. Trust-Policy Issuer

Replay authority signing keys and the entity that
approves replay trust-policy changes are different
security responsibilities.

The policy issuer must have separately approved
administrative authority.

A REPLAY_STATE signing key must not approve its
own enrollment or replacement.

A REPLAY_WITNESS signing key must not approve its
own enrollment or replacement.

A registry ADMIN response must not automatically
authorize changes to replay trust roots.

The policy issuer's authority and credentials require
their own independent bootstrap and protection.

## 11. Administrative Separation

The future security review must identify who can:

- Create replay signing keys.
- Request key enrollment.
- Approve a new public key.
- Activate or disable signing keys.
- Revoke compromised keys.
- Publish an approved policy.
- Advance the protected policy epoch.
- Restore an unavailable trust-policy authority.
- Authorize emergency root recovery.

No single ordinary application role may acquire all
these permissions by default.

Any administrative overlap must be explicitly justified,
reviewed and documented.

## 12. Replay Trust-Policy Snapshot

A proposed authenticated replay trust-policy snapshot
must bind:

- Policy format and protocol versions.
- Registry identity.
- Replay-ledger identity.
- Policy identifier.
- Policy epoch.
- Protected policy generation.
- Recovery epoch.
- Previous approved policy commitment.
- Policy transition identifier.
- Pinned replay authority identities.
- Complete approved signing-key records.
- Key lifecycle and revocation history.
- Approved policy issuer identity.
- Policy approval reference.
- Applicable policy effective conditions.

The exact immutable wire representation will be defined
in a separate implementation gate.

## 13. Existing Policy Compatibility

Gate 3D.12O currently defines:

ReplayResponseKey
ReplayResponseKeyPolicy

ReplayResponseKeyPolicy contains:

- Policy identifier.
- Declared policy epoch.
- Tuple of replay verification keys.

The policy is caller-supplied and unauthenticated.

A future protected snapshot may embed that existing
key policy as its logical verification-key payload.

It must not treat the existing key policy as
independently approved solely because it validates.

Operational policy provenance requires separate evidence.

## 14. Key Records

Each signing-key record must bind:

- Role and authority identifier.
- Key identifier.
- Public-key material and approved fingerprint.
- Algorithm.
- Role-specific signing purpose.
- Lifecycle status.
- Declared validity interval.
- Enrollment policy epoch.
- Relevant retirement or revocation reference.

The verifier must reject unknown or ambiguous identities.

A public key must not silently move between roles.

A key identifier must not be rebound to different
public-key material.

## 15. Policy Commitment

The future policy format requires a deterministic
canonical serialization.

Policy commitments must use a versioned,
domain-separated cryptographic hash.

Commitments must cover the complete security-relevant
policy snapshot, including role bindings and history.

A SHA-256 commitment provides structural integrity
relative to a trusted reference.

It does not, by itself, authenticate policy approval.

An attacker may compute valid commitments for
attacker-created snapshots.

## 16. Authenticated Policy Distribution

A future policy distribution mechanism must ensure that
the verifier receives only independently approved
policy material.

The verifier must separately validate:

- Approved policy issuer identity.
- Correct signed policy purpose.
- Current trusted issuer key.
- Complete canonical policy bytes.
- Approved policy epoch.
- Protected policy generation.
- Recovery epoch.
- Previous policy continuity.
- Revoked and disabled key history.
- Independent rollback checkpoint.

The mere availability of a policy endpoint does
not establish its trustworthiness.

Network transport security alone is not sufficient
to establish policy approval.

## 17. Policy Authentication Ordering

The future operational verification order must be:

1. Load an independently provisioned trust anchor.
2. Verify the trust source and its approved scope.
3. Read the current protected policy position.
4. Independently verify policy rollback protection.
5. Obtain the candidate policy.
6. Verify its canonical signed representation.
7. Verify issuer identity under the approved root.
8. Validate policy continuity and lifecycle rules.
9. Check current revocation requirements.
10. Establish the usable replay response-key policy.
11. Verify REPLAY_STATE and REPLAY_WITNESS responses.
12. Separately assess freshness and replay-state currentness.

The response must not select its own trust source.

The existing Gate 3D.12O verifier performs step 11
only under caller-supplied trust assumptions.

## 18. Ordinary Key Rotation

Ordinary key rotation may enroll a new signing key
without changing the pinned replay authority identity.

The new key must have:

- A new unique key identifier.
- Distinct public-key material.
- Correct role and signing purpose.
- Independently approved enrollment evidence.
- A protected policy transition.
- An updated policy epoch and generation.

A key replacement must not overwrite the historical
record of the previous key.

An ordinary rotation must not change the recovery epoch.

## 19. Key Lifecycle

The proposed ordinary key lifecycle is:

active -> active
active -> disabled
active -> revoked
disabled -> disabled
disabled -> revoked
revoked -> revoked

Disabled or revoked keys must not silently return
to active status.

The same public key must not be re-enrolled as a
new signing identity to bypass revocation history.

A key-material change requires a new key identity.

Emergency exceptions require an independently reviewed
recovery protocol rather than ordinary rotation.

## 20. Revocation

Revocation must be represented in an independently
approved policy transition.

A revoked key must not be accepted merely because
an older snapshot lists it as active.

The verifier must evaluate the applicable protected
current policy and revocation evidence.

The application must not choose an earlier policy
epoch simply to make signature verification pass.

Actual propagation and enforcement latency require
separate operational requirements.

## 21. Declared Key Validity

Gate 3D.12O checks declared signing-key validity
using a caller-supplied timezone-aware assessment time.

That mechanism does not establish trusted time.

An operational system must use a separately approved
freshness or trusted-time mechanism.

A valid signature within a declared interval does
not override a later approved key revocation.

A restored older system clock or policy snapshot
must not silently reactivate a retired key.

## 22. Policy Epoch Continuity

An ordinary policy transition must:

- Advance the policy epoch exactly once.
- Advance the protected policy generation exactly once.
- Preserve the recovery epoch.
- Preserve pinned authority identities.
- Use a fresh transition identifier.
- Commit to the prior approved policy position.
- Preserve required historical key records.
- Change at least one approved lifecycle element.

These are proposed logical continuity requirements.

A separate protected transaction and approval
protocol is needed for real policy advancement.

## 23. Policy Rollback Protection

The policy-state authority must maintain a protected
monotonic policy generation and commitment.

An independently controlled rollback witness must
record the accepted protected policy position.

A restored older policy database must not silently
become the accepted current trust policy.

The rollback witness must be independent of the
administrative domain capable of restoring the
primary policy database.

A local hash chain alone is not rollback protection.

## 24. Primary/Witness Split Commits

The policy-state authority and policy rollback witness
must not be assumed to share an atomic transaction.

Possible outcomes include:

- Both remain at the previous policy position.
- Primary policy state advances before its witness.
- Witness advances while primary policy state is missing.
- Both report the same proposed policy position.
- Primary and witness report conflicting commitments.
- A required authority is unavailable.
- A transition acknowledgement is lost.

Each outcome needs a reviewed fail-closed reconciliation
procedure.

Matching declarations alone do not prove durable
commitment or independently trusted currentness.

## 25. Policy Epoch and Replay-State Alignment

The authenticated replay trust-policy epoch must
be reconciled with the declared epoch in:

ReplayReadChallenge
ReplayProtectedPosition
ReplayResponseKeyPolicy
SignedReplayResponse

A match is necessary for the applicable protocol
but not sufficient for operational trust.

The authoritative current policy epoch must come
from independently protected policy evidence.

Policy epoch agreement must not be asserted solely
from caller-supplied objects.

A key rotation must not silently bypass outstanding
replay challenge and consumption controls.

## 26. Rotation During Pending Requests

The system must explicitly handle a key-policy change
between request reservation and response verification.

A signed response under a key that is now revoked
must not silently pass using the older policy.

The verifier must obtain the relevant independently
approved policy decision before accepting a response.

If this decision is unavailable, the request must
remain blocked or uncertain.

No automatic request retry is approved.

## 27. Emergency Key Compromise

Compromise of a replay signing key requires:

- Immediate incident classification.
- Preservation of relevant evidence.
- Independent revocation authorization.
- Assessment of potentially affected signatures.
- Review of outstanding request lifecycles.
- Reconciliation with replay-state and policy witnesses.
- Separately approved recovery decisions.

A compromised replay authority key must not
self-authorize its replacement.

The process must not erase consumed response history.

## 28. Emergency Trust-Root Recovery

Compromise or loss of the policy-issuing trust root
requires a separately controlled recovery process.

Recovery must bind:

- Approved recovery authority identity.
- Independent recovery approval evidence.
- Affected registry and ledger scope.
- Last independently established policy checkpoint.
- Prior and proposed recovery epochs.
- New authorized trust-root commitment.
- Superseded or revoked root identities.
- Transition and incident references.
- Protected recovery audit evidence.

A policy signed only by the compromised root
cannot independently authorize its own recovery.

No automated root replacement is implemented here.

## 29. Bootstrap and Recovery Separation

An empty policy database does not authorize
creation of a new trusted policy genesis.

Application startup must not initiate trust-root
enrollment automatically.

A disaster-recovery restore must not bypass
independent root verification.

Bootstrap and emergency recovery must require
different, explicit administrative procedures.

The proposed recovery epoch must be protected
against replay or rollback.

## 30. Key Custody and Isolation

Future operations must define secure private-key
custody for replay signing and policy approval.

The selected solution requires an explicit review of:

- Key generation.
- Key export restrictions.
- Service identity.
- Access control.
- Signing permission boundaries.
- Administrative separation.
- Backup and recovery.
- Key destruction.
- Audit evidence.
- Compromise response.

A hardware security module or cloud key manager may
be considered, but neither is selected or approved
by this architecture decision.

## 31. Operational Failure Handling

Operational trust must fail closed when:

- No independently approved trust root exists.
- The claimed authority identity cannot be verified.
- The trusted policy issuer is unavailable.
- A policy signature is invalid.
- Policy continuity cannot be established.
- Protected policy currentness is unknown.
- A required key is revoked or disabled.
- The policy epoch conflicts with replay state.
- A policy rollback is suspected.
- The policy witness is unavailable.
- An approval or recovery decision is missing.
- Trusted freshness cannot be established.

No caller-supplied success flag may override
these missing guarantees.

## 32. Audit and Governance

Future audit evidence must record:

- Trust-root enrollment or recovery reference.
- Independent approvers and authorization scope.
- Policy identifier, epoch and generation.
- Canonical policy commitment.
- Prior and proposed protected commitments.
- Affected replay authority roles.
- Key identifiers and fingerprints.
- Lifecycle changes and revocations.
- Policy and witness reconciliation outcomes.
- Responsible operational and security owners.
- Incident reference where applicable.

Private signing keys and authentication credentials
must not be included in ordinary audit records.

Audit logs are not substitutes for a protected
policy rollback witness.

## 33. Implementation Separation

Gate 3D.12P does not change the Gate 3D.12O
cryptographic signature verifier.

It does not introduce a production trust provider,
new root credentials, live verification endpoints
or policy transaction services.

A future gate may implement a pure, caller-supplied
replay trust-policy continuity model.

The following remain separately gated:

- Independent trust-root provisioning.
- Protected policy authority integration.
- Policy signature verification.
- Trusted freshness verification.
- Durable replay-state authority integration.
- Recovery execution.
- Deployment authorization.

## 34. Future Adversarial Tests

The next implementation must consider:

1. Structurally valid caller-supplied policy.
2. Forged policy with attacker-generated keys.
3. Bootstrap without independent root approval.
4. Invalid policy issuer identity.
5. Wrong registry or replay-ledger identity.
6. Wrong replay authority role binding.
7. Reused signing-key identifiers.
8. Reused key material across roles.
9. Signing-key material replaced under one ID.
10. Ordinary key enrollment with wrong purpose.
11. Policy epoch not advancing.
12. Protected generation not advancing.
13. Reused policy transition identifier.
14. Incorrect previous policy commitment.
15. Removal of historical keys.
16. Reactivation of disabled keys.
17. Reactivation of revoked keys.
18. Revoked key re-enrolled with a new ID.
19. Valid ordinary rotation retaining role identity.
20. Unauthorized replay authority identity change.
21. Unauthorized recovery epoch change.
22. Invalid or missing revocation record.
23. Old active policy after an approved revocation.
24. Old signed response under a revoked key.
25. Pending request during key rotation.
26. Caller-supplied assessment time.
27. Matching forged policy and witness positions.
28. Primary policy ahead of witness.
29. Policy witness ahead of primary.
30. Restored old policy database.
31. Missing independent rollback checkpoint.
32. Lost policy transition acknowledgement.
33. Emergency recovery without approval.
34. Compromised root approving its own replacement.
35. Stale replay-state policy epoch.
36. Distinct labels with shared key custody.
37. Trust-on-first-use enrollment attempt.
38. Valid signature under an unapproved public key.
39. Invalid or unexpected policy wire fields.
40. Attempted Docker authorization after policy validation.

Pure tests must not claim independent policy approval
or operational trust-root authentication.

## 35. Acceptance Criteria

Gate 3D.12P is ready for review when:

1. Replay trust-root sources are independently defined.
2. Initial root enrollment requires external approval.
3. Trust-on-first-use enrollment is prohibited.
4. Policy issuer and response signers are separated.
5. Replay STATE and WITNESS retain distinct roles.
6. Trust-policy contents and epochs are specified.
7. Key rotation preserves continuity and history.
8. Revocation cannot be bypassed with old policies.
9. Policy rollback protection is independently required.
10. Split commitments fail closed.
11. Emergency root recovery requires separate authority.
12. Caller-supplied time remains untrusted.
13. No operational keys or services are introduced.
14. The existing security test suite remains passing.
15. Docker, retries and deployment remain blocked.

## 36. Final Decision

Future Basics must independently establish, protect
and authenticate replay authority trust roots before
using replay response signatures as operational
authority evidence.

The existing Ed25519 verifier, caller-supplied policies,
local commitments and simulated witness checkpoints
do not independently establish trusted provenance.

Gate 3D.12P approves architecture review only.

It does not authorize trust-root provisioning,
operational replay-state verification, recovery,
Docker execution or production deployment.
