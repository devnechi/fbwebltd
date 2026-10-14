# Gate 4D.22C.3D.12R - Replay Policy Issuer Authentication and Protected Currentness

Status: ARCHITECTURE ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retries: DENIED
Production deployment: DISABLED
Independent issuer trust roots: NOT PROVISIONED
Operational issuer authentication: NOT IMPLEMENTED
Authenticated policy distribution: NOT IMPLEMENTED
Protected policy-state authority: NOT IMPLEMENTED
Independent policy rollback witness: NOT IMPLEMENTED
Durable conditional policy commits: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Automatic policy recovery: NOT IMPLEMENTED
Operational replay-state service: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Define how a future replay trust-policy issuer is authenticated
and how the latest approved replay policy position is established.

The architecture must address:

- Independent issuer identity.
- Trust-root bootstrap.
- Canonical signed policy approval.
- Protected policy currentness.
- Independent rollback witnesses.
- Conditional policy transitions.
- Split-commit reconciliation.
- Revocation and recovery evidence.

This gate is architecture-only.

It introduces no signing service, credentials, protected
storage adapter, network interface, retries or deployment.

## 2. Existing Security Foundation

Gate 3D.12H implements offline Ed25519 verification for
registry STATE, WITNESS and ADMIN authority responses.

Gate 3D.12I defines pure registry authority policy continuity.

Gate 3D.12L defines protected replay-state authority requirements.

Gate 3D.12M implements pure protected replay-state contracts.

Gate 3D.12N defines replay authority authentication architecture.

Gate 3D.12O implements offline signature verification for
REPLAY_STATE and REPLAY_WITNESS under caller-supplied keys.

Gate 3D.12P defines independent replay trust-root provisioning.

Gate 3D.12Q implements pure replay trust-policy continuity,
revocation and rollback-observation classification.

None of these gates establishes independently approved
operational issuer keys or protected policy currentness.

## 3. Existing Types

The architecture must preserve the existing contracts:

ReplayResponseKey
ReplayResponseKeyPolicy
ReplayPolicyRoleBindings
ReplayPolicySnapshot
ReplayPolicyCheckpoint
ReplayPolicyTransitionAssessment
ReplayPolicyReconciliationAssessment

ReplayPolicySnapshot already binds:

- Registry and replay-ledger identities.
- Policy format and policy identifier.
- Policy epoch and generation.
- Recovery epoch.
- Previous policy commitment.
- Transition identifier.
- Issuer identifier.
- Approval reference.
- Pinned replay authority identities.
- Complete replay response-key policy.

The issuer identifier and approval reference are currently
caller-supplied strings, not authenticated evidence.

## 4. Fundamental Trust Problem

An attacker can create a structurally valid policy,
calculate its commitment and build a consistent history.

The attacker may also create an Ed25519 key pair and sign
the fabricated policy with the private key.

A mathematically valid signature under a caller-supplied
key does not establish that the issuer was approved.

Likewise, matching primary and witness declarations
do not prove the declared generation is the latest one.

Issuer authentication, approval authority, policy
currentness and durable storage are distinct guarantees.

## 5. Threat Model

The architecture must address:

- Forged policy issuer identities.
- Self-issued policy trust roots.
- Unapproved public-key substitution.
- Compromised replay response signing keys.
- Compromised policy issuer signing keys.
- Unauthorized signing-key enrollment.
- Revoked key reactivation.
- Signed but outdated policies.
- Fabricated approval references.
- Substituted registry or ledger identities.
- Policy epoch rollback.
- Policy generation rollback.
- Replay of an earlier valid issuer signature.
- Forged primary and witness checkpoints.
- Database restoration to a prior policy.
- Lost conditional-commit acknowledgements.
- Split commits between primary and witness.
- Unauthorized recovery-epoch changes.
- Application-runtime compromise.

A valid signature cannot override failed currentness
or independent approval requirements.

## 6. Separate Trust Domains

Required conceptual trust domains are:

A. Application and verification runtime.

B. Replay STATE response-signing authority.

C. Replay WITNESS response-signing authority.

D. Replay policy issuer.

E. Independent policy approval authority.

F. Protected policy-state authority.

G. Independent policy rollback witness.

H. Root enrollment and emergency recovery authority.

I. Registry trust-policy and administrative authorities.

A distinct software role is not proof of separate
key custody or administrative control.

Shared hosting, credentials and recovery privileges
require independent failure-domain assessment.

## 7. Policy Issuer Identity

The policy issuer must have a separately approved identity.

Its identity must be established before verifying
a newly received policy.

Required binding includes:

- Approved issuer identifier.
- Approved public-key fingerprint.
- Approved signing algorithm.
- Policy-signing purpose.
- Registry and replay-ledger scope.
- Permitted policy identifiers.
- Permitted enrollment and rotation authority.
- Issuer-key lifecycle status.

Replay STATE and replay WITNESS keys must not automatically
receive policy-issuer signing authority.

The existing registry ADMIN role must not implicitly
receive replay policy-issuer authority.

## 8. Independent Root Bootstrap

The first issuer trust root must be enrolled through
a separately approved out-of-band process.

Bootstrap must establish:

- Identity of the authorized policy issuer.
- Public-key fingerprint verified independently.
- Exact registry and replay-ledger scope.
- Approved policy-signing purpose.
- Initial policy identifier and epoch.
- Initial policy generation and commitment.
- Initial recovery epoch.
- Protected initial policy-state position.
- Independent initial rollback checkpoint.
- Administrative ownership and approval evidence.

No first response may self-enroll its own trust root.

No caller-created genesis snapshot is bootstrap proof.

Trust-on-first-use is not approved.

## 9. Trust Anchor Custody

The future trust anchor must be protected against
unauthorized replacement by the application runtime.

Its custody model must document:

- Enrollment authority.
- Administrative permissions.
- Key distribution.
- Key rotation.
- Key revocation.
- Protected backup and recovery.
- Audit evidence.
- Independence from replay response signers.
- Protection from application database restoration.

This gate does not select a hardware security module,
cloud key manager, certificate authority or vendor.

Such infrastructure requires separate assessment.

## 10. Distinct Signing Purposes

The replay policy issuer must use a signing purpose
separate from REPLAY_STATE and REPLAY_WITNESS.

Proposed conceptual domain:

FBWEB-LAB-REPLAY-POLICY-ISSUER-SIGNATURE-V1

The exact signed-byte prefix must include an
unambiguous domain separator.

Registry administrative signatures must not validate
as replay policy issuer signatures.

Replay response signatures must not validate as
policy approvals.

A signing purpose is a cryptographic boundary,
not evidence of independent key administration.

## 11. Signed Policy Envelope

A future signed policy envelope must bind:

- Envelope and protocol versions.
- Policy issuer identifier.
- Issuer signing-key identifier.
- Signing purpose and algorithm.
- Registry identity.
- Replay-ledger identity.
- Policy identifier.
- Policy epoch.
- Policy generation.
- Recovery epoch.
- Previous policy commitment.
- Current policy commitment.
- Policy transition identifier.
- Approval reference.
- Exact canonical policy snapshot commitment.
- Signature.

The envelope must identify the signed policy exactly.

A signature over only a mutable filename or URL
is insufficient.

## 12. Canonical Policy Serialization

The future wire format must use one reviewed,
deterministic canonical representation.

It must reject:

- Duplicate object keys.
- Missing required fields.
- Unknown security-relevant fields.
- Noncanonical field ordering or encoding.
- Ambiguous integer representations.
- Boolean values substituted for integers.
- Numeric overflows.
- Invalid registry or ledger identity.
- Incorrect signing purpose.
- Unsupported algorithms.
- Noncanonical signature representation.

The exact schema and size limits require a
separate implementation decision.

## 13. Policy Commitment Binding

The issuer's signed envelope must bind the
canonical commitment of the full ReplayPolicySnapshot.

That commitment must include:

- Pinned replay authority identities.
- Complete signing-key history.
- All key lifecycle statuses.
- Issuer identifier and approval reference.
- Policy and recovery epochs.
- Policy generation.
- Previous commitment and transition identity.

A domain-separated hash proves only a binding
between specified bytes and the calculated digest.

It does not prove that an issuer was independently approved.

## 14. Issuer Verification Ordering

The future issuer verification sequence must:

1. Obtain a previously approved issuer trust anchor.
2. Authenticate the trust-anchor source.
3. Establish the expected issuer identity and scope.
4. Parse the canonical signed policy envelope.
5. Reject unexpected protocol and signing purposes.
6. Check registry, ledger and policy identity.
7. Check the declared issuer and signing-key identity.
8. Verify the signature under the approved issuer key.
9. Validate the complete embedded policy snapshot.
10. Verify continuity from an independently established
    previous policy position.
11. Reconcile the primary protected policy state and
    independent rollback witness.
12. Establish the relevant independently verified
    current policy position.
13. Check applicable key revocations and lifecycle rules.
14. Only then select replay response verification keys.

No missing step may be replaced by a caller-supplied
success indicator.

## 15. Signature Validity Versus Approval

A policy signature can establish that the message was
signed under a particular verification key.

It does not automatically establish:

- Independent issuer approval.
- Valid administrative authorization.
- Protected policy generation.
- Durable conditional policy commitment.
- Fresh policy distribution.
- Latest approved policy currentness.
- Trusted time.
- Protected revocation enforcement.

Future assessments must expose these guarantees
as separately named properties.

## 16. Independent Policy Approval

A signed policy transition must have independently
authorized approval evidence.

The existing ReplayPolicySnapshot.approval_reference
is a label only.

A reference that matches an approval database entry
is insufficient unless that database and its approval
records are independently authenticated.

The approval process must define:

- Authorized approving roles.
- Required separation of duties.
- Change scope.
- Before and after policy commitments.
- Affected signing keys.
- Transition identifier.
- Policy epoch and generation.
- Approval validity and incident references.

This architecture introduces no approval service.

## 17. Issuer Key Rotation

Policy-issuer key rotation differs from ordinary
REPLAY_STATE and REPLAY_WITNESS key rotation.

An issuer must not replace its own root merely by
presenting a newly signed key inside a candidate policy.

Issuer root rotation requires an independently approved
trust-anchor transition procedure.

The procedure must establish continuity with a
previously trusted root or another independently
approved recovery authority.

An unavailable or compromised old root requires
the separate emergency recovery protocol.

## 18. Policy-Key Lifecycle

The ordinary replay response-key lifecycle defined
in Gate 3D.12Q remains unchanged:

active to active, disabled or revoked.

disabled to disabled or revoked.

revoked to revoked only.

Historical key identifiers, public-key material,
purposes and declared validity intervals remain immutable.

A new key requires a new identity and new public-key material.

No older policy may be selected simply to restore
a previously revoked key.

## 19. Protected Policy Position

The future policy-state authority must maintain an
authenticated protected policy position containing:

- Registry identity.
- Replay-ledger identity.
- Policy identity.
- Policy epoch.
- Protected policy generation.
- Policy snapshot commitment.
- Recovery epoch.
- Transition identifier.
- Previous protected-position commitment.

The policy-state position requires a reviewed canonical
wire format and authenticated authority evidence.

An application-controlled policy cache is not
a protected policy-state authority.

## 20. Independent Policy Rollback Witness

The policy rollback witness must record an independently
protected forward-only commitment to the accepted
policy-state position.

The witness must not share the same rollback domain
as the primary policy database.

A restoration of the primary database must not silently
restore the witness to the same older position.

The witness must bind policy identity, epoch, generation,
commitment, recovery epoch and transition identity.

Matching caller-created ReplayPolicyCheckpoint objects
do not demonstrate this requirement.

## 21. Witness Authentication

The future verifier must know the witness identity
through an independently established trust source.

The witness must provide authenticated evidence of:

- Its expected role and authority identity.
- Registry and replay-ledger scope.
- Policy identifier.
- Protected checkpoint commitment.
- Policy epoch and generation.
- Recovery epoch.
- Relevant request and challenge.
- Applicable signing-key identity.

Witness authentication does not, by itself,
prove forward-only storage or independent administration.

Those guarantees require separate operational review.

## 22. Protected Currentness

A valid historical signature may remain mathematically
valid after its policy is superseded.

The verifier must establish the latest independently
accepted policy position rather than relying solely
on a signature's validity.

Currentness requires authenticated reads from the
protected policy-state authority and rollback witness.

It also requires independently established trust
anchors, continuity, revocation information and
the applicable freshness mechanism.

A reported latest generation is not proof of
latest-generation currentness.

## 23. Conditional Policy Commit

An ordinary proposed policy transition must bind:

- Expected policy generation and commitment.
- Expected policy epoch and recovery epoch.
- Candidate policy commitment.
- Previous accepted protected-position commitment.
- Transition identifier.
- Approved issuer and approval evidence.
- Expected independent witness checkpoint.

The policy-state authority must perform actual atomic
conditional updates under a separately approved design.

A pure Python transition assessment is not
a durable compare-and-swap operation.

## 24. Witness Advancement

Following a primary policy commit, any witness advancement
must use an authenticated expected checkpoint.

A stale witness update must not overwrite a newer checkpoint.

The primary write and independent witness advancement
must not be assumed to be one atomic transaction.

A successful primary response alone must not authorize
use of the newly proposed policy while witness continuity
remains unresolved.

No automated witness catch-up is approved by this gate.

## 25. Split-Commit Cases

The architecture must distinguish:

R1: Both authorities report the previous policy position.

R2: Primary policy state is ahead of the witness.

R3: Policy witness is ahead of primary state.

R4: Both authorities report the proposed policy position.

R5: Authorities report unexpected conflicting commitments.

R6: Primary authority is unavailable.

R7: Witness authority is unavailable.

R8: Both authorities are unavailable.

All cases require authenticated evidence before any
operational conclusion can be reached.

Matching reported positions remain insufficient
without independent freshness and durable-currentness proof.

## 26. Unknown Commit Outcomes

A lost acknowledgement must not be interpreted
as proof that a policy transition failed.

A timeout must not automatically permit resubmission
of a policy change.

The future protocol must bind and inspect:

- Original transition identifier.
- Expected previous policy position.
- Candidate policy commitment.
- Reported protected state.
- Reported witness checkpoint.
- Durable outcome evidence.

Until independently authenticated reconciliation
establishes the outcome, policy use must remain blocked
where the unresolved transition affects currentness.

Automatic retries remain denied.

## 27. Rollback Detection

If primary policy generation falls below an independently
established checkpoint, the verifier must fail closed.

If the witness reports a lower generation than its
previously protected accepted checkpoint, the verifier
must treat witness rollback or compromise as possible.

Equal generations with different commitments are
integrity conflicts.

Forward generations with unverified ancestry are
not automatically accepted.

No automatic rollback repair is implemented here.

## 28. Replay-State Policy Alignment

After establishing the current trusted replay policy,
the verifier must compare it with:

ReplayReadChallenge.policy_epoch

ReplayProtectedPosition.policy_epoch

ReplayResponseKeyPolicy.epoch

SignedReplayResponse.policy_epoch

The relevant recovery epoch must also agree.

The comparison must use independently established
policy currentness, not merely caller-supplied equality.

A stale policy must not authorize acceptance
of a replay-state response from a revoked signer.

## 29. Bootstrap Circularity

The system must not claim protected policy currentness
by using a key whose own authority depends on the
unverified policy being evaluated.

Bootstrap requires an independently approved initial
trust root and protected genesis position.

Later policy changes must be anchored to previously
established trusted state.

An empty local database or missing configuration
must never trigger automatic trust-root enrollment.

## 30. Trusted Time and Freshness

A caller-provided timezone-aware timestamp is not
independently trusted time.

An operational design must specify how freshness
of issuer, policy authority and witness evidence
will be established.

A signature under an unexpired key is not sufficient
to establish that the policy remains current.

Revocation and protected policy currentness must
not be bypassed by an older clock value.

This gate does not select a trusted-time provider.

## 31. Administrative Recovery

Recovery of compromised policy issuer keys, lost
protected policy state or an unavailable witness
requires independently approved recovery evidence.

The process must bind:

- Recovery incident identity.
- Last independently verified checkpoint.
- Approved recovery authority.
- Affected registry and ledger scope.
- Prior and proposed recovery epochs.
- Approved replacement trust-root commitment.
- Revoked or superseded issuer identities.
- Recovery transition identifier.
- Audit evidence and responsibilities.

A compromised issuer must not authorize its own
replacement merely through self-signed evidence.

No operational recovery action is implemented.

## 32. Audit Requirements

Future audit evidence should identify:

- Trust-root and issuer identity.
- Issuer signing-key identifier.
- Policy signature commitment.
- Policy identifier, epoch and generation.
- Previous and proposed policy commitments.
- Approval reference and independently verified approval.
- Key enrollment or revocation actions.
- Primary and witness observations.
- Reconciliation classification.
- Uncertain transaction outcomes.
- Relevant recovery or incident reference.

Private keys and authentication credentials
must never be logged.

Normal application logs are not independent
rollback-protection evidence.

## 33. Future Implementation Scope

A subsequent gate may implement pure offline
issuer-signature evidence contracts and tests:

- Immutable issuer-key declarations.
- Immutable policy approval envelopes.
- Canonical signed policy bytes.
- Role-separated Ed25519 issuer verification.
- Policy commitment binding.
- Caller-supplied trust-root shape validation.
- Logical policy checkpoint comparisons.
- Immutable fail-closed classifications.

All inputs must remain caller-supplied unless
a separately approved architecture changes that boundary.

Operational issuer authentication requires further gates.

## 34. Future Adversarial Tests

Tests should include:

1. Correct policy issuer signature under a supplied key.
2. Wrong issuer signing purpose.
3. REPLAY_STATE signature substituted for issuer signature.
4. REPLAY_WITNESS signature substituted for issuer signature.
5. Registry ADMIN signature substituted for issuer signature.
6. Unknown issuer identity.
7. Wrong issuer signing-key identifier.
8. Wrong registry or replay-ledger scope.
9. Wrong policy identifier or epoch.
10. Wrong policy generation.
11. Wrong recovery epoch.
12. Incorrect previous policy commitment.
13. Incorrect candidate policy commitment.
14. Tampered policy signing bytes.
15. Duplicate canonical JSON keys.
16. Missing or unexpected signed fields.
17. Invalid signature encoding.
18. Unsupported algorithm.
19. Disabled or revoked issuer key.
20. Caller-supplied fabricated issuer root.
21. Self-signed unauthorized policy bootstrap.
22. Policy transition without independent approval.
23. Revoked replay signer in older signed policy.
24. Stale but correctly signed policy.
25. Primary policy ahead of witness.
26. Witness ahead of primary policy.
27. Equal generation with different commitments.
28. Rolled-back primary policy.
29. Rolled-back policy witness.
30. Missing protected policy authority.
31. Missing independent witness.
32. Unknown policy commit outcome.
33. Lost policy commit acknowledgement.
34. Reused policy transition identity.
35. Unauthorized issuer root rotation.
36. Unauthorized recovery-epoch change.
37. Forged matching authority observations.
38. Untrusted assessment timestamp.
39. Replay-state policy epoch mismatch.
40. Attempted operational execution authorization.

Pure tests must keep all operational trust
and execution flags false.

## 35. Acceptance Criteria

Gate 3D.12R is ready for architecture review when:

1. Policy issuer identity is independently specified.
2. Out-of-band issuer bootstrap is required.
3. Self-authorizing root enrollment is prohibited.
4. Issuer signing purpose is distinct from replay roles.
5. Signed policy fields and commitments are specified.
6. Approval evidence is separated from signatures.
7. Protected policy positions are defined.
8. Independent witness protection is required.
9. Currentness is distinct from signature validity.
10. Conditional policy transitions are defined.
11. Split commitments and unknown outcomes fail closed.
12. Recovery requires separate approved authority.
13. Existing security tests remain passing.
14. No operational credentials or services are introduced.
15. Docker, retries and deployment remain blocked.

## 36. Final Decision

Future Basics requires an independently authenticated
policy issuer, approved policy changes and protected
policy currentness before replay trust-policy records
can be treated as operational authority.

Valid signatures under caller-supplied keys,
internally consistent policy hashes and matching
caller-created checkpoints are insufficient.

Gate 3D.12R approves architecture only.

It does not authorize live signing, trust-root enrollment,
policy commits, witness updates, automatic recovery,
Docker execution or production deployment.
