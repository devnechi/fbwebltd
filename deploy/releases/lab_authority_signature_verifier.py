#!/usr/bin/env python3
"""Gate 4D.22C.3D.12H: offline Ed25519 authority-response verification.

A valid signature proves integrity under a CALLER-SUPPLIED public key, not
independent authority provenance, freshness, replay resistance or acceptance.
No private keys, network, filesystem access, commits, Docker or deployment.
"""

from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
import base64
import binascii
import json
import re

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from lab_authority_evidence_contract import (
    AuthorityReadEvidence,
    assess_authority_evidence,
)
from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER
from lab_runtime_auth_envelope import ALGORITHM
from lab_runtime_evidence_schema import parse_timestamp

POLICY_ID = "fbweb-lab-authority-response-key-policy-v1"
PURPOSES = {
    "STATE": "fbweb-lab-state-authority-response-v1",
    "WITNESS": "fbweb-lab-witness-authority-response-v1",
    "ADMIN": "fbweb-lab-admin-authority-response-v1",
}
DOMAINS = {
    role: ("FBWEB-LAB-" + role + "-RESPONSE-SIGNATURE-V1\x00").encode("ascii")
    for role in PURPOSES
}
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
SIGNATURE = re.compile(r"[A-Za-z0-9_-]{86}\Z")
MAX_SIGNED_BYTES = 4096
MAX_AUTHORITY_KEYS = 32


@dataclass(frozen=True)
class AuthorityResponseKey:
    role: str
    authority_id: str
    key_id: str
    public_key_hex: str
    algorithm: str
    purpose: str
    status: str
    valid_from: str
    valid_until: str


@dataclass(frozen=True)
class AuthorityResponseKeyPolicy:
    policy_id: str
    keys: tuple


@dataclass(frozen=True)
class SignedAuthorityResponse:
    role: str
    authority_id: str
    key_id: str
    registry_id: str
    request_id: str
    challenge_hex: str
    body_digest: str
    envelope_digest: str
    policy_epoch: int
    algorithm: str
    purpose: str
    signature: str


@dataclass(frozen=True)
class AuthoritySignatureAssessment:
    registry_id: str
    request_id: str
    revision: int
    generation: int
    state_signature_verified_under_supplied_key: bool = True
    witness_signature_verified_under_supplied_key: bool = True
    admin_signature_verified_under_supplied_key: bool = True
    canonical_signed_fields_verified: bool = True
    caller_supplied_key_policy_structurally_valid: bool = True
    independent_authority_identity_authenticated: bool = False
    administrative_policy_authenticated: bool = False
    state_authority_authenticated: bool = False
    rollback_witness_authenticated: bool = False
    independently_trusted_key_provenance_verified: bool = False
    trusted_time_verified: bool = False
    challenge_uniqueness_verified: bool = False
    replay_prevention_verified: bool = False
    authoritative_currentness_verified: bool = False
    protected_state_commit_verified: bool = False
    rollback_prevention_verified: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _identifier(value):
    return type(value) is str and IDENTIFIER.fullmatch(value) is not None


def _digest(value):
    return type(value) is str and DIGEST.fullmatch(value) is not None


def _canonical(obj):
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def validate_authority_response_key_policy(policy):
    """Check declaration shape; do NOT authenticate the supplied policy."""
    if type(policy) is not AuthorityResponseKeyPolicy or policy.policy_id != POLICY_ID:
        raise ValueError("Invalid authority-response key policy")
    if type(policy.keys) is not tuple or not 1 <= len(policy.keys) <= MAX_AUTHORITY_KEYS:
        raise ValueError("Invalid authority-response key count")
    seen_ids, seen_material = set(), set()
    for key in policy.keys:
        if type(key) is not AuthorityResponseKey:
            raise ValueError("Invalid authority-response key record")
        if (type(key.role) is not str or key.role not in PURPOSES
                or not _identifier(key.authority_id)
                or not _identifier(key.key_id)):
            raise ValueError("Invalid authority key role or identity")
        if (not _digest(key.public_key_hex) or key.public_key_hex == "0" * 64
                or key.algorithm != ALGORITHM or key.purpose != PURPOSES[key.role]
                or type(key.status) is not str
                or key.status not in ("active", "disabled", "revoked")):
            raise ValueError("Invalid authority key material or lifecycle")
        if parse_timestamp(key.valid_from) >= parse_timestamp(key.valid_until):
            raise ValueError("Invalid authority key validity interval")
        ident = (key.role, key.authority_id, key.key_id)
        if ident in seen_ids or key.public_key_hex in seen_material:
            raise ValueError("Duplicate signer identity or cross-role key material")
        seen_ids.add(ident)
        seen_material.add(key.public_key_hex)
    return True


def _validate_header(record):
    if type(record) is not SignedAuthorityResponse:
        raise ValueError("SignedAuthorityResponse required")
    if (type(record.role) is not str or record.role not in PURPOSES
            or not _identifier(record.authority_id)
            or not _identifier(record.key_id)
            or type(record.registry_id) is not str or record.registry_id != REGISTRY_ID
            or not _identifier(record.request_id)
            or not _digest(record.challenge_hex) or record.challenge_hex == "0" * 64
            or not _digest(record.body_digest)
            or not _digest(record.envelope_digest)
            or type(record.policy_epoch) is not int
            or not 1 <= record.policy_epoch <= MAX_SAFE_INTEGER
            or type(record.algorithm) is not str or record.algorithm != ALGORITHM
            or type(record.purpose) is not str
            or record.purpose != PURPOSES[record.role]):
        raise ValueError("Invalid signed authority response fields")
    return True


def authority_response_signing_bytes(record):
    """One canonical, role-separated signing message; no signature included."""
    _validate_header(record)
    unsigned = {
        name: value for name, value in asdict(record).items()
        if name != "signature"
    }
    message = DOMAINS[record.role] + _canonical(unsigned)
    if len(message) > MAX_SIGNED_BYTES:
        raise ValueError("Authority signing message exceeds limit")
    return message


def _signature_bytes(signature):
    if type(signature) is not str or SIGNATURE.fullmatch(signature) is None:
        raise ValueError("Invalid authority signature encoding")
    try:
        raw = base64.b64decode(
            signature + "==", altchars=b"-_", validate=True
        )
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid authority signature encoding") from exc
    if (
        len(raw) != 64
        or base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=") != signature
    ):
        raise ValueError("Noncanonical authority signature")
    return raw


def canonical_signed_authority_bytes(record):
    """Strict canonical JSON wrapper; a wire format, NOT trust evidence."""
    authority_response_signing_bytes(record)
    _signature_bytes(record.signature)
    encoded = _canonical(asdict(record))
    if len(encoded) > MAX_SIGNED_BYTES:
        raise ValueError("Signed authority response exceeds limit")
    return encoded


def _unique_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("Duplicate authority response JSON key")
        out[key] = value
    return out


def _invalid_numeric(_value):
    raise ValueError("Unsupported authority response JSON number")


def parse_signed_authority_bytes(raw):
    """Reject duplicate fields, unknown fields and noncanonical wire bytes."""
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_SIGNED_BYTES:
        raise ValueError("Bounded signed authority bytes required")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=_unique_keys,
            parse_float=_invalid_numeric,
            parse_constant=_invalid_numeric,
        )
        if (
            type(value) is not dict
            or set(value) != {f.name for f in fields(SignedAuthorityResponse)}
        ):
            raise ValueError("Unexpected signed authority fields")
        record = SignedAuthorityResponse(**value)
        if canonical_signed_authority_bytes(record) != raw:
            raise ValueError("Noncanonical authority response bytes")
        return record
    except (
        UnicodeError, json.JSONDecodeError, RecursionError, TypeError
    ) as exc:
        raise ValueError("Invalid signed authority response JSON") from exc


def _verify_one(record, evidence, role, challenge, policy, epoch, now):
    if type(evidence) is not AuthorityReadEvidence:
        raise ValueError("AuthorityReadEvidence required")
    _validate_header(record)
    _signature_bytes(record.signature)

    expected_authority = {
        "STATE": challenge.state_authority_id,
        "WITNESS": challenge.witness_authority_id,
        "ADMIN": challenge.admin_authority_id,
    }[role]

    if (
        record.role != role
        or record.authority_id != expected_authority
        or record.authority_id != evidence.authority_id
        or record.registry_id != challenge.registry_id
        or record.request_id != challenge.request_id
        or record.challenge_hex != challenge.challenge_hex
        or record.body_digest != evidence.body_digest
        or record.envelope_digest != evidence.envelope_digest
        or record.policy_epoch != epoch
    ):
        raise ValueError("Signed header and response evidence disagree")

    matches = tuple(
        key for key in policy.keys
        if key.role == role
        and key.authority_id == record.authority_id
        and key.key_id == record.key_id
    )
    if len(matches) != 1:
        raise ValueError("Signing key not found in supplied policy")

    key = matches[0]
    if key.status != "active":
        raise ValueError("Authority signing key not active")
    if not parse_timestamp(key.valid_from) <= now < parse_timestamp(key.valid_until):
        raise ValueError("Authority response outside declared key window")

    try:
        Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(key.public_key_hex)
        ).verify(
            _signature_bytes(record.signature),
            authority_response_signing_bytes(record),
        )
    except (
        InvalidSignature, UnsupportedAlgorithm, ValueError, TypeError
    ) as exc:
        raise ValueError("Invalid authority response Ed25519 signature") from exc


def verify_authority_response_signatures(
    challenge,
    state_evidence,
    witness_evidence,
    admin_evidence,
    state_signed,
    witness_signed,
    admin_signed,
    policy,
    *,
    now,
):
    """Verify three signatures only under CALLER-SUPPLIED keys and time."""
    logical = assess_authority_evidence(
        challenge, state_evidence, witness_evidence, admin_evidence
    )
    validate_authority_response_key_policy(policy)

    if (
        type(now) is not datetime
        or now.tzinfo is None
        or now.utcoffset() is None
    ):
        raise ValueError(
            "Timezone-aware caller-supplied assessment time required"
        )

    instant = now.astimezone(timezone.utc)

    for role, evidence, signed in (
        ("STATE", state_evidence, state_signed),
        ("WITNESS", witness_evidence, witness_signed),
        ("ADMIN", admin_evidence, admin_signed),
    ):
        _verify_one(
            signed, evidence, role, challenge,
            policy, logical.policy_epoch, instant,
        )

    return AuthoritySignatureAssessment(
        registry_id=logical.registry_id,
        request_id=logical.request_id,
        revision=logical.revision,
        generation=logical.generation,
    )
