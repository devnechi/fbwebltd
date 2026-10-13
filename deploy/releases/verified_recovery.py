#!/usr/bin/env python3
"""Bridge verified Docker identities to simulation-only recovery.

No Docker calls, deployment execution, or journal mutation.
"""

from deployment_lock import deployment_lock
from docker_identity import VerifiedIdentity
from docker_snapshot_reader import LAB_PROJECT
from recovery_reconciler import ContainerSnapshot, reconcile
from recovery_simulator import RecoverySimulator


def decide_verified(simulator, release_id, identity):
    """Reconcile one verified identity under the deployment-wide lock.

    The caller must collect the identity from an authorized,
    read-only Docker snapshot source. This function cannot prove
    that a caller-supplied identity is authentic or fresh.
    """
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(identity, VerifiedIdentity):
        raise ValueError("VerifiedIdentity required")

    if not LAB_PROJECT.fullmatch(identity.project):
        raise ValueError("Production projects are prohibited")

    with deployment_lock(simulator.lock_dir):
        record = simulator.journal.read(release_id)
        checkpoint = simulator.read_checkpoint(release_id, record)

        previous = record["previous"]
        candidate = record["candidate"]

        allowed_app = {previous["app"], candidate["app"]}
        allowed_web = {previous["web"], candidate["web"]}

        if identity.app_reference not in allowed_app:
            raise ValueError("Unexpected application digest")

        if identity.web_reference not in allowed_web:
            raise ValueError("Unexpected web digest")

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
            "mode": "simulation-only",
            "project": identity.project,
            "release_id": release_id,
            "state": record["state"],
            "revision": record["revision"],
            "action": action.value,
            "database_identity_matched": (
                identity.db_container_id == checkpoint["db_identity"]
            ),
            "docker_executed": False,
            "production_execution_enabled": False,
        }
