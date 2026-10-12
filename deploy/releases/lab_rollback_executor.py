#!/usr/bin/env python3
"""Restricted laboratory rollback execution, Gate 4D.16AE.7.

Executes only the approved app/web restoration in the exact lab project.
Persists STARTED before execution and keeps it unresolved afterward.

Does not finalize the journal or claim verified attempt completion.
Production execution is prohibited.
"""

import os
import subprocess
from pathlib import Path

from deployment_lock import deployment_lock
from docker_snapshot_reader import collect_allowed_snapshot
from lab_compose_integrity import validate_lab_compose_integrity
from lab_rollback_command import (
    LAB_PROJECT,
    PREVIOUS,
    plan_lab_rollback,
)
from recovery_simulator import RecoverySimulator
from rollback_attempt_store import RollbackAttemptStore
from rollback_planner import ImagePair, State


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
COMMAND_TIMEOUT = 120


def _run_restoration(command):
    """Run one exact Compose command with a restricted environment."""
    command.validate()

    if command.project != LAB_PROJECT or command.images != PREVIOUS:
        raise ValueError("Unauthorized restoration request")

    environment = {
        "PATH": "/usr/bin:/bin",
        "HOME": os.path.expanduser("~"),
        "LAB_APP_IMAGE": PREVIOUS.app,
        "LAB_WEB_IMAGE": PREVIOUS.web,
    }

    return subprocess.run(
        list(command.argv),
        cwd=str(REPOSITORY_ROOT),
        env=environment,
        capture_output=True,
        text=True,
        timeout=COMMAND_TIMEOUT,
        check=False,
    )


def execute_lab_rollback(
    simulator,
    release_id,
    project=LAB_PROJECT,
    *,
    inspection_runner=None,
    command_runner=None,
):
    """Execute one laboratory restoration under a single lock.

    A successful result means a verified previous image pair was
    observed after the command. It does NOT mean rollback finalization.

    On errors or interruption, STARTED remains unresolved. A separate
    recovery procedure must inspect actual Docker state before retry.
    """
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if project != LAB_PROJECT:
        raise ValueError("Production or other project prohibited")

    # Construct the store before taking the coordinator lock because
    # its constructor acquires that lock while provisioning storage.
    store = RollbackAttemptStore(simulator)

    with deployment_lock(simulator.lock_dir) as lease:
        validate_lab_compose_integrity(REPOSITORY_ROOT)

        journal = simulator.journal.read(release_id)

        if journal["state"] != State.ROLLING_BACK.value:
            raise ValueError("Journal must be ROLLING_BACK")

        checkpoint = simulator.read_checkpoint(release_id, journal)

        previous = ImagePair(**journal["previous"])
        candidate = ImagePair(**journal["candidate"])

        if previous != PREVIOUS:
            raise ValueError("Unexpected previous images")

        command = plan_lab_rollback(previous, project=project)
        command.validate()

        # This method conducts its own live eligibility evaluation
        # under the same lease, then durably persists STARTED.
        attempt = store.begin_bound_locked(
            release_id,
            project,
            lease,
            runner=inspection_runner,
        )

        if attempt["schema_version"] != 2:
            raise ValueError("Versioned attempt required")

        if (
            attempt["journal_revision"] != journal["revision"]
            or attempt["database_identity"] != checkpoint["db_identity"]
            or attempt["previous_app"] != previous.app
            or attempt["previous_web"] != previous.web
            or attempt["candidate_app"] != candidate.app
            or attempt["candidate_web"] != candidate.web
        ):
            raise ValueError("Bound attempt does not match release")

        # File contents are checked again immediately before command.
        # Other Docker clients and external file changes remain
        # outside the protection of our cooperative lock.
        validate_lab_compose_integrity(REPOSITORY_ROOT)

        runner = command_runner or _run_restoration

        # No untrusted argv, shell=True, user-selected services,
        # project name, Compose path or image references are accepted.
        result = runner(command)

        if result.returncode != 0:
            raise RuntimeError(
                "Laboratory restoration command failed; "
                "attempt remains STARTED for reconciliation"
            )

        # Post-execution verification requires fresh Docker evidence.
        identity = collect_allowed_snapshot(
            project,
            previous,
            candidate,
            runner=inspection_runner,
        )

        if identity.project != project:
            raise ValueError("Post-restoration project mismatch")

        if identity.db_container_id != checkpoint["db_identity"]:
            raise ValueError(
                "Database identity changed; manual intervention required"
            )

        if (
            identity.app_reference != previous.app
            or identity.web_reference != previous.web
            or not identity.app_healthy
            or not identity.web_healthy
        ):
            raise ValueError(
                "Previous image pair not verified healthy; "
                "attempt remains STARTED"
            )

        current = simulator.journal.read(release_id)

        if (
            current["state"] != State.ROLLING_BACK.value
            or current["revision"] != journal["revision"]
        ):
            raise ValueError("Recovery journal changed during execution")

        return {
            "mode": "isolated-laboratory",
            "release_id": release_id,
            "project": project,
            "execution_id": attempt["execution_id"],
            "attempt_id": attempt["attempt_id"],
            "attempt_status": "STARTED",
            "restoration_verified": True,
            "database_identity_matched": True,
            "journal_state": current["state"],
            "journal_finalized": False,
            "production_execution_enabled": False,
        }
