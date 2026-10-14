#!/usr/bin/env python3
"""Gate 4D.22C.3D.12S: offline NON-AUTHORIZING issuer signatures.

Every key, approver label, policy, clock and expected issuer is caller supplied.
No independently authenticated root, approval, currentness, durable commit,
protected witness, execution, I/O, networking, signing or retries.
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

from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER
from lab_replay_protected_contract import LEDGER_ID
from lab_replay_policy_continuity import (
    ReplayPolicySnapshot, untrusted_replay_policy_commitment,
    validate_replay_policy_snapshot,
)
from lab_replay_signature_verifier import POLICY_ID as REPLAY_KEY_POLICY_ID
from lab_runtime_auth_envelope import ALGORITHM
from lab_runtime_evidence_schema import parse_timestamp

ISSUER_KEY_POLICY_ID = "fbweb-lab-replay-policy-issuer-keys-v1"
ISSUER_PURPOSE = "fbweb-lab-replay-policy-issuer-approval-v1"
ISSUER_DOMAIN = b"FBWEB-LAB-REPLAY-POLICY-ISSUER-SIGNATURE-V1\x00"
APPROVAL_DOMAIN = b"FBWEB-LAB-REPLAY-POLICY-APPROVAL-DECLARATION-V1\x00"
FORMAT_VERSION = 1
MAX_SIGNED_BYTES = 4096
MAX_ISSUER_KEYS = 16
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
SIGNATURE = re.compile(r"[A-Za-z0-9_-]{86}\Z")
DECISIONS = ("BOOTSTRAP_DECLARATION", "ROTATION_DECLARATION")


@dataclass(frozen=True)
class ReplayPolicyIssuerKey:
    issuer_id: str
    key_id: str
    public_key_hex: str
    algorithm: str
    purpose: str
    status: str
    valid_from: str
    valid_until: str


@dataclass(frozen=True)
class ReplayPolicyIssuerKeyPolicy:
    policy_id: str
    keys: tuple


@dataclass(frozen=True)
class ReplayPolicyApprovalDeclaration:
    registry_id: str
    ledger_id: str
    policy_id: str
    issuer_id: str
    approval_reference: str
    transition_id: str
    previous_commitment: str
    proposed_commitment: str
    epoch: int
    generation: int
    recovery_epoch: int
    decision: str
    approver_ids: tuple


@dataclass(frozen=True)
class SignedReplayPolicyEnvelope:
    format_version: int
    issuer_id: str
    key_id: str
    registry_id: str
    ledger_id: str
    policy_id: str
    epoch: int
    generation: int
    recovery_epoch: int
    previous_commitment: str
    transition_id: str
    approval_reference: str
    policy_commitment: str
    approval_commitment: str
    algorithm: str
    purpose: str
    signature: str


@dataclass(frozen=True)
class ReplayPolicyIssuerSignatureAssessment:
    registry_id: str
    ledger_id: str
    policy_id: str
    issuer_id: str
    epoch: int
    generation: int
    policy_commitment: str
    approval_commitment: str
    issuer_signature_verified_under_supplied_key: bool = True
    policy_bytes_logically_bound: bool = True
    approval_declaration_logically_bound: bool = True
    caller_supplied_issuer_key_policy_structurally_valid: bool = True
    independent_issuer_authenticated: bool = False
    independent_root_provenance_verified: bool = False
    issuer_policy_currentness_verified: bool = False
    independent_approver_identity_verified: bool = False
    independent_policy_approval_verified: bool = False
    protected_policy_currentness_verified: bool = False
    independent_policy_witness_verified: bool = False
    durable_policy_commit_verified: bool = False
    trusted_time_verified: bool = False
    replay_prevention_verified: bool = False
    recovery_approved: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    automatic_retry_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


def _identifier(value):
    return type(value) is str and IDENTIFIER.fullmatch(value) is not None


def _digest(value):
    return type(value) is str and DIGEST.fullmatch(value) is not None


def _positive(value):
    return type(value) is int and 1 <= value <= MAX_SAFE_INTEGER


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def validate_issuer_key_policy(policy):
    """Check caller-supplied declarations, not independent root approval."""
    if (type(policy) is not ReplayPolicyIssuerKeyPolicy
            or policy.policy_id != ISSUER_KEY_POLICY_ID
            or type(policy.keys) is not tuple
            or not 1 <= len(policy.keys) <= MAX_ISSUER_KEYS):
        raise ValueError("Invalid supplied replay issuer key policy")
    seen, material = set(), set()
    for key in policy.keys:
        if (type(key) is not ReplayPolicyIssuerKey
                or not _identifier(key.issuer_id)
                or not _identifier(key.key_id)
                or not _digest(key.public_key_hex)
                or key.public_key_hex == "0" * 64
                or key.algorithm != ALGORITHM
                or key.purpose != ISSUER_PURPOSE
                or key.status not in ("active", "disabled", "revoked")
                or type(key.valid_from) is not str
                or type(key.valid_until) is not str):
            raise ValueError("Invalid replay issuer key record")
        if parse_timestamp(key.valid_from) >= parse_timestamp(key.valid_until):
            raise ValueError("Invalid declared issuer key validity")
        identity = (key.issuer_id, key.key_id)
        if identity in seen or key.public_key_hex in material:
            raise ValueError("Reused issuer key identity or public material")
        seen.add(identity)
        material.add(key.public_key_hex)
    if tuple((k.issuer_id, k.key_id) for k in policy.keys) != tuple(sorted(seen)):
        raise ValueError("Noncanonical issuer key policy order")
    return True


def validate_approval_declaration(approval, snapshot):
    """Require exact declared binding, not genuine administrative approval."""
    validate_replay_policy_snapshot(snapshot)
    if type(approval) is not ReplayPolicyApprovalDeclaration:
        raise ValueError("ReplayPolicyApprovalDeclaration required")
    if (approval.registry_id != snapshot.registry_id
            or approval.ledger_id != snapshot.ledger_id
            or approval.policy_id != REPLAY_KEY_POLICY_ID
            or approval.issuer_id != snapshot.issuer_id
            or approval.approval_reference != snapshot.approval_reference
            or approval.transition_id != snapshot.transition_id
            or approval.previous_commitment != snapshot.previous_commitment
            or approval.proposed_commitment != untrusted_replay_policy_commitment(snapshot)
            or type(approval.epoch) is not int or approval.epoch != snapshot.epoch
            or type(approval.generation) is not int
            or approval.generation != snapshot.generation
            or type(approval.recovery_epoch) is not int
            or approval.recovery_epoch != snapshot.recovery_epoch
            or approval.decision != ("BOOTSTRAP_DECLARATION" if snapshot.epoch == 1
                                     else "ROTATION_DECLARATION")
            or type(approval.approver_ids) is not tuple
            or not 2 <= len(approval.approver_ids) <= 4
            or not all(_identifier(a) for a in approval.approver_ids)
            or len(set(approval.approver_ids)) != len(approval.approver_ids)
            or tuple(sorted(approval.approver_ids)) != approval.approver_ids
            or any(a in (snapshot.issuer_id,
                          snapshot.roles.replay_state_authority_id,
                          snapshot.roles.replay_witness_authority_id)
                   for a in approval.approver_ids)):
        raise ValueError("Invalid caller-supplied approval declaration")
    return True


def untrusted_approval_commitment(approval, snapshot):
    validate_approval_declaration(approval, snapshot)
    return hashlib.sha256(APPROVAL_DOMAIN + _canonical(asdict(approval))).hexdigest()


def _validate_header(record):
    if type(record) is not SignedReplayPolicyEnvelope:
        raise ValueError("SignedReplayPolicyEnvelope required")
    if (type(record.format_version) is not int
            or record.format_version != FORMAT_VERSION
            or not _identifier(record.issuer_id)
            or not _identifier(record.key_id)
            or record.registry_id != REGISTRY_ID
            or record.ledger_id != LEDGER_ID
            or record.policy_id != REPLAY_KEY_POLICY_ID
            or not _positive(record.epoch)
            or not _positive(record.generation)
            or not _positive(record.recovery_epoch)
            or not _digest(record.previous_commitment)
            or not _identifier(record.transition_id)
            or not _identifier(record.approval_reference)
            or not _digest(record.policy_commitment)
            or not _digest(record.approval_commitment)
            or record.algorithm != ALGORITHM
            or record.purpose != ISSUER_PURPOSE):
        raise ValueError("Invalid issuer signed envelope")
    return True


def issuer_signing_bytes(record):
    """Versioned domain and canonical fields; not an authorization token."""
    _validate_header(record)
    payload = {name: value for name, value in asdict(record).items()
               if name != "signature"}
    message = ISSUER_DOMAIN + _canonical(payload)
    if len(message) > MAX_SIGNED_BYTES:
        raise ValueError("Oversized issuer signing message")
    return message


def _signature_bytes(value):
    if type(value) is not str or SIGNATURE.fullmatch(value) is None:
        raise ValueError("Invalid issuer signature encoding")
    try:
        decoded = base64.b64decode(value + "==", altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid issuer signature encoding") from exc
    if len(decoded) != 64 or base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=") != value:
        raise ValueError("Noncanonical issuer signature encoding")
    return decoded


def canonical_signed_issuer_bytes(record):
    issuer_signing_bytes(record)
    _signature_bytes(record.signature)
    raw = _canonical(asdict(record))
    if len(raw) > MAX_SIGNED_BYTES:
        raise ValueError("Oversized signed issuer message")
    return raw


def _unique_pairs(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError("Duplicate issuer JSON key")
        result[name] = value
    return result


def _invalid_number(_value):
    raise ValueError("Unsupported issuer JSON numeric form")


def parse_signed_issuer_bytes(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_SIGNED_BYTES:
        raise ValueError("Bounded signed issuer bytes required")
    try:
        obj = json.loads(raw.decode("utf-8", "strict"),
                         object_pairs_hook=_unique_pairs,
                         parse_float=_invalid_number, parse_constant=_invalid_number)
        if type(obj) is not dict or set(obj) != {f.name for f in fields(SignedReplayPolicyEnvelope)}:
            raise ValueError("Unexpected issuer signed fields")
        record = SignedReplayPolicyEnvelope(**obj)
        if canonical_signed_issuer_bytes(record) != raw:
            raise ValueError("Noncanonical issuer signed bytes")
        return record
    except (UnicodeError, json.JSONDecodeError, RecursionError, TypeError) as exc:
        raise ValueError("Invalid issuer JSON") from exc


def verify_replay_policy_issuer_signature(
    snapshot, approval, signed, issuer_key_policy, *, expected_issuer_id, now
):
    """Verify issuer Ed25519 ONLY under supplied key/clock/identity."""
    validate_issuer_key_policy(issuer_key_policy)
    validate_approval_declaration(approval, snapshot)
    _validate_header(signed)
    if not _identifier(expected_issuer_id) or expected_issuer_id != snapshot.issuer_id:
        raise ValueError("Supplied expected issuer and policy disagree")
    commitment = untrusted_replay_policy_commitment(snapshot)
    approval_digest = untrusted_approval_commitment(approval, snapshot)
    if (signed.issuer_id != snapshot.issuer_id
            or signed.registry_id != snapshot.registry_id
            or signed.ledger_id != snapshot.ledger_id
            or signed.policy_id != snapshot.policy_id
            or signed.epoch != snapshot.epoch
            or signed.generation != snapshot.generation
            or signed.recovery_epoch != snapshot.recovery_epoch
            or signed.previous_commitment != snapshot.previous_commitment
            or signed.transition_id != snapshot.transition_id
            or signed.approval_reference != snapshot.approval_reference
            or signed.policy_commitment != commitment
            or signed.approval_commitment != approval_digest):
        raise ValueError("Policy issuer envelope does not bind exact declarations")
    if (type(now) is not datetime or now.tzinfo is None
            or now.utcoffset() is None):
        raise ValueError("Timezone-aware caller-supplied assessment time required")
    instant = now.astimezone(timezone.utc)
    matching = [k for k in issuer_key_policy.keys
                if k.issuer_id == signed.issuer_id and k.key_id == signed.key_id]
    if len(matching) != 1 or matching[0].status != "active":
        raise ValueError("Unknown or inactive caller-supplied issuer key")
    key = matching[0]
    if not parse_timestamp(key.valid_from) <= instant < parse_timestamp(key.valid_until):
        raise ValueError("Issuer key outside supplied validity window")
    if key.public_key_hex in {k.public_key_hex for k in snapshot.key_policy.keys}:
        raise ValueError("Issuer and replay response signing material reused")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(key.public_key_hex)).verify(
            _signature_bytes(signed.signature), issuer_signing_bytes(signed))
    except (InvalidSignature, UnsupportedAlgorithm, ValueError, TypeError) as exc:
        raise ValueError("Invalid replay policy issuer Ed25519 signature") from exc
    return ReplayPolicyIssuerSignatureAssessment(
        registry_id=snapshot.registry_id, ledger_id=snapshot.ledger_id,
        policy_id=snapshot.policy_id, issuer_id=snapshot.issuer_id,
        epoch=snapshot.epoch, generation=snapshot.generation,
        policy_commitment=commitment, approval_commitment=approval_digest,
    )
