# Gate 4D.22C.3D.12L - Protected Replay-State Authority and Recovery

Status: ARCHITECTURE ONLY - OPERATIONAL APPROVAL PENDING
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Operational replay-state authority: NOT IMPLEMENTED
Independent replay rollback witness: NOT IMPLEMENTED
Durable challenge reservation: NOT IMPLEMENTED
Authenticated operational authority adapters: NOT IMPLEMENTED
Independently provisioned trust anchors: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Define an independently protected replay-state authority
and recovery architecture for Future Basics security-authority
requests.

The design must protect challenge reservation, single-use
response consumption, request completion and recovery from
crashes, concurrent operations and database restoration.

This gate defines operational requirements and interface
boundaries only.

It does not implement storage, networking, state writes,
credentials, service adapters, retries or deployment.

## 2. Existing Security Foundation

The design builds on the following gates.

Gate 3D.12C:
Protected registry-state authority interfaces.

Gate 3D.12D:
Authority authentication and split-commit reconciliation.

Gate 3D.12E:
Pure registry-state reconciliation classification.

Gate 3D.12F:
Authority response and challenge binding.

Gate 3D.12G:
Cryptographic authority-response verification architecture.

Gate 3D.12H:
Laboratory Ed25519 response-signature verification.

Gate 3D.12I:
Authority trust-policy continuity.

Gate 3D.12J:
Challenge lifecycle and replay-resistance architecture.

Gate 3D.12K:
Pure challenge lifecycle and replay classification.

Existing laboratory components remain non-authorizing.

## 3. Fundamental Security Problem

Gate 3D.12K can reject repeated requests and responses
inside a supplied immutable ReplayLedgerSnapshot.

It cannot prove that the supplied snapshot is genuine,
the newest snapshot or durably recorded.

A malicious caller may construct a new snapshot.

Two independent callers may start from the same snapshot
and produce competing proposed updates.

A database restored from backup may forget consumed
responses and challenge reservations.

Therefore, genuine replay prevention requires more than
a validated dataclass or matching SHA-256 commitment.

## 4. Trust Domains

The future architecture requires separate control of:

A. The verifier and application runtime.

B. The replay-state transactional authority.

C. The independent replay rollback witness.

D. The authority signing-key trust policy.

E. The registry STATE and WITNESS authorities.

F. The administrative recovery process.

Logical API separation alone does not establish independent
security or administrative control.

The selected services must undergo independent threat
modeling, provisioning and authority-identity review.

## 5. Replay-State Transactional Authority

A future replay-state authority must maintain the currently
accepted challenge lifecycle and response-consumption state.

Required properties include:

- Strongly consistent reads.
- Unique request identifier enforcement.
- Unique challenge commitment enforcement.
- Atomic conditional record transitions.
- Strict monotonic ledger generations.
- Concurrency-safe role consumption.
- Persistent terminal request records.
- Durable commit evidence.
- Authenticated read and write interfaces.
- Protected administrative access.
- Explicit uncertain-outcome handling.

A normal application database must not automatically be
regarded as meeting these requirements.

## 6. Independent Replay Rollback Witness

The replay-state witness must maintain an independently
protected forward-only commitment to the accepted
replay-ledger security position.

The witness must not be controlled by the same
administrative rollback domain as the primary replay ledger.

A restoration of the primary database must not silently
restore the witness to the same older point.

The witness must bind:

- Registry identity.
- Replay ledger identity.
- Protected ledger generation.
- Replay-state commitment.
- Relevant policy epoch.
- Recovery epoch.
- Transition identifier.

The witness cannot be advanced or rolled back merely
because the application supplies a matching dataclass.

## 7. Independence From Registry State Witness

The existing registry rollback-witness architecture and the
proposed replay-state rollback witness protect different data.

Reusing the same provider or underlying service is not
automatically approved.

Any shared infrastructure must undergo an explicit
independence and failure-domain assessment.

A compromised registry-state administrator must not
automatically obtain authority to reset replay history.

A replay-state failure must not silently permit acceptance
of a registry state.

## 8. Protected Replay-Ledger Position

The future protected ledger position should bind:

- Protocol version.
- Registry identity.
- Replay ledger identity.
- Ledger generation.
- Canonical replay-state commitment.
- Policy epoch.
- Recovery epoch.
- Transition identifier.
- Previous protected commitment.

The ledger position and witness checkpoint must use a
reviewed canonical representation.

The exact protected-state wire format requires a separate
implementation decision.

A structural commitment alone does not authenticate the
authority that reports the position.

## 9. Replay Record Requirements

A durable replay record must retain:

- Request identifier.
- Challenge commitment.
- Registry identity.
- Request purpose.
- Expected STATE authority identity.
- Expected WITNESS authority identity.
- Expected ADMIN authority identity.
- Expected policy epoch.
- Expected registry-state generation.
- Request lifecycle state.
- Request record generation.
- Role-specific consumed response references.
- Relevant expiry and recovery metadata.
- Creation and transition audit references.

Challenge commitments must use domain separation.

The design must preserve sufficient information to reject
previously consumed requests and challenges.

## 10. Challenge Material

The approved future challenge generator must use a reviewed
cryptographically secure random source.

The initial target remains 256 bits of unpredictable
challenge material.

Challenge material must be generated by the verifier,
not chosen by an untrusted remote authority.

The generator must fail closed if secure entropy is
unavailable.

The replay authority must reject uniqueness conflicts
against its protected history.

A challenge matching a supplied request does not prove
that the challenge was unpredictable.

This gate does not implement challenge generation.

## 11. Unique Reservation Rules

A request identifier must not be reused for a different
challenge, purpose, authority set or registry scope.

A previously reserved challenge must not be reused under
a different request identifier.

Reservation must be atomic within the replay authority.

If competing clients reserve the same identifier or
challenge, no more than one reservation may commit.

The losing client must not assume its request was reserved.

## 12. Reservation Before Issuance

The future operational sequence must be:

Step 1:
Obtain independently verified authority trust configuration.

Step 2:
Generate a new verifier-owned request identifier and
cryptographically unpredictable challenge.

Step 3:
Read and authenticate the replay-state authority and its
independent witness.

Step 4:
Verify their protected generations and commitments agree.

Step 5:
Submit a conditional reservation of the new request.

Step 6:
Confirm the durable reservation outcome.

Step 7:
Advance and independently verify the replay witness under
a separately reviewed monotonic advancement protocol.

Step 8:
Issue the authority-read request only after the necessary
reservation and witness guarantees have been established.

A successful primary ledger write alone is insufficient
when the witness has not been reconciled.

No automated witness catch-up is approved here.

## 13. Conditional State Transitions

Every future state-changing request must identify:

- Expected ledger generation.
- Expected request record generation.
- Request identifier.
- Transition identifier.
- Intended lifecycle operation.
- Canonical operation commitment.

The authority must reject stale expected generations.

Repeated transition identifiers must not commit different
payloads.

An uncertain response must not be treated as evidence
that a transition failed.

Actual conditional writes require a separately reviewed
storage transaction implementation.

## 14. Role-Specific Response Consumption

Each signed authority response must first be checked
against independently trusted authority key material.

The verifier must validate:

- Signature and role-specific purpose.
- Expected authority identity.
- Registry and request identifier.
- Request challenge.
- Response body and envelope commitments.
- Current relevant authority-key policy.
- Expected protected policy epoch.
- Expected registry-state generation.
- Applicable expiry and freshness rules.

Only after those checks may a future authenticated
conditional consumption operation be considered.

The replay authority must independently enforce that the
role has not already been consumed for the request.

An unkeyed body commitment is not authentication.

## 15. Consumption Commit Semantics

A successfully verified response must not be counted as
newly consumed solely because signature verification passed.

The response must be committed to protected replay state.

The replay witness must be reconciled with the durable
consumption position under the reviewed protocol.

A duplicate receipt must not create another independent
authority confirmation.

A changed receipt for an already consumed role must be
treated as an integrity conflict.

A lost acknowledgement must produce an uncertain outcome,
not an automatic retry.

## 16. Request Completion

The replay record may be logically COMPLETE only when
all three expected roles have been consumed under the
reviewed state-transition protocol.

The final replay-state position must be independently
reconciled with its witness.

Completion does not establish:

- Current registry authority state.
- Current administrative trust policy.
- Trustworthy time.
- Two-authority transaction atomicity.
- Runtime isolation.
- Deployment authorization.

These remain separate security decisions.

## 17. Two-Authority Atomicity

The replay-state authority and independent replay witness
do not automatically share a single atomic transaction.

A primary state commit may succeed while witness
advancement fails.

The witness may report advancement when the primary state
cannot be independently confirmed.

A timeout may hide a successful commit.

The architecture must not treat separate successful API
acknowledgements as proof of atomicity.

Until authenticated reconciliation completes, no new
operational replay acceptance may be established.

## 18. Reconciliation Outcomes

R1 - Both authorities show the previous replay position.

The proposed operation is not independently established
as committed.

No automatic replay or retry is authorized.

R2 - Replay state is ahead of the witness.

Classify as a split commitment.

Fail closed and require independently reviewed recovery.

R3 - Replay witness is ahead of replay state.

Treat as a possible state loss, rollback or unresolved
distributed transaction.

Fail closed without rolling the witness backward.

R4 - Both report the proposed replay position.

Require authenticated identities, fresh independent reads,
durable commit evidence and verified protected currentness.

Matching declarations alone are insufficient.

R5 - Replay positions conflict unexpectedly.

Treat as an integrity incident.

Preserve evidence without attempting silent repair.

R6 - A required authority is unavailable.

Classify the outcome as unavailable or uncertain.

Do not infer commit success or failure from timeout alone.

## 19. Concurrent Requests

Concurrent requests against one replay ledger must use
strict conditional generation checks.

For one request, competing response consumers must not
both create a new role-consumption event.

The authority must enforce request uniqueness and
challenge uniqueness within its transaction boundary.

A stale caller must undergo fresh authenticated reads.

There must be no automatic last-write-wins acceptance.

## 20. Concurrent Witness Advancement

Witness advancement must use an expected checkpoint.

A stale witness checkpoint cannot authorize a new
monotonic position.

If two independent callers attempt advancement, the
witness must prevent an older position from overwriting
a newer accepted checkpoint.

The protocol must define how a losing caller observes
and investigates the committed state.

No implicit automatic retry is authorized.

## 21. Crash Consistency

The future implementation must handle failures after:

1. Challenge generation.
2. Reservation request construction.
3. Primary reservation commit.
4. Replay witness advancement.
5. Authority request issuance.
6. Signed response receipt.
7. Signature verification.
8. Primary role-consumption commit.
9. Witness advancement after consumption.
10. Recording all role receipts.
11. Final request completion.
12. Returning an acknowledgement to the application.

Each failure window must have an explicit outcome
classification and safe reconciliation procedure.

No crash window may silently make a previously used
request or challenge available again.

## 22. Unknown Transaction Outcomes

A communication timeout does not establish that a
transaction failed.

A missing acknowledgement does not establish that a
transaction was never committed.

The future interface must expose a way to inspect
transaction identity and protected generation using
independently authenticated read evidence.

The recovered outcome must be checked against the
separate witness.

Uncertain transactions must remain unavailable for
ordinary automated replay processing until reconciled.

## 23. Process Restart

After a process restart, the application must not trust
only its in-memory challenge history.

It must obtain the protected replay ledger and witness
from independently authenticated authorities.

Any previously incomplete request must be reconciled.

The application must not reconstruct a trusted ledger
solely from cached dataclasses or local logs.

If protected replay state cannot be established,
operational processing must remain blocked.

## 24. Application Database Restoration

Restoring an older application database may erase
knowledge of previously consumed responses.

The replay authority must be independent of ordinary
application database restoration.

If the replay ledger itself is restored from an older
backup, its independent witness must detect that the
protected generation or commitment has regressed.

An old but validly signed response must not become
eligible for acceptance because historical records
disappeared from a restored database.

## 25. Replay Authority Compromise

The threat model must include compromise of:

- Application verifier credentials.
- Replay-ledger write credentials.
- Replay-ledger administrative credentials.
- The primary replay-state database.
- Replay-witness access credentials.
- Authority-signing keys.
- The independently approved trust-policy source.

Compromising one authority must not silently permit
replacement of another authority's trusted identity.

The design must document the blast radius of every
credential and recovery role.

## 26. Recovery Epoch

A protected recovery epoch must identify explicitly
approved recovery transitions.

Ordinary request reservations and consumptions must not
change the recovery epoch.

A recovery operation must not silently reset consumed
request history or administrative key revocation.

An emergency recovery epoch change must have independently
approved authorization and audit evidence.

No emergency recovery implementation is created here.

## 27. Replay-State Bootstrap

An empty application database does not authorize creation
of a new trusted replay ledger.

Bootstrap must be an independently approved procedure.

It must establish:

- Approved registry scope.
- Replay-ledger identity.
- Initial protected generation.
- Initial replay-state commitment.
- Initial recovery epoch.
- Independently approved authority identities.
- Initial witness checkpoint.
- Administrative ownership and audit evidence.

A caller-supplied genesis object is not bootstrap proof.

## 28. Trusted Time and Expiry

Operational request expiry requires an approved freshness
or trusted-time mechanism.

A timezone-aware caller-supplied datetime is not proof
of trusted time.

Expiry must not automatically permit reuse of previously
reserved request identifiers or challenge commitments.

The replay state must preserve enough terminal history
or independently protected non-reuse evidence.

No trusted-time provider is selected.

## 29. Retention and Compaction

The 128-record bound used by Gate 3D.12K is suitable only
for bounded laboratory assessment.

It does not define operational storage capacity.

Future retention and compaction must preserve the
ability to reject previously consumed or reserved
security-critical identities.

Deleting a closed request must not silently make its
challenge reusable.

Compaction requires a separately reviewed commitment
and witness-continuity design.

## 30. Evidence and Audit

Future security audit records should include:

- Registry and replay-ledger identities.
- Request identifier.
- Challenge commitment.
- Authority role and approved identity.
- Policy epoch and protected generation.
- Relevant operation and transition identifiers.
- State and witness commitments.
- Request lifecycle classification.
- Failed verification stage.
- Recovery or incident reference.

Do not log private signing keys, authentication secrets
or unnecessary sensitive response contents.

Logs are not a substitute for a trusted state authority.

## 31. Proposed Future Interfaces

The replay-state authority should expose conceptual
operations similar to:

read_replay_position(registry_id)

read_request_record(request_id)

conditional_reserve_challenge(expected_position, request)

conditional_consume_role(expected_position, request_id, receipt)

conditional_close_request(expected_position, request_id, outcome)

read_transition_outcome(transition_id)

The independent witness should expose:

read_replay_checkpoint(registry_id)

conditional_advance_checkpoint(expected_checkpoint, new_position)

These are architecture-level shapes only.

No concrete Python protocol, storage API or network
endpoint is approved in this gate.

## 32. Authentication Requirements

Future operational reads and writes must authenticate:

- The intended replay authority.
- The intended replay witness.
- The caller's permitted operation.
- The registry scope.
- The request and transition identities.
- The current relevant administrative trust policy.

Authentication cannot rely solely on caller-supplied
authority labels or the response's own public key.

Service-to-service permissions must be independently
provisioned and reviewed.

## 33. Read and Write Separation

Read and conditional-write permissions must be distinct.

An application component allowed to read replay status
must not automatically be able to reset or modify it.

Recovery operations require separately controlled authority.

No normal application role may directly rewrite
consumed response history.

The future design must support independently reviewable
access-control evidence.

## 34. Idempotency

Idempotency must be bound to the full operation:

- Transition identifier.
- Request identity.
- Challenge commitment.
- Expected state generation.
- Authority and role scope.
- Operation payload commitment.

Reusing one transition identifier with different content
must be rejected.

A duplicate acknowledgement must not result in a
second independent consumption event.

Idempotent result retrieval must not be misrepresented
as a newly committed security observation.

No automatic retransmission is permitted by this decision.

## 35. Failure Classifications

Future implementations should distinguish:

AUTHORITY_UNAVAILABLE

WITNESS_UNAVAILABLE

STALE_EXPECTED_GENERATION

REQUEST_ID_ALREADY_RESERVED

CHALLENGE_ALREADY_RESERVED

ROLE_ALREADY_CONSUMED

CONFLICTING_ROLE_RECEIPT

POLICY_EPOCH_CONFLICT

STATE_GENERATION_CONFLICT

UNKNOWN_COMMIT_OUTCOME

STATE_AHEAD_OF_WITNESS

WITNESS_AHEAD_OF_STATE

REPLAY_STATE_ROLLBACK_SUSPECTED

WITNESS_ROLLBACK_SUSPECTED

UNAUTHENTICATED_AUTHORITY

RECOVERY_APPROVAL_MISSING

TRUSTED_TIME_UNAVAILABLE

INVALID_RECOVERY_EPOCH

NO_OPERATIONAL_AUTHORIZATION

Classifications are diagnostic and non-authorizing.

## 36. Required Future Adversarial Tests

The future implementation must test:

1. Correctly authenticated replay-state read.
2. Wrong replay-state authority identity.
3. Wrong replay-witness identity.
4. Replayed authenticated ledger read.
5. Stale ledger generation.
6. Conflicting ledger commitment.
7. Duplicate request reservation.
8. Duplicate challenge reservation.
9. Concurrent duplicate reservations.
10. Reservation committed before request issuance.
11. Request issued without proven reservation.
12. State reservation ahead of witness.
13. Witness ahead of primary state.
14. Lost reservation acknowledgement.
15. Replayed conditional reservation request.
16. Changed payload under the same transition ID.
17. Valid role response with fresh challenge.
18. Duplicate consumed role response.
19. Changed content for a consumed role.
20. Concurrent consumption of the same role.
21. Revoked signing key during collection.
22. Policy epoch changing during collection.
23. Stale protected registry generation.
24. State/witness registry mismatch.
25. Primary consumption ahead of replay witness.
26. Witness ahead after uncertain consumption.
27. Crash before primary commit.
28. Crash after primary commit.
29. Crash after witness advancement.
30. Crash after final completion.
31. Restart with complete protected state.
32. Restart with missing application cache.
33. Restore of an older application database.
34. Restore of an older replay-state database.
35. Replay-witness rollback attempt.
36. Missing replay-witness checkpoint.
37. Compromised replay-state write credential.
38. Unauthorized replay-ledger bootstrap.
39. Unauthorized recovery-epoch reset.
40. Missing trusted time for expiry.
41. Retention that would permit identity reuse.
42. Expired request incorrectly reactivated.
43. Aborted request incorrectly reactivated.
44. Unknown transaction outcome.
45. Reconciliation after a failed network response.
46. Forged matching state and witness records.
47. Stale administrative policy approval.
48. Attempted unauthorized role escalation.
49. Invalid authority key rotation during recovery.
50. Attempted Docker authorization after valid replay checks.

A simulated success must not be reported as actual
durable replay prevention.

## 37. Implementation Boundaries

A subsequent gate may define pure contracts for:

- Transactional replay-state positions.
- Conditional operation intents.
- Replay-witness checkpoints.
- Transition acknowledgement classification.
- Split-commit and recovery assessment.
- Protected generation and digest consistency.

It must not create operational persistence, network
clients, signing keys or automatic recovery.

A real storage adapter requires a separate, explicit
technology and operational security review.

## 38. Acceptance Criteria

Gate 3D.12L is ready for review when:

1. Replay-state authority boundaries are defined.
2. Independent witness responsibilities are explicit.
3. Reservation-before-issuance is preserved.
4. Conditional consumption semantics are defined.
5. Split commits are classified as unsafe.
6. Crash and unknown-commit outcomes are addressed.
7. Recovery and bootstrap require independent approval.
8. Replay history rollback is prohibited.
9. Key-policy provenance remains a separate dependency.
10. Trusted time remains a separate dependency.
11. No operational services or execution are introduced.
12. Existing security tests remain passing.
13. Docker execution and production deployment remain blocked.

## 39. Final Decision

Future Basics will require an independently authenticated
transactional replay-state authority and separately
controlled forward-only replay witness before operational
challenge reservations or response consumptions can be
treated as durable security evidence.

Matching caller-supplied records, valid Ed25519 signatures,
logical lifecycle completion and local SHA-256 commitments
are individually insufficient.

Gate 3D.12L authorizes architecture review only.

Docker execution, automatic retries and production
deployment remain blocked.
