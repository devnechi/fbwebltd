#!/usr/bin/env python3
"""Pure, non-executing release and rollback state planner."""

from dataclasses import dataclass
from enum import Enum
import re


IMAGE_PATTERN = re.compile(
    r"^ghcr\.io/devnechi/fbwebltd-(app|web)"
    r"@sha256:[0-9a-f]{64}$"
)


class State(str, Enum):
    PRECHECK = "PRECHECK"
    READY = "READY"
    ACTIVATING = "ACTIVATING"
    VERIFYING = "VERIFYING"
    SUCCEEDED = "SUCCEEDED"
    ABORTED = "ABORTED"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    RECOVERY_FAILED = "RECOVERY_FAILED"


TRANSITIONS = {
    (State.PRECHECK, "precheck_passed"): State.READY,
    (State.PRECHECK, "precheck_failed"): State.ABORTED,
    (State.READY, "activate"): State.ACTIVATING,
    (State.READY, "cancel"): State.ABORTED,
    (State.ACTIVATING, "activated"): State.VERIFYING,
    (State.ACTIVATING, "failed"): State.ROLLING_BACK,
    (State.VERIFYING, "healthy"): State.SUCCEEDED,
    (State.VERIFYING, "failed"): State.ROLLING_BACK,
    (State.VERIFYING, "timeout"): State.ROLLING_BACK,
    (State.ROLLING_BACK, "restored"): State.ROLLED_BACK,
    (State.ROLLING_BACK, "failed"): State.RECOVERY_FAILED,
}


@dataclass(frozen=True)
class ImagePair:
    app: str
    web: str

    def validate(self):
        for kind, reference in (("app", self.app), ("web", self.web)):
            if not isinstance(reference, str):
                raise ValueError("Image reference must be a string")
            match = IMAGE_PATTERN.fullmatch(reference)
            if match is None or match.group(1) != kind:
                raise ValueError(
                    f"Invalid immutable {kind} image reference"
                )


@dataclass(frozen=True)
class ReleasePlan:
    candidate: ImagePair
    previous: ImagePair
    approval_verified: bool
    provenance_verified: bool
    recovery_record_persisted: bool
    backup_verified: bool
    deployment_lock_acquired: bool
    current_health_verified: bool

    def validate_preconditions(self):
        self.candidate.validate()
        self.previous.validate()

        checks = {
            "approval": self.approval_verified,
            "provenance": self.provenance_verified,
            "recovery record": self.recovery_record_persisted,
            "backup": self.backup_verified,
            "deployment lock": self.deployment_lock_acquired,
            "current health": self.current_health_verified,
        }

        for name, passed in checks.items():
            if passed is not True:
                raise ValueError(f"Missing required {name} verification")

        if self.candidate == self.previous:
            raise ValueError("Candidate already matches previous images")

        return True


def next_state(current, event, plan=None):
    """Return the next permitted state without performing any action."""
    try:
        current = State(current)
    except ValueError as exc:
        raise ValueError("Unknown release state") from exc

    target = TRANSITIONS.get((current, event))
    if target is None:
        raise ValueError(
            f"Forbidden release transition: {current.value} / {event}"
        )

    if (current, event) in (
        (State.PRECHECK, "precheck_passed"),
        (State.READY, "activate"),
    ):
        if not isinstance(plan, ReleasePlan):
            raise ValueError("Validated release plan required")
        plan.validate_preconditions()

    return target


def execution_policy():
    """Static service boundary; not a Docker command generator."""
    return {
        "allowed_services": ("app", "web"),
        "forbidden_services": ("db",),
        "automatic_migrations": False,
        "unrestricted_compose_up": False,
        "production_execution_enabled": False,
    }
