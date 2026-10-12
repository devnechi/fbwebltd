#!/usr/bin/env python3
"""Pure, laboratory-only rollback attempt lifecycle policy.

This module cannot read Docker, issue approval, execute restoration,
write evidence, or change recovery journal states.
"""

from dataclasses import dataclass
from enum import Enum

from rollback_planner import State


MAX_FAILED_ATTEMPTS = 3


class AttemptStatus(str, Enum):
    STARTED = "STARTED"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    INTERRUPTED = "INTERRUPTED"


class AttemptDecision(str, Enum):
    INSPECT_REQUIRED = "INSPECT_REQUIRED"
    RETRY_ELIGIBLE = "RETRY_ELIGIBLE"
    VERIFY_AND_FINALIZE = "VERIFY_AND_FINALIZE"
    MANUAL_INTERVENTION = "MANUAL_INTERVENTION"


@dataclass(frozen=True)
class Attempt:
    attempt_id: str
    status: AttemptStatus

    def validate(self):
        if (
            not isinstance(self.attempt_id, str)
            or not self.attempt_id
            or len(self.attempt_id) > 100
            or not all(
                char.isascii() and (char.isalnum() or char in "-_")
                for char in self.attempt_id
            )
        ):
            raise ValueError("Invalid attempt ID")

        if not isinstance(self.status, AttemptStatus):
            raise ValueError("Invalid attempt status")


def classify_attempts(
    journal_state,
    attempts,
    *,
    fresh_inspection=False,
    previous_pair_healthy=False,
    database_identity_matched=False,
):
    """Return a non-executing recovery recommendation.

    All inspection flags are caller assertions. They must not be
    treated as authenticated evidence or deployment authorization.
    """
    if journal_state != State.ROLLING_BACK.value:
        raise ValueError("Attempt classification requires ROLLING_BACK")

    if not isinstance(attempts, (list, tuple)):
        raise ValueError("Attempt collection required")

    for attempt in attempts:
        if not isinstance(attempt, Attempt):
            raise ValueError("Invalid attempt record")
        attempt.validate()

    ids = [attempt.attempt_id for attempt in attempts]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate attempt ID")

    for value in (
        fresh_inspection,
        previous_pair_healthy,
        database_identity_matched,
    ):
        if type(value) is not bool:
            raise ValueError("Inspection flags must be boolean")

    # Never make recovery decisions on an observed DB mismatch.
    if fresh_inspection and not database_identity_matched:
        return AttemptDecision.MANUAL_INTERVENTION

    # Without fresh inspection, no restoration or finalization decision.
    if not fresh_inspection:
        return AttemptDecision.INSPECT_REQUIRED

    if previous_pair_healthy:
        return AttemptDecision.VERIFY_AND_FINALIZE

    if any(
        attempt.status in (
            AttemptStatus.STARTED,
            AttemptStatus.INTERRUPTED,
        )
        for attempt in attempts
    ):
        return AttemptDecision.INSPECT_REQUIRED

    if any(
        attempt.status == AttemptStatus.SUCCEEDED
        for attempt in attempts
    ):
        return AttemptDecision.MANUAL_INTERVENTION

    failures = sum(
        attempt.status == AttemptStatus.FAILED
        for attempt in attempts
    )

    if failures >= MAX_FAILED_ATTEMPTS:
        return AttemptDecision.MANUAL_INTERVENTION

    return AttemptDecision.RETRY_ELIGIBLE
