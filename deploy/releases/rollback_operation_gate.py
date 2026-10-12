#!/usr/bin/env python3
"""Non-executing rollback operation gate for the isolated Docker lab.

Requires an active matching deployment lease. Rechecks journal,
checkpoint, Docker identity, attempt history and retry policies.

The resulting operation fingerprint is an integrity identifier,
not approval, authentication or execution authorization.
"""

import hashlib
import json
from dataclasses import dataclass

from deployment_lock import DeploymentLease
from docker_snapshot_reader import collect_allowed_snapshot
from lab_rollback_command import (
    LAB_PROJECT,
    PREVIOUS,
    plan_lab_rollback,
)
from recovery_reconciler import ContainerSnapshot
from recovery_simulator import RecoverySimulator
from rollback_attempt_policy import (
    AttemptDecision,
    classify_attempts,
)
from rollback_attempt_view import read_attempts_locked
from rollback_planner import ImagePair, State
from rollback_retry_policy import decide_rollback_retry


@dataclass(frozen=True)
class RollbackOperation:
    release_id: str
    journal_revision: int
    project: str
    previous_app: str
    previous_web: str
    candidate_app: str
    candidate_web: str
    database_identity: str
    command_argv: tuple
    command_environment: tuple
    fingerprint: str
    execution_authorized: bool = False

    def validate_fingerprint(self):
        payload = {
            "release_id": self.release_id,
            "journal_revision": self.journal_revision,
            "project": self.project,
            "previous_app": self.previous_app,
            "previous_web": self.previous_web,
            "candidate_app": self.candidate_app,
            "candidate_web": self.candidate_web,
            "database_identity": self.database_identity,
            "command_argv": list(self.command_argv),
            "command_environment": [
                list(item) for item in self.command_environment
            ],
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        expected = hashlib.sha256(encoded).hexdigest()

        if self.fingerprint != expected:
            raise ValueError("Rollback operation fingerprint mismatch")

        if self.execution_authorized is not False:
            raise ValueError("Operation fingerprint cannot grant authorization")

        return True


def evaluate_rollback_operation_locked(
    simulator,
    release_id,
    project,
    lease,
    runner=None,
):
    """Construct an eligible operation without execution or persistence.

    This is a single-observation, cooperative-lock decision.
    It does not eliminate external Docker races or authenticate evidence.
    """
    if not isinstance(simulator, RecoverySimulator):
        raise ValueError("RecoverySimulator required")

    if not isinstance(lease, DeploymentLease):
        raise RuntimeError("Deployment lease required")

    lease.require(simulator.lock_dir)

    if project != LAB_PROJECT:
        raise ValueError("Only the exact executor laboratory is allowed")

    journal = simulator.journal.read(release_id)

    if journal["state"] != State.ROLLING_BACK.value:
        raise ValueError("Journal must be ROLLING_BACK")

    checkpoint = simulator.read_checkpoint(release_id, journal)

    previous = ImagePair(**journal["previous"])
    candidate = ImagePair(**journal["candidate"])

    previous.validate()
    candidate.validate()

    if previous != PREVIOUS:
        raise ValueError("Unexpected previous release image pair")

    command = plan_lab_rollback(previous, project=project)
    command.validate()

    identity = collect_allowed_snapshot(
        project,
        previous,
        candidate,
        runner=runner,
    )

    if identity.project != project:
        raise ValueError("Observed Docker project mismatch")

    if identity.db_container_id != checkpoint["db_identity"]:
        raise ValueError("Database checkpoint identity mismatch")

    snapshot = ContainerSnapshot(
        app_image=identity.app_reference,
        web_image=identity.web_reference,
        db_identity=identity.db_container_id,
        app_healthy=identity.app_healthy,
        web_healthy=identity.web_healthy,
    )

    attempts = read_attempts_locked(simulator, release_id)

    previous_healthy = (
        identity.app_reference == previous.app
        and identity.web_reference == previous.web
        and identity.app_healthy
        and identity.web_healthy
    )

    retry_action = decide_rollback_retry(
        journal,
        snapshot,
        checkpoint["db_identity"],
    )

    attempt_action = classify_attempts(
        journal["state"],
        attempts,
        fresh_inspection=True,
        previous_pair_healthy=previous_healthy,
        database_identity_matched=True,
    )

    if (
        retry_action.value != "RESTORE_PREVIOUS"
        or attempt_action != AttemptDecision.RETRY_ELIGIBLE
    ):
        raise ValueError(
            "Restoration is not eligible: "
            f"retry={retry_action.value}, "
            f"attempt={attempt_action.value}"
        )

    payload = {
        "release_id": release_id,
        "journal_revision": journal["revision"],
        "project": project,
        "previous_app": previous.app,
        "previous_web": previous.web,
        "candidate_app": candidate.app,
        "candidate_web": candidate.web,
        "database_identity": checkpoint["db_identity"],
        "command_argv": list(command.argv),
        "command_environment": [
            list(item) for item in command.environment
        ],
    }

    fingerprint = hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    operation = RollbackOperation(
        release_id=release_id,
        journal_revision=journal["revision"],
        project=project,
        previous_app=previous.app,
        previous_web=previous.web,
        candidate_app=candidate.app,
        candidate_web=candidate.web,
        database_identity=checkpoint["db_identity"],
        command_argv=command.argv,
        command_environment=command.environment,
        fingerprint=fingerprint,
    )

    operation.validate_fingerprint()
    return operation
