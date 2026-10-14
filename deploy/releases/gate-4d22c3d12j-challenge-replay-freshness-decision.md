# Gate 4D.22C.3D.12J - Challenge Lifecycle, Replay Resistance and Freshness

Status: ARCHITECTURE ONLY - OPERATIONAL APPROVAL PENDING
Date: 2026-10-14

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Operational challenge generator: NOT IMPLEMENTED
Protected replay-state service: NOT IMPLEMENTED
Authenticated authority trust roots: NOT PROVISIONED
Trusted time source: NOT IMPLEMENTED
Persistent replay prevention: NOT IMPLEMENTED
Independent rollback resistance: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Define a secure challenge lifecycle and response-freshness
architecture for the Future Basics security-authority system.

The design must prevent previously observed authority responses
from being accepted as new operational evidence.

It must support independent STATE, WITNESS and ADMIN authorities.

This gate defines requirements only.

No operational code, database, network service, private key,
challenge generator, replay cache or execution permission
is introduced.

## 2. Existing Security Foundation

The architecture builds upon:

Gate 3D.11B:
Administrative registry-signature verification.

Gate 3D.11F:
Offline, non-authorizing verification composition.

Gate 3D.12C:
Protected-state contracts.

Gate 3D.12D:
Independent authority authentication and reconciliation design.

Gate 3D.12E:
Pure reconciliation classification.

Gate 3D.12F:
Authority-evidence request and challenge binding.

Gate 3D.12G:
Cryptographic authority-response verification architecture.

Gate 3D.12H:
Laboratory Ed25519 authority-response verification.

Gate 3D.12I:
Authority trust-policy continuity and key rotation.

These gates establish logical and cryptographic contracts.

They do not establish independently provisioned trust anchors,
protected replay state or operational currentness.

## 3. Security Problem

An attacker may capture a previously valid authority response.

The response may contain:

- A valid Ed25519 signature.
- An approved-looking authority identifier.
- A consistent registry identity.
- A valid policy epoch.
- A correct state generation.
- A matching request identifier.
- A matching challenge.
- A consistent body and envelope commitment.

None of these properties independently proves that the
response is fresh or represents the currently accepted state.

A previously authentic response may be stale.

A previously accepted request may be replayed.

The system must distinguish signature validity from freshness,
challenge uniqueness, protected currentness and authorization.

## 4. Threat Model

The design must address an adversary who can:

- Capture legitimate response messages.
- Replay an earlier response.
- Delay or reorder messages.
- Duplicate requests or responses.
- Substitute an endpoint.
- Trigger communication failures.
- Restart an application process.
- Restore an older application database.
- Submit an old but validly signed response.
- Reuse a prior request identifier.
- Attempt cross-role response substitution.
- Force competing requests to execute concurrently.
- Exploit inconsistent response-consumption records.

A stronger adversary may compromise application configuration,
the challenge generator or the replay-state service.

This architecture must not assume that an application database
is independently protected merely because it is persistent.

## 5. Security Objectives

The future protocol must establish:

1. Unpredictable challenges.
2. Distinct request identities.
3. Binding to the intended authority roles.
4. Authenticated response-message integrity.
5. Bounded response-validity rules.
6. Durable tracking of issued challenges.
7. Prevention of accepted-response reuse.
8. Safe handling of uncertain outcomes.
9. Concurrency-safe challenge consumption.
10. Fail-closed behavior after restart or state loss.

These requirements are separate from proving that the reported
registry position is the latest authoritative position.

## 6. Challenge Generation

Operational challenges must originate from a reviewed
cryptographically secure random source.

The preferred initial security target is a minimum of
256 bits of unpredictable challenge material.

The existing Gate 3D.12F challenge_hex field represents
32 bytes encoded as 64 lowercase hexadecimal characters.

The future generator must not derive challenge material
solely from:

- Current timestamps.
- Process identifiers.
- Sequential database identifiers.
- Client-supplied values.
- Registry revision numbers.
- Deterministic counters without secret entropy.
- Untrusted environment variables.
- Previously issued challenge material.

Failure of the random source must deny request issuance.

No insecure fallback generator is permitted.

This gate does not implement a generator.

## 7. Request Identity

Every verifier-initiated authority-read operation must carry
a distinct request identifier.

The request identifier must be created and tracked within
the verifier's protected request lifecycle.

A request identifier is not itself proof of unpredictability.

The pair of request identity and challenge must be bound to
the expected registry, authority set and request purpose.

Reusing an existing request identifier for different
challenge material or a different request purpose is invalid.

## 8. Authority Role Binding

The existing challenge contract identifies three roles:

STATE
WITNESS
ADMIN

One logical request currently carries a shared challenge
that is expected in three role-separated responses.

The existing Gate 3D.12H signatures are domain-separated.

The future replay ledger must independently track response
consumption for each expected role within that request.

A valid STATE response must not satisfy WITNESS or ADMIN.

A response from an unapproved authority identity must fail.

An unexpected fourth authority cannot silently join a request.

A later change to per-role challenge generation would require
a separately versioned protocol and compatibility review.

## 9. Proposed Request Record

A future protected challenge record should bind:

- Protocol version.
- Registry identity.
- Request identifier.
- Challenge commitment.
- Request purpose.
- Expected STATE authority.
- Expected WITNESS authority.
- Expected ADMIN authority.
- Expected policy epoch.
- Relevant protected generation.
- Request lifecycle state.
- Expected response roles.
- Roles already processed.
- Issuance and expiry metadata.
- Protected request-generation number.
- Recovery or service epoch.
- Relevant audit correlation identifier.

The record must not accept arbitrary role changes
after the challenge has been issued.

A domain-separated commitment may identify a challenge
without requiring its full value in routine audit logs.

A commitment does not replace cryptographic randomness.

## 10. Request Lifecycle

The proposed future lifecycle is:

CREATED
The request has been constructed but not issued.

RESERVED
The request identifier and challenge have been durably
reserved against reuse in the protected replay ledger.

ISSUED
The reserved request has been sent to the expected authorities.

COLLECTING
Authenticated responses are being received and checked.

COMPLETE
The required response set has been processed.

EXPIRED
The request has exceeded an independently verified expiry rule.

ABORTED
The request is deliberately closed without acceptance.

UNCERTAIN
A communication or persistence failure prevents the verifier
from establishing the request's exact processing outcome.

The exact operational state machine must be approved
before any persistent implementation.

## 11. Required Ordering

The future implementation must durably reserve the challenge
before transmitting a request that relies upon it.

A request must not be issued first and recorded later
without an independently reviewed recovery protocol.

The verifier must check that the challenge belongs
to a live, protected request before processing a response.

After accepting a role-specific response for processing,
its consumption state must be protected against rollback.

Completing all three roles does not by itself establish
that their underlying security positions are current.

Currentness remains a separate protected-state decision.

## 12. Single-Use Semantics

A challenge must not be silently recycled for a new request.

A role-specific response must not be accepted twice
as two independent pieces of security evidence.

A duplicate response must be detected and classified.

A duplicate message must not create an additional
authority confirmation.

If a protocol later permits idempotent retrieval of an
already recorded result, that retrieval must not count
as a new acceptance or new trusted observation.

Automatic retransmission is not approved in this gate.

## 13. Persistent Replay Ledger

The future replay ledger must survive normal process restarts.

It must provide protected records of:

- Issued request identifiers.
- Reserved challenge commitments.
- Request-to-authority bindings.
- Role-specific response processing.
- Completed and invalidated requests.
- Relevant policy and recovery epochs.
- Outstanding uncertain operations.

The design requires atomic conditional transitions.

Simple application-memory sets are insufficient.

An ordinary application database without independent
rollback protection cannot prove durable replay resistance.

The future storage technology remains unselected.

## 14. Concurrency

Multiple workers may receive identical responses concurrently.

The protected replay ledger must prevent both workers
from consuming the same role-specific response as new evidence.

Conditional updates should use a protected record generation
or equivalent reviewed compare-and-swap mechanism.

A losing concurrent request must not infer acceptance
from another worker's success.

The design must specify how stale reads and conflicting
conditional updates are handled.

No automatic retry is authorized.

## 15. Crash Consistency

The system may crash after:

- Reserving a challenge.
- Sending a request.
- Receiving a validly signed response.
- Verifying a signature.
- Recording one authority response.
- Recording the final authority response.
- Updating the replay ledger.
- Returning a response to the application.

A crash can leave an uncertain outcome.

An uncertain outcome must not automatically be treated
as either successful consumption or unused challenge state.

The future recovery protocol must obtain independently
protected evidence of the last durable request state.

If that evidence is unavailable, processing must fail closed.

## 16. Restart and Database Restoration

After restarting, the verifier must not assume that its
local challenge history is complete.

A restored application database may omit previously
consumed requests.

A validly signed old response could then appear unused.

The replay-state service must therefore have protection
against silent rollback of its accepted generation.

Recovery must not reconstruct trusted replay state solely
from ordinary application logs.

If protected replay history cannot be established,
new operational acceptance must be denied.

## 17. Replay-State Rollback Witness

The future design must evaluate whether the replay ledger
requires an independently controlled monotonic witness.

The witness must not be silently reset during ordinary
application restore or administrative recovery.

A replay-state witness must bind a protected replay-state
generation or equivalent forward-only commitment.

The existing registry rollback witness may be considered
for composition only after explicit security review.

Separate security authorities must not be declared
independent merely because their logical APIs differ.

No replay witness is implemented by this gate.

## 18. Expiration and Retention

Operational requests must have bounded validity.

A request's expiry must be checked using a separately
reviewed trusted time or freshness mechanism.

An application-provided timestamp alone does not establish
trusted expiry.

Expiration must not automatically make previously used
request identifiers safe to reuse.

The system must retain sufficient history or a separately
protected monotonic marker to prevent accepted replay
within the applicable security horizon.

Retention, compaction and deletion require a future policy.

## 19. Trusted Time

The future design must distinguish:

Wall-clock time:
Used for absolute validity intervals and audit timestamps.

Monotonic elapsed time:
Potentially used for in-process deadlines where suitable.

Protected time evidence:
Needed where security decisions require independent assurance
of time or freshness across failures and restarts.

A local monotonic clock cannot reconstruct an authenticated
deadline across arbitrary database restoration and reboot.

A timezone-aware datetime supplied by a caller is not
independent proof of trusted time.

No trusted-time provider is selected in this gate.

## 20. Signature Verification

Authority response signatures must be verified using
the Gate 3D.12H Ed25519 verification boundary.

Signature verification must use the correct role-specific
signing domain and declared request bindings.

A valid signature establishes integrity relative to the
selected verification key.

It does not establish:

- That the key was independently provisioned.
- That the response has not been used before.
- That its signing key is currently authorized.
- That the response is the newest authority state.
- That the authority's backing state is rollback-resistant.
- That execution is permitted.

These remain separate requirements.

## 21. Trust Policy Freshness

The future verifier must reconcile authority key-policy
currentness with challenge processing.

The request must not silently accept a revoked signing key
merely because the key was active when the request began.

A policy rotation during an outstanding request must have
reviewed semantics.

The system must establish which independently trusted
policy generation governs verification.

An outstanding request must not override a later
administrative revocation.

The existing Gate 3D.12I policy chain is caller-supplied
and does not prove protected policy currentness.

## 22. Registry State Freshness

The transactional state authority may return a validly signed
record from an older registry generation.

A valid challenge match does not prove that the returned
generation is current.

The future protocol must reconcile authenticated STATE and
WITNESS positions against independently protected security
state and policy epochs.

A stale but validly signed record must not be accepted
merely because its challenge is fresh.

## 23. Split-Commit Behavior

Challenge completion does not resolve split commits between
the transactional registry state and rollback witness.

The following remain fail-closed situations:

- STATE advanced while WITNESS remained behind.
- WITNESS advanced while STATE remained behind.
- Unknown transactional commit outcome.
- Conflicting protected generations.
- Conflicting revocation commitments.
- Stale administrative trust policy.
- Missing or unverified replay history.

The existing Gate 3D.12E reconciliation classifier remains
non-authorizing.

## 24. Failure Classification

A future replay evaluator should distinguish:

UNKNOWN_REQUEST
The request identifier is absent from protected history.

UNRESERVED_CHALLENGE
The challenge was not durably reserved.

CHALLENGE_MISMATCH
The response does not match the reserved request.

ROLE_MISMATCH
The response is associated with the wrong authority role.

DUPLICATE_RESPONSE
The role-specific response was already processed.

EXPIRED_REQUEST
The protected expiry condition has been reached.

ABORTED_REQUEST
The request was invalidated.

UNCERTAIN_OUTCOME
The protected consumption outcome cannot be established.

REPLAY_STATE_UNAVAILABLE
The independently protected replay ledger cannot be read.

REPLAY_STATE_ROLLBACK
An older ledger generation or conflicting witness is observed.

POLICY_EPOCH_MISMATCH
The response does not match the applicable protected policy.

STATE_FRESHNESS_UNVERIFIED
The response cannot be established as the current state.

Classification alone must never authorize execution.

## 25. Communication Failure

Timeouts must not automatically release a reserved challenge.

A timeout does not prove that the authority failed
to process a request.

A lost acknowledgement does not prove that the replay
ledger failed to record response consumption.

Unknown outcomes must be reconciled using independently
protected evidence.

A new request, if eventually authorized, must use a
fresh request identity and fresh challenge material.

No automatic retry is permitted here.

## 26. Idempotency

Idempotency must not weaken single-use replay semantics.

A repeated request may refer to an earlier durable result
only under a reviewed, authenticated retrieval procedure.

Repeated processing must not produce additional independent
authority confirmations.

A request identifier cannot be rebound to different
challenge material, authority identities or registry scope.

An attacker must not substitute new payload content
under a previously recorded request identity.

## 27. Operational Trust Separation

The proposed security architecture requires distinct:

1. Authority signing-key trust.
2. Authority response authentication.
3. Challenge generation and reservation.
4. Protected replay-state tracking.
5. Policy and registry currentness verification.
6. Durable state/witness reconciliation.
7. Runtime execution authorization.

The successful completion of one control must not
automatically authorize the next.

The system must remain fail closed when a required
control is unavailable or unverified.

## 28. Administrative Recovery

Emergency replay-state recovery requires an independently
reviewed administrative ceremony.

The procedure must preserve evidence of previously
consumed requests and protected state generations.

Recovery must not simply reset the replay ledger to empty.

The ADMIN authority must not silently authorize recovery
of its own compromised trust configuration.

The recovery authority and approval process remain
outside the present implementation.

## 29. Security Logging

Future audit records should include:

- Request identifier.
- Authority role and approved identifier.
- Registry identity.
- Challenge commitment.
- Policy epoch and request generation.
- Response-verification classification.
- Replay-detection outcome.
- Relevant protected record generation.
- Recovery or incident reference.

Private keys, authentication secrets and unnecessary
sensitive payloads must never be included in logs.

Audit logs are evidence for investigation, not a
substitute for protected replay-state authority.

## 30. Adversarial Test Requirements

A subsequent implementation gate must test:

1. Structurally valid challenge.
2. Malformed challenge.
3. Invalid request identifier.
4. Duplicate request identifier.
5. Duplicate challenge material.
6. Reused request ID with changed challenge.
7. Reused challenge with changed request ID.
8. Unreserved challenge.
9. Request issued before reservation.
10. Previously consumed response.
11. Duplicate concurrent response.
12. STATE response substituted for WITNESS.
13. WITNESS response substituted for ADMIN.
14. Wrong registry identity.
15. Wrong expected authority identity.
16. Wrong request purpose.
17. Valid signature on an old request.
18. Valid signature on an expired request.
19. Expired request incorrectly reactivated.
20. Previously aborted request.
21. Partially collected request.
22. Replayed role confirmation.
23. Changed protected policy epoch.
24. Revoked signing key during processing.
25. Stale registry generation.
26. STATE/WITNESS split commitment.
27. Unknown commit outcome.
28. Lost response acknowledgement.
29. Crash before replay-state consumption.
30. Crash after replay-state consumption.
31. Restart with complete protected state.
32. Restart with missing replay records.
33. Restored older application database.
34. Rolled-back replay-ledger generation.
35. Conflicting replay-witness commitment.
36. Missing trusted time.
37. Untrusted caller-provided timestamp.
38. Exhausted challenge generation source.
39. Replay-ledger authority unavailable.
40. Concurrent duplicate challenge reservation.
41. Unauthorized bootstrap.
42. Unauthorized recovery.
43. Forged self-consistent replay records.
44. Successful logical analysis without authentication.
45. Attempted Docker authorization after replay checks.

Tests must preserve false operational authorization flags.

A test fixture that supplies an expected challenge
does not prove its challenge was unpredictable.

A simulated replay ledger does not prove durable
protection against actual rollback.

## 31. Gate 3D.12K Implementation Boundary

The next implementation gate may introduce:

- Immutable challenge-lifecycle dataclasses.
- Bounded lifecycle state enumerations.
- Pure transition-validation functions.
- Non-authorizing replay classifications.
- Simulated race and crash scenarios.
- Adversarial laboratory unit tests.

It must not introduce:

- Operational random challenge generation.
- Persistent replay-state writes.
- Network authority clients.
- Automated recovery or retries.
- Independent trust-anchor provisioning.
- Production credentials.
- Docker execution.
- Production deployment.

Any actual replay-state service must receive a separate
architecture review and operational security approval.

## 32. Acceptance Criteria

Gate 3D.12J is ready for architecture review when:

1. Challenge generation requirements are explicit.
2. Request identities and authority roles are bound.
3. Reservation must precede issuance.
4. Single-use consumption requirements are defined.
5. Persistent replay-state requirements are defined.
6. Crash and restart cases are addressed.
7. Database rollback risks are addressed.
8. Trusted time dependencies are explicit.
9. Policy and registry freshness are distinguished.
10. No operational implementation is introduced.
11. Existing security tests remain passing.
12. Docker execution and deployment remain blocked.

## 33. Final Decision

Future Basics will require independently protected
challenge reservation, response-consumption tracking,
and freshness verification before accepting operational
authority evidence.

A valid Ed25519 signature, a matching challenge and a
logically consistent registry position are individually
insufficient to establish authoritative currentness.

Gate 3D.12J approves architecture review only.

Docker execution, automatic retries and production
deployment remain blocked.
