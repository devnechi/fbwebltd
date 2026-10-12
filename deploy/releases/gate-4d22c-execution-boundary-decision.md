# Gate 4D.22C — Single Execution Boundary

Status: DESIGN ACCEPTED; ENFORCEMENT NOT IMPLEMENTED
Date: 2026-10-12
Production deployment: DISABLED
Production authorization: BLOCKED

## Context

Gate 4D.22B established:

- Linux PID and kernel-start-time identification.
- Durable PREPARED and OBSERVED execution evidence.
- An inert subprocess start barrier.
- Lease enforcement through LockedEvidenceStore.
- SIGKILL testing before and after barrier release.
- Prevention of duplicate preparation after controller death.

These are laboratory observations, not deployment authorization.

## Findings

### F1 — Base evidence store bypass

DockerExecutionEvidenceStore exposes prepare, observe and
record_exit without enforcing the deployment lease.

LockedEvidenceStore applies lease checks, but its inherited
base methods remain callable separately.

### F2 — Legacy Docker launcher

lab_rollback_executor._run_restoration currently invokes
subprocess.run directly.

It does not use durable process supervision or the blocked
child launch protocol.

### F3 — Unrecorded release transition

OBSERVED means a subprocess PID and start ticks were durably
recorded.

It does not establish whether the release byte was sent,
received or acted upon.

A controller crash around barrier release remains ambiguous.

### F4 — Cooperative lock limitation

DeploymentLease is process-local and thread-bound.

A controller's SIGKILL releases its flock. The Docker operation
or another child process can continue after that release.

Reacquiring the lock does not establish quiescence.

## Decision

Do not integrate the current launcher with Docker until
all execution-entry boundaries have been hardened.

The eventual restricted execution path must:

1. Validate the exact laboratory project and pinned image pair.
2. Hold a valid deployment lease.
3. Verify the bound STARTED rollback attempt.
4. Durably persist PREPARED before child launch.
5. Spawn the exact allowed child behind a start barrier.
6. Durably persist PID and kernel start ticks.
7. Revalidate the attempt, process, command and lease.
8. Send the release signal only after those checks pass.
9. Preserve unresolved evidence through controller termination.
10. Reject duplicate restoration while reconciliation is pending.
11. Reconcile against real Docker state and database identity.
12. Never treat child exit alone as proof of Docker completion.

## Required boundary remediation

- Enforce lease validation in the evidence mutation boundary,
  not merely in a subclass.
- Prevent direct use of an uninstrumented Docker launcher.
- Retain fail-closed behavior for ambiguous release state.
- Preserve existing durable attempt identity and journal semantics.
- Keep production deployment disabled.
- Add adversarial tests before any real Docker integration.

## Acceptance policy

This design decision is not proof that the remediation exists.

Gate 4D.22C remains BLOCKED until the implementation and
integration tests pass.

No production authorization or deployment is granted.
