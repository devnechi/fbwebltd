# Gate 4D.22C.3D.3 — Independent Laboratory Runtime Evidence

Status: DESIGN PROPOSED — IMPLEMENTATION NOT AUTHORIZED
Date: 2026-10-13

Production deployment: DISABLED
Laboratory Docker execution: DENIED
Automatic retry: DENIED

## 1. Objective

Define a trustworthy evidence architecture for determining
whether the proposed Future Basics Docker laboratory is
independent of the development host and production resources.

This gate establishes evidence requirements and acceptance
criteria only.

It does not implement a runtime collector, connect to Docker,
provision a VM or authorize execution.

## 2. Existing Controls

The following components provide supporting observations:

- lab_runtime_preflight.py
- lab_vm_isolation_policy.py
- lab_daemon_isolation_policy.py
- lab_daemon_identity.py
- lab_endpoint_continuity.py
- docker_process_supervision.py
- docker_snapshot_reader.py

Existing observations must not be treated as independent
verification of laboratory isolation.

docker_snapshot_reader.py invokes Docker inspection commands.
It is outside the permitted evidence-collection boundary
for this gate.

## 3. Evidence Trust Boundaries

Three boundaries must be assessed independently.

### E1 — Virtual Machine Identity

Evidence must establish:

- Unique VM identity.
- VM lifecycle state.
- VM configuration identity.
- Guest-to-host separation.
- Snapshot or restoration identity.
- Absence of production resource passthrough.

VM identity claims must be checked against independently
obtained configuration or hypervisor evidence.

Guest-provided declarations alone are insufficient.

### E2 — Docker Daemon Identity

Evidence must establish:

- Actual daemon process identity.
- PID and kernel process start time.
- Process ownership and privileges.
- Effective daemon configuration.
- Effective Docker data root.
- Private socket binding.
- Independent daemon lifecycle.

A socket pathname, inode or process name alone is
insufficient to establish daemon identity.

### E3 — Runtime Isolation

Evidence must address:

- Host Docker socket exclusion.
- Production credentials exclusion.
- Production filesystem and volume exclusion.
- Runtime and storage separation.
- Network isolation.
- Privilege and namespace boundaries.
- No conflicting shared daemon resources.

Network isolation must be verified through approved
configuration and independent observation.

Documentation-only network addresses do not prove
a functioning isolated network.

## 4. Evidence Provenance

Every accepted evidence record must identify:

- Evidence type and schema version.
- Subject VM or runtime identity.
- Collection source and method.
- Collector identity.
- Collection timestamp.
- Collection scope.
- Trust boundary being evaluated.
- Integrity and provenance information.
- Relevant verification limitations.

Evidence must be bound to the same runtime subject.

Evidence from different VMs, daemons or collection
sessions must not be combined without validating
identity continuity.

A timestamp alone does not prove freshness or integrity.

## 5. Consistency Requirements

The future verifier must reject evidence when:

- Required records are missing.
- Evidence is malformed or unreadable.
- VM identities disagree.
- Daemon process identities disagree.
- Socket binding is ambiguous.
- Runtime configuration differs from the approved baseline.
- Evidence is stale or its freshness cannot be established.
- Collection is incomplete.
- Evidence provenance cannot be verified.
- Production resource isolation cannot be established.

Unreadable /proc entries must not be interpreted as proof
that no other socket holders exist.

A process disappearing must not establish Docker quiescence.

## 6. Collection Boundary

The initial evidence collection design must not:

- Invoke Docker or Docker Compose.
- Connect to any Docker socket.
- Execute subprocesses.
- Start or stop processes.
- Modify system configuration.
- Change network configuration.
- Access production credentials.
- Modify Docker containers, images or volumes.
- Trigger recovery or rollback operations.

Any future host or hypervisor integration requires
a separate review of the collector's privileges,
interfaces and trust assumptions.

This design does not authorize that integration.

## 7. Evidence Assessment

The future design must distinguish:

1. Evidence unavailable.
2. Evidence incomplete.
3. Evidence contradictory.
4. Evidence consistent but independently unverified.
5. Evidence independently verified.

Only an independently supported assessment may establish
that the particular isolation controls were verified.

An isolation assessment must never grant Docker execution
or production deployment authorization.

## 8. Fail-Closed Requirements

Until a separately reviewed mechanism establishes
independent runtime evidence:

- runtime_evidence_verified = false
- daemon_identity_proven = false
- daemon_isolation_proven = false
- docker_execution_permitted = false
- production_execution_enabled = false
- automatic_retry_permitted = false
- manual_verification_required = true

These are required security outcomes across relevant
assessment types, not a shared object schema.

Missing or ambiguous evidence requires manual investigation.

## 9. Future Verification Tests

A subsequent implementation gate must test:

- Missing VM identity.
- Mismatched VM identities.
- Daemon PID reuse.
- Daemon restart during inspection.
- Socket substitution.
- Multiple socket holders.
- Unreadable procfs records.
- Incorrect daemon data root.
- Host Docker socket exposure.
- Production mount exposure.
- Network isolation uncertainty.
- Stale evidence.
- Conflicting collection sessions.
- Forged or incomplete provenance.
- Collector failure during inspection.

All such conditions must fail closed.

## 10. Acceptance Criteria

This architecture decision may be accepted when:

1. Existing evidence mechanisms are correctly classified.
2. VM, daemon and isolation trust boundaries are defined.
3. Docker inspection is excluded from initial collection.
4. Evidence provenance and continuity are specified.
5. Missing or contradictory evidence fails closed.
6. Execution authorization remains a separate decision.
7. Production deployment remains disabled.
8. Review and repository validation are completed.

Passing these criteria approves this design only.

## 11. Deferred Work

The following require separate gates:

- Evidence schema implementation.
- Independent evidence collector design.
- Collector implementation and adversarial testing.
- Hypervisor integration.
- Runtime attestation or independent verification.
- Any Docker daemon interaction.
- Any laboratory execution authorization.
- Any production deployment authorization.

## 12. Decision

Independent laboratory verification requires correlated,
trustworthy evidence of the VM, daemon and isolation state.

Existing filesystem, procfs and Docker inspection mechanisms
do not collectively provide that proof.

The next stage may define an evidence schema and pure
verification interface without accessing Docker.

Laboratory execution and production deployment remain blocked.
