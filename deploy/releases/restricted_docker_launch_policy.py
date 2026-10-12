#!/usr/bin/env python3
"""Gate 4D.22C.3B.1: non-executing Docker launch policy.

Validates the exact laboratory command, durable execution record,
bound rollback attempt, active deployment lease and Linux process
identity.

Does not execute Docker, authorize deployment or permit retry.
"""

from dataclasses import dataclass

from docker_execution_evidence import (
    OBSERVED,
    command_fingerprint,
    validate_record,
)
from docker_process_supervision import (
    ProcessIdentity,
    ProcessStatus,
    observe_linux_process,
)
from lab_rollback_command import (
    LAB_PROJECT,
    PREVIOUS,
    plan_lab_rollback,
)
from locked_durable_barrier import LockedEvidenceStore
from rollback_attempt_store import validate_attempt_record


@dataclass(frozen=True)
class LaunchAssessment:
    eligible_for_barrier_release: bool
    docker_operation_settled: bool
    automatic_retry_permitted: bool
    production_execution_enabled: bool
    reason: str


def validate_launch_binding(
    store,
    attempt,
    command,
    identity,
    *,
    process_observer=observe_linux_process,
):
    """Validate all recorded facts before a potential barrier release.

    This is a necessary precondition, never independent authorization.
    """
    if not isinstance(store, LockedEvidenceStore):
        raise RuntimeError("Lease-enforced evidence store required")

    store.require_lease()

    validate_attempt_record(attempt)
    command.validate()

    if not isinstance(identity, ProcessIdentity):
        raise ValueError("Linux process identity required")

    identity.validate()

    if (
        attempt.get("schema_version") != 2
        or attempt["status"] != "STARTED"
        or attempt["project"] != LAB_PROJECT
        or attempt["previous_app"] != PREVIOUS.app
        or attempt["previous_web"] != PREVIOUS.web
    ):
        raise ValueError("Bound laboratory STARTED attempt required")

    if command != plan_lab_rollback(PREVIOUS):
        raise ValueError("Unexpected restoration command")

    record = store.read(attempt["release_id"])
    validate_record(record)

    if record["phase"] != OBSERVED:
        raise ValueError("Durable OBSERVED evidence required")

    expected_fields = {
        "release_id": attempt["release_id"],
        "attempt_id": attempt["attempt_id"],
        "execution_id": attempt["execution_id"],
        "operation_fingerprint": attempt["operation_fingerprint"],
        "command_fingerprint": command_fingerprint(command),
        "project": LAB_PROJECT,
        "pid": identity.pid,
        "start_ticks": identity.start_ticks,
    }

    for field, expected in expected_fields.items():
        if record[field] != expected:
            raise ValueError(
                f"Durable execution binding mismatch: {field}"
            )

    observed = process_observer(identity)

    if observed.status != ProcessStatus.ACTIVE:
        raise ValueError("Original subprocess is not active")

    store.require_lease()

    return LaunchAssessment(
        eligible_for_barrier_release=True,
        docker_operation_settled=False,
        automatic_retry_permitted=False,
        production_execution_enabled=False,
        reason=(
            "Laboratory launch preconditions satisfied; "
            "no Docker execution or approval was performed"
        ),
    )
