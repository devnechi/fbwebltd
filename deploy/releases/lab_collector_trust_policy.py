#!/usr/bin/env python3
"""Gate 4D.22C.3D.9: pure laboratory collector-key policy.

Validates verifier-supplied collector/key declarations and checks
whether one key is eligible for a future signature-verification step.

Registry authenticity is a caller responsibility.

No signature verification, key generation, filesystem access,
Docker, subprocess, network, replay storage or authorization.
"""

from dataclasses import dataclass
from datetime import timezone
import re

from lab_runtime_auth_envelope import (
    ALGORITHM,
    PURPOSE,
    validate_envelope,
)

from lab_runtime_canonical_payload import parse_canonical_json
from lab_runtime_evidence_schema import parse_timestamp


REGISTRY_ID = "fbweb-lab-collector-registry-v1"
MAX_KEYS = 128

IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
PUBLIC_KEY_HEX = re.compile(r"[0-9a-f]{64}\Z")

KEY_STATUSES = frozenset({
    "active",
    "disabled",
    "revoked",
})


@dataclass(frozen=True)
class CollectorKeyRecord:
    collector_id: str
    key_id: str
    algorithm: str
    public_key_hex: str
    purpose: str
    vm_id: str
    daemon_id: str
    valid_from: str
    valid_until: str
    status: str


@dataclass(frozen=True)
class CollectorTrustRegistry:
    registry_id: str
    revision: int
    keys: tuple


@dataclass(frozen=True)
class CollectorPolicyAssessment:
    registry_structure_valid: bool
    collector_key_binding_matches: bool
    subject_scope_matches: bool
    key_eligible_for_future_verification: bool
    registry_revision: int
    reason: str

    registry_authenticity_verified: bool = False
    signature_verified: bool = False
    collector_authenticated: bool = False
    freshness_verified: bool = False
    replay_prevention_verified: bool = False
    runtime_evidence_verified: bool = False
    isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _identifier(value, label):
    if (
        type(value) is not str
        or not IDENTIFIER.fullmatch(value)
    ):
        raise ValueError("Invalid " + label)


def validate_registry(registry):
    """Validate every record, including records not being selected.

    A structurally valid registry is not necessarily a trusted
    registry. Trust-source authentication is outside this gate.
    """
    if type(registry) is not CollectorTrustRegistry:
        raise ValueError("CollectorTrustRegistry required")

    if registry.registry_id != REGISTRY_ID:
        raise ValueError("Unexpected trust registry identity")

    if (
        type(registry.revision) is not int
        or registry.revision <= 0
    ):
        raise ValueError("Invalid trust registry revision")

    if (
        type(registry.keys) is not tuple
        or not 1 <= len(registry.keys) <= MAX_KEYS
    ):
        raise ValueError("Invalid trust registry records")

    identities = set()
    key_material = set()

    for record in registry.keys:
        if type(record) is not CollectorKeyRecord:
            raise ValueError("Invalid collector key record")

        for field in (
            "collector_id",
            "key_id",
            "vm_id",
            "daemon_id",
        ):
            _identifier(
                getattr(record, field),
                field,
            )

        if record.algorithm != ALGORITHM:
            raise ValueError("Unsupported key algorithm")

        if record.purpose != PURPOSE:
            raise ValueError("Invalid key purpose")

        if (
            type(record.public_key_hex) is not str
            or not PUBLIC_KEY_HEX.fullmatch(
                record.public_key_hex
            )
            or record.public_key_hex == "0" * 64
        ):
            raise ValueError("Invalid public key representation")

        # This checks representation only. A future cryptographic
        # verifier must validate the key using its approved library.
        if (
            type(record.status) is not str
            or record.status not in KEY_STATUSES
        ):
            raise ValueError("Invalid key lifecycle status")

        beginning = parse_timestamp(record.valid_from)
        ending = parse_timestamp(record.valid_until)

        if beginning >= ending:
            raise ValueError("Invalid key validity interval")

        identity = (record.collector_id, record.key_id)

        if identity in identities:
            raise ValueError("Duplicate collector/key identity")

        # Do not permit the same raw key to represent multiple
        # collector identities, scopes or lifecycle records.
        if record.public_key_hex in key_material:
            raise ValueError("Reused public key material")

        identities.add(identity)
        key_material.add(record.public_key_hex)

    return True


def assess_collector_policy(
    envelope,
    expected,
    registry,
    *,
    now,
):
    """Assess key eligibility without authenticating the collector.

    Both expected and registry must originate from a separately
    controlled verifier. This function cannot prove that origin.
    """
    # Existing envelope checks remain authoritative.
    validate_envelope(
        envelope,
        expected,
        now=now,
    )

    # Reject a malformed registry in its entirety.
    validate_registry(registry)

    matching = tuple(
        record
        for record in registry.keys
        if (
            record.collector_id == expected.collector_id
            and record.key_id == expected.key_id
        )
    )

    if len(matching) != 1:
        raise ValueError("Collector verification key not found")

    record = matching[0]

    if record.status != "active":
        raise ValueError("Collector key is not active")

    if (
        record.vm_id != expected.vm_id
        or record.daemon_id != expected.daemon_id
    ):
        raise ValueError("Collector key subject scope mismatch")

    issued = parse_timestamp(envelope["issued_at"])
    expires = parse_timestamp(envelope["expires_at"])
    collected = parse_timestamp(
        envelope["evidence"]["provenance"]["collected_at"]
    )

    beginning = parse_timestamp(record.valid_from)
    ending = parse_timestamp(record.valid_until)

    # validate_envelope already requires timezone-aware now.
    instant = now.astimezone(timezone.utc)

    if not (
        beginning <= collected
        <= issued
        < expires
        <= ending
    ):
        raise ValueError(
            "Evidence is outside collector key validity"
        )

    if not beginning <= instant < ending:
        raise ValueError(
            "Collector key is not currently valid"
        )

    return CollectorPolicyAssessment(
        registry_structure_valid=True,
        collector_key_binding_matches=True,
        subject_scope_matches=True,
        key_eligible_for_future_verification=True,
        registry_revision=registry.revision,
        reason=(
            "Collector key policy is eligible, but registry "
            "authenticity and Ed25519 signature remain unverified"
        ),
    )


def assess_collector_policy_bytes(
    raw,
    expected,
    registry,
    *,
    now,
):
    """Apply the policy to original canonical envelope JSON bytes.

    Raw input must not be pre-parsed by a duplicate-key-permissive
    JSON parser.
    """
    envelope = parse_canonical_json(raw)

    return assess_collector_policy(
        envelope,
        expected,
        registry,
        now=now,
    )
