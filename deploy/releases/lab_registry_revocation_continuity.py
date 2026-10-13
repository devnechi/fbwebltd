#!/usr/bin/env python3
"""Gate 4D.22C.3D.11E: pure collector-key lifecycle continuity.

Compares two canonical registry declarations and caller-supplied
revision/revocation snapshots. Neither the snapshots nor registry
signatures are authenticated by this module. Proposals are NOT commits.
No files, network, subprocess, Docker, private keys or authorization.
"""

from dataclasses import dataclass

from lab_collector_trust_policy import (
    IDENTIFIER,
    PUBLIC_KEY_HEX,
    REGISTRY_ID,
)
from lab_registry_revision_continuity import (
    RevisionStateSnapshot,
    assess_registry_revision_bytes,
    validate_revision_snapshot,
)
from lab_registry_wire_format import parse_signed_registry_bytes

MAX_TOMBSTONES = 4096
INACTIVE_STATUSES = frozenset({"disabled", "revoked"})
ALLOWED_TRANSITIONS = {
    "active": frozenset({"active", "disabled", "revoked"}),
    "disabled": frozenset({"disabled", "revoked"}),
    "revoked": frozenset({"revoked"}),
}


@dataclass(frozen=True)
class KeyLifecycleTombstone:
    collector_id: str
    key_id: str
    public_key_hex: str
    status: str


@dataclass(frozen=True)
class RevocationHistorySnapshot:
    registry_id: str
    revision: int
    signing_digest: str
    generation: int
    tombstones: tuple


@dataclass(frozen=True)
class RevocationHistoryProposal:
    registry_id: str
    candidate_revision: int
    candidate_signing_digest: str
    tombstones: tuple


@dataclass(frozen=True)
class RevocationContinuityAssessment:
    previous_revision: int
    candidate_revision: int
    logical_revision_continuity_valid: bool
    logical_lifecycle_continuity_valid: bool
    proposal: RevocationHistoryProposal

    registry_signature_verified: bool = False
    administrative_policy_authenticated: bool = False
    snapshot_provenance_authenticated: bool = False
    revocation_history_authenticated: bool = False
    revocation_currentness_verified: bool = False
    rollback_prevention_verified: bool = False
    trusted_time_source_verified: bool = False
    state_commit_performed: bool = False
    revocation_history_persisted: bool = False
    atomic_update_authorized: bool = False
    collector_authenticated: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _identity(record):
    return (record.collector_id, record.key_id)


def _tombstone(record):
    return KeyLifecycleTombstone(
        collector_id=record.collector_id,
        key_id=record.key_id,
        public_key_hex=record.public_key_hex,
        status=record.status,
    )


def validate_revocation_history(history, state):
    """Validate structural binding; never infer external authenticity."""
    validate_revision_snapshot(state)

    if type(history) is not RevocationHistorySnapshot:
        raise ValueError("RevocationHistorySnapshot required")

    if (
        type(history.registry_id) is not str
        or history.registry_id != REGISTRY_ID
        or history.registry_id != state.registry_id
        or type(history.revision) is not int
        or history.revision != state.revision
        or type(history.signing_digest) is not str
        or history.signing_digest != state.signing_digest
        or type(history.generation) is not int
        or history.generation != state.generation
    ):
        raise ValueError(
            "Revocation snapshot does not match revision state"
        )

    if (
        type(history.tombstones) is not tuple
        or len(history.tombstones) > MAX_TOMBSTONES
    ):
        raise ValueError("Invalid revocation history collection")

    previous_identity = None
    seen_material = set()

    for tombstone in history.tombstones:
        if type(tombstone) is not KeyLifecycleTombstone:
            raise ValueError("Invalid lifecycle tombstone")

        if (
            type(tombstone.collector_id) is not str
            or not IDENTIFIER.fullmatch(tombstone.collector_id)
            or type(tombstone.key_id) is not str
            or not IDENTIFIER.fullmatch(tombstone.key_id)
            or type(tombstone.public_key_hex) is not str
            or not PUBLIC_KEY_HEX.fullmatch(
                tombstone.public_key_hex
            )
            or tombstone.public_key_hex == "0" * 64
            or type(tombstone.status) is not str
            or tombstone.status not in INACTIVE_STATUSES
        ):
            raise ValueError("Malformed lifecycle tombstone")

        identity = _identity(tombstone)

        if (
            previous_identity is not None
            and identity <= previous_identity
        ):
            raise ValueError(
                "Tombstones must be strictly sorted and unique"
            )

        if tombstone.public_key_hex in seen_material:
            raise ValueError("Tombstone public key material reused")

        previous_identity = identity
        seen_material.add(tombstone.public_key_hex)

    return True


def assess_registry_revocation_bytes(
    previous_raw,
    candidate_raw,
    state,
    history,
):
    """Evaluate proposed one-step lifecycle change, without side effects.

    Both registry documents and both snapshots are caller-controlled.
    Logical agreement cannot establish signatures, trusted state,
    revocation freshness, persistence or execution authorization.
    """
    validate_revocation_history(history, state)

    before = assess_registry_revision_bytes(previous_raw, state)

    if not before.matches_existing_revision:
        raise ValueError(
            "Previous registry does not match supplied state"
        )

    after = assess_registry_revision_bytes(candidate_raw, state)

    if after.relationship != "consecutive_revision":
        raise ValueError(
            "A new consecutive registry revision is required"
        )

    previous = parse_signed_registry_bytes(previous_raw)
    candidate = parse_signed_registry_bytes(candidate_raw)

    old = {
        (item["collector_id"], item["key_id"]): item
        for item in previous["keys"]
    }

    new = {
        (item["collector_id"], item["key_id"]): item
        for item in candidate["keys"]
    }

    tombstones = {
        _identity(item): item
        for item in history.tombstones
    }

    historical_material = {
        item["public_key_hex"]
        for item in previous["keys"]
    }

    historical_material.update(
        item.public_key_hex
        for item in history.tombstones
    )

    # Previously inactive records must already be reflected
    # in supplied history. Missing historical state fails closed.
    for identity, record in old.items():
        prior = tombstones.get(identity)

        if record["status"] in INACTIVE_STATUSES:
            if (
                prior is None
                or prior.public_key_hex != record["public_key_hex"]
                or prior.status != record["status"]
            ):
                raise ValueError(
                    "Missing or conflicting previous lifecycle tombstone"
                )

        elif prior is not None:
            raise ValueError(
                "Previously inactive collector key reactivated"
            )

    # Existing key identities and security scope are immutable.
    # Only approved lifecycle state transitions may change.
    for identity, record in old.items():
        successor = new.get(identity)

        if successor is None:
            if record["status"] == "active":
                raise ValueError(
                    "Active collector key removed without deactivation"
                )
            continue

        if any(
            successor[field] != value
            for field, value in record.items()
            if field != "status"
        ):
            raise ValueError(
                "Existing key identity, material or scope changed"
            )

        if (
            successor["status"]
            not in ALLOWED_TRANSITIONS[record["status"]]
        ):
            raise ValueError("Collector key lifecycle reversal")

    # Block resurrection of removed keys, changed key material,
    # and reuse of historical public keys under new identities.
    for identity, record in new.items():
        prior = tombstones.get(identity)

        if prior is not None:
            if (
                record["public_key_hex"]
                != prior.public_key_hex
            ):
                raise ValueError(
                    "Tombstoned identity reused with different key"
                )

            if (
                record["status"]
                not in ALLOWED_TRANSITIONS[prior.status]
            ):
                raise ValueError(
                    "Tombstoned collector key reactivated"
                )

        if identity not in old:
            if prior is not None:
                raise ValueError(
                    "Removed collector identity reintroduced"
                )

            if record["public_key_hex"] in historical_material:
                raise ValueError(
                    "Previously used public key material reused"
                )

    # Create a PROPOSAL only; no revocation state is written.
    updated = dict(tombstones)

    for identity, record in new.items():
        if record["status"] in INACTIVE_STATUSES:
            updated[identity] = KeyLifecycleTombstone(
                collector_id=record["collector_id"],
                key_id=record["key_id"],
                public_key_hex=record["public_key_hex"],
                status=record["status"],
            )

    if len(updated) > MAX_TOMBSTONES:
        raise ValueError("Lifecycle history capacity exceeded")

    proposal = RevocationHistoryProposal(
        registry_id=state.registry_id,
        candidate_revision=after.candidate_revision,
        candidate_signing_digest=after.candidate_signing_digest,
        tombstones=tuple(
            updated[key]
            for key in sorted(updated)
        ),
    )

    return RevocationContinuityAssessment(
        previous_revision=state.revision,
        candidate_revision=after.candidate_revision,
        logical_revision_continuity_valid=True,
        logical_lifecycle_continuity_valid=True,
        proposal=proposal,
    )
