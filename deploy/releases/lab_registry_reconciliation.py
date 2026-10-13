#!/usr/bin/env python3
"""Gate 4D.22C.3D.12E: pure, non-authorizing reconciliation classifier.

All observations, acknowledgements and previous state are CALLER-SUPPLIED.
Their agreement proves neither authenticity nor durable commitment.
No filesystem, services, credentials, subprocess, Docker or state mutation.
"""

from dataclasses import dataclass

from lab_protected_state_contract import (
    ProtectedPosition,
    ProtectedReadBundle,
    ProtectedTransitionIntent,
    WitnessCheckpoint,
    assess_transition_contract,
    revocation_commitment,
    validate_position,
    validate_read_contract,
)
from lab_registry_revision_continuity import RevisionStateSnapshot
from lab_registry_revocation_continuity import (
    RevocationHistorySnapshot,
    validate_revocation_history,
)

REPORTS = frozenset({
    "NOT_ATTEMPTED",
    "ACKNOWLEDGED",
    "REJECTED",
    "UNKNOWN",
})


@dataclass(frozen=True)
class ReconciliationObservation:
    """Untrusted reports and records; None means no readable result."""

    state_position: object
    state_history: object
    witness_checkpoint: object
    state_commit_report: str = "UNKNOWN"
    witness_advance_report: str = "UNKNOWN"


@dataclass(frozen=True)
class ReconciliationAssessment:
    classification: str
    state_relation: str
    witness_relation: str
    reports_consistent_with_observations: bool
    reported_outcome_uncertain: bool
    logical_pair_matches_proposal: bool
    prior_position: ProtectedPosition
    proposed_position: ProtectedPosition

    authority_identity_authenticated: bool = False
    witness_identity_authenticated: bool = False
    administrative_policy_authenticated: bool = False
    snapshot_provenance_authenticated: bool = False
    state_response_freshness_verified: bool = False
    witness_response_freshness_verified: bool = False
    trusted_time_verified: bool = False
    authoritative_currentness_verified: bool = False
    durable_state_commit_verified: bool = False
    witness_commit_verified: bool = False
    two_authority_atomicity_verified: bool = False
    rollback_prevention_verified: bool = False
    revocation_currentness_verified: bool = False
    collector_authenticated: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _snapshot(position):
    return RevisionStateSnapshot(
        registry_id=position.registry_id,
        format_version=position.format_version,
        revision=position.revision,
        signing_digest=position.signing_digest,
        generation=position.generation,
    )


def _validate_state_read(position, history):
    if type(position) is not ProtectedPosition:
        raise ValueError("Invalid observed state position")

    if type(history) is not RevocationHistorySnapshot:
        raise ValueError("Invalid observed revocation history")

    validate_position(position)
    validate_revocation_history(history, _snapshot(position))

    if (
        revocation_commitment(history.tombstones)
        != position.revocation_digest
    ):
        raise ValueError(
            "Observed state and history commitment disagree"
        )


def _relation(observed, previous, proposed):
    if observed is None:
        return "UNAVAILABLE"

    if observed == previous:
        return "PREVIOUS"

    if observed == proposed:
        return "PROPOSED"

    if (
        observed.revision < previous.revision
        or observed.generation < previous.generation
        or observed.policy_epoch < previous.policy_epoch
        or observed.recovery_epoch < previous.recovery_epoch
    ):
        return "ROLLBACK"

    if observed.transition_id == proposed.transition_id:
        return "TRANSITION_ID_CONFLICT"

    return "OTHER"


def _report_contradicts(report, relation):
    # Acknowledgements are untrusted hints, not commit evidence.
    if report == "ACKNOWLEDGED" and relation != "PROPOSED":
        return True

    if (
        report in ("REJECTED", "NOT_ATTEMPTED")
        and relation == "PROPOSED"
    ):
        return True

    return False


def assess_reconciliation(previous_bundle, intent, observation):
    """Classify simulated split outcomes; NEVER accept or repair state.

    The expected/proposed positions are RECOMPUTED by the existing
    pure transition contract. Observations cannot inject a proposal.
    """
    validate_read_contract(previous_bundle)

    if type(intent) is not ProtectedTransitionIntent:
        raise ValueError("ProtectedTransitionIntent required")

    if type(observation) is not ReconciliationObservation:
        raise ValueError("ReconciliationObservation required")

    if (
        type(observation.state_commit_report) is not str
        or observation.state_commit_report not in REPORTS
        or type(observation.witness_advance_report) is not str
        or observation.witness_advance_report not in REPORTS
    ):
        raise ValueError(
            "Invalid caller-supplied provider reports"
        )

    proposal = assess_transition_contract(
        previous_bundle,
        intent,
    )

    previous = previous_bundle.position
    future = proposal.proposed_position

    if (
        (observation.state_position is None)
        != (observation.state_history is None)
    ):
        raise ValueError("Partial observed state/history pair")

    if observation.state_position is not None:
        _validate_state_read(
            observation.state_position,
            observation.state_history,
        )

    if observation.witness_checkpoint is not None:
        if (
            type(observation.witness_checkpoint)
            is not WitnessCheckpoint
        ):
            raise ValueError(
                "Invalid observed witness checkpoint"
            )

        validate_position(
            observation.witness_checkpoint.position
        )

        witness_position = (
            observation.witness_checkpoint.position
        )
    else:
        witness_position = None

    state = _relation(
        observation.state_position,
        previous,
        future,
    )
    witness = _relation(
        witness_position,
        previous,
        future,
    )

    if "ROLLBACK" in (state, witness):
        classification = "ROLLBACK_SUSPECTED"

    elif "TRANSITION_ID_CONFLICT" in (state, witness):
        classification = "TRANSITION_ID_CONFLICT"

    elif "OTHER" in (state, witness):
        classification = "CONFLICTING_POSITION"

    elif "UNAVAILABLE" in (state, witness):
        classification = "AUTHORITY_UNAVAILABLE"

    elif state == "PREVIOUS" and witness == "PREVIOUS":
        classification = "BOTH_PREVIOUS"

    elif state == "PROPOSED" and witness == "PREVIOUS":
        classification = "STATE_AHEAD"

    elif state == "PREVIOUS" and witness == "PROPOSED":
        classification = "WITNESS_AHEAD"

    elif state == "PROPOSED" and witness == "PROPOSED":
        classification = "BOTH_PROPOSED_UNTRUSTED"

    else:
        raise ValueError(
            "Unclassified reconciliation observation"
        )

    reports_consistent = not (
        _report_contradicts(
            observation.state_commit_report,
            state,
        )
        or _report_contradicts(
            observation.witness_advance_report,
            witness,
        )
    )

    reported_uncertain = (
        observation.state_commit_report == "UNKNOWN"
        or observation.witness_advance_report == "UNKNOWN"
    )

    return ReconciliationAssessment(
        classification=classification,
        state_relation=state,
        witness_relation=witness,
        reports_consistent_with_observations=reports_consistent,
        reported_outcome_uncertain=reported_uncertain,
        logical_pair_matches_proposal=(
            state == "PROPOSED"
            and witness == "PROPOSED"
        ),
        prior_position=previous,
        proposed_position=future,
    )
