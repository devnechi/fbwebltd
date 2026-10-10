#!/usr/bin/env python3
"""Pure recovery decisions for interrupted releases. No Docker execution."""

from dataclasses import dataclass
from enum import Enum

from rollback_planner import ImagePair, State


class RecoveryAction(str, Enum):
    NO_ACTION = "NO_ACTION"
    ABORT_BEFORE_ACTIVATION = "ABORT_BEFORE_ACTIVATION"
    RESTORE_PREVIOUS = "RESTORE_PREVIOUS"
    MANUAL_INTERVENTION = "MANUAL_INTERVENTION"


@dataclass(frozen=True)
class ContainerSnapshot:
    app_image: str
    web_image: str
    db_identity: str
    app_healthy: bool
    web_healthy: bool

    def validate(self):
        ImagePair(self.app_image, self.web_image).validate()
        if not isinstance(self.db_identity, str) or not self.db_identity:
            raise ValueError("Missing database container identity")
        if type(self.app_healthy) is not bool:
            raise ValueError("Invalid app health status")
        if type(self.web_healthy) is not bool:
            raise ValueError("Invalid web health status")


def reconcile(record, snapshot, expected_db_identity):
    """Choose a recovery action without performing one.

    Docker discovery, approval verification and actual restoration
    are responsibilities of future trusted components.
    """
    if not isinstance(record, dict):
        raise ValueError("Recovery journal required")

    from recovery_journal import validate_record
    validate_record(record)

    if not isinstance(snapshot, ContainerSnapshot):
        raise ValueError("Container snapshot required")
    snapshot.validate()

    if not isinstance(expected_db_identity, str):
        raise ValueError("Expected database identity required")
    if not expected_db_identity:
        raise ValueError("Expected database identity required")

    if snapshot.db_identity != expected_db_identity:
        return RecoveryAction.MANUAL_INTERVENTION

    state = State(record["state"])
    previous = ImagePair(**record["previous"])
    candidate = ImagePair(**record["candidate"])
    running = ImagePair(snapshot.app_image, snapshot.web_image)

    if state in (State.SUCCEEDED, State.ABORTED, State.ROLLED_BACK):
        return RecoveryAction.NO_ACTION

    if state == State.RECOVERY_FAILED:
        return RecoveryAction.MANUAL_INTERVENTION

    if state == State.PRECHECK:
        if running == previous:
            return RecoveryAction.ABORT_BEFORE_ACTIVATION
        return RecoveryAction.MANUAL_INTERVENTION

    if state == State.READY:
        if running == previous:
            return RecoveryAction.ABORT_BEFORE_ACTIVATION
        return RecoveryAction.MANUAL_INTERVENTION

    if state in (
        State.ACTIVATING,
        State.VERIFYING,
        State.ROLLING_BACK,
    ):
        if running == previous:
            if snapshot.app_healthy and snapshot.web_healthy:
                return RecoveryAction.NO_ACTION
            return RecoveryAction.MANUAL_INTERVENTION

        if running == candidate or (
            running.app in (previous.app, candidate.app)
            and running.web in (previous.web, candidate.web)
        ):
            return RecoveryAction.RESTORE_PREVIOUS

        return RecoveryAction.MANUAL_INTERVENTION

    return RecoveryAction.MANUAL_INTERVENTION
