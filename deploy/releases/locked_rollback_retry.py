#!/usr/bin/env python3
"""Read-only, laboratory-only interrupted rollback inspection.

A single deployment-wide lock covers journal reading, checkpoint
validation, Docker inspection, and recovery classification.

This module never executes restoration or finalizes a journal.
"""

from deployment_lock import deployment_lock
from docker_snapshot_reader import (
    LAB_PROJECT,
    collect_allowed_snapshot,
)
from recovery_reconciler import ContainerSnapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, State
from rollback_retry_policy import decide_rollback_retry


def decide_retry_from_docker(
    simulator,
    release_id,
    project,
    runner=None,
):
    """Classify an interrupted rollback from one live observation."""
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(project, str) or not LAB_PROJECT.fullmatch(project):
        raise ValueError("Only isolated laboratory projects are permitted")

    with deployment_lock(simulator.lock_dir):
        record = simulator.journal.read(release_id)

        if record["state"] != State.ROLLING_BACK.value:
            raise ValueError("Journal must be ROLLING_BACK")

        checkpoint = simulator.read_checkpoint(release_id, record)

        previous = ImagePair(**record["previous"])
        candidate = ImagePair(**record["candidate"])

        identity = collect_allowed_snapshot(
            project,
            previous,
            candidate,
            runner=runner,
        )

        if identity.project != project:
            raise ValueError("Docker observation project mismatch")

        snapshot = ContainerSnapshot(
            app_image=identity.app_reference,
            web_image=identity.web_reference,
            db_identity=identity.db_container_id,
            app_healthy=identity.app_healthy,
            web_healthy=identity.web_healthy,
        )

        action = decide_rollback_retry(
            record,
            snapshot,
            checkpoint["db_identity"],
        )

        return {
            "mode": "laboratory-read-only",
            "release_id": release_id,
            "project": project,
            "state": record["state"],
            "revision": record["revision"],
            "action": action.value,
            "app_reference": identity.app_reference,
            "web_reference": identity.web_reference,
            "app_healthy": identity.app_healthy,
            "web_healthy": identity.web_healthy,
            "db_container_id": identity.db_container_id,
            "database_identity_matched": (
                identity.db_container_id == checkpoint["db_identity"]
            ),
            "docker_inspection_performed": True,
            "docker_mutation_performed": False,
            "journal_mutation_performed": False,
            "production_execution_enabled": False,
        }
