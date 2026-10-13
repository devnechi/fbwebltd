# Gate 4D.22C.3D.12D - Authority Authentication and Reconciliation

Status: ARCHITECTURE PROPOSED - OPERATIONAL APPROVAL PENDING
Date: 2026-10-13

Laboratory Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Trusted state authority: NOT IMPLEMENTED
Independent rollback witness: NOT IMPLEMENTED
Operational administrative keys: NOT PROVISIONED
Trusted time: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Define how Future Basics will authenticate its independent
security authorities and safely handle incomplete registry
state transitions.

The decision builds on:

- Gate 3D.11F: offline registry verification composition.
- Gate 3D.12A: independent trust architecture.
- Gate 3D.12B: preferred security-state authority.
- Gate 3D.12C: protected-state contract interfaces.

This gate is architecture-only.

It creates no operational trust, credentials, network
connections, state writes, containers or deployments.

## 2. Existing Security Boundary

Gate 3D.12C defines:

- ProtectedPosition.
- WitnessCheckpoint.
- ProtectedReadBundle.
- ProtectedTransitionIntent.
- ProtectedTransitionAssessment.
- TransactionalStateAuthority protocol.
- RollbackWitnessAuthority protocol.

The contract validates logical consistency.

It does not authenticate either authority.

A malicious caller can construct matching state and witness
objects without controlling any legitimate security service.

Structural agreement must never be treated as proof
of independent authority or currentness.

## 3. Independent Trust Domains

The future architecture requires three distinct controls.

### A. Administrative Trust Authority

Controls approved registry administrative signing identities.

Owns administrative policy versions, key enrollment,
revocation, rotation and recovery authorization.

The registry cannot create its own approved signer.

### B. Transactional State Authority

Controls the accepted registry revision, signing digest,
generation, revocation-history commitment and transaction
identifier.

Provides authenticated, strongly consistent reads and
conditional state updates.

### C. Independent Rollback Witness

Maintains a separately protected forward-only commitment
to the authoritative registry state.

Its administrative and rollback-control domain must be
independent of the transactional state authority.

A rollback of the transactional state must not
automatically roll back the witness.

No specific provider is approved by this gate.

## 4. Authority Identity

Every future operational service must have an independently
approved authority identity.

Authority identity must not be derived solely from:

- Caller-supplied hostnames.
- Registry content.
- Environment variables.
- Application database rows.
- Unauthenticated discovery.
- Unreviewed certificate files.
- Test-only dataclasses.

The verification configuration must bind the expected
authority to its role and registry scope.

The architecture must define how trusted identities
are first enrolled and safely rotated.

Failure to establish authority identity must deny
operational state acceptance.

## 5. Authenticated Communication

A future implementation may evaluate mutually authenticated
TLS or another reviewed authenticated transport.

The design must establish:

- Independent provisioning of authority credentials.
- Verification of the intended authority identity.
- Credential expiry and revocation checks.
- Purpose and registry-scope binding.
- Protection of requests and responses in transit.
- Separation of read and commit permissions.
- Protection from endpoint substitution.
- Failure behavior during credential rotation.

A successful TLS handshake alone does not establish that
the service is the authorized security-state authority.

Authorization and independent identity provisioning
remain separate requirements.

## 6. Response Integrity and Freshness

An operational read must bind the response to:

- Requested registry identity.
- Responding authority identity and role.
- Relevant state generation.
- Accepted registry revision and digest.
- Administrative trust-policy reference.
- Revocation-history commitment.
- Recovery or transaction epoch.
- Request correlation or challenge information.

The architecture must prevent replay of previously valid
responses being mistaken for current state.

A request nonce can help bind responses to an exchange,
but cannot alone establish current authoritative state.

Currentness also requires appropriately protected state,
consistency guarantees and independent authority evidence.

Trusted time remains a separate dependency.

## 7. Administrative Trust Policy

The operational verifier must obtain administrative
trust policy through an independently approved authority.

The verifier must establish:

- Policy authority identity.
- Policy version or protected epoch.
- Approved administrative public keys.
- Allowed signing purposes.
- Current key lifecycle state.
- Policy revocation and rotation status.
- Authorized registry scope.

The policy must not be accepted merely because it validates
against the current Python data schema.

A candidate registry cannot update the trust policy
that is used to authenticate itself.

## 8. Read Reconciliation

Before evaluating a new authoritative transition,
the future verifier must obtain separate evidence from:

1. The transactional state authority.
2. The rollback witness.
3. The administrative trust authority.

The state and witness must agree on the committed
security position, including the revocation commitment
and protected generation.

Their authenticated provenance must be verified separately.

Equal state values are necessary but insufficient.

If any required authority is unavailable, stale,
unauthenticated or inconsistent, operational acceptance
must fail closed.

Offline analysis may continue only when explicitly
identified as non-authorizing.

## 9. Proposed Normal Transition Sequence

A future implementation may use the following conceptual
sequence, subject to separate protocol review.

Step 1: Authenticate all necessary authority identities.

Step 2: Read the committed transactional state and
rollback-witness checkpoint.

Step 3: Independently validate their identity, provenance,
scope, version, freshness and consistency.

Step 4: Obtain the independently authorized administrative
trust policy and trusted time.

Step 5: Execute the existing offline signature, revision
and revocation verification checks.

Step 6: Prepare an immutable, non-authorizing transition
proposal bound to the observed generation.

Step 7: Request an authenticated conditional transaction
against the transactional state authority.

Step 8: Independently confirm the transaction outcome.

Step 9: Submit the confirmed state commitment to the
separate rollback-witness authority through a reviewed
monotonic advancement protocol.

Step 10: Independently read and reconcile both authorities.

Step 11: Only after separate operational security approval
may a committed state be recognized as authoritative.

No step authorizes Docker execution or production deployment.

This sequence is a design candidate, not an implemented
distributed transaction protocol.

## 10. Two-Authority Atomicity Limitation

The transactional state and rollback witness have separate
administrative and persistence boundaries.

Their updates are not automatically atomic together.

An apparently successful update from one authority does
not establish success at the other.

The design must explicitly handle a crash or communication
loss between their updates.

Until both authorities have been independently reconciled,
the proposed new registry must not be reported as
operationally accepted.

The protocol must be reviewed for safety, durability,
idempotency and recovery before implementation.

## 11. Reconciliation Outcomes

### R1 - Both Authorities Remain at Previous State

No new transition has been established.

The candidate remains uncommitted.

A retry or reassessment requires separately approved
future protocol semantics.

### R2 - Transactional State Advanced; Witness Did Not

The system has a split commitment.

The new registry must not be accepted operationally.

Recovery must use independently verified transaction
evidence and a reviewed reconciliation procedure.

Automatic witness advancement is not authorized here.

### R3 - Witness Advanced; Transactional State Did Not

The authorities disagree.

The system must fail closed.

The situation requires security investigation and
independently authorized reconciliation.

The witness must not be automatically rolled backward.

### R4 - Both Authorities Report the Proposed Position

The position is logically consistent.

Operational currentness still requires authenticated
authority provenance and verified commit evidence.

Caller-constructed matching records are not sufficient.

### R5 - Both Authorities Report Conflicting Positions

Treat as an integrity or consistency incident.

Deny operational acceptance and preserve audit evidence.

### R6 - Authority or Communication Failure

The commit outcome may be unknown.

Do not infer failure or success solely from a timeout.

Reconcile against the independent authorities using
authenticated read and transaction evidence.

Until resolved, deny operational acceptance.

## 12. Idempotency and Transaction Identity

Future transitions must carry a unique transition
identifier bound to the expected and proposed positions.

The protocol must define how an authority recognizes
a repeated request after an uncertain outcome.

A repeated request must not create a second commitment.

The identifier must not be accepted without validating
the complete authenticated transition binding.

An attacker must not be able to substitute different
candidate content under an existing identifier.

Idempotency must not bypass revision, policy or
revocation checks.

## 13. Concurrency

The transactional authority must reject conditional
updates against stale revisions or generations.

Two independently valid candidates may compete from
the same prior state.

At most one can advance that state.

A losing candidate must undergo a fresh security
assessment against the latest authenticated position.

No stale result can be reused to authorize a different
transition.

Concurrent state and witness operations must not
establish divergent accepted histories.

## 14. Rollback-Witness Requirements

The witness must support independently authenticated
reads and a protected forward-only advancement contract.

Its security properties must be evaluated against
database restoration, host compromise and replay.

The witness must bind:

- Registry identity.
- Committed revision.
- Registry signing digest.
- Protected generation.
- Revocation-history commitment.
- Administrative policy epoch.
- Recovery epoch.
- Transition identifier.

A validly signed older checkpoint must not be accepted
as the current checkpoint.

The actual witness technology remains unselected.

## 15. Revocation Integrity

Revocation history must advance with the protected
transactional state.

Its commitment must agree with the independent
rollback-witness checkpoint.

A removed collector key must retain its required
historical tombstone.

A revoked public key must not be silently reused.

A split commitment cannot authorize revoked or
previously disabled key reactivation.

## 16. Bootstrap

An absent security-state record must not trigger
automatic bootstrap.

Initial authority setup requires independent approval.

The bootstrap ceremony must establish the authorized:

- Registry identity.
- Administrative trust anchors.
- Initial protected state.
- Initial revocation baseline.
- Rollback-witness checkpoint.
- Recovery authorities.
- Audit evidence.

No bootstrap functionality is implemented here.

## 17. Recovery

A future recovery process must establish the last
independently confirmed committed position.

Recovery must not silently decrease the accepted
revision or reset revocation history.

The procedure must address:

- Unknown commit outcomes.
- Lost response after commit.
- State ahead of witness.
- Witness ahead of state.
- Stale replicas.
- Backup restoration.
- Compromised credentials.
- Administrative signing-key compromise.
- Partial service restoration.

Automatic recovery is not permitted by this gate.

## 18. Failure and Audit Evidence

Security incident evidence should record:

- Authority identity and role.
- Requested registry scope.
- Observed and proposed generations.
- Revision and digest references.
- Transition identifier.
- Reconciliation classification.
- Failed verification step.
- Responsible authority or failed interface.
- Review and recovery status.

Audit evidence must not include private signing keys,
authentication secrets or unnecessary sensitive payloads.

Logs are not substitutes for trusted state.

## 19. Required Adversarial Tests

Future implementation tests must cover:

1. Correct state-authority identity.
2. Wrong state-authority identity.
3. Correct rollback-witness identity.
4. Substituted witness endpoint.
5. Unapproved administrative trust policy.
6. Administrative key revocation.
7. Replayed authenticated response.
8. Response bound to wrong registry.
9. Expired or missing authority credentials.
10. Stale state generation.
11. Stale witness checkpoint.
12. Both authorities reporting the previous state.
13. State advanced without witness advancement.
14. Witness advanced without state advancement.
15. Both authorities reporting the new state.
16. Both authorities reporting conflicting new states.
17. Transactional state authority unavailable.
18. Rollback witness unavailable.
19. Unknown transaction outcome.
20. Duplicate transition identifier.
21. Different payload under an existing transition ID.
22. Two concurrent candidate commits.
23. Revocation-history commitment mismatch.
24. State backup rollback.
25. Witness rollback.
26. Compromise of one authority domain.
27. Unauthorized bootstrap.
28. Unauthorized recovery.
29. Missing trusted time.
30. Attempted execution after uncertain state acceptance.

Contract tests must not claim that simulated authorities
provide genuine authentication or rollback resistance.

## 20. Implementation Boundaries

Gate 3D.12D introduces only this architecture decision.

It does not add:

- A security-state server.
- A network client.
- TLS credentials.
- A database.
- A hardware security device.
- A rollback-witness adapter.
- Administrative key provisioning.
- Operational automatic reconciliation.
- Container execution.
- Production release automation.

The next development gate may implement a pure,
non-authorizing reconciliation classifier and test it
against simulated failure scenarios.

Real operational adapters require separate approval.

## 21. Acceptance Criteria

This architecture gate is ready for review when:

1. Authority identities are explicitly separated.
2. Authenticated read requirements are defined.
3. Replay and freshness risks are addressed.
4. Transactional and witness updates remain distinct.
5. Split-commit failure cases are documented.
6. Uncertain outcomes fail closed.
7. Administrative trust remains independently controlled.
8. Bootstrap and recovery require independent approval.
9. No runtime authorization is introduced.
10. Existing security tests remain passing.

## 22. Final Decision

Future Basics will not treat matching state and witness
records as sufficient proof of security authority.

The future design must authenticate each authority
independently and verify the complete committed position.

Partially committed, stale, conflicting or uncertain
state must never grant operational acceptance.

Gate 3D.12D approves architecture review only.

Docker execution, automatic retries and production
deployment remain blocked.
