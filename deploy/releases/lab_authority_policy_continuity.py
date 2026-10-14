#!/usr/bin/env python3
"""Gate 4D.22C.3D.12I: pure, NON-AUTHORIZING trust-policy continuity.

All snapshots, key material and role bindings are supplied by the caller.
Neither matching hashes nor a logical rotation proves independent approval,
protected storage, currentness or administrative authority.
No IO, signing, service calls, key generation, commits or runtime permission.
"""

from dataclasses import asdict, dataclass
import hashlib
import json

from lab_authority_signature_verifier import (
    AuthorityResponseKeyPolicy,
    PURPOSES,
    POLICY_ID,
    IDENTIFIER,
    validate_authority_response_key_policy,
)
from lab_authority_evidence_contract import (
    AuthorityReadChallenge,
    validate_authority_challenge,
)
from lab_collector_trust_policy import REGISTRY_ID
from lab_protected_state_contract import ProtectedPosition, validate_position
from lab_registry_wire_format import MAX_SAFE_INTEGER

DOMAIN = b"FBWEB-LAB-AUTHORITY-POLICY-SNAPSHOT-V1\x00"
GENESIS_DIGEST = "0" * 64
MAX_POLICY_KEYS = 32


@dataclass(frozen=True)
class AuthorityRoleBindings:
    state_authority_id: str
    witness_authority_id: str
    admin_authority_id: str


@dataclass(frozen=True)
class AuthorityPolicySnapshot:
    registry_id: str
    policy_id: str
    epoch: int
    generation: int
    recovery_epoch: int
    previous_commitment: str
    transition_id: str
    roles: AuthorityRoleBindings
    key_policy: AuthorityResponseKeyPolicy


@dataclass(frozen=True)
class AuthorityPolicyTransitionAssessment:
    previous_commitment: str
    proposed_commitment: str
    previous_epoch: int
    proposed_epoch: int
    new_keys: tuple
    status_changes: tuple
    logical_continuity_valid: bool = True
    independently_trusted_policy: bool = False
    policy_approval_authenticated: bool = False
    independent_bootstrap_verified: bool = False
    protected_epoch_committed: bool = False
    policy_provenance_authenticated: bool = False
    protected_storage_verified: bool = False
    recovery_authorized: bool = False
    authority_identity_authenticated: bool = False
    trusted_time_verified: bool = False
    replay_prevention_verified: bool = False
    rollback_prevention_verified: bool = False
    durable_commit_verified: bool = False
    runtime_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _positive(value):
    return type(value) is int and 1 <= value <= MAX_SAFE_INTEGER


def _identifier(value):
    return type(value) is str and IDENTIFIER.fullmatch(value) is not None


def _keys(policy):
    return {(k.role, k.authority_id, k.key_id): k for k in policy.keys}


def validate_authority_policy_snapshot(snapshot):
    """Validate caller-supplied shape and role continuity prerequisites."""
    if type(snapshot) is not AuthorityPolicySnapshot:
        raise ValueError("AuthorityPolicySnapshot required")
    if snapshot.registry_id != REGISTRY_ID or snapshot.policy_id != POLICY_ID:
        raise ValueError("Unexpected registry or policy identity")
    if not all(_positive(v) for v in (
        snapshot.epoch, snapshot.generation, snapshot.recovery_epoch,
    )):
        raise ValueError("Invalid policy epoch or generation")
    if not _identifier(snapshot.transition_id):
        raise ValueError("Invalid policy transition identifier")
    if (type(snapshot.previous_commitment) is not str
            or len(snapshot.previous_commitment) != 64
            or any(c not in "0123456789abcdef" for c in snapshot.previous_commitment)):
        raise ValueError("Invalid previous policy commitment")
    if snapshot.epoch == 1:
        if snapshot.generation != 1 or snapshot.previous_commitment != GENESIS_DIGEST:
            raise ValueError("Invalid declared bootstrap position")
    elif snapshot.previous_commitment == GENESIS_DIGEST:
        raise ValueError("Non-genesis snapshot needs previous commitment")
    roles = snapshot.roles
    if type(roles) is not AuthorityRoleBindings:
        raise ValueError("AuthorityRoleBindings required")
    role_ids = (roles.state_authority_id, roles.witness_authority_id,
                roles.admin_authority_id)
    if not all(_identifier(x) for x in role_ids) or len(set(role_ids)) != 3:
        raise ValueError("Invalid independent role labels")
    validate_authority_response_key_policy(snapshot.key_policy)
    entries = snapshot.key_policy.keys
    if len(entries) > MAX_POLICY_KEYS:
        raise ValueError("Policy exceeds laboratory key bound")
    identifiers = {
        "STATE": roles.state_authority_id,
        "WITNESS": roles.witness_authority_id,
        "ADMIN": roles.admin_authority_id,
    }
    identities = tuple((key.role, key.authority_id, key.key_id) for key in entries)
    if identities != tuple(sorted(identities)):
        raise ValueError("Policy keys must be canonically sorted")
    for key in entries:
        if key.authority_id != identifiers[key.role]:
            raise ValueError("Signer outside pinned authority role")
    for role in PURPOSES:
        if not any(key.role == role and key.status == "active" for key in entries):
            raise ValueError("Every authority role needs an active declared key")
    return True


def untrusted_policy_commitment(snapshot):
    """Domain-separated deterministic digest, NOT authenticated evidence."""
    validate_authority_policy_snapshot(snapshot)
    payload = json.dumps(
        asdict(snapshot), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")
    return hashlib.sha256(DOMAIN + payload).hexdigest()


def validate_policy_binding(snapshot, challenge, position):
    """Compare supplied role/epoch declarations; never authorize a read."""
    validate_authority_policy_snapshot(snapshot)
    validate_authority_challenge(challenge)
    validate_position(position)
    if (challenge.registry_id != snapshot.registry_id
            or position.registry_id != snapshot.registry_id
            or position.policy_epoch != snapshot.epoch
            or (challenge.state_authority_id,
                challenge.witness_authority_id,
                challenge.admin_authority_id) != (
                snapshot.roles.state_authority_id,
                snapshot.roles.witness_authority_id,
                snapshot.roles.admin_authority_id)):
        raise ValueError("Supplied authority labels or policy epoch disagree")
    return True


def assess_authority_policy_transition(previous, proposed):
    """Check a logical chain link; no trust-anchor or state advancement."""
    validate_authority_policy_snapshot(previous)
    validate_authority_policy_snapshot(proposed)
    if previous.epoch == MAX_SAFE_INTEGER or previous.generation == MAX_SAFE_INTEGER:
        raise ValueError("Policy epoch or generation exhausted")
    if (proposed.epoch != previous.epoch + 1
            or proposed.generation != previous.generation + 1
            or proposed.recovery_epoch != previous.recovery_epoch
            or proposed.roles != previous.roles
            or proposed.registry_id != previous.registry_id
            or proposed.policy_id != previous.policy_id
            or proposed.transition_id == previous.transition_id
            or proposed.previous_commitment != untrusted_policy_commitment(previous)):
        raise ValueError("Invalid policy continuity or protected-role change")

    old = _keys(previous.key_policy)
    current = _keys(proposed.key_policy)
    new_keys, changes = [], []
    for identity, key in old.items():
        candidate = current.get(identity)
        if candidate is None:
            raise ValueError("Authority key history removed")
        for name in (
            "role", "authority_id", "key_id", "public_key_hex",
            "algorithm", "purpose", "valid_from", "valid_until",
        ):
            if getattr(key, name) != getattr(candidate, name):
                raise ValueError("Existing authority key identity or validity changed")
        allowed = {
            "active": ("active", "disabled", "revoked"),
            "disabled": ("disabled", "revoked"),
            "revoked": ("revoked",),
        }
        if candidate.status not in allowed[key.status]:
            raise ValueError("Retired authority key reactivated")
        if candidate.status != key.status:
            changes.append(identity + (key.status, candidate.status))
    for identity in current:
        if identity not in old:
            if current[identity].status != "active":
                raise ValueError("Newly enrolled key must start active")
            new_keys.append(identity)
    if not new_keys and not changes:
        raise ValueError("Empty policy transition is not a rotation")
    return AuthorityPolicyTransitionAssessment(
        previous_commitment=untrusted_policy_commitment(previous),
        proposed_commitment=untrusted_policy_commitment(proposed),
        previous_epoch=previous.epoch,
        proposed_epoch=proposed.epoch,
        new_keys=tuple(sorted(new_keys)),
        status_changes=tuple(sorted(changes)),
    )
