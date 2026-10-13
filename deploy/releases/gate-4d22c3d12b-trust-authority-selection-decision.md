# Gate 4D.22C.3D.12B - Trust Authority Selection

Status: PREFERRED ARCHITECTURE - OPERATIONAL APPROVAL PENDING
Date: 2026-10-13

Production deployment: DISABLED
Laboratory Docker execution: DENIED
Automatic retry: DENIED
Operational protected-state service: NOT IMPLEMENTED
Independent trust-anchor provisioning: NOT AUTHORIZED
Rollback-resistant checkpoint: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Purpose

Select a preferred architecture for independently protecting
Future Basics laboratory registry revision and revocation state.

This decision follows Gate 4D.22C.3D.12A.

The existing offline registry composition verifies administrative
signatures and evaluates logical revision and revocation continuity.

However, the administrative policy and state snapshots are still
caller-supplied.

This gate identifies a preferred security architecture for
addressing that limitation.

No service is installed, configured or authorized by this decision.

## 2. Security Problem

A correctly signed registry is not necessarily current.

An attacker could present an older signed registry together
with an older revision-state snapshot.

The existing offline evaluators may find those inputs internally
consistent without establishing their authoritative provenance.

A future operational verifier therefore requires independently
protected information about:

- Approved administrative signing authorities.
- Highest committed registry revision.
- Accepted registry signing digest.
- Protected state generation.
- Collector-key revocation history.
- Administrative trust-policy version.
- Recovery and bootstrap authority.

The trusted authority must not be controlled by the registry
document, the evidence collector or the application workload.

## 3. Selection Principles

The selected architecture must provide:

1. Independent security administration.
2. Authenticated state reads.
3. Authenticated conditional state updates.
4. Strong consistency for accepted registry revisions.
5. Atomic revision and revocation updates.
6. Protection against unauthorized state rollback.
7. Durable committed-state evidence.
8. Secure administrator trust-policy management.
9. Controlled bootstrap and recovery.
10. Explicit failure and audit semantics.

Meeting a data-format contract is not proof of authority.

A signed file or database transaction alone does not establish
rollback resistance.

## 4. Candidate A - Independent Transactional Service

Description:

An independently administered security-state service holds
registry revisions, signing digests, generations and revocation
history.

The service exposes authenticated read and conditional update
operations.

Advantages:

- Centralized revision history.
- Strong concurrency controls.
- Consistent state for multiple verifiers.
- Operationally understandable transaction model.
- Possible integration with existing organizational operations.
- Clear separation between read and commit permissions.

Limitations:

- Database backups may be restored to earlier states.
- Database administrators may have powerful privileges.
- Storage-level rollback can defeat ordinary transactions.
- Service compromise may compromise all protected state.
- Availability depends on the security-service infrastructure.

Assessment:

Suitable as a transactional authority only if independent
administration and external rollback detection are demonstrated.

A standard application database is not sufficient by itself.

## 5. Candidate B - Hardware Monotonic Authority

Description:

A protected hardware mechanism maintains monotonic state,
such as a generation or counter.

Advantages:

- Potential resistance to application-host rollback.
- Security state can be separated from ordinary files.
- Some compromise scenarios require access to hardware authority.

Limitations:

- Hardware capabilities vary.
- Counter exhaustion or rate limits may matter.
- Hardware replacement requires controlled recovery.
- Multiple verifier hosts need coordinated state.
- Hardware availability and lifecycle add dependencies.
- A monotonic number alone cannot protect full revocation history.

Assessment:

Potentially useful as a rollback witness or anchor.

Not selected as the sole registry-state database.

Any hardware-backed proposal requires a specific threat model
and verified implementation behavior.

## 6. Candidate C - Dedicated Security Control Plane

Description:

A separately operated security platform manages administrative
trust anchors, registry revisions, revocations and protected
state transitions.

Advantages:

- Strong organizational separation.
- Centralized policy administration.
- Independent security auditing.
- Potential for coordinated recovery and revocation publication.

Limitations:

- Higher operational complexity.
- Additional infrastructure and access-control requirements.
- Potential service availability dependencies.
- Custom implementations introduce additional attack surface.
- Rollback resistance still requires an explicit design.

Assessment:

A possible longer-term architecture.

Not selected as an unrestricted custom implementation.

## 7. Preferred Architecture

Preferred candidate:

INDEPENDENT TRANSACTIONAL SECURITY-STATE AUTHORITY
WITH A SEPARATELY PROTECTED ROLLBACK WITNESS.

This is a conditional architecture preference.

It is not a product selection or operational authorization.

The design has three distinct elements:

### 7.1 Administrative Trust Authority

An independently managed authority controls the approved
administrative public-key policy.

It is responsible for:

- Initial approved administrative keys.
- Signing-authority lifecycle.
- Key rotation and revocation.
- Policy versioning.
- Administrative recovery.
- Independent authorization evidence.

The collector registry cannot create its own trust anchors.

Administrative trust-policy epochs require protection against
unauthorized rollback.

### 7.2 Transactional Registry-State Authority

An independently administered transactional service owns:

- Registry identity.
- Registry format version.
- Highest committed revision.
- Accepted registry signing digest.
- Protected state generation.
- Approved trust-policy reference.
- Revocation-history contents or authenticated digest.
- Committed transition identifier.
- Transaction and recovery status.

Updates must use authenticated, linearizable conditional
transactions or equivalent guarantees.

Revision and revocation-history changes must be committed
as one logical unit.

### 7.3 Independent Rollback Witness

A separately controlled witness maintains a forward-only,
authenticated record of the committed security-state position.

The witness must bind the relevant:

- Registry identity.
- Registry revision.
- Registry signing digest.
- Protected state generation.
- Revocation-history commitment.
- Administrative trust-policy epoch.
- Commit or recovery epoch.

The witness must be outside the effective rollback-control
domain of the transactional-state administrator.

Ordinary signing of a witness record is not enough.

The witness must itself resist replacement with an older
validly signed witness record.

Its threat model, durability and monotonicity must be
independently evaluated before approval.

## 8. Authority Separation

The application workload must not administer the security
authority.

Evidence collectors must not write authoritative registry state.

Registry issuers must not directly reset the trusted revision
floor or revoke protected history.

The verifier may request a read or submit a conditional
transition only through approved authenticated interfaces.

The rollback witness must not accept unverified registry
claims as authoritative state.

Administrative bootstrap and recovery must require
independent approval.

## 9. State Read Contract

A future protected read must provide:

- Authenticated authority identity.
- Registry-state identity.
- Current committed revision and digest.
- Protected generation.
- Revocation-history commitment.
- Administrative policy reference.
- Transaction status.
- Witness reconciliation status.

A successful service response is not automatically a
trusted response.

The verifier must validate the authority identity, response
integrity, freshness and relevant witness relationship.

A stale, unsigned or unauthenticated response must not
establish registry currentness.

## 10. Conditional Commit Contract

A candidate transition must require:

candidate.revision = committed.revision + 1

candidate.previous_revision = committed.revision

candidate.previous_digest = committed.signing_digest

The expected protected generation must also match.

The transition must atomically bind registry revision,
signing digest and revocation history.

At most one competing update may advance a particular
protected generation.

An offline composition result is an input to future
authorization review, not permission to commit.

## 11. Witness and Commit Coordination

The transactional service and rollback witness are separate
security authorities.

Their updates must not be described as atomically coordinated
unless the implementation proves that property.

A possible future protocol must explicitly handle:

- State transaction prepared but not committed.
- State committed but witness not advanced.
- Witness advanced but state not durably committed.
- Both operations committed.
- Response lost after an uncertain commit.
- Process or host crash between operations.
- Conflicting or duplicated update requests.

The design must define authoritative commit visibility.

No registry transition may be reported as trusted merely
because one of the two authorities advanced.

Any uncertain, missing or contradictory commitment evidence
must fail closed pending trusted reconciliation.

## 12. Rollback Detection

The future verifier must compare the authenticated
transactional state against the independently protected
witness position.

If the transactional state is restored to an older revision
while the witness has advanced, the disagreement must be
detected and operational acceptance denied.

If the witness is stale or unavailable, operational
acceptance must remain denied.

A consistent pair of values is not enough unless the witness
and state authority have independently verified provenance.

A compromise that can roll back both authorities may defeat
the protection.

The approved threat model must address common-mode compromise.

## 13. Administrative Trust Policy

Administrative public-key policies must be provisioned
outside the registry publication path.

The architecture must provide:

- Independently authorized enrollment.
- Approved identity and purpose binding.
- Trust-policy versioning.
- Secure public-key distribution.
- Independent administrative revocation.
- Rotation and compromise handling.
- Audit evidence.
- Controlled historical verification policy.

A registry signature under an attacker-supplied administrator
key must not establish registry authorization.

No private-key provisioning is permitted by this gate.

## 14. Collector Revocation History

Collector-key revocation history must remain linked to the
protected committed revision.

The state authority must preserve revoked and disabled
key tombstones across registry updates.

Removal of a registry record cannot erase historical
revocation information.

Previously revoked public-key material must not be
silently reused under another collector identity.

The witness must bind the authenticated revocation-history
commitment to the accepted state generation.

## 15. Multi-Host Consistency

All operational verifiers must share one coordinated
authoritative security-state history.

Independent verifier hosts must not accept conflicting
registry revisions as current.

A stale replica cannot authorize registry advancement.

Network partitions must not permit divergent commits.

Disconnected verifiers may perform explicitly labeled
offline analysis, but must not claim authoritative currentness.

## 16. Trusted Time Dependency

The preferred architecture does not itself establish
trusted time.

A separate trusted-time mechanism must provide verified
time information and explicit uncertainty bounds.

Current registry validity, administrative key validity and
revocation freshness must depend on independently verified
time and current security policy.

Missing or uncertain trusted time must block
operational registry acceptance.

## 17. Bootstrap and Recovery

The initial protected state requires independently
approved bootstrap authorization.

Missing state must not automatically initialize revision one.

Recovery must not silently lower the revision floor.

A recovery procedure must reconcile:

- Last independently confirmed state generation.
- Last accepted signing digest.
- Highest committed registry revision.
- Protected revocation history.
- Administrative trust-policy version.
- Rollback-witness checkpoint.
- Recovery and approval evidence.

Conflicting evidence must result in restricted operation.

This gate does not implement bootstrap or recovery tools.

## 18. Authorization and Identity

The future authority must distinguish identities permitted
to perform:

- Protected read.
- Candidate submission.
- Conditional commit.
- Administrative trust-policy update.
- Recovery.
- Audit review.
- Rollback-witness administration.

Application credentials must not automatically grant
security-authority administrative privileges.

Privileged access requires separately reviewed authorization,
credential lifecycle and audit controls.

No credentials are created by this decision.

## 19. Failure Conditions

The future implementation must fail closed on:

- Unauthenticated authority response.
- Missing administrative trust policy.
- Revoked administrative signing key.
- Corrupted protected state.
- State generation mismatch.
- Registry revision rollback.
- Invalid previous signing digest.
- Missing revocation tombstone.
- Reintroduced revoked key.
- Conditional update conflict.
- Witness/state disagreement.
- Witness unavailability.
- Security authority unavailability.
- Uncertain commit outcome.
- Unauthorized bootstrap.
- Unapproved recovery.
- Trusted-time failure.

Failure cannot grant Docker or production authorization.

## 20. Operational Feasibility Gate

Before operational implementation, a security and
infrastructure review must establish:

- Which independent service would host transactional state.
- Who administers that service.
- Which authority owns the rollback witness.
- Whether common-mode rollback is possible.
- Whether authenticated linearizable updates are supported.
- How witness/state coordination will be recovered.
- How credentials and administrative keys are provisioned.
- How backups and emergency restoration work.
- Whether multi-host consistency is required.
- Whether service availability meets project needs.
- What logs and monitoring will be protected.
- Expected operating and recovery costs.

If these conditions cannot be demonstrated, this preferred
candidate must remain unapproved.

The project may reconsider the alternatives.

## 21. Required Proof-of-Concept Tests

Any future implementation must demonstrate:

1. Authenticated protected-state read.
2. Unauthenticated read rejection.
3. Conditional revision advancement.
4. Conflicting simultaneous update rejection.
5. Atomic registry/revocation change.
6. Revocation-history rollback detection.
7. Database snapshot rollback detection.
8. Stale witness detection.
9. Witness outage fail-closed behavior.
10. State-service outage fail-closed behavior.
11. Crash before transactional commit.
12. Crash after transactional commit.
13. Crash before witness advancement.
14. Crash after witness advancement.
15. Indeterminate commit reconciliation.
16. Multi-host competing update handling.
17. Administrative policy rollback detection.
18. Revoked administrator rejection.
19. Unauthorized bootstrap rejection.
20. Unauthorized recovery rejection.
21. Historical key-material reuse rejection.
22. Stale replica rejection.
23. Trusted-time failure rejection.
24. Invalid signature rejection.
25. False isolation evidence rejection.
26. Execution attempt after failed security assessment.

Tests must verify the selected technology, not merely
an in-memory imitation of its interface.

## 22. Next Gate - 3D.12C

The next gate may define typed protected-state interfaces
and adversarial contract tests.

The initial implementation should be pure and testable.

A fake in-memory provider may model:

- Authenticated-read result shapes.
- Expected revision and generation checks.
- Conditional state transitions.
- Revocation-history bindings.
- Commit results and error states.
- Witness reconciliation decisions.

Such a provider must not be called independently trusted.

The contract must avoid granting operational authority
to caller-constructed objects.

Operational storage adapters remain deferred until the
security authority is selected and independently reviewed.

## 23. Final Decision

Preferred architecture:

Independent transactional security-state authority with
a separately protected rollback witness and independent
administrative trust-policy authority.

Selection is conditional on operational threat-model
validation, feasibility review and approved implementation.

No specific product, cloud provider, database, hardware
device or operational service is approved.

No trusted state is created or advanced by this decision.

The existing Gate 3D.11F assessment remains non-authorizing.

Independent runtime isolation remains unverified.

Laboratory Docker execution, automatic retries and
production deployment remain blocked.
