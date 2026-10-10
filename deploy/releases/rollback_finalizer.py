#!/usr/bin/env python3
"""Laboratory-only verified rollback journal finalization.

No container modifications, production execution, or approval issuance.
"""

from deployment_lock import deployment_lock
from docker_snapshot_reader import LAB_PROJECT, collect_allowed_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, State


def finalize_rollback(simulator, release_id, project, runner=None):
    """Mark ROLLED_BACK only after inspecting a healthy previous pair."""
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(project, str) or not LAB_PROJECT.fullmatch(project):
        raise ValueError("Laboratory project required")

    with deployment_lock(simulator.lock_dir):
        record = simulator.journal.read(release_id)

        if record["state"] != State.ROLLING_BACK.value:
            raise ValueError("Journal must be ROLLING_BACK")

        checkpoint = simulator.read_checkpoint(release_id, record)

        previous = ImagePair(**record["previous"])
        candidate = ImagePair(**record["candidate"])

        identity = collect_allowed_snapshot(
            project, previous, candidate, runner=runner
        )

        if identity.db_container_id != checkpoint["db_identity"]:
            raise ValueError("Database identity changed")

        if (
            identity.app_reference != previous.app
            or identity.web_reference != previous.web
        ):
            raise ValueError("Previous image pair not restored")

        if not identity.app_healthy or not identity.web_healthy:
            raise ValueError("Restored services are not healthy")

        updated = simulator.journal.advance(
            release_id,
            record["revision"],
            "restored",
        )

        return {
            "mode": "laboratory-only",
            "release_id": release_id,
            "state": updated["state"],
            "revision": updated["revision"],
            "database_identity_matched": True,
            "docker_mutation_performed": False,
            "production_execution_enabled": False,
        }
