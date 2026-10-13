# Gate 4D.21 — Independent Release Authorization

Status: DESIGN ACCEPTED FOR LABORATORY IMPLEMENTATION
Production authorization status: NOT IMPLEMENTED
Production deployment status: DISABLED

## Decision

Separate three independent facts:

1. Provenance: the application and web images were built by the
   expected workflow from the expected source commit.

2. Release intent: the exact candidate images, rollback images,
   environment, source commit and maintenance window are recorded
   as one canonical request with a stable SHA-256 fingerprint.

3. Authorization: a trusted external authority confirms that a
   permitted human approver approved that exact request.

None of these facts substitutes for either of the others.

## Release intent fields

- Schema version
- Source repository
- Full source commit SHA
- Source ref
- Target environment
- Candidate application image digest
- Candidate web image digest
- Rollback application image digest
- Rollback web image digest
- Maintenance window start and end
- Change-control reference

All release images must be immutable GHCR digest references.

The canonical release intent is hashed with SHA-256.
The hash is an identifier and integrity binding, not a signature.

## Approval authority

Approval must be independently verified using a trusted provider.
For the intended GitHub Actions implementation, require:

- An independently controlled production environment.
- Required reviewers configured outside the feature branch.
- Evidence identifying the actual reviewer.
- Evidence bound to the exact release intent fingerprint.
- Verification of review timing and authorization validity.
- Explicit rejection of stale, revoked or mismatched decisions.
- Enforcement at the deployment boundary, not only in tests.

A GitHub environment approval alone does not automatically prove
that the reviewer approved a particular immutable image pair.
Additional binding between the reviewed request and the protected
deployment job will be required.

## Mandatory rejection conditions

Reject the release when:

- An image digest differs from the approved release intent.
- The expected rollback destination changes.
- The deployment environment differs.
- The source commit differs.
- The approval is missing.
- The approval has expired or been revoked.
- The approval cannot be attributed to an authorized identity.
- The maintenance window has not begun or has expired.
- The execution context cannot validate approval independently.
- The release intent has been modified after review.

## Trust boundary

Files in the repository, local shell variables, test fixtures,
Python flags and release-intent fingerprints cannot independently
grant production authorization.

The GitHub workflow's production deploy job stays disabled.

The draft pull request remains unmerged.

## Gate closure

21A: Canonical release intent implementation and adversarial tests.

21B: A separately controlled approval authority and independently
verified evidence bound to the exact release intent.

21C: Enforcement at a reviewed execution boundary, with negative
tests demonstrating that unauthorized execution is impossible.

Completion of 21A must not be described as production authorization.
