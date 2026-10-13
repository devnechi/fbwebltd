# Gate 4D.22C.3D.11F - Offline Registry Assessment Composition

Status: PROPOSED FOR REVIEW - NON-AUTHORIZING IMPLEMENTATION
Date: 2026-10-13

Docker execution: DENIED
Automatic retry: DENIED
Production deployment: DISABLED
Trusted registry state: NOT IMPLEMENTED
Independent trust-anchor provenance: NOT ESTABLISHED
Trusted clock: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Objective

Compose the existing laboratory registry signature, revision
continuity and collector-key revocation continuity assessments.

One rejected prerequisite must prevent a positive combined result.

This is an offline, side-effect-free security assessment.
It does not authorize accepting, storing or executing a registry.

## 2. Inputs

The composition requires:

- Previous canonical registry bytes.
- Candidate canonical registry bytes.
- A separately supplied administrator key policy.
- A separately supplied revision-state snapshot.
- A separately supplied revocation-history snapshot.
- A separately supplied timezone-aware assessment time.

These inputs are not independently authenticated by composition.

The candidate must be a consecutive new revision.

Genesis bootstrap, historical recovery and equal-revision
recognition are outside this composition contract.

## 3. Execution Contract

The composition must:

1. Verify the candidate administrative signature using Gate 3D.11B.
2. Compare the candidate revision and signing digest through 3D.11D.
3. Validate the previous/candidate lifecycle transition using 3D.11E.
4. Cross-check revision identity and signing digest across results.
5. Return an immutable non-authorizing assessment.

Failure of any prerequisite must raise ValueError.

No partial positive assessment may be returned on failure.

All modules must evaluate the same candidate original bytes.

## 4. Previous Registry Boundary

Gate 3D.11E compares previous registry content with a
caller-supplied revision snapshot.

This composition verifies the candidate signature only.

Matching the previous registry to a caller-supplied digest
does not authenticate that previous registry.

Historical signature and administrative-key rotation policy
require separate designs. Do not claim previous-registry
authentication or protected-state provenance.

## 5. Positive Result Semantics

A successful result can establish:

- Candidate signature validity under the supplied admin key.
- Logical candidate revision continuity against supplied state.
- Logical collector-key lifecycle continuity against supplied history.
- Agreement of the calculated candidate digests and revisions.
- A proposed next revocation-history declaration.

A successful result does not establish:

- Independently authorized administrator identity.
- Authenticated previous-registry content.
- Independently protected revision-state provenance.
- Authoritative currentness or revocation freshness.
- Trusted time.
- Durable rollback protection.
- Atomic state commitment.
- Evidence replay prevention.
- Collector authentication.
- VM or Docker runtime isolation.
- Docker execution permission.
- Production deployment authorization.

All execution and trust-authority flags must remain false.

## 6. Failure Contract

The composite assessment must fail closed when:

- Registry bytes are malformed or noncanonical.
- The candidate administrator signature is invalid.
- The administrator key is disabled, revoked or unknown.
- The candidate registry is expired or future-dated
  under the supplied assessment time.
- A revision rolls backward or skips a predecessor.
- Signing digests disagree.
- Revocation history conflicts with the prior declaration.
- Collector keys are improperly reactivated, substituted
  or reused.
- The previous registry does not match supplied state.
- Snapshots are missing, malformed or inconsistent.

A valid candidate signature cannot override a failed
revision or revocation check.

Likewise, passing the logical continuity checks cannot
override an invalid candidate signature.

## 7. Deferred Trust Controls

Future gates must separately specify and review:

- Independent administrative trust-anchor provisioning.
- Trusted revision and revocation-state authority.
- Atomic compare-and-swap with durable commit semantics.
- Protected revocation publication and reconciliation.
- Trusted clock and evidence replay protection.
- Administrative rotation and emergency recovery.
- Independent laboratory runtime isolation.
- Explicit execution authorization.

No operational persistence or privileged connector is
introduced in Gate 3D.11F.

## 8. Acceptance Criteria

- Three existing modules are reused without relaxing them.
- Candidate signature verification is mandatory.
- Candidate revision and digest results agree.
- Revocation transition failures block the assessment.
- Malformed inputs fail closed.
- Successful assessments remain immutable and non-authorizing.
- All baseline and new tests pass.
- Docker and production execution remain blocked.

Acceptance of this gate is not an operational security
approval and does not permit deployment.
