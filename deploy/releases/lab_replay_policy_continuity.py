#!/usr/bin/env python3
"""Gate 4D.22C.3D.12Q: PURE, NON-AUTHORIZING replay-key policy continuity.

All policy snapshots, issuers, approvals and witness observations are supplied
by the caller. Hash continuity does not authenticate bootstrap, key provenance,
policy approval, rollback resistance, trusted time or currentness.
No I/O, keys, signatures, writes, retries, Docker or deployment.
"""

from dataclasses import asdict, dataclass
import hashlib
import json

from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER
from lab_replay_protected_contract import (
    LEDGER_ID, ReplayProtectedPosition, validate_replay_position,
)
from lab_replay_signature_verifier import (
    POLICY_ID, PURPOSES, ReplayReadChallenge, ReplayResponseKeyPolicy,
    validate_replay_read_challenge, validate_replay_response_key_policy,
)

DOMAIN = b"FBWEB-LAB-REPLAY-KEY-POLICY-SNAPSHOT-V1\x00"
GENESIS_DIGEST = "0" * 64
FORMAT_VERSION = 1
MAX_POLICY_KEYS = 32


@dataclass(frozen=True)
class ReplayPolicyRoleBindings:
    replay_state_authority_id: str
    replay_witness_authority_id: str


@dataclass(frozen=True)
class ReplayPolicySnapshot:
    registry_id: str
    ledger_id: str
    format_version: int
    policy_id: str
    epoch: int
    generation: int
    recovery_epoch: int
    previous_commitment: str
    transition_id: str
    issuer_id: str
    approval_reference: str
    roles: ReplayPolicyRoleBindings
    key_policy: ReplayResponseKeyPolicy


@dataclass(frozen=True)
class ReplayPolicyCheckpoint:
    registry_id: str
    ledger_id: str
    policy_id: str
    epoch: int
    generation: int
    recovery_epoch: int
    policy_commitment: str


@dataclass(frozen=True)
class ReplayPolicyTransitionAssessment:
    previous_commitment: str
    proposed_commitment: str
    previous_epoch: int
    proposed_epoch: int
    previous_generation: int
    proposed_generation: int
    new_keys: tuple
    status_changes: tuple
    logical_continuity_valid: bool = True
    independent_issuer_authenticated: bool = False
    independent_trust_root_verified: bool = False
    independent_bootstrap_verified: bool = False
    independent_policy_approval_verified: bool = False
    protected_policy_storage_verified: bool = False
    policy_currentness_verified: bool = False
    trusted_time_verified: bool = False
    durable_policy_commit_verified: bool = False
    independent_witness_verified: bool = False
    rollback_prevention_verified: bool = False
    recovery_approved: bool = False
    replay_prevention_verified: bool = False
    runtime_isolation_proven: bool = False
    automatic_retry_permitted: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


@dataclass(frozen=True)
class ReplayPolicyReconciliationAssessment:
    classification: str
    state_and_witness_authenticated: bool = False
    independent_trust_root_verified: bool = False
    protected_policy_currentness_verified: bool = False
    durable_policy_commit_verified: bool = False
    independent_rollback_prevention_verified: bool = False
    recovery_approved: bool = False
    automatic_retry_permitted: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


def _positive(value):
    return type(value) is int and 1 <= value <= MAX_SAFE_INTEGER


def _identifier(value):
    return (type(value) is str and 1 <= len(value) <= 80
            and value[0].isalnum() and value[0].isascii()
            and all(ch.isascii() and (ch.isalnum() or ch in "_-") for ch in value))


def _digest(value):
    return (type(value) is str and len(value) == 64
            and all(c in "0123456789abcdef" for c in value))


def _keys(snapshot):
    return {(k.role, k.authority_id, k.key_id): k
            for k in snapshot.key_policy.keys}


def validate_replay_policy_snapshot(snapshot):
    """Check a declaration's structure; does NOT authenticate its issuer."""
    if type(snapshot) is not ReplayPolicySnapshot:
        raise ValueError("ReplayPolicySnapshot required")
    if (snapshot.registry_id != REGISTRY_ID or snapshot.ledger_id != LEDGER_ID
            or type(snapshot.format_version) is not int
            or snapshot.format_version != FORMAT_VERSION
            or snapshot.policy_id != POLICY_ID):
        raise ValueError("Invalid replay policy scope or protocol")
    if not all(_positive(n) for n in (snapshot.epoch, snapshot.generation,
                                     snapshot.recovery_epoch)):
        raise ValueError("Invalid replay policy epochs or generation")
    if (not _identifier(snapshot.transition_id)
            or not _identifier(snapshot.issuer_id)
            or not _identifier(snapshot.approval_reference)
            or not _digest(snapshot.previous_commitment)):
        raise ValueError("Invalid declared replay policy metadata")
    if snapshot.epoch == 1:
        if snapshot.generation != 1 or snapshot.previous_commitment != GENESIS_DIGEST:
            raise ValueError("Invalid caller-supplied policy genesis")
    elif snapshot.previous_commitment == GENESIS_DIGEST:
        raise ValueError("Non-genesis policy cannot use genesis commitment")
    if type(snapshot.roles) is not ReplayPolicyRoleBindings:
        raise ValueError("ReplayPolicyRoleBindings required")
    state_id = snapshot.roles.replay_state_authority_id
    witness_id = snapshot.roles.replay_witness_authority_id
    if not (_identifier(state_id) and _identifier(witness_id)
            and state_id != witness_id):
        raise ValueError("Invalid replay role bindings")
    validate_replay_response_key_policy(snapshot.key_policy)
    if (snapshot.key_policy.epoch != snapshot.epoch
            or len(snapshot.key_policy.keys) > MAX_POLICY_KEYS):
        raise ValueError("Key policy and protected epoch disagree")
    identifiers = {"REPLAY_STATE": state_id, "REPLAY_WITNESS": witness_id}
    entries = snapshot.key_policy.keys
    identities = tuple((k.role, k.authority_id, k.key_id) for k in entries)
    if identities != tuple(sorted(identities)):
        raise ValueError("Replay policy keys must be canonically sorted")
    for key in entries:
        if key.authority_id != identifiers[key.role]:
            raise ValueError("Replay signer outside pinned authority")
    for role in PURPOSES:
        if not any(k.role == role and k.status == "active" for k in entries):
            raise ValueError("Every replay role needs a declared active key")
    return True


def untrusted_replay_policy_commitment(snapshot):
    """Domain-separated checksum, not an approval signature or trust root."""
    validate_replay_policy_snapshot(snapshot)
    raw = json.dumps(asdict(snapshot), sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(DOMAIN + raw).hexdigest()


def assess_replay_policy_transition(previous, proposed):
    """Assess a single ordinary policy step, never write or approve it."""
    validate_replay_policy_snapshot(previous)
    validate_replay_policy_snapshot(proposed)
    if previous.epoch == MAX_SAFE_INTEGER or previous.generation == MAX_SAFE_INTEGER:
        raise ValueError("Replay policy epoch or generation exhausted")
    if (proposed.epoch != previous.epoch + 1
            or proposed.generation != previous.generation + 1
            or proposed.recovery_epoch != previous.recovery_epoch
            or proposed.registry_id != previous.registry_id
            or proposed.ledger_id != previous.ledger_id
            or proposed.policy_id != previous.policy_id
            or proposed.format_version != previous.format_version
            or proposed.roles != previous.roles
            or proposed.issuer_id != previous.issuer_id
            or proposed.transition_id == previous.transition_id
            or proposed.approval_reference == previous.approval_reference
            or proposed.previous_commitment != untrusted_replay_policy_commitment(previous)):
        raise ValueError("Invalid replay policy continuity or pinned identity")
    old = _keys(previous)
    new = _keys(proposed)
    additions, changes = [], []
    allowed = {"active": ("active", "disabled", "revoked"),
               "disabled": ("disabled", "revoked"), "revoked": ("revoked",)}
    old_material = {key.public_key_hex for key in old.values()}
    for identity, key in old.items():
        candidate = new.get(identity)
        if candidate is None:
            raise ValueError("Historical replay signing key was removed")
        for field in ("role", "authority_id", "key_id", "public_key_hex",
                      "algorithm", "purpose", "valid_from", "valid_until"):
            if getattr(key, field) != getattr(candidate, field):
                raise ValueError("Replay signing key rebound or validity rewritten")
        if candidate.status not in allowed[key.status]:
            raise ValueError("Disabled/revoked replay signing key reactivated")
        if candidate.status != key.status:
            changes.append(identity + (key.status, candidate.status))
    for identity, key in new.items():
        if identity not in old:
            if key.status != "active" or key.public_key_hex in old_material:
                raise ValueError("Invalid new replay signing key enrollment")
            additions.append(identity)
    if not additions and not changes:
        raise ValueError("Empty replay policy transition")
    return ReplayPolicyTransitionAssessment(
        previous_commitment=untrusted_replay_policy_commitment(previous),
        proposed_commitment=untrusted_replay_policy_commitment(proposed),
        previous_epoch=previous.epoch, proposed_epoch=proposed.epoch,
        previous_generation=previous.generation,
        proposed_generation=proposed.generation,
        new_keys=tuple(sorted(additions)), status_changes=tuple(sorted(changes)),
    )


def validate_replay_policy_binding(snapshot, challenge, position):
    """Compare caller-declared scopes/epochs; no independent authentication."""
    validate_replay_policy_snapshot(snapshot)
    validate_replay_read_challenge(challenge)
    validate_replay_position(position)
    if (challenge.registry_id != snapshot.registry_id
            or challenge.ledger_id != snapshot.ledger_id
            or position.registry_id != snapshot.registry_id
            or position.ledger_id != snapshot.ledger_id
            or challenge.policy_epoch != snapshot.epoch
            or position.policy_epoch != snapshot.epoch
            or challenge.recovery_epoch != snapshot.recovery_epoch
            or position.recovery_epoch != snapshot.recovery_epoch
            or challenge.state_authority_id != snapshot.roles.replay_state_authority_id
            or challenge.witness_authority_id != snapshot.roles.replay_witness_authority_id):
        raise ValueError("Untrusted replay policy, challenge and position disagree")
    return True


def replay_policy_checkpoint(snapshot):
    """Create an UNAUTHENTICATED logical checkpoint from a supplied snapshot."""
    validate_replay_policy_snapshot(snapshot)
    return ReplayPolicyCheckpoint(
        snapshot.registry_id, snapshot.ledger_id, snapshot.policy_id,
        snapshot.epoch, snapshot.generation, snapshot.recovery_epoch,
        untrusted_replay_policy_commitment(snapshot),
    )


def validate_replay_policy_checkpoint(checkpoint):
    if type(checkpoint) is not ReplayPolicyCheckpoint:
        raise ValueError("ReplayPolicyCheckpoint required")
    if (checkpoint.registry_id != REGISTRY_ID or checkpoint.ledger_id != LEDGER_ID
            or checkpoint.policy_id != POLICY_ID
            or not all(_positive(v) for v in (checkpoint.epoch,
                                             checkpoint.generation,
                                             checkpoint.recovery_epoch))
            or not _digest(checkpoint.policy_commitment)):
        raise ValueError("Invalid replay policy checkpoint declaration")
    return True


def classify_replay_policy_reconciliation(previous, proposed,
                                          observed_state, observed_witness):
    """Classify SUPPLIED observations; no trusted authority or auto recovery."""
    assess_replay_policy_transition(previous, proposed)
    base = replay_policy_checkpoint(previous)
    target = replay_policy_checkpoint(proposed)
    if observed_state is None or observed_witness is None:
        if observed_state is None and observed_witness is None:
            label = "BOTH_POLICY_AUTHORITIES_UNAVAILABLE"
        elif observed_state is None:
            label = "POLICY_STATE_UNAVAILABLE"
        else:
            label = "POLICY_WITNESS_UNAVAILABLE"
        return ReplayPolicyReconciliationAssessment(label)
    validate_replay_policy_snapshot(observed_state)
    validate_replay_policy_checkpoint(observed_witness)
    state = replay_policy_checkpoint(observed_state)
    witness = observed_witness
    if state.generation < base.generation or state.epoch < base.epoch:
        label = "POLICY_STATE_ROLLBACK_SUSPECTED"
    elif witness.generation < base.generation or witness.epoch < base.epoch:
        label = "POLICY_WITNESS_ROLLBACK_SUSPECTED"
    elif state == base and witness == base:
        label = "BOTH_PREVIOUS_UNTRUSTED"
    elif state == target and witness == base:
        label = "POLICY_STATE_AHEAD_OF_WITNESS"
    elif state == base and witness == target:
        label = "POLICY_WITNESS_AHEAD_OF_STATE"
    elif state == target and witness == target:
        label = "BOTH_PROPOSED_UNTRUSTED"
    else:
        label = "CONFLICTING_OR_UNEXPECTED_POLICY_POSITIONS"
    return ReplayPolicyReconciliationAssessment(label)
