#!/usr/bin/env python3
"""Laboratory-only, read-only recovery decision coordinator.

Acquire one global lock before reading the release record, collecting
Docker metadata, and producing a recovery decision.

No Docker mutation, journal mutation, or approval issuance.
"""

from deployment_lock import deployment_lock
from docker_snapshot_reader import (
    LAB_PROJECT,
    collect_allowed_snapshot,
)
from recovery_reconciler import ContainerSnapshot, reconcile
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair


def decide_from_docker(
    simulator,
    release_id,
    project,
    runner=None,
):
    """Produce one recovery decision from a fresh laboratory observation."""
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(project, str) or not LAB_PROJECT.fullmatch(project):
        raise ValueError("Production Docker inspection prohibited")

    with deployment_lock(simulator.lock_dir):
        record = simulator.journal.read(release_id)
        checkpoint = simulator.read_checkpoint(release_id, record)

        previous = ImagePair(**record["previous"])
        candidate = ImagePair(**record["candidate"])

        identity = collect_allowed_snapshot(
            project,
            previous,
            candidate,
            runner=runner,
        )

        snapshot = ContainerSnapshot(
            app_image=identity.app_reference,
            web_image=identity.web_reference,
            db_identity=identity.db_container_id,
            app_healthy=identity.app_healthy,
            web_healthy=identity.web_healthy,
        )

        action = reconcile(
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
            "app_container_id": identity.app_container_id,
            "web_container_id": identity.web_container_id,
            "db_container_id": identity.db_container_id,
            "database_identity_matched": (
                identity.db_container_id == checkpoint["db_identity"]
            ),
            "docker_inspection_performed": True,
            "docker_mutation_performed": False,
            "journal_mutation_performed": False,
            "production_execution_enabled": False,
        }
