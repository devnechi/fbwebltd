# Gate 4D.22C.3D.2 — Laboratory Runtime Isolation Decision

Status: DESIGN PROPOSED — RUNTIME EVIDENCE NOT VERIFIED
Date: 2026-10-13
Production deployment: DISABLED
Docker execution authorization: DENIED
Automatic retry: DENIED

## 1. Purpose

Define the required isolation architecture for the Future Basics
Docker laboratory before any additional execution capability is
considered.

This decision consolidates the existing VM, daemon, socket and
execution-boundary policies.

It does not provision infrastructure, verify a running daemon,
authorize Docker commands or permit production deployment.

## 2. Existing Architecture

The following controls are already implemented:

- lab_vm_isolation_policy.py
- lab_daemon_isolation_policy.py
- lab_daemon_identity.py
- lab_endpoint_continuity.py
- lab_runtime_preflight.py
- sealed_lab_launch_contract.py

The execution-boundary decision is documented in:

- gate-4d22c-execution-boundary-decision.md

These components provide declaration validation, limited
filesystem observations, environment evidence and fail-closed
execution restrictions.

They do not collectively establish independent runtime isolation.

## 3. Environment Findings

Gate 4D.22C.3D.1 observed:

- Linux environment with UID 1000.
- Docker CLI and dockerd executables present.
- System Docker socket present.
- System Docker socket owned by root.
- Dedicated laboratory socket not detected.
- Rootless Docker tools not detected.
- User namespaces enabled.
- Subordinate UID and GID mappings present.

These findings describe the inspected development environment.

They do not prove Docker daemon isolation, operator authorization,
VM isolation or the absence of production resources.

No Docker connection or execution is authorized by these findings.

## 4. Architecture Decision

### D1 — Dedicated Laboratory VM

Docker execution experiments must take place in a dedicated,
disposable laboratory VM.

The development host's default Docker daemon must not be
accepted as the laboratory execution target.

The VM must be independently identifiable and have an
independently managed lifecycle.

### D2 — Dedicated Docker Daemon

The laboratory must use its own Docker daemon with:

- A distinct runtime identity.
- An independent lifecycle.
- A dedicated Docker data root.
- A dedicated Unix socket.
- Explicitly constrained privileges.
- No dependence on the host Docker daemon.

The required declared daemon name is:

fbweb-dedicated-lab

A daemon name alone is not runtime identity evidence.

### D3 — Approved Socket and Storage Locations

The VM baseline specifies:

Docker data root:
  /var/lib/fbweb-lab-docker

Docker socket:
  /run/fbweb-lab/docker-lab.sock

These paths are policy declarations.

The actual runtime must be independently checked before
any future authorization decision.

The socket must not be replaced by:

- /var/run/docker.sock
- /run/docker.sock
- An inherited host Docker socket.
- A symlink to an untrusted endpoint.

### D4 — Filesystem Isolation

The laboratory must not receive:

- Host Docker socket mounts.
- Production application volumes.
- Production database volumes.
- Production credential stores.
- Unreviewed host filesystem passthrough.
- Shared container runtime state.

Any permitted laboratory storage must be independently
identified and separated from production resources.

### D5 — Network Isolation

The initial laboratory configuration must use an isolated
internal-only network.

Production networks must not be reachable.

The 192.0.2.0/24 range in the VM declaration policy is a
documentation-only TEST-NET-1 placeholder.

It must not be interpreted as evidence that a real,
functioning or isolated guest network has been configured.

A future implementation must document its actual network
arrangement and independently verify its isolation.

### D6 — Independent Runtime Evidence

Before considering laboratory execution, the evidence
process must establish:

1. The laboratory VM identity and lifecycle.
2. The daemon process identity.
3. The actual Docker socket-to-daemon binding.
4. Socket ownership and permissions.
5. The daemon's effective data-root configuration.
6. The absence of host Docker socket sharing.
7. The absence of production mounts and credentials.
8. Effective network isolation.
9. Relevant privilege and namespace restrictions.
10. The absence of conflicting or ambiguous runtime evidence.

Declarations, filesystem metadata, executable discovery
and environment-variable presence are insufficient alone.

Evidence must be gathered independently from the proposed
configuration and bound to the runtime being evaluated.

### D7 — Execution Authorization Boundary

A valid declaration is not execution authorization.

A successful read-only preflight is not execution authorization.

A stable socket inode is not proof of daemon identity.

Passing automated unit tests is not execution authorization.

Laboratory execution remains denied until a separate,
reviewed authorization mechanism establishes all required
conditions for a specific bounded operation.

Existing execution-boundary and recovery protections must
not be bypassed.

### D8 — Fail-Closed Handling

Missing, contradictory, stale or unverifiable evidence
must produce a blocked assessment.

No automatic retries are permitted.

A blocked assessment requires manual investigation.

A controller crash or lock release must not be interpreted
as proof that a Docker operation has stopped.

Existing durable recovery and execution evidence must
remain authoritative.

## 5. Mandatory Security Outcomes

Until independent verification and a separate execution
authorization are implemented:

- runtime_evidence_verified = false
- isolation_proven = false
- daemon_identity_proven = false
- docker_execution_permitted = false
- production_execution_enabled = false
- automatic_retry_permitted = false
- manual_verification_required = true

These represent required safety outcomes across relevant
assessment types, not a new shared object schema.

## 6. Scope Exclusions

This gate does not:

- Create or start a VM.
- Install or start a Docker daemon.
- Connect to a Docker socket.
- Invoke Docker or Docker Compose.
- Create containers or volumes.
- Modify firewall or networking configuration.
- Provision secrets or credentials.
- Execute rollback commands.
- Authorize production deployment.
- Enable automatic recovery or retry.

## 7. Acceptance Criteria

Gate 4D.22C.3D.2 can be accepted as an architecture decision
when:

1. Its requirements are consistent with existing policies.
2. The trust boundaries are explicitly defined.
3. The development-host Docker socket remains untrusted.
4. Unverified declarations cannot authorize execution.
5. The independent evidence requirements are documented.
6. The production deployment restriction is preserved.
7. The decision is reviewed and integrated through CI.

Passing these criteria accepts the architecture only.

It does not prove that the laboratory VM or daemon exists
or satisfies the architecture.

## 8. Deferred Work

A subsequent gate may design a read-only independent
runtime-evidence mechanism.

That mechanism must be reviewed separately before adding
any connection to a Docker daemon or other execution
capability.

Any laboratory VM provisioning, Docker launch capability
or production release authorization requires its own
explicit architecture and security review.

## 9. Final Decision

A dedicated disposable VM with a separately identifiable
Docker daemon is the required laboratory architecture.

The existing system Docker daemon is not an approved
substitute.

Current laboratory runtime isolation remains unverified.

Docker execution, automatic retry and production deployment
remain blocked.

Gate 4D.22C.3D.2 is a documentation and architecture
decision only.
