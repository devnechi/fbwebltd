# Gate 4D.22C.3D.12N - Authenticated Replay Authority Evidence and Reconciliation

Status: ARCHITECTURE ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Independent replay authority trust roots: NOT PROVISIONED
Authenticated replay authority adapters: NOT IMPLEMENTED
Replay authority signature verifier: NOT IMPLEMENTED
Operational challenge generation: NOT IMPLEMENTED
Durable replay challenge reservation: NOT IMPLEMENTED
Independent replay rollback witness: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Operational recovery authorization: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Decision

Define the identity, cryptographic evidence and reconciliation
contracts required to authenticate a future replay-state
authority and separately controlled replay rollback witness.

This is an architecture-only milestone.

No new Python verifier, signing service, storage adapter,
database transaction, private key or network client is
authorized by this decision.

All existing laboratory operations remain non-authorizing.

## 2. Existing Architecture

Gate 3D.12H provides Ed25519 signature verification for
the registry STATE, WITNESS and ADMIN authority responses.

Gate 3D.12I defines logical authority trust-policy continuity.

Gate 3D.12J defines challenge lifecycle and freshness
requirements.

Gate 3D.12K provides pure, untrusted challenge-lifecycle
classification.

Gate 3D.12L defines the protected replay-state authority
and independent replay rollback witness.

Gate 3D.12M provides immutable replay positions, logical
witness checkpoints, transition intents and non-authorizing
reconciliation classifications.

This gate defines the missing replay-authority authentication
protocol.

## 3. Existing Code Boundaries

The replay authority authentication protocol must build upon
the following existing laboratory types:

ReplayLedgerSnapshot
ReplayProtectedPosition
ReplayWitnessCheckpoint
ReplayProtectedReadBundle
ReplayConditionalTransitionIntent

The existing replay-position commitment is an unkeyed,
domain-separated SHA-256 value.

That value binds bytes but does not authenticate their source.

The existing ReplayProtectedReadBundle requires logical
primary and witness equality.

Authentication and split-commit analysis must also support
separate state and witness observations that disagree.

The existing SignedAuthorityResponse is restricted to
STATE, WITNESS and ADMIN.

It must not silently be extended or reused for different
replay-authority trust roles.

## 4. Security Objective

Establish a future verification architecture capable of
checking whether a response was signed by the intended
replay authority under a separately approved key policy.

A positive cryptographic result alone must not prove:

- Independently controlled trust-root provenance.
- Replay challenge uniqueness.
- Fresh operational state.
- A durable database commit.
- Independent witness advancement.
- Prevention of ledger rollback.
- Trusted time.
- Successful administrative recovery.
- Application execution authorization.

Each property requires its own evidence and controls.

## 5. Threat Model

An adversary may:

- Forge unsigned replay-state observations.
- Substitute a replay authority identifier.
- Replay an older validly signed position.
- Replay an older witness checkpoint.
- Use a valid signature with an unapproved key.
- Present a caller-created trust policy.
- Mix primary and witness responses from different reads.
- Substitute a registry STATE response for replay STATE.
- Swap replay STATE and replay WITNESS messages.
- Rebind a response to another request identifier.
- Rebind a response to another replay-ledger identity.
- Change a position while preserving its declared label.
- Replay an old transition acknowledgement.
- Hide a successful commit behind a timeout.
- Restore an older application or replay database.
- Attempt unauthorized key rotation or recovery.
- Supply a forged but internally consistent state chain.

The protocol must fail closed when an expected security
property cannot be established.

## 6. Independent Replay Authority Roles

Define two new authority-signing roles:

REPLAY_STATE
The transactional replay-state authority.

REPLAY_WITNESS
The independent replay rollback witness.

These are not equivalent to the registry roles:

STATE
WITNESS
ADMIN

The replay-state authority must not use registry STATE
signing purpose or key policy implicitly.

The replay witness must not use registry WITNESS signing
purpose or key policy implicitly.

A new versioned protocol is required.

## 7. Cryptographic Separation

Replay authority response signatures should use Ed25519
with separate, versioned signed-message domains.

Proposed conceptual domain prefixes:

FBWEB-LAB-REPLAY-STATE-RESPONSE-V1
FBWEB-LAB-REPLAY-WITNESS-RESPONSE-V1

The actual signing-byte representation must include an
unambiguous domain separator and canonical payload.

A signature produced for REPLAY_STATE must never validate
for REPLAY_WITNESS.

A registry-state signature must never validate as a
replay-state signature.

Separate role labels alone do not prove independent key
custody or administrative control.

## 8. Replay Authority Identity

Each authority must have a separately approved identity.

The verifier must know the expected authority identity
before accepting the response.

The identity must bind to:

- Registry identity.
- Replay-ledger identity.
- Authority role.
- Authority identifier.
- Approved signing-key identifier.
- Signing purpose.
- Current applicable policy epoch.

Authority identity must not be taken solely from the
response being verified.

A matching caller-supplied string is not authentication.

## 9. Trust Policy Provisioning

The future implementation requires independently provisioned
and protected replay authority verification keys.

A response must not introduce its own trusted public key.

A key policy supplied inside a response is not proof
that the policy was approved.

The trust source must be established through a separate,
reviewed provisioning and administrative control procedure.

The initial trust-root enrollment requires independent
authorization and evidence.

This gate does not select the trust provider or custody model.

## 10. Replay Authority Key Policy

The proposed future replay signing-key policy must bind:

- Policy identifier and protocol version.
- Registry identity and replay-ledger identity.
- Authority role and authority identifier.
- Key identifier and public key.
- Algorithm and signing purpose.
- Key lifecycle status.
- Declared validity interval.
- Protected policy epoch.
- Recovery epoch where relevant.

The policy must reject ambiguous identities, duplicate
signing-key identifiers and cross-role key reuse.

The future protocol must define rotation, retirement,
revocation and emergency key-compromise handling.

Logical policy continuity does not establish policy approval.

## 11. Separate Administrative Authority

The registry ADMIN role must not automatically administer
replay authority trust roots.

Any shared administrative authority requires a separate
review of duties, permission boundaries and failure domains.

No replay authority may authorize replacement of its own
root merely by signing a proposed replacement policy.

Emergency trust-root recovery must be handled through
an independently controlled procedure.

## 12. Authentication Challenge

Authenticated replay authority reads require fresh,
verifier-originated challenge material.

Challenge issuance and challenge consumption must be
bound to a reviewed request lifecycle.

The initial security target is at least 256 bits of
unpredictable material from an approved cryptographic
random source.

Caller-provided fixture challenges prove no randomness.

Challenge reuse is prohibited.

The same challenge must not be rebound to different
request purposes, ledger identities or authority sets.

## 13. Bootstrap and Read Dependency

A future replay authority may need to be read before the
first authority-read request can be durably reserved.

The design must distinguish:

A. A bootstrap or discovery read, which is not trusted
merely because it returned a claimed position.

B. A protected reservation transaction, which requires
independently authenticated state and witness controls.

C. A subsequent authority response, which must match a
properly reserved request and validated response purpose.

The system must not assume that an unreserved bootstrap
challenge has operational replay protection.

No circular claim of freshness may be used to authorize
initial challenge reservation.

The bootstrap procedure requires separate approval.

## 14. Replay Read Request

The future replay read request must bind:

- Protocol version.
- Registry identity.
- Replay-ledger identity.
- Request identifier.
- Verifier-originated challenge.
- Request purpose.
- Expected replay-state authority identity.
- Expected replay-witness authority identity.
- Expected key-policy epoch.
- Recovery epoch, when applicable.
- Expected protected-position reference, if applicable.

A future wire format must define field lengths, allowed
values and canonical encoding precisely.

Unknown or ambiguous fields must fail closed.

## 15. Separate Signed Replay Responses

Replay STATE and replay WITNESS must produce distinct,
role-separated signed response envelopes.

Each signed response must bind the request identity and
challenge to the authority's own response body.

The response envelope must not depend on a mutable
external object without a canonical commitment.

The signing operation must not treat an arbitrary caller
digest as proof that the underlying body is authentic.

## 16. Minimum Signed Response Fields

A future response should bind:

- Protocol and response schema versions.
- Signing role and authority identity.
- Registry and replay-ledger identities.
- Request identifier and challenge commitment.
- Request purpose.
- Signing key identifier and declared policy epoch.
- Response body commitment.
- Full replay protected-position commitment.
- Protected replay generation.
- Recovery epoch.
- Observation or transition identifier.
- Response status or outcome classification.
- Cryptographic algorithm and signing purpose.

The exact field schema must be frozen before implementing
a signature verifier.

A supplied observation timestamp cannot independently
establish freshness.

## 17. Canonical Signed Wire Format

The implementation gate must define one canonical
representation for every signed message.

The format must reject:

- Duplicate object keys.
- Unexpected fields.
- Missing required fields.
- Noncanonical serialization.
- Invalid string encodings.
- Invalid integer types.
- Negative or overflowing generations.
- Noncanonical signature encodings.
- Unsupported algorithms.
- Invalid identity lengths.
- Incorrect signing domains.

Signed bytes must be reconstructed deterministically.

No generic JSON reserialization may be assumed safe
without validating the exact canonical profile.

## 18. Primary Replay-State Evidence

A signed REPLAY_STATE response must commit to the complete
reported replay protected position.

If it includes the replay ledger or selected request
records, their canonical digest must match the position's
ledger commitment.

The response must distinguish:

- Read-position evidence.
- Conditional-operation acknowledgement.
- Unknown transaction outcome.
- Explicit rejection or conflict.

A signature on an acknowledgement is not necessarily
proof that the associated database write was durable.

The authority's storage guarantees require separate
operational verification.

## 19. Replay Witness Evidence

A signed REPLAY_WITNESS response must bind:

- The independently maintained checkpoint.
- Its protected generation and commitment.
- Registry and replay-ledger identities.
- Applicable policy and recovery epochs.
- Request and challenge.
- Authority identity and signing purpose.
- The result of any conditional witness operation.

A matching checkpoint does not prove that the witness
is independently controlled.

The control and protection of witness state remain
separate operational dependencies.

## 20. Transition Acknowledgement Evidence

The future protocol must not treat every signed response
as a successful transition acknowledgement.

A conditional-operation response must identify:

- Requested transition identifier.
- Full operation commitment.
- Expected protected position.
- Reported resulting position.
- Operation result classification.
- Authority-specific durable outcome evidence.

A timeout or unavailable acknowledgement is an
UNKNOWN_COMMIT_OUTCOME.

Unknown outcomes do not authorize automatic retransmission
or an assumption of failure.

## 21. Cross-Response Binding

Primary and witness responses must belong to the same
intended verification operation.

The verifier must compare:

- Registry and replay-ledger identities.
- Request identifier.
- Original verifier challenge.
- Expected replay authority identities.
- Relevant policy and recovery epochs.
- Signed response purposes.
- Protected replay-position generation and commitment.
- Transition identity when assessing a commit.

Responses from different requests cannot be combined
into apparently consistent evidence.

Matching fields remain non-authorizing without separate
source authentication and currentness checks.

## 22. Signature Verification Ordering

A future verifier should:

1. Parse the exact canonical signed response bytes.
2. Validate the expected protocol and role.
3. Validate request, challenge and authority bindings.
4. Select the independently approved verification key.
5. Verify the correct role-specific Ed25519 signature.
6. Validate the committed body and position.
7. Check current protected key-policy restrictions.
8. Assess request replay and consumption state.
9. Compare primary and witness observations.
10. Evaluate authenticated freshness and currentness.

Failure at any required step must deny operational
acceptance.

This sequence is conceptual, not implemented.

## 23. Supplied-Key Laboratory Verification

An intermediate implementation may verify replay response
signatures under caller-supplied keys.

Such a result must be named explicitly, for example:

signature_verified_under_supplied_key

It must not set:

independent_authority_identity_authenticated
independent_trust_roots_verified
durable_commit_verified
replay_prevention_verified
authoritative_currentness_verified

A valid signature under an attacker-chosen key must not
become an operational authorization signal.

## 24. Primary/Witness Reconciliation

After signed response verification, the system must
separately reconcile the replay-state position and
replay-witness checkpoint.

The existing Gate 3D.12M classifier provides
non-authorizing logical outcomes.

Its classifications include:

BOTH_PREVIOUS_UNTRUSTED
STATE_AHEAD_OF_WITNESS
WITNESS_AHEAD_OF_STATE
BOTH_PROPOSED_UNTRUSTED
CONFLICTING_OR_UNEXPECTED_POSITIONS
REPLAY_STATE_ROLLBACK_SUSPECTED
REPLAY_WITNESS_ROLLBACK_SUSPECTED

The future authenticated reconciliation layer must
preserve the fail-closed behavior of these cases.

Do not reinterpret BOTH_PROPOSED_UNTRUSTED as a durable
commit or verified currentness.

## 25. Split-Commit Handling

When primary replay state is ahead of its witness:

- Do not accept new operational replay evidence.
- Do not silently advance the witness.
- Preserve the conflicting observations.
- Require independently approved reconciliation.

When the witness is ahead of primary replay state:

- Do not roll the witness backward.
- Treat primary rollback or state loss as possible.
- Preserve the protected comparison evidence.
- Require independently approved reconciliation.

The architecture does not implement reconciliation writes.

## 26. Replay Prevention

A verified replay authority signature does not establish
that a challenge has not previously been consumed.

The future service must durably enforce:

- Unique request identifier reservations.
- Unique challenge material reservations.
- Single-use role response consumption.
- Terminal request history retention.
- Conditional generation advancement.

The primary replay-state service and its witness must
provide separately authenticated, protected evidence.

The existing pure snapshots do not satisfy this requirement.

## 27. Freshness and Currentness

A signed response may be authentic but stale.

The verifier must distinguish:

Signature validity:
The response was signed under a particular key.

Policy currentness:
The verification key remains approved under a trusted policy.

Challenge freshness:
The challenge belongs to a valid protected request lifecycle.

Replay currentness:
Previously consumed responses cannot be treated as new.

State currentness:
The reported protected replay position is current.

Time validity:
Relevant deadlines are checked against trusted time.

These must never be collapsed into one boolean.

## 28. Key Rotation During a Request

The protocol must define how pending reads behave when
the relevant replay signing key becomes disabled or revoked.

A key that was active when a request began must not
silently override a later independently approved revocation.

The applicable trusted policy epoch must be established
before accepting the response.

Caller-supplied policy epochs are not protected currentness.

No automatic request retry is authorized.

## 29. Recovery Evidence

Emergency recovery requires evidence from an independent
recovery approval process.

A replay-state response may report a new recovery epoch,
but that report does not authorize the recovery.

The future process must bind approved recovery identity,
scope, epoch, earlier protected checkpoint and audit evidence.

Ordinary challenge reads must not change the recovery epoch.

This gate introduces no recovery authority or procedure
that modifies protected state.

## 30. Missing or Compromised Authorities

Operational acceptance must be denied when:

- The replay-state authority is unavailable.
- The replay witness is unavailable.
- A required signing key is revoked or unknown.
- Trust-root provenance cannot be established.
- The replay ledger and witness cannot be reconciled.
- The protected replay history is missing.
- A replay position has apparently rolled back.
- A transaction outcome remains uncertain.
- Trusted freshness cannot be established.

The verifier must not substitute a caller-provided
successful-looking result.

## 31. Audit Requirements

Future audit evidence should record:

- Registry and replay-ledger identities.
- Verification request and challenge commitment.
- Expected authority role and identifier.
- Verification key identifier and policy epoch.
- Signed response commitment.
- Observed protected position and generation.
- Reconciliation classification.
- Relevant transition identifier.
- Failed verification stage.
- Recovery or incident reference.

Private keys, service credentials and unnecessary
sensitive payloads must never be logged.

Ordinary logs are not an independent rollback witness.

## 32. Future Implementation Scope

A subsequent gate may introduce:

- Immutable replay read challenges.
- Immutable signed replay response records.
- Canonical replay response signing bytes.
- Strict wire-format parser.
- Pure Ed25519 verification under supplied keys.
- Role-separated signing domains.
- Logical replay position and witness binding.
- Immutable non-authorizing signature assessments.
- Adversarial offline verification tests.

Such an implementation must not introduce:

- Independently provisioned operational signing keys.
- Network authority clients.
- Production replay-state reads or writes.
- Durable replay transaction services.
- Automatic recovery or retries.
- Docker execution.
- Production deployment.

## 33. Adversarial Test Requirements

The subsequent implementation must cover:

1. Correct canonical replay-state signature.
2. Correct canonical replay-witness signature.
3. Incorrect signature under an otherwise valid key.
4. Replay STATE signature substituted for replay WITNESS.
5. Registry STATE signature substituted for replay STATE.
6. Wrong replay authority identifier.
7. Wrong registry identifier.
8. Wrong replay-ledger identifier.
9. Wrong request identifier.
10. Wrong challenge.
11. Wrong request purpose.
12. Wrong policy epoch.
13. Wrong recovery epoch.
14. Wrong protected replay generation.
15. Wrong ledger commitment.
16. Wrong protected-position commitment.
17. Mismatched response body and signed digest.
18. Duplicate canonical JSON keys.
19. Noncanonical JSON serialization.
20. Unknown or missing signed fields.
21. Invalid signature encoding.
22. Invalid Ed25519 public-key encoding.
23. Disabled signing key.
24. Revoked signing key.
25. Expired declared key validity.
26. Wrong declared signing purpose.
27. Cross-role key material reuse.
28. Caller-supplied forged trust policy.
29. Replayed earlier signed response.
30. Valid signature on a stale replay generation.
31. Duplicate role-consumption evidence.
32. Primary replay state ahead of witness.
33. Witness ahead of replay state.
34. Conflicting primary and witness commitments.
35. Unknown conditional commit outcome.
36. Lost transition acknowledgement.
37. Unauthenticated bootstrap declaration.
38. Unauthorized recovery-epoch change.
39. Missing trusted time.
40. Valid signatures without independent root provenance.
41. Matching forged primary and witness reports.
42. Attempted execution authorization after verification.

All simulated successes must keep operational authorization
flags false.

## 34. Acceptance Criteria

Gate 3D.12N is complete for architecture review when:

1. Replay STATE and replay WITNESS are separately identified.
2. Their signature purposes and domains are independent.
3. Canonical signed evidence requirements are explicit.
4. Expected identities are provisioned outside responses.
5. Challenge and request binding is explicit.
6. Primary/witness position binding is explicit.
7. Unknown commit outcomes remain non-authorizing.
8. Freshness and independent trust provenance remain separate.
9. Recovery and split-commit behavior fail closed.
10. No production interfaces or credentials are introduced.
11. Existing security tests continue to pass.
12. All execution restrictions remain enforced.

## 35. Final Decision

Future Basics will require authenticated, role-separated
replay authority and replay witness evidence before it can
treat replay-state observations as operationally meaningful.

Cryptographic verification under caller-supplied keys may
be implemented for laboratory analysis, but it does not
establish independently trusted authority provenance,
protected replay-state currentness or durable commits.

Gate 3D.12N approves architecture review only.

Docker execution, automatic retries and production
deployment remain blocked.
