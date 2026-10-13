#!/usr/bin/env python3
"""Gate 4D.22C.3D.11D: pure offline registry revision continuity.

Checks logical revision and predecessor-digest relationships against
a caller-supplied snapshot.

SECURITY LIMITS:
- The snapshot is NOT independently authenticated.
- Registry signatures are NOT cryptographically verified here.
- No registry is accepted, installed or committed by this module.
- No state persistence, filesystem, subprocess, Docker or network.
- No trusted clock, revocation enforcement or execution permission.
"""

from dataclasses import dataclass
import hashlib
import re

from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import (
    MAX_SAFE_INTEGER,
    REGISTRY_FORMAT_VERSION,
    parse_signed_registry_bytes,
    registry_signing_bytes,
)

DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class RevisionStateSnapshot:
    registry_id: str
    format_version: int
    revision: int
    signing_digest: str
    generation: int


@dataclass(frozen=True)
class RevisionContinuityAssessment:
    candidate_revision: int
    candidate_signing_digest: str
    snapshot_revision: int
    snapshot_generation: int
    relationship: str
    logical_continuity_valid: bool
    matches_existing_revision: bool

    registry_signature_verified: bool = False
    administrative_policy_authenticated: bool = False
    snapshot_provenance_authenticated: bool = False
    registry_currentness_verified: bool = False
    rollback_prevention_verified: bool = False
    revocation_history_verified: bool = False
    trusted_time_source_verified: bool = False
    state_commit_performed: bool = False
    atomic_update_authorized: bool = False
    collector_authenticated: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def validate_revision_snapshot(snapshot):
    """Validate snapshot shape without authenticating its origin."""
    if type(snapshot) is not RevisionStateSnapshot:
        raise ValueError("RevisionStateSnapshot required")

    if (
        type(snapshot.registry_id) is not str
        or snapshot.registry_id != REGISTRY_ID
    ):
        raise ValueError("Invalid snapshot registry identity")

    if (
        type(snapshot.format_version) is not int
        or snapshot.format_version != REGISTRY_FORMAT_VERSION
    ):
        raise ValueError("Invalid snapshot registry format")

    if (
        type(snapshot.revision) is not int
        or not 1 <= snapshot.revision <= MAX_SAFE_INTEGER
    ):
        raise ValueError("Invalid snapshot revision")

    if (
        type(snapshot.generation) is not int
        or not 1 <= snapshot.generation <= MAX_SAFE_INTEGER
    ):
        raise ValueError("Invalid snapshot generation")

    if (
        type(snapshot.signing_digest) is not str
        or not DIGEST_PATTERN.fullmatch(snapshot.signing_digest)
        or snapshot.signing_digest == "0" * 64
    ):
        raise ValueError("Invalid snapshot signing digest")

    return True


def assess_registry_revision_bytes(raw, snapshot):
    """Compare registry metadata with an untrusted supplied snapshot.

    The result is a logical comparison only. It MUST NOT serve as
    evidence of a committed, trusted or current registry revision.

    The calling system must separately establish registry signature
    validity, administrative authority and protected state provenance.
    """
    validate_revision_snapshot(snapshot)

    # Parse original bytes, retaining duplicate-key and canonical
    # representation protections established in Gate 3D.11B.
    document = parse_signed_registry_bytes(raw)

    if (
        document["registry_id"] != snapshot.registry_id
        or document["registry_format_version"]
        != snapshot.format_version
    ):
        raise ValueError("Registry identity or format mismatch")

    candidate_revision = document["revision"]

    # Signed-content digest excludes the signature field and
    # includes the registry-specific domain-separation prefix.
    candidate_digest = hashlib.sha256(
        registry_signing_bytes(document)
    ).hexdigest()

    if candidate_revision < snapshot.revision:
        raise ValueError("Registry revision rollback detected")

    if candidate_revision == snapshot.revision:
        if candidate_digest != snapshot.signing_digest:
            raise ValueError(
                "Conflicting content at existing registry revision"
            )

        return RevisionContinuityAssessment(
            candidate_revision=candidate_revision,
            candidate_signing_digest=candidate_digest,
            snapshot_revision=snapshot.revision,
            snapshot_generation=snapshot.generation,
            relationship="same_revision_same_digest",
            logical_continuity_valid=True,
            matches_existing_revision=True,
        )

    if candidate_revision != snapshot.revision + 1:
        raise ValueError("Missing intermediate registry revision")

    if document["previous_revision"] != snapshot.revision:
        raise ValueError("Registry predecessor revision mismatch")

    if document["previous_digest"] != snapshot.signing_digest:
        raise ValueError("Registry predecessor digest mismatch")

    return RevisionContinuityAssessment(
        candidate_revision=candidate_revision,
        candidate_signing_digest=candidate_digest,
        snapshot_revision=snapshot.revision,
        snapshot_generation=snapshot.generation,
        relationship="consecutive_revision",
        logical_continuity_valid=True,
        matches_existing_revision=False,
    )
