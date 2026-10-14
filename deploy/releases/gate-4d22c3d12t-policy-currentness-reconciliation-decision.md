# Gate 4D.22C.3D.12T - Protected Replay Policy Currentness and Issuer-Evidence Reconciliation

Status: ARCHITECTURE ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retries: DENIED
Production deployment: DISABLED
Independent issuer trust roots: NOT PROVISIONED
Independent administrative approval: NOT IMPLEMENTED
Protected policy-state authority: NOT IMPLEMENTED
Independent policy rollback witness: NOT IMPLEMENTED
Authenticated currentness evidence: NOT IMPLEMENTED
Durable policy-state persistence: NOT IMPLEMENTED
Trusted freshness and time: NOT IMPLEMENTED
Operational policy transactions: NOT IMPLEMENTED
Automatic witness catch-up: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Operational replay authority: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Decision

Define the architecture for reconciling issuer-signed replay
trust-policy evidence with independently authenticated,
protected policy-state and rollback-witness observations.

A valid policy signature is necessary but is not sufficient
to establish the latest approved policy position.

This gate introduces no executable security contracts,
network interfaces, credentials, storage adapters or commits.

## 2. Existing Security Foundation

Gate 3D.12O verifies replay STATE and WITNESS signatures
under caller-supplied public keys.

Gate 3D.12P defines independent replay trust-root
provisioning and policy authentication requirements.

Gate 3D.12Q provides pure replay trust-policy snapshots,
key lifecycle validation and logical reconciliation.

Gate 3D.12R defines policy issuer authentication and
protected policy-currentness requirements.

Gate 3D.12S provides offline Ed25519 verification for
caller-supplied replay policy issuer keys and approval
declarations.

No existing gate establishes operational policy currentness.

## 3. Existing Contract Preservation

Do not change the following existing contracts:

ReplayPolicySnapshot
ReplayPolicyCheckpoint
ReplayPolicyTransitionAssessment
ReplayPolicyReconciliationAssessment
ReplayPolicyIssuerKey
ReplayPolicyIssuerKeyPolicy
ReplayPolicyApprovalDeclaration
SignedReplayPolicyEnvelope
ReplayPolicyIssuerSignatureAssessment
ReplayResponseKeyPolicy

Future implementation must use separate types for any
new authority response and durable transition evidence.

Existing types remain caller-supplied and non-authorizing.

## 4. Security Problem

A historical replay trust policy may have:

- Valid canonical bytes.
- A correct policy commitment.
- A valid issuer Ed25519 signature.
- Matching declared approval information.
- A logically consistent policy history.

It may nevertheless be outdated, revoked, rolled back,
superseded or never accepted by a protected authority.

Policy signature correctness must not be interpreted
as protected policy currentness.

## 5. Security Goals

The future system must separately establish:

1. Approved issuer-key provenance.
2. Issuer signature validity.
3. Independent administrative approval.
4. Protected policy-state identity.
5. Protected policy-state currentness.
6. Independent rollback-witness identity.
7. Witness checkpoint currentness.
8. Policy continuity and revocation history.
9. Request freshness and replay prevention.
10. Durable transaction outcomes.

No single signature or success flag proves all ten.

## 6. Trust Domains

The architecture distinguishes:

A. Application verification runtime.
B. Policy issuer.
C. Independent administrative approvers.
D. Protected policy-state authority.
E. Independent policy rollback witness.
F. Trust-root provisioning authority.
G. Emergency recovery authority.
H. Replay STATE response authority.
I. Replay WITNESS response authority.
J. Registry STATE, WITNESS and ADMIN authorities.

A shared name, server or configuration file does not
establish independence.

Administrative and failure-domain separation must
be evaluated before operational integration.

## 7. Issuer Trust-Root Prerequisite

The expected issuer public key must come from an
independently approved protected trust source.

A public key embedded in the policy being verified
cannot authenticate that same policy's issuer.

A first valid signature cannot establish trust-on-first-use.

The expected issuer identity and policy-signing purpose
must be known independently before verification.

## 8. Issuer Evidence Boundary

Gate 3D.12S SignedReplayPolicyEnvelope binds:

- Issuer identity and signing-key identifier.
- Registry, ledger and policy identities.
- Policy epoch and generation.
- Recovery epoch.
- Previous policy commitment.
- Transition identifier.
- Approval reference.
- Proposed policy commitment.
- Approval declaration commitment.
- Signature purpose and algorithm.

These fields establish cryptographic binding only
under the selected verification key.

They do not establish operational policy acceptance.

## 9. Approval Evidence Boundary

ReplayPolicyApprovalDeclaration contains caller-supplied
approver identifiers and a declared decision.

It is not proof of real human approval, authenticated
roles, consent, permission or separation of duties.

Operational policy acceptance requires independently
authenticated approval evidence.

The future approval evidence must bind the exact proposed
policy commitment and transition identifier.

An issuer must not authenticate its own approvers merely
by signing their names in a policy declaration.

## 10. Protected Policy-State Authority

The future protected policy-state authority must maintain
an independently authenticated policy position.

Its state must not be replaceable by an ordinary application
configuration update or database restore.

The authority must support a reviewed method to read
the accepted policy position.

An observed policy snapshot must not be accepted merely
because its checksum matches the snapshot contents.

## 11. Protected Policy Position

Define a future immutable protected position containing:

- Protocol version.
- Registry identity.
- Replay-ledger identity.
- Policy identifier.
- Policy epoch.
- Policy generation.
- Recovery epoch.
- Accepted policy snapshot commitment.
- Previous accepted position commitment.
- Last accepted transition identifier.
- Protected position commitment.

The exact wire format must be frozen in a subsequent gate.

A protected position differs from the caller-created
ReplayPolicyCheckpoint of Gate 3D.12Q.

## 12. Independent Policy Rollback Witness

The independent witness must maintain a forward-only
checkpoint of accepted protected policy positions.

It must have a separately approved authority identity.

Its storage must not be rollback-equivalent to the
primary policy database.

The independent witness must protect:

- Policy scope.
- Accepted policy epoch.
- Protected generation.
- Recovery epoch.
- Accepted policy commitment.
- Accepted transition identifier.
- Checkpoint ancestry.

A caller-created matching checkpoint is insufficient.

## 13. Authority Identity Separation

Introduce conceptual future roles:

REPLAY_POLICY_STATE

REPLAY_POLICY_WITNESS

These names identify proposed policy authority roles.

They are separate from:

REPLAY_STATE
REPLAY_WITNESS
STATE
WITNESS
ADMIN
REPLAY_POLICY_ISSUER

The final role names and signing domains must be
frozen before an implementation gate.

No existing signing purpose is inherited automatically.

## 14. Authenticated Policy Reads

Each future protected read must return:

- The expected authority role.
- Approved authority identity.
- Signing-key identifier.
- Protocol and response purpose.
- Request identifier and challenge.
- Registry, ledger and policy scope.
- Protected policy position.
- Exact position commitment.
- Appropriate policy and recovery epochs.
- Canonical cryptographic response evidence.

A signed read must bind to the original verification
request rather than a newly supplied request label.

## 15. Read Challenge Requirements

Operational policy reads require unpredictable
verifier-originated challenge material.

The security target is at least 256 bits of entropy
from an approved cryptographic random source.

The challenge must be bound to:

- Request identifier.
- Registry and replay-ledger scope.
- Expected policy authority identities.
- Read purpose.
- Relevant policy and recovery epochs.
- Applicable protected position reference.

A caller-created challenge string does not prove
fresh issuance, uniqueness or durable reservation.

## 16. Challenge Replay Resistance

Operational challenge consumption must use a protected
request lifecycle.

The system must prevent reuse of a consumed challenge
for a different response, purpose or authority set.

The read protocol must handle the bootstrap dependency
between reading replay protection and reserving reads.

A logically unique request identifier does not establish
durable replay resistance.

No automatic reissuance is authorized by this decision.

## 17. Canonical Authority Response Format

Future authority responses must use a single reviewed
canonical wire representation per signing role.

The format must reject:

- Duplicate object keys.
- Unexpected fields.
- Missing fields.
- Noncanonical encodings.
- Invalid integer types.
- Epoch or generation overflow.
- Incorrect role or response purpose.
- Unsupported algorithms.
- Wrong registry, ledger or policy identity.
- Invalid signatures.
- Ambiguous signature encodings.
- Oversized messages.

Signed response bytes must include a versioned,
role-separated cryptographic domain.

## 18. Policy Position Commitment

The protected position commitment must bind the full
accepted policy-state position.

The calculation must include policy epoch, generation,
recovery epoch, accepted policy checksum, predecessor
commitment and transition identity.

A domain-separated digest is a structural commitment.

Its independence depends upon authenticated authority
evidence and protected storage.

A forged position and matching forged checksum remain
untrusted.

## 19. Protected Currentness

Protected policy currentness requires establishing the
latest accepted position through independently controlled
authority evidence.

A high generation number is not sufficient.

A currently valid issuer signature is not sufficient.

Matching primary and witness declarations are not
sufficient without independent authority authentication.

The verifier must distinguish:

- Signature verification.
- Trust-root authentication.
- Approval authentication.
- Protected state verification.
- Witness verification.
- Currentness verification.
- Durable acceptance.

Each security guarantee must be assessed separately.

## 20. Policy History and Revocation

The current protected policy must preserve the required
history of signing-key enrollment and retirement.

An earlier signed policy must not reactivate a key
revoked in a later independently accepted policy.

The verifier must not choose whichever historical
policy permits a requested signature to pass.

A valid older issuer signature does not override
current revocation restrictions.

Policy-history compaction requires a separately
reviewed, rollback-resistant design.

## 21. Ordinary Policy Transition

A future conditional policy transition must bind:

- Previously accepted protected position.
- Expected policy epoch and generation.
- Expected witness checkpoint.
- Proposed ReplayPolicySnapshot.
- Proposed policy commitment.
- Exact policy transition identifier.
- Authenticated issuer evidence.
- Independently authenticated approval evidence.
- Expected recovery epoch.

The transition may be proposed only after all required
logical checks pass.

Logical validity is not a durable database commit.

## 22. Conditional Commit Semantics

The protected policy-state authority must perform
an actual conditional commit against the expected
previous protected position.

It must reject stale predecessor commitments and
conflicting transitions.

The transaction must have a reviewed durability model.

An operation acknowledgement must identify the exact
request and transition it describes.

No caller-supplied success declaration can substitute
for durable commit evidence.

## 23. Witness Advancement

After a primary policy transition, the independent
witness must receive a conditional advancement request.

That request must bind:

- Its current expected checkpoint.
- Proposed protected policy position.
- Proposed policy commitment.
- Transition identifier.
- Policy and recovery epochs.
- Authenticated authority evidence.

A stale witness update cannot overwrite a newer position.

No automatic witness catch-up is introduced here.

## 24. Signed Versus Committed

The system must not equate:

SIGNED_POLICY

with:

APPROVED_POLICY

or:

DURABLY_COMMITTED_POLICY

or:

INDEPENDENTLY_WITNESSED_CURRENT_POLICY

These are different states of knowledge.

Signing a valid policy proposal does not prove that
either the primary or witness accepted it.

Receiving an acknowledgement does not prove durability
unless the authority's guarantees have been independently
established.

## 25. Reconciliation Scenarios

The future reconciliation protocol must distinguish:

R1: Both authorities report the previous position.

R2: Primary is at proposed position; witness is previous.

R3: Witness is proposed; primary is previous.

R4: Both report the proposed position.

R5: Primary and witness have conflicting commitments.

R6: Primary policy authority is unavailable.

R7: Independent witness is unavailable.

R8: Both policy authorities are unavailable.

R9: Primary is below the last independently established
    checkpoint.

R10: Witness is below its last independently established
     checkpoint.

R11: Equal generations contain different commitments.

R12: An observed higher generation has unknown ancestry.

R13: A signed policy is valid but no longer current.

R14: Transaction outcome is unknown after a timeout.

All unverified observations remain non-authorizing.

## 26. Reconciliation Classification

A future pure assessor may report classifications such as:

BOTH_PREVIOUS_UNTRUSTED
PRIMARY_AHEAD_UNTRUSTED
WITNESS_AHEAD_UNTRUSTED
BOTH_PROPOSED_UNTRUSTED
CONFLICTING_POSITIONS
PRIMARY_ROLLBACK_SUSPECTED
WITNESS_ROLLBACK_SUSPECTED
UNKNOWN_POLICY_ANCESTRY
STALE_SIGNED_POLICY
UNKNOWN_COMMIT_OUTCOME
PRIMARY_UNAVAILABLE
WITNESS_UNAVAILABLE
BOTH_UNAVAILABLE

These are proposed classifications, not implemented
operational authority decisions.

Every assessment must preserve its trust limitations.

## 27. Unknown Commit Outcomes

A timeout or missing response cannot establish whether
a conditional commit succeeded.

Such an operation must be classified:

UNKNOWN_COMMIT_OUTCOME

The verifier must retain the original transition
identifier and expected/proposed commitments.

A new attempt must not be automatically submitted.

The operator must obtain independently authenticated
reconciliation evidence before recovery is considered.

Automatic retries remain DENIED.

## 28. Split-Commit Handling

The primary and independent witness must not be assumed
to share a single atomic database transaction.

A primary-ahead state may indicate a completed primary
write with an incomplete witness advancement.

A witness-ahead state may indicate an incomplete or
unavailable primary state.

Neither outcome authorizes automatic catch-up,
automatic rollback or production use.

The future recovery design must separately review each
possible split-commit condition.

## 29. Rollback and Equivocation

Rollback must be suspected when a reported authority
position is below a previously independently accepted
protected checkpoint.

Equal generations with different accepted commitments
indicate a possible integrity conflict or equivocation.

An unexpected forward generation must not be accepted
without validated ancestry and approval evidence.

No local hash chain alone establishes rollback resistance.

A disagreement must block operational policy acceptance.

## 30. Replay Authority Alignment

The accepted replay trust policy must be reconciled with:

ReplayReadChallenge.policy_epoch
ReplayProtectedPosition.policy_epoch
ReplayResponseKeyPolicy.epoch
SignedReplayResponse.policy_epoch

Recovery epochs must also agree where applicable.

The comparison must use the independently established
accepted policy position.

Agreement among caller-created epoch fields is not
independent authorization.

## 31. Issuer Key Rotation and Compromise

Issuer-key rotation requires a separately approved
trust-anchor transition.

A compromised issuer cannot self-authorize its
replacement by signing a new issuer key.

Compromise response must preserve:

- Last independently accepted issuer trust root.
- Last accepted policy-state checkpoint.
- Last independent witness checkpoint.
- Affected policy transition identifiers.
- Revocation evidence.
- Pending request and commit outcomes.

An ordinary replay response-key rotation must not be
mistaken for policy issuer root rotation.

## 32. Emergency Recovery

Policy rollback, witness compromise, lost trust roots
or unknown commits require separate reviewed recovery.

Recovery evidence must bind:

- Incident identifier.
- Authorized recovery authority.
- Last verified protected policy position.
- Last verified independent checkpoint.
- Previous and proposed recovery epochs.
- Replacement trust-root commitment if applicable.
- Affected policies, keys and requests.
- Recovery transition identifier.
- Independent approval evidence.

No operational recovery is approved by this gate.

## 33. Audit and Evidence

A future evidence trail must record:

- Registry, ledger and policy scope.
- Issuer and policy-authority identities.
- Public signing-key identifiers.
- Canonical policy and position commitments.
- Original read and transition identifiers.
- Request challenge references.
- Approval and recovery references.
- Primary and witness positions.
- Reconciliation outcomes.
- Unknown commit classifications.
- Revoked signing-key references.

No private signing keys or credentials may be logged.

Ordinary audit logs are not an independent rollback witness.

## 34. Implementation Roadmap

A subsequent gate may implement pure, immutable
caller-supplied policy-currentness evidence contracts.

It may define:

- PolicyReadChallenge.
- PolicyProtectedPosition.
- PolicyStateReadEvidence.
- PolicyWitnessReadEvidence.
- PolicyReconciliationAssessment.
- PolicyConditionalTransitionIntent.

Those names are conceptual and may be refined.

The implementation must not include:

- Operational network requests.
- Production trust-root enrollment.
- Live signing credentials.
- Protected database writes.
- Actual witness advancement.
- Automatic reconciliation retries.
- Docker execution.
- Production deployment.

## 35. Acceptance Criteria

This gate is ready for review when:

1. Gate 3D.12S issuer evidence is correctly distinguished
   from independent issuer authentication.
2. Approval declarations remain unauthenticated.
3. Protected policy positions are explicitly defined.
4. Primary and witness authorities are separated.
5. Verifier-originated challenges are required.
6. Canonical authority responses are specified.
7. Policy currentness is not inferred from signatures.
8. Revoked older policies cannot bypass current policy.
9. Conditional commit requirements are documented.
10. Split commits remain unresolved without recovery.
11. Unknown outcomes prohibit automatic retries.
12. Rollback and equivocation fail closed.
13. Emergency recovery requires separate authorization.
14. Existing Python security tests remain passing.
15. No operational services or credentials are introduced.
16. Docker, automatic retries and deployment remain blocked.

## 36. Final Decision

Future Basics must establish independently authenticated
policy-state and rollback-witness evidence before treating
an issuer-signed replay trust policy as operationally current.

Valid signatures, declared approvals, logical continuity,
matching checkpoints and local commitments are insufficient
to establish that currentness.

Gate 3D.12T approves architecture only.

It does not authorize trust-root provisioning, operational
policy commits, witness updates, automatic recovery,
Docker execution, automatic retries or production deployment.
