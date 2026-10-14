#!/usr/bin/env python3
"""Gate 4D.22C.3D.12M: pure UNAUTHENTICATED replay-state/witness contracts.

All records are supplied by the caller. No authority reads, durable commits,
protected rollback witness, trusted keys/time, I/O, retries or execution.
"""

from dataclasses import dataclass
import hashlib
import json
import re

from lab_challenge_lifecycle import (
    ReplayLedgerSnapshot, ROLES, TERMINAL,
    untrusted_ledger_commitment, validate_replay_ledger,
)
from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER

LEDGER_ID = "fbweb-lab-authority-replay-ledger-v1"
FORMAT_VERSION = 1
POSITION_DOMAIN = b"FBWEB-LAB-REPLAY-PROTECTED-POSITION-V1\x00"
OPERATION_DOMAIN = b"FBWEB-LAB-REPLAY-CONDITIONAL-INTENT-V1\x00"
ZERO_DIGEST = "0" * 64
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
ACTIONS = ("RESERVE", "ISSUE", "CONSUME", "COMPLETE", "EXPIRE", "ABORT", "UNCERTAIN")


@dataclass(frozen=True)
class ReplayProtectedPosition:
    registry_id: str
    ledger_id: str
    format_version: int
    generation: int
    ledger_digest: str
    policy_epoch: int
    recovery_epoch: int
    transition_id: str
    previous_position_digest: str


@dataclass(frozen=True)
class ReplayWitnessCheckpoint:
    position: ReplayProtectedPosition


@dataclass(frozen=True)
class ReplayProtectedReadBundle:
    ledger: ReplayLedgerSnapshot
    position: ReplayProtectedPosition
    witness: ReplayWitnessCheckpoint


@dataclass(frozen=True)
class ReplayConditionalTransitionIntent:
    expected_position: ReplayProtectedPosition
    expected_witness: ReplayWitnessCheckpoint
    candidate_ledger: ReplayLedgerSnapshot
    action: str
    request_id: str
    transition_id: str
    operation_digest: str


@dataclass(frozen=True)
class ReplayTransitionAssessment:
    classification: str
    proposed_position: ReplayProtectedPosition
    proposed_ledger: ReplayLedgerSnapshot
    logical_transition_valid: bool = True
    authority_identity_authenticated: bool = False
    witness_identity_authenticated: bool = False
    independent_trust_roots_verified: bool = False
    actual_conditional_commit_verified: bool = False
    durable_ledger_write_verified: bool = False
    witness_advanced: bool = False
    atomic_two_authority_commit_verified: bool = False
    independent_rollback_prevention_verified: bool = False
    policy_currentness_verified: bool = False
    trusted_time_verified: bool = False
    replay_prevention_verified: bool = False
    recovery_approved: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    automatic_retry_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


@dataclass(frozen=True)
class ReplayReconciliationAssessment:
    classification: str
    logical_positions_compared: bool = True
    state_authority_authenticated: bool = False
    witness_authority_authenticated: bool = False
    protected_state_currentness_verified: bool = False
    durable_commit_verified: bool = False
    rollback_prevention_verified: bool = False
    recovery_approved: bool = False
    automatic_retry_permitted: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


def _integer(value, *, zero=False):
    return type(value) is int and (0 if zero else 1) <= value <= MAX_SAFE_INTEGER


def _identifier(value):
    return type(value) is str and IDENTIFIER.fullmatch(value) is not None


def _digest(value):
    return type(value) is str and DIGEST.fullmatch(value) is not None


def _canonical(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def _position_fields(position):
    return {
        "registry_id": position.registry_id,
        "ledger_id": position.ledger_id,
        "format_version": position.format_version,
        "generation": position.generation,
        "ledger_digest": position.ledger_digest,
        "policy_epoch": position.policy_epoch,
        "recovery_epoch": position.recovery_epoch,
        "transition_id": position.transition_id,
        "previous_position_digest": position.previous_position_digest,
    }


def validate_replay_position(position):
    """Validate a caller-created position, never its authority or freshness."""
    if type(position) is not ReplayProtectedPosition:
        raise ValueError("ReplayProtectedPosition required")

    if (
        type(position.registry_id) is not str
        or position.registry_id != REGISTRY_ID
        or type(position.ledger_id) is not str
        or position.ledger_id != LEDGER_ID
        or type(position.format_version) is not int
        or position.format_version != FORMAT_VERSION
        or not _integer(position.generation, zero=True)
        or not _integer(position.policy_epoch)
        or not _integer(position.recovery_epoch)
        or not _digest(position.ledger_digest)
        or not _identifier(position.transition_id)
        or not _digest(position.previous_position_digest)
    ):
        raise ValueError("Invalid replay protected position")

    if (
        (position.generation == 0)
        != (position.previous_position_digest == ZERO_DIGEST)
    ):
        raise ValueError("Invalid replay genesis/previous digest relation")

    return True


def untrusted_position_commitment(position):
    """Domain-separated SHA-256; not an authenticated forward-only witness."""
    validate_replay_position(position)

    return hashlib.sha256(
        POSITION_DOMAIN + _canonical(_position_fields(position))
    ).hexdigest()


def validate_replay_protected_read(bundle):
    """Validate logical primary/witness equality only, no trusted read."""
    if type(bundle) is not ReplayProtectedReadBundle:
        raise ValueError("ReplayProtectedReadBundle required")

    validate_replay_ledger(bundle.ledger)
    validate_replay_position(bundle.position)

    if (
        type(bundle.witness) is not ReplayWitnessCheckpoint
        or type(bundle.witness.position) is not ReplayProtectedPosition
    ):
        raise ValueError("ReplayWitnessCheckpoint required")

    validate_replay_position(bundle.witness.position)

    if (
        bundle.ledger.registry_id != bundle.position.registry_id
        or bundle.ledger.generation != bundle.position.generation
        or untrusted_ledger_commitment(bundle.ledger)
        != bundle.position.ledger_digest
        or bundle.position != bundle.witness.position
    ):
        raise ValueError("Untrusted replay primary and witness mismatch")

    return True


def untrusted_operation_commitment(
    expected, candidate, action, request_id, transition_id
):
    """Commit caller-declared conditional operation; no MAC or authorization."""
    validate_replay_position(expected)
    validate_replay_ledger(candidate)

    if (
        type(action) is not str
        or action not in ACTIONS
        or not _identifier(request_id)
        or not _identifier(transition_id)
    ):
        raise ValueError("Invalid replay operation fields")

    data = {
        "expected_position_digest": untrusted_position_commitment(expected),
        "candidate_ledger_digest": untrusted_ledger_commitment(candidate),
        "action": action,
        "request_id": request_id,
        "transition_id": transition_id,
    }

    return hashlib.sha256(
        OPERATION_DOMAIN + _canonical(data)
    ).hexdigest()


def _compare_request_change(before, after, action, request_id):
    """Forbid silent deletion or edits to unrelated replay request history."""
    old = {
        r.challenge.request_id: r for r in before.records
    }
    new = {
        r.challenge.request_id: r for r in after.records
    }

    if action == "RESERVE":
        if request_id in old or set(new) != set(old) | {request_id}:
            raise ValueError("Reservation must add exactly one new request")

        for rid in old:
            if old[rid] != new[rid]:
                raise ValueError("Reservation changed existing replay history")

        added = new[request_id]

        if (
            added.state != "RESERVED"
            or added.generation != 1
            or added.receipts != ()
        ):
            raise ValueError("Invalid newly reserved request")

        return

    if request_id not in old or set(new) != set(old):
        raise ValueError("Request transition must retain complete history")

    for rid in old:
        if rid != request_id and old[rid] != new[rid]:
            raise ValueError("Unrelated request changed")

    previous = old[request_id]
    proposed = new[request_id]

    if (
        previous.state in TERMINAL
        or proposed.generation != previous.generation + 1
        or proposed.challenge != previous.challenge
        or proposed.purpose != previous.purpose
        or proposed.policy_epoch != previous.policy_epoch
        or proposed.state_generation != previous.state_generation
    ):
        raise ValueError("Invalid request continuity or terminal modification")

    original = previous.receipts
    updated = proposed.receipts

    if action == "ISSUE":
        allowed = (
            previous.state == "RESERVED"
            and proposed.state == "ISSUED"
            and updated == original
        )

    elif action == "CONSUME":
        new_roles = (
            {r.role for r in updated}
            - {r.role for r in original}
        )
        preserved = all(r in updated for r in original)

        allowed = (
            previous.state in ("ISSUED", "COLLECTING")
            and proposed.state == "COLLECTING"
            and len(updated) == len(original) + 1
            and len(new_roles) == 1
            and preserved
        )

    elif action == "COMPLETE":
        allowed = (
            previous.state == "COLLECTING"
            and proposed.state == "COMPLETE"
            and tuple(r.role for r in original) == ROLES
            and updated == original
        )

    elif action in ("EXPIRE", "ABORT", "UNCERTAIN"):
        target = {
            "EXPIRE": "EXPIRED",
            "ABORT": "ABORTED",
            "UNCERTAIN": "UNCERTAIN",
        }[action]

        allowed = (
            proposed.state == target
            and updated == original
        )

    else:
        allowed = False

    if not allowed:
        raise ValueError("Invalid logical replay lifecycle transition")


def assess_replay_conditional_transition(bundle, intent):
    """Create a PROPOSAL only. No commit, CAS, witness update or recovery."""
    validate_replay_protected_read(bundle)

    if type(intent) is not ReplayConditionalTransitionIntent:
        raise ValueError("ReplayConditionalTransitionIntent required")

    if (
        type(intent.expected_witness) is not ReplayWitnessCheckpoint
        or intent.expected_position != bundle.position
        or intent.expected_witness != bundle.witness
    ):
        raise ValueError("Stale conditional replay state or witness")

    if (
        not _identifier(intent.transition_id)
        or intent.transition_id == bundle.position.transition_id
        or not _identifier(intent.request_id)
        or type(intent.action) is not str
        or intent.action not in ACTIONS
    ):
        raise ValueError("Invalid replay transition identity or action")

    validate_replay_ledger(intent.candidate_ledger)

    if (
        bundle.position.generation == MAX_SAFE_INTEGER
        or intent.candidate_ledger.registry_id != bundle.ledger.registry_id
        or intent.candidate_ledger.generation != bundle.ledger.generation + 1
    ):
        raise ValueError("Invalid replay ledger generation advance")

    digest = untrusted_operation_commitment(
        bundle.position,
        intent.candidate_ledger,
        intent.action,
        intent.request_id,
        intent.transition_id,
    )

    if (
        type(intent.operation_digest) is not str
        or intent.operation_digest != digest
    ):
        raise ValueError("Untrusted replay operation commitment mismatch")

    _compare_request_change(
        bundle.ledger,
        intent.candidate_ledger,
        intent.action,
        intent.request_id,
    )

    if intent.action == "RESERVE":
        added = next(
            r for r in intent.candidate_ledger.records
            if r.challenge.request_id == intent.request_id
        )

        if added.policy_epoch != bundle.position.policy_epoch:
            raise ValueError(
                "Reservation conflicts with declared protected policy epoch"
            )

    proposed = ReplayProtectedPosition(
        registry_id=bundle.position.registry_id,
        ledger_id=bundle.position.ledger_id,
        format_version=bundle.position.format_version,
        generation=intent.candidate_ledger.generation,
        ledger_digest=untrusted_ledger_commitment(intent.candidate_ledger),
        policy_epoch=bundle.position.policy_epoch,
        recovery_epoch=bundle.position.recovery_epoch,
        transition_id=intent.transition_id,
        previous_position_digest=untrusted_position_commitment(
            bundle.position
        ),
    )

    validate_replay_position(proposed)

    return ReplayTransitionAssessment(
        classification="PROPOSED_UNCOMMITTED_TRANSITION",
        proposed_position=proposed,
        proposed_ledger=intent.candidate_ledger,
    )


def classify_replay_reconciliation(
    expected, proposed, observed_state, observed_witness
):
    """Classify untrusted reports; matching reports never establish a commit."""
    validate_replay_position(expected)
    validate_replay_position(proposed)

    if (
        proposed.registry_id != expected.registry_id
        or proposed.ledger_id != expected.ledger_id
        or proposed.format_version != expected.format_version
        or proposed.generation != expected.generation + 1
        or proposed.policy_epoch != expected.policy_epoch
        or proposed.recovery_epoch != expected.recovery_epoch
        or proposed.previous_position_digest
        != untrusted_position_commitment(expected)
        or proposed.transition_id == expected.transition_id
    ):
        raise ValueError(
            "Expected and proposed replay positions do not form a link"
        )

    if observed_state is None or observed_witness is None:
        if observed_state is None and observed_witness is None:
            label = "BOTH_AUTHORITIES_UNAVAILABLE"
        elif observed_state is None:
            label = "REPLAY_AUTHORITY_UNAVAILABLE"
        else:
            label = "REPLAY_WITNESS_UNAVAILABLE"

        return ReplayReconciliationAssessment(
            label, logical_positions_compared=False
        )

    if type(observed_witness) is not ReplayWitnessCheckpoint:
        raise ValueError("ReplayWitnessCheckpoint required")

    validate_replay_position(observed_state)
    validate_replay_position(observed_witness.position)

    witness = observed_witness.position

    if observed_state.generation < expected.generation:
        return ReplayReconciliationAssessment(
            "REPLAY_STATE_ROLLBACK_SUSPECTED"
        )

    if witness.generation < expected.generation:
        return ReplayReconciliationAssessment(
            "REPLAY_WITNESS_ROLLBACK_SUSPECTED"
        )

    if observed_state == expected and witness == expected:
        classification = "BOTH_PREVIOUS_UNTRUSTED"

    elif observed_state == proposed and witness == expected:
        classification = "STATE_AHEAD_OF_WITNESS"

    elif observed_state == expected and witness == proposed:
        classification = "WITNESS_AHEAD_OF_STATE"

    elif observed_state == proposed and witness == proposed:
        classification = "BOTH_PROPOSED_UNTRUSTED"

    else:
        classification = "CONFLICTING_OR_UNEXPECTED_POSITIONS"

    return ReplayReconciliationAssessment(classification)
