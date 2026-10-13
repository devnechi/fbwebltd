#!/usr/bin/env python3
"""Laboratory-only rollback finalization with an active lock lease.

Does not modify Docker, grant production approval, or execute
restoration. The caller must verify restoration before finalization.
"""

from deployment_lock import DeploymentLease, deployment_lock
from docker_snapshot_reader import LAB_PROJECT, collect_allowed_snapshot
from recovery_simulator import RecoverySimulator
from rollback_planner import ImagePair, State


def finalize_rollback_locked(
    simulator,
    release_id,
    project,
    lease,
    runner=None,
):
    """Verify and finalize while retaining the caller's global lock."""
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(lease, DeploymentLease):
        raise RuntimeError("Deployment lease required")

    lease.require(simulator.lock_dir)

    if not isinstance(project, str) or not LAB_PROJECT.fullmatch(project):
        raise ValueError("Laboratory project required")

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
        raise ValueError("Docker project mismatch")

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


def finalize_rollback(simulator, release_id, project, runner=None):
    """Backward-compatible wrapper acquiring the deployment lock."""
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    with deployment_lock(simulator.lock_dir) as lease:
        return finalize_rollback_locked(
            simulator,
            release_id,
            project,
            lease,
            runner=runner,
        )
