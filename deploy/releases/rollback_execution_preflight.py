#!/usr/bin/env python3
"""Read-only preflight for isolated laboratory rollback execution.

Holds one deployment lock across journal, checkpoint, persisted attempt
history, Docker inspection, and policy evaluation.

This is NOT an execution authorization or a Docker executor.
"""

from deployment_lock import deployment_lock
from docker_snapshot_reader import LAB_PROJECT, collect_allowed_snapshot
from recovery_reconciler import ContainerSnapshot
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import (
    Attempt,
    AttemptStatus,
    classify_attempts,
)
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair, State
from rollback_retry_policy import decide_rollback_retry


def inspect_rollback_preflight(simulator, release_id, project, runner=None):
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(project, str) or not LAB_PROJECT.fullmatch(project):
        raise ValueError("Production project prohibited")

    # Constructor provisions the private attempt directory.
    # It must run before acquiring the outer lock.
    store = RollbackAttemptStore(simulator)

    with deployment_lock(simulator.lock_dir):
        record = simulator.journal.read(release_id)

        if record["state"] != State.ROLLING_BACK.value:
            raise ValueError("Journal must be ROLLING_BACK")

        checkpoint = simulator.read_checkpoint(release_id, record)

        previous = ImagePair(**record["previous"])
        candidate = ImagePair(**record["candidate"])

        # One Docker collection, with only in-memory validation thereafter.
        identity = collect_allowed_snapshot(
            project,
            previous,
            candidate,
            runner=runner,
        )

        if identity.project != project:
            raise ValueError("Docker project identity mismatch")

        snapshot = ContainerSnapshot(
            app_image=identity.app_reference,
            web_image=identity.web_reference,
            db_identity=identity.db_container_id,
            app_healthy=identity.app_healthy,
            web_healthy=identity.web_healthy,
        )

        # Read without reacquiring the global lock.
        records = store._read_unlocked(release_id)

        attempts = [
            Attempt(
                item["attempt_id"],
                AttemptStatus(item["status"]),
            )
            for item in records
        ]

        database_matches = (
            identity.db_container_id == checkpoint["db_identity"]
        )

        previous_healthy = (
            identity.app_reference == previous.app
            and identity.web_reference == previous.web
            and identity.app_healthy
            and identity.web_healthy
        )

        retry_action = decide_rollback_retry(
            record,
            snapshot,
            checkpoint["db_identity"],
        )

        attempt_action = classify_attempts(
            record["state"],
            attempts,
            fresh_inspection=True,
            previous_pair_healthy=previous_healthy,
            database_identity_matched=database_matches,
        )

        # A policy can report retry eligibility only when both policies
        # agree that restoration, rather than finalization, is needed.
        retry_candidate = (
            retry_action.value == "RESTORE_PREVIOUS"
            and attempt_action.value == "RETRY_ELIGIBLE"
        )

        return {
            "mode": "laboratory-read-only-preflight",
            "release_id": release_id,
            "project": project,
            "journal_state": record["state"],
            "journal_revision": record["revision"],
            "retry_action": retry_action.value,
            "attempt_action": attempt_action.value,
            "retry_candidate": retry_candidate,
            "attempt_count": len(attempts),
            "database_identity_matched": database_matches,
            "previous_pair_healthy": previous_healthy,
            "docker_inspection_performed": True,
            "docker_mutation_performed": False,
            "journal_mutation_performed": False,
            "execution_authorized": False,
            "production_execution_enabled": False,
        }
