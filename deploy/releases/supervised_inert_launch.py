#!/usr/bin/env python3
"""Gate 4D.22C.3A: supervised inert laboratory launch.

Coordinates lease, durable evidence, process barrier and exit
observation. Does not invoke Docker or authorize deployment.

The caller must supply an active LockedEvidenceStore and a bound
STARTED rollback attempt. Successful child exit never permits retry.
"""

from dataclasses import dataclass

from docker_execution_evidence import EXIT_OBSERVED
from locked_durable_barrier import (
    LockedEvidenceStore,
    prepare_locked_barrier,
)
from rollback_attempt_store import validate_attempt_record


@dataclass(frozen=True)
class InertLaunchResult:
    release_id: str
    execution_id: str
    operation_fingerprint: str
    pid: int
    start_ticks: int
    exit_code: int
    evidence_phase: str
    docker_operation_settled: bool = False
    automatic_retry_permitted: bool = False
    manual_reconciliation_required: bool = True
    production_execution_enabled: bool = False


def execute_supervised_inert(store, attempt, marker):
    """Run the fixed inert child once under an existing deployment lease.

    The evidence remains unresolved even after exit. This function
    never retries, cleans up Docker state or finalizes a journal.
    """
    if not isinstance(store, LockedEvidenceStore):
        raise RuntimeError("LockedEvidenceStore required")

    store.require_lease()
    validate_attempt_record(attempt)

    if (
        attempt.get("schema_version") != 2
        or attempt["status"] != "STARTED"
    ):
        raise ValueError("Bound STARTED attempt required")

    binding = prepare_locked_barrier(store, attempt, marker)

    try:
        store.require_lease()
        binding.verify()

        record = store.read(attempt["release_id"])

        if (
            record["execution_id"] != attempt["execution_id"]
            or record["attempt_id"] != attempt["attempt_id"]
            or record["operation_fingerprint"]
            != attempt["operation_fingerprint"]
        ):
            raise ValueError("Durable attempt binding mismatch")

        identity = binding.child.identity

        # Exactly one explicit release of the inert test child.
        binding.release()

        # A timeout or controller crash leaves OBSERVED unresolved.
        code = binding.wait(timeout=10)

        store.require_lease()

        observed = store.read(attempt["release_id"])

        if (
            observed["execution_id"] != attempt["execution_id"]
            or observed["pid"] != identity.pid
            or observed["start_ticks"] != identity.start_ticks
            or observed["phase"] != "OBSERVED"
        ):
            raise ValueError("Execution identity changed after child exit")

        exited = store.record_exit(attempt["release_id"], code)

        if exited["phase"] != EXIT_OBSERVED:
            raise ValueError("Durable exit observation missing")

        assessment = store.assess(attempt["release_id"])

        if (
            assessment.docker_operation_settled
            or assessment.automatic_retry_permitted
            or not assessment.manual_reconciliation_required
        ):
            raise RuntimeError("Unsafe execution settlement policy")

        return InertLaunchResult(
            release_id=attempt["release_id"],
            execution_id=attempt["execution_id"],
            operation_fingerprint=attempt["operation_fingerprint"],
            pid=identity.pid,
            start_ticks=identity.start_ticks,
            exit_code=code,
            evidence_phase=exited["phase"],
        )

    finally:
        # Before release this causes EOF; after release it does
        # not terminate the child or prove execution has settled.
        binding.close_without_release()
