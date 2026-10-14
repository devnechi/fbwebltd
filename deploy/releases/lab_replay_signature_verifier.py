#!/usr/bin/env python3
"""Gate 4D.22C.3D.12O: offline, NON-AUTHORIZING replay-response Ed25519.

All keys, key-policy epochs, evidence and timestamps are caller supplied.
A valid signature is NOT independently trusted provenance, freshness, durable
replay prevention, witness advancement, permission or execution approval.
No I/O, state writes, retries, signing keys, networking or Docker.
"""

from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
import base64
import binascii
import hashlib
import json
import re

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from lab_challenge_lifecycle import ReplayLedgerSnapshot, untrusted_ledger_commitment
from lab_collector_trust_policy import REGISTRY_ID
from lab_replay_protected_contract import (
    LEDGER_ID, ReplayProtectedPosition, ReplayWitnessCheckpoint,
    untrusted_position_commitment, validate_replay_position,
)
from lab_registry_wire_format import MAX_SAFE_INTEGER
from lab_runtime_auth_envelope import ALGORITHM
from lab_runtime_evidence_schema import parse_timestamp

ROLES = ("REPLAY_STATE", "REPLAY_WITNESS")
PURPOSES = {
    "REPLAY_STATE": "fbweb-lab-replay-state-response-v1",
    "REPLAY_WITNESS": "fbweb-lab-replay-witness-response-v1",
}
DOMAINS = {
    "REPLAY_STATE": b"FBWEB-LAB-REPLAY-STATE-RESPONSE-SIGNATURE-V1\x00",
    "REPLAY_WITNESS": b"FBWEB-LAB-REPLAY-WITNESS-RESPONSE-SIGNATURE-V1\x00",
}
BODY_DOMAINS = {
    "REPLAY_STATE": b"FBWEB-LAB-REPLAY-STATE-READ-BODY-V1\x00",
    "REPLAY_WITNESS": b"FBWEB-LAB-REPLAY-WITNESS-READ-BODY-V1\x00",
}
POLICY_ID = "fbweb-lab-replay-response-key-policy-v1"
REQUEST_PURPOSE = "REPLAY_READ_POSITION"
STATUS = "POSITION_READ"
PROTOCOL_VERSION = 1
MAX_SIGNED_BYTES = 4096
MAX_KEYS = 32
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
SIGNATURE = re.compile(r"[A-Za-z0-9_-]{86}\Z")


@dataclass(frozen=True)
class ReplayReadChallenge:
    registry_id: str
    ledger_id: str
    request_id: str
    challenge_hex: str
    state_authority_id: str
    witness_authority_id: str
    policy_epoch: int
    recovery_epoch: int
    purpose: str = REQUEST_PURPOSE


@dataclass(frozen=True)
class ReplayStateReadBody:
    ledger: ReplayLedgerSnapshot
    position: ReplayProtectedPosition


@dataclass(frozen=True)
class ReplayReadEvidence:
    role: str
    authority_id: str
    registry_id: str
    ledger_id: str
    request_id: str
    challenge_hex: str
    body_digest: str
    body: object


@dataclass(frozen=True)
class ReplayResponseKey:
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
class ReplayResponseKeyPolicy:
    policy_id: str
    epoch: int
    keys: tuple


@dataclass(frozen=True)
class SignedReplayResponse:
    protocol_version: int
    role: str
    authority_id: str
    key_id: str
    registry_id: str
    ledger_id: str
    request_id: str
    challenge_hex: str
    response_status: str
    body_digest: str
    position_digest: str
    ledger_digest: str
    generation: int
    policy_epoch: int
    recovery_epoch: int
    transition_id: str
    algorithm: str
    purpose: str
    signature: str


@dataclass(frozen=True)
class ReplaySignatureAssessment:
    registry_id: str
    ledger_id: str
    request_id: str
    state_generation: int
    witness_generation: int
    reconciliation_classification: str
    state_signature_verified_under_supplied_key: bool = True
    witness_signature_verified_under_supplied_key: bool = True
    canonical_signed_fields_verified: bool = True
    caller_supplied_key_policy_structurally_valid: bool = True
    independent_authority_identity_authenticated: bool = False
    independent_trust_roots_verified: bool = False
    state_authority_authenticated: bool = False
    witness_authority_authenticated: bool = False
    key_policy_currentness_verified: bool = False
    challenge_randomness_verified: bool = False
    challenge_uniqueness_verified: bool = False
    replay_prevention_verified: bool = False
    trusted_time_verified: bool = False
    protected_state_currentness_verified: bool = False
    durable_state_commit_verified: bool = False
    witness_advancement_verified: bool = False
    independent_rollback_prevention_verified: bool = False
    recovery_approved: bool = False
    runtime_isolation_proven: bool = False
    automatic_retry_permitted: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


def _identifier(value):
    return type(value) is str and IDENTIFIER.fullmatch(value) is not None


def _digest(value):
    return type(value) is str and DIGEST.fullmatch(value) is not None


def _positive(value):
    return type(value) is int and 1 <= value <= MAX_SAFE_INTEGER


def _canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def validate_replay_read_challenge(challenge):
    """Validate supplied labels, not issuance or secure randomness."""
    if type(challenge) is not ReplayReadChallenge or (
        challenge.registry_id != REGISTRY_ID
        or challenge.ledger_id != LEDGER_ID
        or not _identifier(challenge.request_id)
        or not _digest(challenge.challenge_hex)
        or challenge.challenge_hex == "0" * 64
        or not _identifier(challenge.state_authority_id)
        or not _identifier(challenge.witness_authority_id)
        or challenge.state_authority_id == challenge.witness_authority_id
        or not _positive(challenge.policy_epoch)
        or not _positive(challenge.recovery_epoch)
        or challenge.purpose != REQUEST_PURPOSE
    ):
        raise ValueError("Invalid caller-supplied replay read challenge")
    return True


def validate_replay_response_key_policy(policy):
    """Structural validation only: attacker-supplied keys remain untrusted."""
    if (
        type(policy) is not ReplayResponseKeyPolicy
        or policy.policy_id != POLICY_ID
        or not _positive(policy.epoch)
        or type(policy.keys) is not tuple
        or not 1 <= len(policy.keys) <= MAX_KEYS
    ):
        raise ValueError("Invalid caller-supplied replay key policy")
    seen, material = set(), set()
    for key in policy.keys:
        if type(key) is not ReplayResponseKey or (
            key.role not in ROLES
            or not _identifier(key.authority_id)
            or not _identifier(key.key_id)
            or not _digest(key.public_key_hex)
            or key.public_key_hex == "0" * 64
            or key.algorithm != ALGORITHM
            or key.purpose != PURPOSES[key.role]
            or key.status not in ("active", "disabled", "revoked")
            or type(key.valid_from) is not str
            or type(key.valid_until) is not str
        ):
            raise ValueError("Invalid replay verification key")
        if parse_timestamp(key.valid_from) >= parse_timestamp(key.valid_until):
            raise ValueError("Invalid declared key validity interval")
        ident = (key.role, key.authority_id, key.key_id)
        if ident in seen or key.public_key_hex in material:
            raise ValueError("Duplicate replay key identity or cross-role material")
        seen.add(ident)
        material.add(key.public_key_hex)
    return True


def _body_position(role, body):
    if role == "REPLAY_STATE":
        if type(body) is not ReplayStateReadBody:
            raise ValueError("ReplayStateReadBody required")
        from lab_challenge_lifecycle import validate_replay_ledger
        validate_replay_ledger(body.ledger)
        validate_replay_position(body.position)
        if (
            body.ledger.registry_id != body.position.registry_id
            or body.ledger.generation != body.position.generation
            or untrusted_ledger_commitment(body.ledger)
            != body.position.ledger_digest
        ):
            raise ValueError("Replay state ledger/position commitment mismatch")
        return body.position
    if role == "REPLAY_WITNESS":
        if type(body) is not ReplayWitnessCheckpoint:
            raise ValueError("ReplayWitnessCheckpoint required")
        validate_replay_position(body.position)
        return body.position
    raise ValueError("Unsupported replay role")


def untrusted_replay_body_commitment(role, body):
    """Bind canonical body bytes; no source authentication is implied."""
    _body_position(role, body)
    return hashlib.sha256(
        BODY_DOMAINS[role] + _canonical({"role": role, "body": asdict(body)})
    ).hexdigest()


def _signature_bytes(signature):
    if type(signature) is not str or SIGNATURE.fullmatch(signature) is None:
        raise ValueError("Invalid canonical replay signature encoding")
    try:
        raw = base64.b64decode(signature + "==", altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid replay signature encoding") from exc
    if (
        len(raw) != 64
        or base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=") != signature
    ):
        raise ValueError("Noncanonical replay signature")
    return raw


def _validate_header(record):
    if type(record) is not SignedReplayResponse:
        raise ValueError("SignedReplayResponse required")
    if (
        type(record.protocol_version) is not int
        or record.protocol_version != PROTOCOL_VERSION
        or record.role not in ROLES
        or not _identifier(record.authority_id)
        or not _identifier(record.key_id)
        or record.registry_id != REGISTRY_ID
        or record.ledger_id != LEDGER_ID
        or not _identifier(record.request_id)
        or not _digest(record.challenge_hex)
        or record.challenge_hex == "0" * 64
        or record.response_status != STATUS
        or not _digest(record.body_digest)
        or not _digest(record.position_digest)
        or not _digest(record.ledger_digest)
        or type(record.generation) is not int
        or not 0 <= record.generation <= MAX_SAFE_INTEGER
        or not _positive(record.policy_epoch)
        or not _positive(record.recovery_epoch)
        or not _identifier(record.transition_id)
        or record.algorithm != ALGORITHM
        or record.purpose != PURPOSES[record.role]
    ):
        raise ValueError("Invalid signed replay response header")
    return True


def replay_response_signing_bytes(record):
    """Canonical, role-specific message excluding only the signature field."""
    _validate_header(record)
    unsigned = {k: v for k, v in asdict(record).items() if k != "signature"}
    message = DOMAINS[record.role] + _canonical(unsigned)
    if len(message) > MAX_SIGNED_BYTES:
        raise ValueError("Replay signing message exceeds bound")
    return message


def canonical_signed_replay_bytes(record):
    replay_response_signing_bytes(record)
    _signature_bytes(record.signature)
    raw = _canonical(asdict(record))
    if len(raw) > MAX_SIGNED_BYTES:
        raise ValueError("Signed replay response exceeds bound")
    return raw


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate replay JSON field")
        result[key] = value
    return result


def _invalid_number(_value):
    raise ValueError("Invalid replay JSON numeric value")


def parse_signed_replay_bytes(raw):
    """Reject duplicate, unknown, missing, noncanonical or unbounded fields."""
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_SIGNED_BYTES:
        raise ValueError("Bounded signed replay bytes required")
    try:
        decoded = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=_unique_pairs,
            parse_float=_invalid_number,
            parse_constant=_invalid_number,
        )
        if type(decoded) is not dict or set(decoded) != {
            f.name for f in fields(SignedReplayResponse)
        }:
            raise ValueError("Unexpected signed replay fields")
        record = SignedReplayResponse(**decoded)
        if canonical_signed_replay_bytes(record) != raw:
            raise ValueError("Noncanonical signed replay bytes")
        return record
    except (UnicodeError, json.JSONDecodeError, RecursionError, TypeError) as exc:
        raise ValueError("Invalid replay signed JSON") from exc


def _check_evidence(challenge, evidence, role):
    if type(evidence) is not ReplayReadEvidence or evidence.role != role:
        raise ValueError("Wrong replay evidence role")
    expected_id = (
        challenge.state_authority_id if role == "REPLAY_STATE"
        else challenge.witness_authority_id
    )
    if (
        evidence.authority_id != expected_id
        or evidence.registry_id != challenge.registry_id
        or evidence.ledger_id != challenge.ledger_id
        or evidence.request_id != challenge.request_id
        or evidence.challenge_hex != challenge.challenge_hex
    ):
        raise ValueError("Replay evidence/request mismatch")
    position = _body_position(role, evidence.body)
    if (
        position.policy_epoch != challenge.policy_epoch
        or position.recovery_epoch != challenge.recovery_epoch
        or evidence.body_digest != untrusted_replay_body_commitment(role, evidence.body)
    ):
        raise ValueError("Replay evidence epoch or body commitment mismatch")
    return position


def _verify_one(challenge, evidence, record, role, policy, instant):
    position = _check_evidence(challenge, evidence, role)
    _validate_header(record)
    if (
        record.role != role
        or record.authority_id != evidence.authority_id
        or record.registry_id != challenge.registry_id
        or record.ledger_id != challenge.ledger_id
        or record.request_id != challenge.request_id
        or record.challenge_hex != challenge.challenge_hex
        or record.body_digest != evidence.body_digest
        or record.position_digest != untrusted_position_commitment(position)
        or record.ledger_digest != position.ledger_digest
        or record.generation != position.generation
        or record.policy_epoch != position.policy_epoch
        or record.recovery_epoch != position.recovery_epoch
        or record.transition_id != position.transition_id
    ):
        raise ValueError("Signed replay response/body binding mismatch")
    keys = [
        k for k in policy.keys if (
            k.role == role
            and k.authority_id == record.authority_id
            and k.key_id == record.key_id
        )
    ]
    if len(keys) != 1 or keys[0].status != "active":
        raise ValueError("Missing or inactive replay signing key")
    key = keys[0]
    if not parse_timestamp(key.valid_from) <= instant < parse_timestamp(key.valid_until):
        raise ValueError("Replay response outside supplied key validity interval")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(key.public_key_hex)).verify(
            _signature_bytes(record.signature), replay_response_signing_bytes(record)
        )
    except (InvalidSignature, UnsupportedAlgorithm, ValueError, TypeError) as exc:
        raise ValueError("Invalid replay authority Ed25519 signature") from exc
    return position


def verify_replay_read_signatures(
    challenge, state_evidence, witness_evidence,
    state_signed, witness_signed, policy, *, now
):
    """Verify two responses under supplied keys and time; NEVER authorize."""
    validate_replay_read_challenge(challenge)
    validate_replay_response_key_policy(policy)
    if policy.epoch != challenge.policy_epoch:
        raise ValueError("Supplied replay key policy epoch mismatch")
    if (
        type(now) is not datetime
        or now.tzinfo is None
        or now.utcoffset() is None
    ):
        raise ValueError("Timezone-aware supplied assessment time required")
    instant = now.astimezone(timezone.utc)
    state = _verify_one(
        challenge, state_evidence, state_signed, "REPLAY_STATE", policy, instant
    )
    witness = _verify_one(
        challenge, witness_evidence, witness_signed,
        "REPLAY_WITNESS", policy, instant
    )
    if state == witness:
        classification = "MATCHING_UNTRUSTED"
    elif state.generation > witness.generation:
        classification = "REPLAY_STATE_AHEAD_UNTRUSTED"
    elif witness.generation > state.generation:
        classification = "REPLAY_WITNESS_AHEAD_UNTRUSTED"
    else:
        classification = "CONFLICTING_UNTRUSTED"
    return ReplaySignatureAssessment(
        registry_id=challenge.registry_id,
        ledger_id=challenge.ledger_id,
        request_id=challenge.request_id,
        state_generation=state.generation,
        witness_generation=witness.generation,
        reconciliation_classification=classification,
    )
