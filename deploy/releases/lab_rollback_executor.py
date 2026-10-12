#!/usr/bin/env python3
"""Restricted laboratory rollback execution with bounded verification.

Executes only the approved app/web restoration in the exact lab project.
Persists STARTED before execution and keeps it unresolved afterward.

Repeated Docker inspections are allowed while health becomes ready.
Restoration commands are never retried automatically.

No production execution or journal finalization.
"""

import os
import subprocess
import time
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
VERIFY_ATTEMPTS = 20
VERIFY_INTERVAL = 2


def _run_restoration(command):
    """Execute only the strictly validated laboratory Compose command."""
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


def _verify_restoration(
    project,
    previous,
    candidate,
    expected_db_identity,
    *,
    runner=None,
    attempts=VERIFY_ATTEMPTS,
    interval=VERIFY_INTERVAL,
):
    """Poll health without repeating any Docker-changing command.

    An unavailable or invalid Docker observation fails closed.
    The image pair and DB identity must match at every observation.
    Only health status is permitted to become ready over time.
    """
    if type(attempts) is not int or not 1 <= attempts <= 30:
        raise ValueError("Invalid verification attempt count")

    if type(interval) not in (int, float) or not 0 <= interval <= 5:
        raise ValueError("Invalid verification interval")

    for index in range(attempts):
        identity = collect_allowed_snapshot(
            project,
            previous,
            candidate,
            runner=runner,
        )

        if identity.project != project:
            raise ValueError("Post-restoration project mismatch")

        if identity.db_container_id != expected_db_identity:
            raise ValueError(
                "Database identity changed; manual intervention required"
            )

        if (
            identity.app_reference != previous.app
            or identity.web_reference != previous.web
        ):
            raise ValueError(
                "Previous image pair not restored; "
                "attempt remains STARTED"
            )

        if identity.app_healthy and identity.web_healthy:
            return identity

        if index + 1 < attempts:
            time.sleep(interval)

    raise ValueError(
        "Restored image pair did not become healthy within "
        "the verification limit; attempt remains STARTED"
    )


def execute_lab_rollback(
    simulator,
    release_id,
    project=LAB_PROJECT,
    *,
    inspection_runner=None,
    command_runner=None,
    verification_attempts=VERIFY_ATTEMPTS,
    verification_interval=VERIFY_INTERVAL,
):
    """Restore lab app/web under one lock, retaining STARTED evidence.

    Successful inspection is not a journal transition or a terminal
    attempt status. Failures remain unresolved until reconciliation.
    """
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if project != LAB_PROJECT:
        raise ValueError("Production or other project prohibited")

    # Reject invalid verification settings before provisioning attempts.
    if (
        type(verification_attempts) is not int
        or not 1 <= verification_attempts <= 30
    ):
        raise ValueError("Invalid verification attempt count")

    if (
        type(verification_interval) not in (int, float)
        or not 0 <= verification_interval <= 5
    ):
        raise ValueError("Invalid verification interval")

    # The constructor provisions the private attempt directory
    # while holding its own global lock.
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

        # Fresh live eligibility evaluation occurs under this lease.
        # STARTED is durably published before Docker execution.
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

        validate_lab_compose_integrity(REPOSITORY_ROOT)

        runner = command_runner or _run_restoration

        # Exactly one restoration command invocation.
        result = runner(command)

        if result.returncode != 0:
            raise RuntimeError(
                "Laboratory restoration command failed; "
                "attempt remains STARTED for reconciliation"
            )

        _verify_restoration(
            project,
            previous,
            candidate,
            checkpoint["db_identity"],
            runner=inspection_runner,
            attempts=verification_attempts,
            interval=verification_interval,
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
