#!/usr/bin/env python3
"""Pure policy for resuming an interrupted laboratory rollback.

No Docker calls, journal writes, approval issuance, or execution.
"""

from enum import Enum

from recovery_journal import validate_record
from recovery_reconciler import ContainerSnapshot
from rollback_planner import ImagePair, State


class RollbackRetryAction(str, Enum):
    RESTORE_PREVIOUS = "RESTORE_PREVIOUS"
    VERIFY_AND_FINALIZE = "VERIFY_AND_FINALIZE"
    MANUAL_INTERVENTION = "MANUAL_INTERVENTION"


def decide_rollback_retry(record, snapshot, expected_db_identity):
    """Classify a journal already in ROLLING_BACK.

    VERIFY_AND_FINALIZE is not permission to mark ROLLED_BACK
    without performing a fresh, locked finalizer inspection.
    """
    validate_record(record)

    if State(record["state"]) != State.ROLLING_BACK:
        raise ValueError("Rollback retry requires ROLLING_BACK state")

    if not isinstance(snapshot, ContainerSnapshot):
        raise ValueError("ContainerSnapshot required")

    snapshot.validate()

    if (
        not isinstance(expected_db_identity, str)
        or not expected_db_identity
    ):
        raise ValueError("Expected database identity required")

    if snapshot.db_identity != expected_db_identity:
        return RollbackRetryAction.MANUAL_INTERVENTION

    previous = ImagePair(**record["previous"])
    candidate = ImagePair(**record["candidate"])

    running = ImagePair(
        snapshot.app_image,
        snapshot.web_image,
    )

    if running == previous:
        if snapshot.app_healthy and snapshot.web_healthy:
            return RollbackRetryAction.VERIFY_AND_FINALIZE

        return RollbackRetryAction.MANUAL_INTERVENTION

    allowed_app = {previous.app, candidate.app}
    allowed_web = {previous.web, candidate.web}

    if running.app in allowed_app and running.web in allowed_web:
        return RollbackRetryAction.RESTORE_PREVIOUS

    return RollbackRetryAction.MANUAL_INTERVENTION
