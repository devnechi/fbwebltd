# Gate 4D.22C.3D.12A - Independent Trust and Protected State

Status: DESIGN PROPOSED - IMPLEMENTATION NOT AUTHORIZED
Date: 2026-10-13

Production deployment: DISABLED
Laboratory Docker execution: DENIED
Automatic retry: DENIED
Registry state persistence: NOT IMPLEMENTED
Administrative trust provisioning: NOT AUTHORIZED
Trusted time infrastructure: NOT IMPLEMENTED
Independent runtime isolation: NOT VERIFIED

## 1. Objective

Define the architecture for independently authenticating
administrative trust anchors, registry revision state and
collector-key revocation history.

This gate follows successful offline verification composition
under Gate 4D.22C.3D.11F.

The objective is to establish the requirements for moving
from caller-supplied security declarations toward protected,
authoritative security information.

This is a documentation-only architecture gate.

## 2. Existing Capabilities

The repository currently provides:

- Strict canonical registry wire-format validation.
- Administrative Ed25519 signature verification.
- Collector-key policy validation.
- Logical registry revision continuity.
- Logical collector-key revocation continuity.
- Revocation-history proposals.
- Combined fail-closed offline registry assessments.
- Non-authorizing security assessment results.

The current laboratory assessment does not establish:

- Independent administrative-key provenance.
- Authoritative current registry revision.
- Protected revocation-history storage.
- Durable atomic registry acceptance.
- Trusted time.
- Evidence replay resistance.
- Independent runtime isolation.
- Docker or production execution authorization.

These limitations remain binding.

## 3. Security Objective

A future operational registry verifier must obtain
security-critical information from independently controlled
authorities.

It must not trust information solely because:

- It is supplied by an API caller.
- It appears in a signed registry.
- Its digital signature is mathematically valid.
- It matches an unprotected local configuration file.
- It is present in an ordinary application database.
- It is included in a deployment artifact.
- It was previously accepted by an untrusted process.

The system must distinguish cryptographic correctness
from independently established authority and currentness.

## 4. Threat Model

The architecture must address an attacker capable of:

- Substituting administrative public keys.
- Supplying an attacker-controlled key policy.
- Replaying an older signed registry.
- Replacing stored revision information.
- Restoring historical application backups.
- Reintroducing previously revoked collector keys.
- Replaying old revocation-history snapshots.
- Triggering concurrent registry updates.
- Interrupting a state update before durable completion.
- Presenting stale state from another verifier host.
- Manipulating application-controlled files.
- Manipulating an unprotected database.
- Influencing untrusted system time.
- Attempting unauthorized bootstrap or recovery.

A compromised protected-state authority, compromised
administrator or compromised host requires a separate
operational threat assessment.

No storage mechanism is considered secure merely by name.

## 5. Trust Domains

The future architecture must keep the following domains
separate.

### T1 - Administrative Trust Authority

Owns the approved registry administrative signing policy.

Controls administrative-key enrollment, rotation,
revocation and emergency deactivation.

It must be independent of the registry under assessment.

### T2 - Registry Issuing Authority

Produces authorized canonical signed registry revisions.

A registry issuer cannot unilaterally modify the
verifier's administrative trust anchors.

### T3 - Protected Revision-State Authority

Maintains the authoritative highest accepted registry
revision and its associated signing digest.

It must provide authenticated reads and atomic,
rollback-resistant updates.

### T4 - Protected Revocation-State Authority

Maintains authenticated collector-key lifecycle history.

It must prevent removed or revoked keys from being
silently reintroduced.

Revision and revocation updates must be committed
atomically as one logical transition.

The two types of state may share a protected service,
but must retain their distinct security meanings.

### T5 - Independent Time Authority

Provides trustworthy time information with defined
accuracy, availability and failure handling.

Registry-supplied timestamps do not constitute trusted time.

### T6 - Runtime and Deployment Authority

Controls VM isolation, Docker permissions and
deployment authorization.

Registry validity must never directly grant execution.

## 6. Administrative Trust-Anchor Decision

Administrative public keys must be provisioned through
a separately authorized process.

The provisioning authority must define:

- Approved key custodians.
- Signing purpose and authorized registry scope.
- Initial enrollment authorization.
- Approved public-key distribution.
- Key lifecycle and validity periods.
- Administrative revocation procedures.
- Trust-policy versioning.
- Recovery and compromise procedures.
- Independent review and audit evidence.

The registry must never enroll its own trusted signer.

An administrator key must not also serve as a collector
evidence-signing key.

The existing caller-supplied AdministrativeKeyPolicy is
a policy declaration, not proof of independent authority.

No operational administrative keys are provisioned
by this decision.

## 7. Signing-Key Custody

Operational administrative private-key custody requires
a separately approved security assessment.

The evaluation must consider:

- Separation of signing and verification roles.
- Private-key export restrictions.
- Key generation and custody controls.
- Access control and approval separation.
- Auditability of signing actions.
- Compromise detection and response.
- Backup and disaster recovery.
- Rotation without losing historical integrity.

A hardware-backed signing service or managed key service
may be considered.

Neither is automatically approved.

Private keys, credentials and enrollment secrets must
not be committed to the repository or included in
GitHub Actions configuration as part of this gate.

## 8. Authoritative State Record

A future protected registry state record must include:

- Registry identity.
- Registry format version.
- Highest accepted revision.
- SHA-256 registry signing digest.
- Protected generation or transaction epoch.
- Approved administrative trust-policy reference.
- Authenticated revocation-history reference or contents.
- Committed transition identifier.
- Recovery or migration epoch where applicable.

The record must identify the authority controlling
its provenance.

Untrusted callers must not be able to fabricate an
accepted state merely by constructing a valid dataclass.

## 9. Digest Continuity Contract

The existing Gate 3D.11B registry signing digest is:

SHA256(registry_signing_bytes(document))

The bytes are domain-separated and exclude the
registry signature field.

Gate 3D.11D compares candidate revision metadata
with an explicitly supplied revision snapshot.

Gate 3D.11E compares lifecycle changes with an explicitly
supplied revocation-history snapshot.

Gate 3D.11F combines those checks.

Future integration must preserve the exact digest contract
unless a separately approved version migration occurs.

Protected state must bind the accepted revision and digest.

A higher revision with an incorrect predecessor digest
must not be committed.

## 10. Atomic Acceptance Contract

Operational registry acceptance must be implemented
as a protected conditional state transition.

An ordinary update must satisfy:

candidate.revision = protected.revision + 1

candidate.previous_revision = protected.revision

candidate.previous_digest = protected.signing_digest

The transition must additionally validate current
administrative authorization and revocation history.

The commit must atomically bind:

- New registry revision.
- New registry signing digest.
- New revocation-history state.
- New protected generation.
- Committed transition identity.

A partially completed update must not be treated
as accepted.

The next registry must never be authorized solely
on the basis of a successful offline assessment.

## 11. Concurrency and Consistency

The protected authority must support an authenticated
compare-and-swap or equivalent transactional operation.

Two competing candidates must not both advance the
same protected revision.

Any update conflict must cause rejection or a new
assessment against current protected state.

The architecture must define its consistency model
for multiple verifier processes and hosts.

Stale local snapshots cannot establish currentness.

Disconnected verifiers must fail closed for operational
registry acceptance.

## 12. Storage Selection Requirements

Candidate mechanisms for future evaluation include:

A. Independently administered transactional state service.

B. Hardware-backed monotonic state or counter mechanism.

C. Separately protected security control-plane service.

The implementation decision must compare:

- Security independence from the application host.
- Integrity of authenticated reads.
- Rollback resistance.
- Durable atomic conditional updates.
- Multi-host consistency.
- State availability.
- Recovery and backup controls.
- Operational complexity.
- Failure isolation.
- Auditing and monitoring.
- Cost and infrastructure requirements.

No candidate is selected or deployed in this gate.

An ordinary database transaction is not sufficient
when an attacker can restore the entire database
to an older snapshot.

A simple signed state file is not sufficient when
the file and its signing policy can both be rolled back.

## 13. Protected Revocation History

Collector-key revocation history must be bound to
the authoritative revision-state transition.

Previously revoked public-key material must remain
recognizable after a registry record is removed.

Revocation tombstones must survive:

- Registry replacement.
- State-service restart.
- Collector-key rotation.
- Database restoration.
- Disaster recovery.
- Administrative migration.

Lifecycle reactivation cannot be authorized by a
higher registry revision alone.

Reactivation exceptions require a separate approved
security policy and auditable authorization.

## 14. Administrative Revocation and Rotation

Administrative revocation policy must remain independent
of collector registry content.

The architecture must specify how verifiers learn
that an administrative signing key has been disabled
or compromised.

Historical signatures require an explicit historical
validation policy.

A currently revoked administrator must not sign an
acceptable new registry under ordinary operation.

Administrative trust-policy rollback must be prevented
by an independently protected policy version or epoch.

Operational administrative rotation is not implemented
here.

## 15. Trusted Time and Freshness

A future operational verifier must obtain time from
an independently controlled, verified time source.

It must define:

- Accepted clock accuracy.
- Maximum permitted uncertainty.
- Time-source authentication.
- Source unavailability handling.
- Clock rollback and forward-jump handling.
- Registry issuance and expiry evaluation.
- Administrative key validity evaluation.
- Maximum permitted state staleness.

A caller-supplied timezone-aware datetime is useful for
offline testing but is not proof of trusted time.

An uncertain or unavailable trusted time source must
block operational acceptance.

## 16. Previous Registry Authentication

The current composition verifies the candidate registry
signature but not the previous registry signature.

Previous-registry content is matched to a supplied digest.

Future protected-state integration must establish
that the previous digest originates from an authorized,
previously committed registry transition.

Historical signer authorization and bootstrap integrity
require explicit policies.

Matching a prior digest does not, on its own,
establish its provenance.

## 17. Bootstrap Requirements

Missing protected state must not be interpreted as
permission to initialize revision one.

The future bootstrap process must independently establish:

- Approved administrative trust anchors.
- Registry identity and format.
- Initial authorized registry digest.
- Protected state authority identity.
- Initial revision and revocation history.
- Security recovery authority.
- Bootstrap audit record.

Bootstrap requires explicit authorization.

Automatic bootstrap is prohibited.

## 18. Recovery and Rollback Protection

Recovery must not silently lower the revision floor.

A recovery process must distinguish:

- Corrupted state.
- Unavailable state service.
- Interrupted transaction.
- Incomplete replication.
- Unauthorized rollback attempt.
- Legitimate disaster recovery.

Any uncertain or inconsistent state must fail closed.

Recovery must verify previous committed state and
revocation continuity.

A new recovery epoch may be required.

Emergency recovery requires separately approved
authorization and an auditable procedure.

This gate does not create recovery scripts.

## 19. Read and Commit API Requirements

A future protected-state interface should separate
read and update operations.

An authenticated read must provide a verified state
snapshot with explicit provenance and generation.

A protected conditional commit must validate the
expected revision, digest and generation atomically.

A failed read, authentication check or commit must not
produce an accepted registry result.

Returned errors must distinguish:

- Invalid authentication.
- Revision conflict.
- Stale generation.
- Unavailable authority.
- Integrity failure.
- Indeterminate commit result.

Error details must not disclose secrets.

No operational API endpoints are created by this gate.

## 20. Composition Integration Boundary

The existing Gate 3D.11F assessment remains offline
and non-authorizing.

Future integration must not simply modify its flags
to true after constructing a caller-supplied state object.

Independent authorities must establish:

- Administrative trust policy provenance.
- Protected previous-registry state.
- Protected revocation history.
- Trusted current time.
- Durable atomic transition confirmation.

Only a separately approved operational integration
may establish these claims.

Even after successful protected-state acceptance,
Docker execution and production deployment require
their own security decisions.

## 21. Audit and Observability

The future authority must provide protected audit
evidence for:

- Administrative key enrollment.
- Administrative key rotation and revocation.
- Registry acceptance.
- Rejected revision rollback.
- Same-revision digest conflict.
- Revoked-key reactivation attempts.
- Concurrent update conflicts.
- Trust authority unavailability.
- Protected state corruption.
- Recovery and restoration.

Audit records must be protected against unauthorized
modification and deletion.

Ordinary application logs must not serve as the sole
trusted revision authority.

## 22. Required Security Tests

Future implementation gates must test:

1. Legitimate administrative key enrollment.
2. Unauthorized key enrollment.
3. Administrative key substitution.
4. Revoked administrator signing attempt.
5. Stale administrative policy.
6. Valid signature under unapproved trust anchor.
7. Lower signed registry revision.
8. Conflicting same-revision digest.
9. Missing predecessor revision.
10. Mismatched predecessor digest.
11. Concurrent conflicting state updates.
12. Protected-state rollback attempt.
13. Restored old state-service backup.
14. Interrupted state transaction.
15. Unknown commit outcome.
16. Unavailable state authority.
17. Corrupted state authentication.
18. Stale state replica.
19. Revoked collector-key reactivation.
20. Removed revoked-key reintroduction.
21. Historical key-material reuse.
22. Trust-policy rotation.
23. Missing trusted time.
24. Clock rollback.
25. Expired registry.
26. Unauthorized bootstrap.
27. Unauthorized recovery.
28. Previous-registry provenance failure.
29. False runtime-isolation claim.
30. Attempted Docker execution after failed trust checks.

Every unresolved security outcome must fail closed.

## 23. Implementation Sequence

### Gate 3D.12B - Trust Authority Selection

Evaluate candidate trust-anchor and protected-state
mechanisms against the required threat model.

Document the chosen candidate, deployment assumptions,
limitations and rejection criteria.

No operational deployment is authorized by this decision.

### Gate 3D.12C - Protected State Interface

Define typed interfaces and adversarial contract tests
for authenticated reads and conditional updates.

A fake or in-memory implementation may be used in tests.

Such tests must not claim operational rollback resistance.

### Gate 3D.12D - Administrative Trust Integration

Design independently controlled administrative trust
policy provisioning and lifecycle verification.

Operational key enrollment requires separate approval.

### Gate 3D.12E - Protected State Integration

Integrate an explicitly approved protected-state authority.

Review atomicity, crash behavior, consistency and recovery.

No runtime execution permission follows automatically.

### Later Gates

Address trusted time, replay prevention, independent
laboratory isolation and execution authorization separately.

## 24. Acceptance Criteria

Gate 3D.12A may be accepted when:

1. Trust domains are explicitly separated.
2. Administrative trust-anchor provenance is defined.
3. Protected revision and revocation state are specified.
4. Atomic state transitions are required.
5. Multi-host consistency expectations are defined.
6. Bootstrap and recovery are independently authorized.
7. Trusted time is treated as a separate security dependency.
8. Existing signature and digest contracts are preserved.
9. Candidate trust mechanisms are identified for evaluation.
10. Missing protections are clearly documented.
11. Existing tests remain passing.
12. Docker, retry and production execution remain blocked.

Acceptance authorizes architecture review only.

## 25. Final Decision

Future Basics must not treat internally consistent
security declarations as independently trusted facts.

The next development phase will evaluate independent
administrative trust and protected registry state
mechanisms before integrating operational persistence.

No operational trust authority is selected, provisioned
or enabled by Gate 3D.12A.

The existing offline verifier remains non-authorizing.

Docker execution, automatic retries and production
deployment remain blocked.
