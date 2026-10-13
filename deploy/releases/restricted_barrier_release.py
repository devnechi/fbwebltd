#!/usr/bin/env python3
"""Gate 4D.22C.3B.2: policy-checked inert barrier release.

This coordinator combines durable barrier verification with the
restricted Docker command policy. Its child remains the fixed
inert marker writer.

No Docker commands are executed. No production deployment,
automatic retry, or release-journal finalization is authorized.
"""

from dataclasses import dataclass

from docker_execution_evidence import OBSERVED
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from locked_durable_barrier import (
    LockedEvidenceStore,
    prepare_locked_barrier,
)
from restricted_docker_launch_policy import validate_launch_binding
from rollback_attempt_store import validate_attempt_record


@dataclass(frozen=True)
class RestrictedReleaseResult:
    release_id: str
    execution_id: str
    pid: int
    start_ticks: int
    exit_code: int
    evidence_phase: str
    docker_executed: bool = False
    docker_operation_settled: bool = False
    automatic_retry_permitted: bool = False
    manual_reconciliation_required: bool = True
    production_execution_enabled: bool = False


def execute_restricted_inert(
    store,
    attempt,
    marker,
    *,
    command=None,
    process_observer=None,
):
    """Execute exactly one inert child after command-policy checks.

    process_observer is injectable only for non-production testing.
    The executable child action is not customizable.
    """
    if not isinstance(store, LockedEvidenceStore):
        raise RuntimeError("Locked evidence store required")

    store.require_lease()
    validate_attempt_record(attempt)

    if attempt.get("schema_version") != 2:
        raise ValueError("Versioned attempt required")

    if attempt["status"] != "STARTED":
        raise ValueError("STARTED attempt required")

    expected = plan_lab_rollback(PREVIOUS)
    selected = expected if command is None else command
    selected.validate()

    if selected != expected:
        raise ValueError("Unexpected laboratory command")

    binding = prepare_locked_barrier(store, attempt, marker)

    try:
        store.require_lease()
        binding.verify()

        identity = binding.child.identity

        kwargs = {}

        if process_observer is not None:
            kwargs["process_observer"] = process_observer

        assessment = validate_launch_binding(
            store,
            attempt,
            selected,
            identity,
            **kwargs,
        )

        if (
            not assessment.eligible_for_barrier_release
            or assessment.docker_operation_settled
            or assessment.automatic_retry_permitted
            or assessment.production_execution_enabled
        ):
            raise RuntimeError(
                "Restricted launch policy did not permit inert release"
            )

        # Revalidate real child and lease immediately before release.
        # The injectable observer is not trusted for this final check.
        store.require_lease()
        binding.verify()
        binding.release()

        code = binding.wait(timeout=10)

        store.require_lease()

        persisted = store.read(attempt["release_id"])

        if (
            persisted["phase"] != OBSERVED
            or persisted["execution_id"] != attempt["execution_id"]
            or persisted["operation_fingerprint"]
            != attempt["operation_fingerprint"]
            or persisted["pid"] != identity.pid
            or persisted["start_ticks"] != identity.start_ticks
        ):
            raise ValueError("Durable child identity changed")

        exited = store.record_exit(attempt["release_id"], code)
        result = store.assess(attempt["release_id"])

        if (
            result.docker_operation_settled
            or result.automatic_retry_permitted
            or not result.manual_reconciliation_required
        ):
            raise RuntimeError("Unsafe evidence settlement state")

        return RestrictedReleaseResult(
            release_id=attempt["release_id"],
            execution_id=attempt["execution_id"],
            pid=identity.pid,
            start_ticks=identity.start_ticks,
            exit_code=code,
            evidence_phase=exited["phase"],
        )

    finally:
        # Closing the barrier prevents an unreleased inert child
        # from executing. Reap it to avoid subprocess warnings.
        binding.close_without_release()
        binding.wait(timeout=10)
