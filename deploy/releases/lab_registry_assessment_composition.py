#!/usr/bin/env python3
"""Gate 4D.22C.3D.11F: non-authorizing registry composition.

Combines candidate Ed25519 signature verification, revision
continuity and collector-key revocation continuity.

All trust policies, snapshots and assessment time are supplied
by the caller. Previous-registry signatures are not verified.

NO persistence, privileged operations, Docker or deployment.
"""

from dataclasses import dataclass

from lab_registry_signature_verifier import (
    verify_registry_signature_bytes,
)
from lab_registry_revision_continuity import (
    assess_registry_revision_bytes,
)
from lab_registry_revocation_continuity import (
    assess_registry_revocation_bytes,
    RevocationHistoryProposal,
)


@dataclass(frozen=True)
class RegistryCompositionAssessment:
    candidate_revision: int
    candidate_signing_digest: str
    previous_revision: int
    snapshot_generation: int
    signature_matches_supplied_admin_key: bool
    revision_matches_supplied_snapshot: bool
    lifecycle_matches_supplied_history: bool
    proposed_history: RevocationHistoryProposal

    registry_provenance_authenticated: bool = False
    previous_registry_authenticated: bool = False
    administrative_identity_authenticated: bool = False
    administrative_policy_authenticated: bool = False
    snapshot_provenance_authenticated: bool = False
    revocation_history_authenticated: bool = False
    registry_currentness_verified: bool = False
    revocation_currentness_verified: bool = False
    trusted_time_source_verified: bool = False
    rollback_prevention_verified: bool = False
    replay_prevention_verified: bool = False
    state_commit_performed: bool = False
    revocation_history_persisted: bool = False
    atomic_update_authorized: bool = False
    collector_authenticated: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def assess_registry_composition_bytes(
    previous_raw,
    candidate_raw,
    administrators,
    state,
    history,
    *,
    now,
):
    """Run all local checks on one immutable candidate byte string.

    A positive result reports logical and cryptographic consistency
    under caller-supplied inputs. It is NOT registry acceptance,
    authoritative currentness or execution authorization.

    Any failed check raises ValueError instead of returning
    a partially successful assessment.
    """
    # Gate 3D.11B: candidate Ed25519 signature under the
    # supplied administrative public-key policy.
    signature = verify_registry_signature_bytes(
        candidate_raw,
        administrators,
        now=now,
    )

    # Gate 3D.11D: consecutive logical revision relationship.
    revision = assess_registry_revision_bytes(
        candidate_raw,
        state,
    )

    # Gate 3D.11E: historical lifecycle transitions and
    # uncommitted revocation-history proposal.
    lifecycle = assess_registry_revocation_bytes(
        previous_raw,
        candidate_raw,
        state,
        history,
    )

    proposal = lifecycle.proposal

    if not (
        signature.registry_structure_valid
        and signature.registry_signature_verified
        and signature.administrative_key_policy_eligible
        and signature.declared_window_matches
        and revision.logical_continuity_valid
        and revision.relationship == "consecutive_revision"
        and not revision.matches_existing_revision
        and lifecycle.logical_revision_continuity_valid
        and lifecycle.logical_lifecycle_continuity_valid
    ):
        raise ValueError(
            "Composite registry prerequisite failed"
        )

    # All components must refer to one registry identity,
    # exactly one candidate revision and exactly the same
    # domain-separated unsigned signing digest.
    if not (
        signature.registry_declaration.registry_id
        == state.registry_id
        == proposal.registry_id
        and signature.registry_revision
        == revision.candidate_revision
        == lifecycle.candidate_revision
        == proposal.candidate_revision
        and revision.snapshot_revision
        == lifecycle.previous_revision
        == state.revision
        and revision.snapshot_generation
        == state.generation
        and signature.registry_signing_digest
        == revision.candidate_signing_digest
        == proposal.candidate_signing_digest
    ):
        raise ValueError(
            "Composite registry revision or digest disagreement"
        )

    return RegistryCompositionAssessment(
        candidate_revision=revision.candidate_revision,
        candidate_signing_digest=revision.candidate_signing_digest,
        previous_revision=revision.snapshot_revision,
        snapshot_generation=revision.snapshot_generation,
        signature_matches_supplied_admin_key=True,
        revision_matches_supplied_snapshot=True,
        lifecycle_matches_supplied_history=True,
        proposed_history=proposal,
    )
