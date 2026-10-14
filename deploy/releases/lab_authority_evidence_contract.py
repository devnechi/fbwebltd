#!/usr/bin/env python3
"""Gate 4D.22C.3D.12F: pure UNAUTHENTICATED authority evidence contracts.

Caller-provided identity labels, challenge and digests prove no independent
identity, origin, freshness, replay resistance, state commit or permission.
No network, filesystem, credentials, signing, storage, Docker or execution.
"""

from dataclasses import asdict, dataclass
import hashlib
import json
import re

from lab_collector_trust_policy import REGISTRY_ID
from lab_protected_state_contract import (
    ProtectedPosition,
    WitnessCheckpoint,
    revocation_commitment,
    validate_position,
)
from lab_registry_revision_continuity import RevisionStateSnapshot
from lab_registry_revocation_continuity import (
    RevocationHistorySnapshot,
    validate_revocation_history,
)
from lab_registry_signature_verifier import (
    AdministrativeKeyPolicy,
    validate_administrative_policy,
)
from lab_registry_wire_format import MAX_SAFE_INTEGER

IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
ROLES = ("STATE", "WITNESS", "ADMIN")
BODY_DOMAIN = b"FBWEB-LAB-AUTHORITY-READ-BODY-V1\x00"
ENVELOPE_DOMAIN = b"FBWEB-LAB-AUTHORITY-READ-ENVELOPE-V1\x00"


@dataclass(frozen=True)
class AuthorityReadChallenge:
    registry_id: str
    request_id: str
    challenge_hex: str
    state_authority_id: str
    witness_authority_id: str
    admin_authority_id: str


@dataclass(frozen=True)
class StateReadBody:
    position: ProtectedPosition
    history: RevocationHistorySnapshot


@dataclass(frozen=True)
class AdminPolicyReadBody:
    policy: AdministrativeKeyPolicy
    policy_epoch: int


@dataclass(frozen=True)
class AuthorityReadEvidence:
    role: str
    authority_id: str
    registry_id: str
    request_id: str
    challenge_hex: str
    body_digest: str
    envelope_digest: str
    body: object


@dataclass(frozen=True)
class AuthorityEvidenceAssessment:
    registry_id: str
    request_id: str
    revision: int
    generation: int
    policy_epoch: int
    logical_response_binding_valid: bool = True
    logical_position_consistency_valid: bool = True
    local_body_commitments_match: bool = True
    independent_authority_identity_authenticated: bool = False
    administrative_policy_authenticated: bool = False
    state_authority_authenticated: bool = False
    rollback_witness_authenticated: bool = False
    transport_authenticated: bool = False
    response_signature_verified: bool = False
    challenge_uniqueness_verified: bool = False
    replay_prevention_verified: bool = False
    authoritative_currentness_verified: bool = False
    trusted_time_verified: bool = False
    revocation_currentness_verified: bool = False
    durable_state_commit_verified: bool = False
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


def validate_authority_challenge(challenge):
    """Validate supplied labels, NOT their origin or nonce freshness."""
    if type(challenge) is not AuthorityReadChallenge:
        raise ValueError("AuthorityReadChallenge required")
    if challenge.registry_id != REGISTRY_ID:
        raise ValueError("Invalid request registry identity")
    if not _identifier(challenge.request_id):
        raise ValueError("Invalid request identifier")
    if not _digest(challenge.challenge_hex) or challenge.challenge_hex == "0" * 64:
        raise ValueError("Invalid request challenge")
    names = (
        challenge.state_authority_id,
        challenge.witness_authority_id,
        challenge.admin_authority_id,
    )
    if not all(_identifier(name) for name in names) or len(set(names)) != 3:
        raise ValueError("Expected authority labels must be distinct")
    return True


def _snapshot(position):
    return RevisionStateSnapshot(
        registry_id=position.registry_id,
        format_version=position.format_version,
        revision=position.revision,
        signing_digest=position.signing_digest,
        generation=position.generation,
    )


def _validate_body(role, body):
    if role == "STATE":
        if type(body) is not StateReadBody:
            raise ValueError("StateReadBody required")
        validate_position(body.position)
        validate_revocation_history(body.history, _snapshot(body.position))
        if revocation_commitment(body.history.tombstones) != body.position.revocation_digest:
            raise ValueError("State revocation commitment mismatch")
    elif role == "WITNESS":
        if type(body) is not WitnessCheckpoint:
            raise ValueError("WitnessCheckpoint required")
        validate_position(body.position)
    elif role == "ADMIN":
        if type(body) is not AdminPolicyReadBody:
            raise ValueError("AdminPolicyReadBody required")
        validate_administrative_policy(body.policy)
        if (type(body.policy_epoch) is not int
                or not 1 <= body.policy_epoch <= MAX_SAFE_INTEGER):
            raise ValueError("Invalid declared administrative policy epoch")
    else:
        raise ValueError("Unsupported authority role")


def _canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def untrusted_body_commitment(role, body):
    """Deterministic checksum; NOT an authenticated signature or MAC."""
    _validate_body(role, body)
    return hashlib.sha256(
        BODY_DOMAIN + _canonical_bytes({"role": role, "body": asdict(body)})
    ).hexdigest()


def untrusted_envelope_commitment(role, authority_id, registry_id,
                                  request_id, challenge_hex, body_digest):
    """Bind label/challenge/body fields, not their authoritative source."""
    if role not in ROLES or not _identifier(authority_id):
        raise ValueError("Invalid envelope role or authority label")
    if registry_id != REGISTRY_ID or not _identifier(request_id):
        raise ValueError("Invalid envelope registry or request")
    if not _digest(challenge_hex) or challenge_hex == "0" * 64:
        raise ValueError("Invalid envelope challenge")
    if not _digest(body_digest):
        raise ValueError("Invalid envelope body digest")
    fields = {
        "role": role,
        "authority_id": authority_id,
        "registry_id": registry_id,
        "request_id": request_id,
        "challenge_hex": challenge_hex,
        "body_digest": body_digest,
    }
    return hashlib.sha256(
        ENVELOPE_DOMAIN + _canonical_bytes(fields)
    ).hexdigest()


def _check_evidence(evidence, challenge, role, expected_id):
    if type(evidence) is not AuthorityReadEvidence:
        raise ValueError("AuthorityReadEvidence required")
    if (type(evidence.role) is not str or evidence.role != role
            or type(evidence.authority_id) is not str
            or evidence.authority_id != expected_id
            or type(evidence.registry_id) is not str
            or evidence.registry_id != challenge.registry_id
            or type(evidence.request_id) is not str
            or evidence.request_id != challenge.request_id
            or type(evidence.challenge_hex) is not str
            or evidence.challenge_hex != challenge.challenge_hex):
        raise ValueError("Role, identity, registry or challenge mismatch")
    actual_body = untrusted_body_commitment(role, evidence.body)
    if type(evidence.body_digest) is not str or evidence.body_digest != actual_body:
        raise ValueError("Authority body commitment mismatch")
    actual_envelope = untrusted_envelope_commitment(
        role, expected_id, challenge.registry_id,
        challenge.request_id, challenge.challenge_hex, actual_body,
    )
    if type(evidence.envelope_digest) is not str or evidence.envelope_digest != actual_envelope:
        raise ValueError("Authority envelope commitment mismatch")
    return evidence.body


def assess_authority_evidence(challenge, state_evidence, witness_evidence,
                              admin_evidence):
    """Evaluate three caller-supplied declarations, without authenticating them."""
    validate_authority_challenge(challenge)
    state = _check_evidence(
        state_evidence, challenge, "STATE", challenge.state_authority_id,
    )
    witness = _check_evidence(
        witness_evidence, challenge, "WITNESS", challenge.witness_authority_id,
    )
    admin = _check_evidence(
        admin_evidence, challenge, "ADMIN", challenge.admin_authority_id,
    )
    if state.position != witness.position:
        raise ValueError("State and witness positions disagree")
    if admin.policy_epoch != state.position.policy_epoch:
        raise ValueError("Declared administrative policy epoch disagrees")
    return AuthorityEvidenceAssessment(
        registry_id=challenge.registry_id,
        request_id=challenge.request_id,
        revision=state.position.revision,
        generation=state.position.generation,
        policy_epoch=state.position.policy_epoch,
    )
