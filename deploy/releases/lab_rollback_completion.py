#!/usr/bin/env python3
"""Evidence-checked completion of a bound laboratory rollback.

No Docker mutations. STARTED -> SUCCEEDED -> ROLLED_BACK,
with restart recovery between the two durable writes.

The cooperative deployment lock is not production authorization.
"""

from deployment_lock import deployment_lock
from docker_snapshot_reader import collect_allowed_snapshot
from lab_rollback_command import LAB_PROJECT, PREVIOUS, plan_lab_rollback
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import AttemptStatus
from rollback_attempt_store import (
    RollbackAttemptStore,
    now,
    validate_attempt_record,
)
from rollback_finalizer import finalize_rollback_locked
from rollback_operation_gate import RollbackOperation
from rollback_planner import ImagePair, State


def _check_binding(record, journal, checkpoint, release_id):
    """Rebuild the operation fingerprint from durable release evidence."""
    if record.get("schema_version") != 2:
        raise ValueError("Only bound version-2 attempts can complete")

    if record["release_id"] != release_id:
        raise ValueError("Attempt release identity mismatch")

    if record["project"] != LAB_PROJECT:
        raise ValueError("Unexpected laboratory project")

    if record["journal_revision"] != 3 or journal["revision"] not in (3, 4):
        raise ValueError("Unexpected recovery journal revision")

    previous = ImagePair(**journal["previous"])
    candidate = ImagePair(**journal["candidate"])

    if previous != PREVIOUS:
        raise ValueError("Unexpected previous release images")

    if (
        record["previous_app"] != previous.app
        or record["previous_web"] != previous.web
        or record["candidate_app"] != candidate.app
        or record["candidate_web"] != candidate.web
        or record["database_identity"] != checkpoint["db_identity"]
    ):
        raise ValueError("Attempt differs from recovery checkpoint")

    command = plan_lab_rollback(previous, project=LAB_PROJECT)
    command.validate()

    operation = RollbackOperation(
        release_id=release_id,
        journal_revision=record["journal_revision"],
        project=LAB_PROJECT,
        previous_app=previous.app,
        previous_web=previous.web,
        candidate_app=candidate.app,
        candidate_web=candidate.web,
        database_identity=checkpoint["db_identity"],
        command_argv=command.argv,
        command_environment=command.environment,
        fingerprint=record["operation_fingerprint"],
    )

    operation.validate_fingerprint()
    return previous, candidate


def _inspect_restored(project, previous, candidate, db_identity, runner):
    identity = collect_allowed_snapshot(
        project,
        previous,
        candidate,
        runner=runner,
    )

    if identity.project != project:
        raise ValueError("Docker project identity mismatch")

    if identity.db_container_id != db_identity:
        raise ValueError("Database checkpoint identity mismatch")

    if (
        identity.app_reference != previous.app
        or identity.web_reference != previous.web
        or not identity.app_healthy
        or not identity.web_healthy
    ):
        raise ValueError("Restoration not verified healthy")

    return identity


def complete_lab_rollback(
    simulator,
    release_id,
    project=LAB_PROJECT,
    *,
    inspection_runner=None,
):
    """Complete or resume an already executed laboratory rollback.

    Never starts or retries Docker restoration. The same operation
    can resume if SUCCEEDED was durable but journal finalization
    had not yet occurred.
    """
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if project != LAB_PROJECT:
        raise ValueError("Only the exact rollback laboratory is allowed")

    # Constructor provisions the store using its own lock.
    store = RollbackAttemptStore(simulator)

    with deployment_lock(simulator.lock_dir) as lease:
        journal = simulator.journal.read(release_id)

        if journal["state"] not in (
            State.ROLLING_BACK.value,
            State.ROLLED_BACK.value,
        ):
            raise ValueError("Journal is not in a completion state")

        checkpoint = simulator.read_checkpoint(release_id, journal)
        attempts = store.read_locked(release_id, lease)

        if len(attempts) != 1:
            raise ValueError(
                "Completion requires exactly one recorded attempt"
            )

        attempt = attempts[0]
        validate_attempt_record(attempt)

        if attempt["status"] not in (
            AttemptStatus.STARTED.value,
            AttemptStatus.SUCCEEDED.value,
        ):
            raise ValueError("Attempt is not eligible for completion")

        previous, candidate = _check_binding(
            attempt,
            journal,
            checkpoint,
            release_id,
        )

        # Required even when resuming from a previously saved SUCCEEDED.
        _inspect_restored(
            project,
            previous,
            candidate,
            checkpoint["db_identity"],
            inspection_runner,
        )

        if journal["state"] == State.ROLLED_BACK.value:
            if attempt["status"] != AttemptStatus.SUCCEEDED.value:
                raise ValueError("Final journal lacks a successful attempt")

            return {
                "release_id": release_id,
                "attempt_id": attempt["attempt_id"],
                "attempt_status": "SUCCEEDED",
                "journal_state": "ROLLED_BACK",
                "already_complete": True,
                "docker_mutation_performed": False,
                "production_execution_enabled": False,
            }

        if attempt["status"] == AttemptStatus.STARTED.value:
            updated = dict(attempt)
            updated["status"] = AttemptStatus.SUCCEEDED.value
            updated["revision"] += 1
            updated["updated_at"] = now()

            validate_attempt_record(updated)

            directory = store.directory(release_id)
            destination = directory / "000001.json"

            # Durable fsync + atomic replacement. A crash here leaves
            # either STARTED or SUCCEEDED, both safely reconcilable.
            store._write(
                directory,
                destination,
                updated,
                replace=True,
            )

            attempt = updated

        # This finalizer makes its own fresh inspection while the
        # same deployment lease remains active.
        result = finalize_rollback_locked(
            simulator,
            release_id,
            project,
            lease,
            runner=inspection_runner,
        )

        if result["state"] != State.ROLLED_BACK.value:
            raise ValueError("Journal finalization did not complete")

        return {
            "release_id": release_id,
            "attempt_id": attempt["attempt_id"],
            "attempt_status": attempt["status"],
            "journal_state": result["state"],
            "already_complete": False,
            "docker_mutation_performed": False,
            "production_execution_enabled": False,
        }
