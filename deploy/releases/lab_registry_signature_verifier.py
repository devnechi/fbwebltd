#!/usr/bin/env python3
"""Gate 4D.22C.3D.11B: offline administrative registry signatures.

The administrative public-key policy is an UNAUTHENTICATED caller input.
A valid Ed25519 signature establishes no independent provenance, current
revision, trusted time, revocation delivery, isolation or authorization.
No file access, network, Docker, subprocess or private signing keys.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import re

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from lab_runtime_auth_envelope import ALGORITHM
from lab_runtime_evidence_schema import parse_timestamp
from lab_registry_wire_format import (
    REGISTRY_PURPOSE,
    _valid_signature_encoding,
    parse_signed_registry_bytes,
    registry_signing_bytes,
    validate_registry_wire,
)

ADMIN_POLICY_ID = "fbweb-lab-registry-admin-policy-v1"
MAX_ADMINISTRATORS = 16
KEY_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
PUBLIC_KEY_HEX = re.compile(r"[0-9a-f]{64}\Z")
ADMIN_STATES = frozenset({"active", "disabled", "revoked"})


@dataclass(frozen=True)
class AdministrativeKeyRecord:
    key_id: str
    public_key_hex: str
    algorithm: str
    purpose: str
    valid_from: str
    valid_until: str
    status: str


@dataclass(frozen=True)
class AdministrativeKeyPolicy:
    policy_id: str
    keys: tuple


@dataclass(frozen=True)
class RegistrySignatureAssessment:
    registry_structure_valid: bool
    registry_signature_verified: bool
    administrative_key_policy_eligible: bool
    registry_revision: int
    registry_signing_digest: str
    declared_window_matches: bool
    registry_declaration: object
    registry_provenance_authenticated: bool = False
    administrative_identity_authenticated: bool = False
    trusted_time_source_verified: bool = False
    registry_revision_current: bool = False
    registry_freshness_verified: bool = False
    rollback_prevention_verified: bool = False
    collector_authenticated: bool = False
    evidence_signature_verified: bool = False
    replay_prevention_verified: bool = False
    runtime_evidence_verified: bool = False
    isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def validate_administrative_policy(policy):
    """Validate declared admin keys, without trusting their provenance."""
    if type(policy) is not AdministrativeKeyPolicy or policy.policy_id != ADMIN_POLICY_ID:
        raise ValueError("Invalid administrative trust-policy identity")
    if type(policy.keys) is not tuple or not 1 <= len(policy.keys) <= MAX_ADMINISTRATORS:
        raise ValueError("Invalid administrative trust-policy keys")
    key_ids, key_bytes = set(), set()
    for key in policy.keys:
        if type(key) is not AdministrativeKeyRecord:
            raise ValueError("Invalid administrative key record")
        if type(key.key_id) is not str or not KEY_ID.fullmatch(key.key_id):
            raise ValueError("Invalid administrative key identifier")
        if (type(key.public_key_hex) is not str
                or not PUBLIC_KEY_HEX.fullmatch(key.public_key_hex)
                or key.public_key_hex == "0" * 64):
            raise ValueError("Invalid administrative public key")
        if key.algorithm != ALGORITHM or key.purpose != REGISTRY_PURPOSE:
            raise ValueError("Invalid administrative algorithm or purpose")
        if type(key.status) is not str or key.status not in ADMIN_STATES:
            raise ValueError("Invalid administrative key status")
        if parse_timestamp(key.valid_from) >= parse_timestamp(key.valid_until):
            raise ValueError("Invalid administrative key validity")
        if key.key_id in key_ids or key.public_key_hex in key_bytes:
            raise ValueError("Duplicate administrative identifier or key material")
        key_ids.add(key.key_id)
        key_bytes.add(key.public_key_hex)
    return True


def verify_registry_signature_bytes(raw, administrators, *, now):
    """Verify registry bytes under caller-supplied administrator key policy.

    This function must not be used as a standalone registry trust or
    anti-rollback gate. No persistent state is consulted or updated.
    """
    document = parse_signed_registry_bytes(raw)
    registry = validate_registry_wire(document)
    validate_administrative_policy(administrators)

    if (not isinstance(now, datetime) or now.tzinfo is None
            or now.utcoffset() is None):
        raise ValueError("Verifier-supplied timezone-aware time required")
    instant = now.astimezone(timezone.utc)
    issued = parse_timestamp(document["issued_at"])
    expires = parse_timestamp(document["expires_at"])
    if not issued <= instant < expires:
        raise ValueError("Registry outside declared assessment window")

    matches = tuple(
        key for key in administrators.keys
        if key.key_id == document["issuer_key_id"]
    )
    if len(matches) != 1:
        raise ValueError("Unknown administrative issuer key")
    admin_key = matches[0]
    if admin_key.status != "active":
        raise ValueError("Administrative signing key not active")
    start = parse_timestamp(admin_key.valid_from)
    end = parse_timestamp(admin_key.valid_until)
    if not (start <= issued < expires <= end and start <= instant < end):
        raise ValueError("Registry outside administrative key validity")

    # Prevent the same key material being both an administrator and
    # an evidence collector in this offline policy assessment.
    if admin_key.public_key_hex in {key.public_key_hex for key in registry.keys}:
        raise ValueError("Administrative/collector signing key role overlap")

    message = registry_signing_bytes(document)
    signature = _valid_signature_encoding(document["signature"])
    try:
        public_key = Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(admin_key.public_key_hex)
        )
        public_key.verify(signature, message)
    except (InvalidSignature, UnsupportedAlgorithm, ValueError, TypeError) as exc:
        raise ValueError("Invalid administrative registry signature") from exc

    return RegistrySignatureAssessment(
        registry_structure_valid=True,
        registry_signature_verified=True,
        administrative_key_policy_eligible=True,
        registry_revision=registry.revision,
        registry_signing_digest=hashlib.sha256(message).hexdigest(),
        declared_window_matches=True,
        registry_declaration=registry,
    )
