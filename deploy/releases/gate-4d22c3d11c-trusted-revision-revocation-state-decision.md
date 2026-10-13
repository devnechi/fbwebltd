# Gate 4D.22C.3D.11C - Trusted Revision and Revocation State

Status: DESIGN PROPOSED - IMPLEMENTATION NOT AUTHORIZED
Date: 2026-10-13

Production deployment: DISABLED
Laboratory Docker execution: DENIED
Automatic retry: DENIED
Independent runtime isolation: NOT VERIFIED
Operational trust-anchor provisioning: NOT AUTHORIZED
Trusted persistent registry state: NOT IMPLEMENTED

## 1. Objective

Define the security architecture for protecting laboratory
collector registry revisions against rollback, conflicting
updates, unauthorized key reactivation and state corruption.

This decision extends Gates 4D.22C.3D.11A and 3D.11B.

The gate establishes an architecture and acceptance criteria.
It does not introduce operational persistent storage, key
provisioning, Docker access or execution authorization.

## 2. Existing Security Boundary

The current implementation provides:

- Versioned registry wire-format validation.
- Canonical administrative signing bytes.
- Administrative Ed25519 signature verification.
- Administrative key eligibility checks.
- Declared registry validity-window checks.
- Registry content digest calculation.
- Collector key eligibility evaluation.

The current implementation does not establish:

- Independently trusted administrative key provenance.
- The highest authoritative registry revision.
- Registry revision continuity.
- Durable prevention of registry rollback.
- Durable collector revocation history.
- Cross-process atomic acceptance.
- Cross-host consistency.
- Trusted recovery from compromised state.

These distinctions must be preserved.

## 3. Threat Model

The architecture must address an attacker who can:

- Replay an older, correctly signed registry.
- Replace a registry with another signed revision.
- Restore old registry distribution files.
- Present conflicting content for the same revision.
- Interrupt a registry update.
- Trigger competing concurrent update attempts.
- Restore an old verifier state backup.
- Attempt to reactivate a revoked collector key.
- Supply a fabricated registry public-key policy.
- Manipulate unprotected local filesystem data.

A valid Ed25519 signature does not eliminate these threats.

The design must explicitly identify which threats require
an independently protected state authority.

## 4. Security Decisions

### C1 - Trusted State Ownership

An independent verifier-controlled authority must own the
highest accepted registry revision.

The state authority must be separate from:

- Registry distribution.
- Laboratory evidence collectors.
- Untrusted registry documents.
- Docker runtime components.
- Release rollback journals.
- Ordinary unprotected application configuration.

Registry content must never define, lower or reset the
trusted revision floor.

The state authority must provide authenticated reads
and protected updates under an independently reviewed
operational trust model.

This gate does not select or configure that authority.

### C2 - Registry Content Digest

The existing registry verifier computes:

registry_signing_digest =
    SHA256(registry_signing_bytes(document))

The signed bytes include the registry-specific domain prefix
and canonical unsigned registry content.

The signature field is excluded.

Future continuity verification must use this exact digest
contract unless a separately versioned migration is approved.

The previous_digest field in a new registry must match
the signing digest of the immediately preceding accepted
registry.

A digest value inside the submitted registry cannot prove
that the predecessor was previously accepted.

### C3 - Protected State Record

A future protected registry state record must bind:

- Registry identity.
- Registry wire-format version.
- Highest accepted revision.
- Accepted registry signing digest.
- Trusted state generation or epoch.
- Approved administrative trust-policy reference.
- Revocation continuity data or authenticated references.
- State update identifier.
- Last committed transition status.

The authoritative value must not be assembled from
untrusted registry-supplied claims.

Administrative trust-anchor policy requires a separate
independently protected authority.

A state record whose integrity or provenance cannot be
verified must not be accepted.

### C4 - Initial Bootstrap

The initial registry must not become trusted simply because
its revision number is 1.

First-time initialization requires a separately authorized
bootstrap ceremony.

The bootstrap process must establish:

- Registry identity.
- Approved administrative signing authority.
- Initial registry digest.
- Initial revision.
- Trusted state ownership.
- Initial revocation baseline.
- Recovery authority.
- Audit record of bootstrap authorization.

A missing state record must not automatically trigger
bootstrap or reset the revision floor.

The version 1 wire format requires genesis documents to
declare previous_revision = 0 and an all-zero previous_digest.

These values are structural rules, not authorization.

### C5 - Normal Revision Continuity

For ordinary registry updates, the future acceptance gate
must require:

candidate.revision = trusted.revision + 1

candidate.previous_revision = trusted.revision

candidate.previous_digest = trusted.digest

All values must refer to the same registry identity and
compatible approved wire-format version.

The candidate signature and administrative key policy must
be checked before its state transition can be authorized.

A revision gap must fail closed.

Missing intermediate revisions must be supplied and
validated in sequence.

Skipping revisions requires a separately approved recovery
or migration process.

### C6 - Lower Revision Rejection

Any candidate with a revision lower than the protected
accepted revision must be rejected.

This applies even when:

- The signature is valid.
- The signing administrator was previously authorized.
- The registry is inside its declared validity window.
- The old registry contains an active collector key.
- The registry was previously accepted on another host.

An old signed registry is not current authority.

### C7 - Same-Revision Handling

For equal revisions:

- A different signing digest must be rejected.
- An identical signing digest may be recognized as the
  same previously recorded content.
- Recognition must not advance state.
- Recognition must not reset revocation history.
- Recognition must not bypass current administrative
  trust or freshness requirements.

An equal-revision match is not a new state-acceptance event.

A conflicting digest must be treated as potential
equivocation and surfaced for security review.

### C8 - Atomic State Transition

Registry advancement must be performed using an atomic
conditional update against the previously observed
trusted revision, digest and generation.

The operation must ensure that only one candidate can
successfully advance a particular trusted state.

The update must protect the registry state and required
revocation continuity information together.

A verifier must not report an authoritative new revision
before the protected update is durably committed.

Separate uncoordinated writes of revision and digest
are prohibited.

### C9 - Concurrent Update Behavior

When two candidates attempt to advance from the same
trusted revision:

1. Both may independently pass signature verification.
2. Both must compare against current protected state.
3. At most one may commit the expected state transition.
4. The losing candidate must be rejected or reassessed.
5. No stale read may authorize a conflicting write.

Concurrent verification success does not imply
concurrent update authorization.

An implementation must include adversarial race tests.

### C10 - Crash and Durability Semantics

The state authority must define behavior for failures
before, during and after committing a transition.

If the commit outcome is uncertain, the verifier must
reconcile against independently trusted state.

A process restart must not reset the accepted revision.

Power loss or storage failure must not silently restore
a previously accepted lower revision.

An unprotected filesystem journal or ordinary fsync
operation is insufficient to prove rollback resistance.

Until reconciliation succeeds, the verifier must fail
closed.

### C11 - Protected Storage Threat Model

The operational design must evaluate an appropriate
trusted-state mechanism.

Possible candidates include:

- An independently administered transactional service
  with authenticated compare-and-swap operations.
- A hardware-backed monotonic state mechanism.
- A separately protected security control-plane service.

No mechanism is approved merely by its category.

The selected mechanism must address:

- Authentication.
- Authorization.
- State integrity.
- Rollback resistance.
- Durability.
- Availability.
- Multi-process concurrency.
- Backup and restoration.
- Host compromise.
- Auditability.

Ordinary application database transactions alone cannot
prove resistance to rollback by an attacker who can
restore the entire database or its underlying storage.

### C12 - Cross-Host Consistency

Multiple verifiers must not independently establish
different authoritative registry histories.

If multiple hosts participate, they must use a
coordinated state authority with defined consistency
guarantees.

Disconnected hosts must not silently accept registry
updates based on stale local state.

Any offline verification mode must explicitly distinguish
cryptographic signature validity from currentness.

Network partitions, stale replicas and conflicting state
must fail closed for operational registry acceptance.

### C13 - Collector Revocation Continuity

The authoritative lifecycle policy must prevent a
previously revoked collector key from being silently
reactivated by later registry content.

Revocation history must survive:

- Registry replacement.
- Collector record removal.
- Verifier restart.
- Trusted-state recovery.
- Key rotation.
- Backup restoration.

The future design must preserve authenticated revocation
tombstones or equivalent durable lifecycle history.

Tombstones must identify the revoked collector/key
relationship and relevant public-key material.

Removal of a revoked record from a registry must not
erase its revocation history.

### C14 - Reactivation and Rotation

A revoked key must not automatically return to active
status through a later signed registry.

Replacing a compromised key must require:

- A new authorized key identity.
- Distinct approved public-key material.
- Independently authorized lifecycle changes.
- Updated registry publication.
- Continuity with the protected revocation history.

Exceptional reactivation or revocation reversal requires
a separately reviewed emergency policy.

Neither ordinary registry signing nor a higher revision
alone is sufficient to override protected revocation state.

### C15 - Administrative Key Revocation

Administrator key lifecycle policy must remain independent
of collector registry content.

A newly submitted registry must not:

- Reactivate a revoked administrator.
- Replace a trusted administrative public key.
- Remove an authoritative administrative revocation.
- Reset the approved administrator policy version.

Operational registry acceptance requires the current,
independently authorized administrative trust policy.

Compromised signing authority requires independent
recovery authorization.

### C16 - Registry Freshness

Registry freshness requires verifier-controlled trusted time.

A valid signed registry must be rejected for operational
acceptance when its authorized validity window has ended.

Future-dated registry issuance must not authorize early
acceptance.

Administrative key validity and revocation must be
evaluated separately from registry timestamps.

Failure or uncertainty in the trusted clock must
prevent operational acceptance.

This gate does not implement trusted clock infrastructure.

### C17 - Revocation Publication and Staleness

The operational architecture must define how current
revocation decisions reach all participating verifiers.

It must specify:

- Maximum permitted registry staleness.
- Revocation publication procedures.
- Revocation delivery confirmation.
- Handling of disconnected verifiers.
- Emergency administrator deactivation.
- Recovery after missed registry revisions.

A verifier unable to establish current authoritative
revocation state must not claim collector authentication.

A cryptographically valid old signature cannot override
a current revocation decision.

### C18 - Emergency Recovery

Recovery of trusted state must require independently
authorized procedures.

Recovery must not be implemented as an automatic revision
reset or acceptance of a lower signed registry.

A recovery procedure must document:

- The reason recovery is necessary.
- The highest previously committed revision.
- The last trusted registry digest.
- The affected authority and verifier scope.
- Administrator approval.
- Revocation history reconciliation.
- A new state generation or recovery epoch.
- Audit evidence.
- Recovery validation before operational acceptance.

If trustworthy prior state cannot be reconstructed,
verification must remain restricted.

This gate does not authorize emergency recovery tools.

### C19 - Failure and Audit Evidence

The future implementation must generate audit evidence for:

- Accepted revision transitions.
- Rejected lower revisions.
- Equal-revision digest conflicts.
- Missing predecessor revisions.
- Predecessor digest mismatches.
- Revoked key reactivation attempts.
- Storage integrity failures.
- Concurrent update conflicts.
- Administrative trust-policy failures.
- Recovery operations.

Audit logs must not themselves become the sole source
of the trusted revision floor.

Sensitive key material and unnecessary evidence payloads
must not be exposed in diagnostic output.

### C20 - Authorization Separation

Trusted registry state must not directly grant:

- Docker socket access.
- Docker container execution.
- Virtual machine startup.
- Network isolation approval.
- Production deployment.
- Automatic recovery or rollback.
- Release image publishing.
- Runtime permission changes.

Registry authenticity, currentness and revocation validity
are prerequisites for higher-level trust decisions.

They are not substitutes for independent runtime isolation
verification or explicit execution authorization.

## 5. Proposed Acceptance State Machine

The future registry acceptance process must distinguish
the following conceptual states:

UNVERIFIED
  -> SIGNATURE_VALID
  -> TRUST_POLICY_ELIGIBLE
  -> CONTINUITY_VALID
  -> STATE_COMMIT_PENDING
  -> STATE_COMMITTED

Any failure must result in rejection or manual review.

SIGNATURE_VALID means only that cryptographic verification
succeeded under the selected administrative public key.

TRUST_POLICY_ELIGIBLE requires an independently approved
current administrative key policy.

CONTINUITY_VALID requires comparison against authenticated
protected revision and revocation state.

STATE_COMMIT_PENDING must not authorize downstream use.

STATE_COMMITTED requires an independently confirmed durable
atomic state transition.

No state in this sequence proves VM or Docker isolation.

## 6. Existing Implementation Boundaries

lab_registry_wire_format.py validates revision-field shape
and the internally declared previous revision relationship.

It does not compare the previous digest against trusted state.

lab_registry_signature_verifier.py computes the SHA-256
digest of domain-separated unsigned registry signing bytes.

It does not consult or update an independently protected
revision authority.

Existing Docker execution evidence, rollback attempt stores,
recovery journals and release authorization records belong
to different security purposes.

They must not be repurposed as authoritative registry
anti-rollback storage without a separate approved design.

This gate makes no changes to those implementations.

## 7. Future Implementation Stages

### Gate 3D.11D - Pure Revision Continuity Contract

A future implementation may introduce a pure function
that evaluates candidate registry metadata against an
explicitly supplied trusted-state snapshot.

The function must:

- Reject lower revisions.
- Detect conflicting equal revisions.
- Enforce consecutive revision advancement.
- Compare previous_digest with trusted digest.
- Reject malformed state.
- Preserve fail-closed assessment results.

The supplied state must not be described as independently
trusted merely because it matches a schema.

No filesystem or persistent state operations may be added
under this pure evaluation stage.

### Gate 3D.11E - Revocation Continuity Contract

Define and test transitions for:

- Active collector keys.
- Disabled collector keys.
- Revoked collector keys.
- Removed collector records.
- New rotated keys.
- Attempted resurrection of revoked keys.
- Administrative key lifecycle restrictions.

Revocation evaluation must remain separate from the
signature and runtime isolation assessments.

### Future Protected-State Integration

Operational state persistence requires a separately
approved storage threat model and implementation review.

The design must specify independent state provenance,
atomicity, recovery, synchronization and audit controls.

No operational persistent state authority is introduced
by Gate 3D.11C.

## 8. Required Adversarial Acceptance Tests

Future security tests must cover:

1. Lower validly signed revision.
2. Conflicting content at the same revision.
3. Identical same-revision candidate.
4. Missing intermediate revision.
5. Mismatched previous revision.
6. Mismatched previous signing digest.
7. Different registry identity.
8. Unsupported wire-format transition.
9. Malformed protected state.
10. Replaced protected state.
11. Replayed previously committed state.
12. Concurrent competing revisions.
13. Lost update during concurrent acceptance.
14. Crash before commit.
15. Crash after an uncertain commit.
16. Protected-storage read failure.
17. Protected-storage write failure.
18. Restored stale database backup.
19. Stale verifier replica.
20. Disconnected verifier.
21. Revoked key reactivation.
22. Removed and reintroduced revoked key.
23. Reuse of compromised key material.
24. Unauthorized administrative key replacement.
25. Administrator key revocation.
26. Expired registry.
27. Future-dated registry.
28. Trusted clock failure.
29. Corrupted revocation history.
30. Unauthorized bootstrap or recovery.
31. Valid signatures with false isolation claims.
32. State-commit failure followed by an execution attempt.

All uncertain acceptance outcomes must fail closed.

## 9. Acceptance Criteria

Gate 3D.11C may be accepted when:

1. Trusted state ownership is explicitly separated from
   submitted registry content.
2. The registry signing digest contract is preserved.
3. Normal revision continuity is defined.
4. Lower revision and equal-revision conflicts are handled.
5. Atomic update requirements are documented.
6. Crash and concurrency behavior are specified.
7. Durable revocation continuity is defined.
8. Administrator trust-policy independence is maintained.
9. Bootstrap and recovery require separate authorization.
10. Existing runtime and production restrictions remain.
11. Repository tests and architecture review are completed.

Acceptance approves the architecture only.

## 10. Final Decision

Future Basics laboratory registry acceptance requires more
than valid administrative signatures.

It requires independently protected revision history,
verified predecessor digests, revocation continuity and
atomic state advancement.

Gate 3D.11C defines these requirements but does not
implement operational trusted persistence.

Administrative trust-anchor provisioning, durable rollback
protection and authoritative currentness remain unverified.

Laboratory Docker execution, automatic retries and
production deployment remain blocked.
