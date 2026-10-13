#!/usr/bin/env python3
"""Gate 4D.22C.3D.12C: PURE, NON-AUTHORIZING protected-state contracts.

Caller-created state and witness records are NOT authenticated. This module
neither commits changes nor coordinates transactional state with a witness.
No filesystem, credentials, network, subprocess, Docker or runtime permission.
"""

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import re
from typing import Protocol

from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_revision_continuity import RevisionStateSnapshot
from lab_registry_revocation_continuity import (
    KeyLifecycleTombstone,
    MAX_TOMBSTONES,
    RevocationHistoryProposal,
    RevocationHistorySnapshot,
    validate_revocation_history,
)
from lab_registry_wire_format import MAX_SAFE_INTEGER, REGISTRY_FORMAT_VERSION

DIGEST = re.compile(r"[0-9a-f]{64}\Z")
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
REVOCATION_DOMAIN = b"FBWEB-LAB-REVOCATION-COMMITMENT-V1\x00"


@dataclass(frozen=True)
class ProtectedPosition:
    registry_id: str
    format_version: int
    revision: int
    signing_digest: str
    generation: int
    policy_epoch: int
    recovery_epoch: int
    revocation_digest: str
    transition_id: str


@dataclass(frozen=True)
class WitnessCheckpoint:
    position: ProtectedPosition


@dataclass(frozen=True)
class ProtectedReadBundle:
    position: ProtectedPosition
    witness: WitnessCheckpoint
    history: RevocationHistorySnapshot


@dataclass(frozen=True)
class ProtectedTransitionIntent:
    expected_position: ProtectedPosition
    candidate_revision: int
    candidate_signing_digest: str
    proposed_history: RevocationHistoryProposal
    transition_id: str


class TransactionalStateAuthority(Protocol):
    """FUTURE adapter shape, not a trust or implementation guarantee."""

    def read_state(self, registry_id: str) -> tuple[ProtectedPosition, RevocationHistorySnapshot]:
        ...

    def conditional_commit(self, intent: ProtectedTransitionIntent) -> str:
        """Return a provider-specific result, including uncertain outcomes."""
        ...


class RollbackWitnessAuthority(Protocol):
    """Separately controlled FUTURE adapter, not implemented here."""

    def read_checkpoint(self, registry_id: str) -> WitnessCheckpoint:
        ...

    def advance_checkpoint(self, expected: WitnessCheckpoint, proposed: ProtectedPosition) -> str:
        """A witness update is NOT atomic with a state update by default."""
        ...


@dataclass(frozen=True)
class ProtectedTransitionAssessment:
    proposed_position: ProtectedPosition
    proposed_history: RevocationHistorySnapshot
    logical_conditions_match: bool = True
    commit_status: str = "NOT_ATTEMPTED"
    authority_identity_authenticated: bool = False
    witness_identity_authenticated: bool = False
    policy_provenance_authenticated: bool = False
    snapshot_provenance_authenticated: bool = False
    trusted_time_verified: bool = False
    rollback_prevention_verified: bool = False
    revocation_currentness_verified: bool = False
    durable_state_commit_verified: bool = False
    witness_advanced: bool = False
    atomic_two_authority_commit_verified: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _valid_digest(value):
    return (type(value) is str and DIGEST.fullmatch(value) is not None
            and value != "0" * 64)


def _positive_integer(value):
    return type(value) is int and 1 <= value <= MAX_SAFE_INTEGER


def validate_position(position):
    """Validate shape, NOT provenance, freshness or authority."""
    if type(position) is not ProtectedPosition:
        raise ValueError("ProtectedPosition required")
    if (type(position.registry_id) is not str
            or position.registry_id != REGISTRY_ID
            or type(position.format_version) is not int
            or position.format_version != REGISTRY_FORMAT_VERSION):
        raise ValueError("Invalid registry identity or format")
    for value in (
        position.revision, position.generation, position.policy_epoch,
        position.recovery_epoch,
    ):
        if not _positive_integer(value):
            raise ValueError("Invalid protected state integer")
    if (not _valid_digest(position.signing_digest)
            or not _valid_digest(position.revocation_digest)):
        raise ValueError("Invalid protected state digest")
    if (type(position.transition_id) is not str
            or not IDENTIFIER.fullmatch(position.transition_id)):
        raise ValueError("Invalid protected transition identifier")
    return True


def revocation_commitment(tombstones):
    """Domain-separated deterministic history digest; NOT authenticated."""
    if (type(tombstones) is not tuple
            or len(tombstones) > MAX_TOMBSTONES
            or any(type(item) is not KeyLifecycleTombstone for item in tombstones)):
        raise ValueError("Bounded lifecycle tombstone tuple required")
    # Callers must separately validate tombstone ordering and lifecycle.
    try:
        payload = json.dumps(
            [asdict(item) for item in tombstones],
            sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        ).encode("ascii")
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid revocation commitment input") from exc
    return hashlib.sha256(REVOCATION_DOMAIN + payload).hexdigest()


def _revision_snapshot(position):
    return RevisionStateSnapshot(
        registry_id=position.registry_id,
        format_version=position.format_version,
        revision=position.revision,
        signing_digest=position.signing_digest,
        generation=position.generation,
    )


def validate_read_contract(bundle):
    """Ensure three untrusted declarations agree; NOT a trusted read."""
    if type(bundle) is not ProtectedReadBundle:
        raise ValueError("ProtectedReadBundle required")
    validate_position(bundle.position)
    if type(bundle.witness) is not WitnessCheckpoint:
        raise ValueError("WitnessCheckpoint required")
    validate_position(bundle.witness.position)
    if bundle.witness.position != bundle.position:
        raise ValueError("Witness and state position disagree")
    validate_revocation_history(bundle.history, _revision_snapshot(bundle.position))
    if (revocation_commitment(bundle.history.tombstones)
            != bundle.position.revocation_digest):
        raise ValueError("Revocation commitment disagrees with state")
    return True


def assess_transition_contract(bundle, intent):
    """Produce an UNCOMMITTED proposal; never authorize a real update."""
    validate_read_contract(bundle)
    if type(intent) is not ProtectedTransitionIntent:
        raise ValueError("ProtectedTransitionIntent required")
    if type(intent.expected_position) is not ProtectedPosition:
        raise ValueError("Invalid expected position")
    validate_position(intent.expected_position)
    previous = bundle.position
    if intent.expected_position != previous:
        raise ValueError("Stale or conflicting expected position")
    if (type(intent.candidate_revision) is not int
            or previous.revision >= MAX_SAFE_INTEGER
            or intent.candidate_revision != previous.revision + 1):
        raise ValueError("Invalid proposed revision advancement")
    if not _valid_digest(intent.candidate_signing_digest):
        raise ValueError("Invalid candidate signing digest")
    if (type(intent.transition_id) is not str
            or not IDENTIFIER.fullmatch(intent.transition_id)
            or intent.transition_id == previous.transition_id):
        raise ValueError("Invalid or repeated transition identifier")
    proposal = intent.proposed_history
    if type(proposal) is not RevocationHistoryProposal:
        raise ValueError("RevocationHistoryProposal required")
    if (proposal.registry_id != previous.registry_id
            or type(proposal.candidate_revision) is not int
            or proposal.candidate_revision != intent.candidate_revision
            or type(proposal.candidate_signing_digest) is not str
            or proposal.candidate_signing_digest != intent.candidate_signing_digest):
        raise ValueError("Revocation proposal does not match candidate")
    if previous.generation >= MAX_SAFE_INTEGER:
        raise ValueError("Protected generation exhausted")
    future = replace(
        previous,
        revision=intent.candidate_revision,
        signing_digest=intent.candidate_signing_digest,
        generation=previous.generation + 1,
        revocation_digest=revocation_commitment(proposal.tombstones),
        transition_id=intent.transition_id,
    )
    proposed_history = RevocationHistorySnapshot(
        registry_id=future.registry_id,
        revision=future.revision,
        signing_digest=future.signing_digest,
        generation=future.generation,
        tombstones=proposal.tombstones,
    )
    validate_revocation_history(proposed_history, _revision_snapshot(future))
    previous_marks = {
        (item.collector_id, item.key_id): item
        for item in bundle.history.tombstones
    }
    future_marks = {
        (item.collector_id, item.key_id): item
        for item in proposed_history.tombstones
    }
    for identity, old in previous_marks.items():
        new = future_marks.get(identity)
        if (new is None or new.public_key_hex != old.public_key_hex
                or (old.status == "revoked" and new.status != "revoked")
                or (old.status == "disabled"
                    and new.status not in ("disabled", "revoked"))):
            raise ValueError("Revocation history regression")
    return ProtectedTransitionAssessment(
        proposed_position=future,
        proposed_history=proposed_history,
    )
