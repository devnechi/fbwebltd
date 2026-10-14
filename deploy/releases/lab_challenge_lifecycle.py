#!/usr/bin/env python3
"""Gate 4D.22C.3D.12K: PURE, NON-AUTHORIZING replay lifecycle analysis.

All ledger records and authority responses are CALLER SUPPLIED. Transitions
return proposed immutable snapshots only. No random generation, I/O, clocks,
locks, storage, authority authentication, retries, Docker or deployment.
"""

from dataclasses import dataclass, replace
import hashlib
import json
from dataclasses import asdict

from lab_authority_evidence_contract import (
    AuthorityReadChallenge,
    AuthorityReadEvidence,
    untrusted_body_commitment,
    untrusted_envelope_commitment,
    validate_authority_challenge,
)
from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER

ROLES = ("STATE", "WITNESS", "ADMIN")
OPEN = ("RESERVED", "ISSUED", "COLLECTING")
TERMINAL = ("COMPLETE", "EXPIRED", "ABORTED", "UNCERTAIN")
STATES = OPEN + TERMINAL
ACTIONS = ("ISSUE", "CONSUME", "COMPLETE", "EXPIRE", "ABORT", "UNCERTAIN")
MAX_RECORDS = 128
LEDGER_DOMAIN = b"FBWEB-LAB-REPLAY-LEDGER-V1\x00"


@dataclass(frozen=True)
class RoleReceipt:
    role: str
    body_digest: str
    envelope_digest: str


@dataclass(frozen=True)
class ChallengeRecord:
    challenge: AuthorityReadChallenge
    purpose: str
    policy_epoch: int
    state_generation: int
    state: str
    generation: int
    receipts: tuple = ()


@dataclass(frozen=True)
class ReplayLedgerSnapshot:
    registry_id: str
    generation: int
    records: tuple


@dataclass(frozen=True)
class ReplayLifecycleAssessment:
    classification: str
    proposed_snapshot: object = None
    logical_transition_proposed: bool = False
    replay_or_conflict_detected: bool = False
    independent_authority_authenticated: bool = False
    response_signatures_verified: bool = False
    challenge_randomness_verified: bool = False
    protected_reservation_verified: bool = False
    role_consumption_durable: bool = False
    replay_prevention_verified: bool = False
    trusted_time_verified: bool = False
    state_currentness_verified: bool = False
    independent_rollback_witness_verified: bool = False
    protected_storage_verified: bool = False
    automatic_retry_permitted: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    manual_verification_required: bool = True


def _positive(value):
    return type(value) is int and 1 <= value <= MAX_SAFE_INTEGER


def _digest(value):
    return (
        type(value) is str
        and len(value) == 64
        and all(c in "0123456789abcdef" for c in value)
    )


def _role_id(challenge, role):
    return {
        "STATE": challenge.state_authority_id,
        "WITNESS": challenge.witness_authority_id,
        "ADMIN": challenge.admin_authority_id,
    }[role]


def validate_replay_ledger(ledger):
    """Validate UNTRUSTED bounded snapshot; no persistence guarantee."""
    if (
        type(ledger) is not ReplayLedgerSnapshot
        or ledger.registry_id != REGISTRY_ID
    ):
        raise ValueError("Invalid replay ledger identity")

    if (
        type(ledger.generation) is not int
        or not 0 <= ledger.generation <= MAX_SAFE_INTEGER
    ):
        raise ValueError("Invalid replay ledger generation")

    if (
        type(ledger.records) is not tuple
        or len(ledger.records) > MAX_RECORDS
    ):
        raise ValueError("Invalid replay ledger records")

    if ledger.records and ledger.generation == 0:
        raise ValueError("Nonempty replay ledger has zero generation")

    ids, challenges = [], set()

    for record in ledger.records:
        if type(record) is not ChallengeRecord:
            raise ValueError("Invalid challenge record")

        validate_authority_challenge(record.challenge)

        if (
            record.challenge.registry_id != ledger.registry_id
            or record.purpose != "AUTHORITY_READ"
            or not _positive(record.policy_epoch)
            or not _positive(record.state_generation)
            or record.state not in STATES
            or not _positive(record.generation)
            or record.generation > ledger.generation
            or type(record.receipts) is not tuple
        ):
            raise ValueError("Invalid reserved request state")

        ids.append(record.challenge.request_id)

        if record.challenge.challenge_hex in challenges:
            raise ValueError("Duplicate stored challenge")

        challenges.add(record.challenge.challenge_hex)
        roles = []

        for receipt in record.receipts:
            if (
                type(receipt) is not RoleReceipt
                or receipt.role not in ROLES
                or not _digest(receipt.body_digest)
                or not _digest(receipt.envelope_digest)
            ):
                raise ValueError("Invalid role receipt")

            roles.append(receipt.role)

        if tuple(roles) != tuple(r for r in ROLES if r in roles):
            raise ValueError("Duplicate or noncanonical role receipts")

        if (
            (record.state in ("RESERVED", "ISSUED") and roles)
            or (record.state == "COLLECTING" and not roles)
            or (
                record.state == "COMPLETE"
                and tuple(roles) != ROLES
            )
        ):
            raise ValueError("Invalid role receipt lifecycle")

    if ids != sorted(set(ids)):
        raise ValueError("Duplicate or unsorted request identifiers")

    return True


def untrusted_ledger_commitment(ledger):
    """Checksum for caller-supplied snapshots; NOT rollback protection."""
    validate_replay_ledger(ledger)

    raw = json.dumps(
        asdict(ledger),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")

    return hashlib.sha256(LEDGER_DOMAIN + raw).hexdigest()


def _denied(reason, replay=False):
    return ReplayLifecycleAssessment(
        reason,
        replay_or_conflict_detected=replay,
    )


def _proposed(reason, snapshot):
    return ReplayLifecycleAssessment(
        reason,
        snapshot,
        logical_transition_proposed=True,
    )


def _advance(ledger, old, new):
    if ledger.generation == MAX_SAFE_INTEGER:
        return _denied("GENERATION_EXHAUSTED")

    records = tuple(sorted(
        (
            new if r.challenge.request_id == old.challenge.request_id else r
            for r in ledger.records
        ),
        key=lambda r: r.challenge.request_id,
    ))

    next_ledger = ReplayLedgerSnapshot(
        ledger.registry_id,
        ledger.generation + 1,
        records,
    )

    validate_replay_ledger(next_ledger)
    return next_ledger


def assess_reservation(
    ledger,
    challenge,
    *,
    purpose,
    policy_epoch,
    state_generation,
    expected_ledger_generation,
):
    """Propose reserving caller-supplied challenge BEFORE simulated issue."""
    validate_replay_ledger(ledger)
    validate_authority_challenge(challenge)

    if (
        purpose != "AUTHORITY_READ"
        or not _positive(policy_epoch)
        or not _positive(state_generation)
        or type(expected_ledger_generation) is not int
        or expected_ledger_generation < 0
    ):
        raise ValueError("Invalid reservation inputs")

    if ledger.generation != expected_ledger_generation:
        return _denied("CONCURRENT_GENERATION_CONFLICT", True)

    if any(
        r.challenge.request_id == challenge.request_id
        for r in ledger.records
    ):
        return _denied("REQUEST_ID_REUSE", True)

    if any(
        r.challenge.challenge_hex == challenge.challenge_hex
        for r in ledger.records
    ):
        return _denied("CHALLENGE_REUSE", True)

    if len(ledger.records) >= MAX_RECORDS:
        return _denied("LEDGER_CAPACITY_EXHAUSTED")

    if ledger.generation == MAX_SAFE_INTEGER:
        return _denied("GENERATION_EXHAUSTED")

    record = ChallengeRecord(
        challenge,
        purpose,
        policy_epoch,
        state_generation,
        "RESERVED",
        1,
    )

    snapshot = ReplayLedgerSnapshot(
        REGISTRY_ID,
        ledger.generation + 1,
        tuple(sorted(
            ledger.records + (record,),
            key=lambda r: r.challenge.request_id,
        )),
    )

    validate_replay_ledger(snapshot)
    return _proposed("PROPOSED_RESERVATION", snapshot)


def _check_response(record, response):
    if type(response) is not AuthorityReadEvidence:
        raise ValueError("AuthorityReadEvidence required")

    if response.role not in ROLES:
        return "ROLE_MISMATCH"

    ch = record.challenge

    if (
        response.registry_id != ch.registry_id
        or response.request_id != ch.request_id
        or response.challenge_hex != ch.challenge_hex
    ):
        return "CHALLENGE_MISMATCH"

    if response.authority_id != _role_id(ch, response.role):
        return "ROLE_MISMATCH"

    try:
        body_digest = untrusted_body_commitment(
            response.role,
            response.body,
        )
        envelope_digest = untrusted_envelope_commitment(
            response.role,
            response.authority_id,
            response.registry_id,
            response.request_id,
            response.challenge_hex,
            body_digest,
        )
    except (TypeError, ValueError):
        return "MALFORMED_RESPONSE"

    if (
        body_digest != response.body_digest
        or envelope_digest != response.envelope_digest
    ):
        return "RESPONSE_COMMITMENT_MISMATCH"

    if response.role == "ADMIN":
        if response.body.policy_epoch != record.policy_epoch:
            return "POLICY_EPOCH_MISMATCH"
    else:
        position = response.body.position

        if position.policy_epoch != record.policy_epoch:
            return "POLICY_EPOCH_MISMATCH"

        if position.generation != record.state_generation:
            return "STATE_GENERATION_MISMATCH"

    return None


def assess_request_action(
    ledger,
    request_id,
    action,
    *,
    expected_ledger_generation,
    expected_request_generation,
    response=None,
):
    """Classify logical single-request action without committing any state."""
    validate_replay_ledger(ledger)

    if (
        type(request_id) is not str
        or not request_id
        or action not in ACTIONS
        or type(expected_ledger_generation) is not int
        or type(expected_request_generation) is not int
    ):
        raise ValueError("Invalid challenge action")

    if ledger.generation != expected_ledger_generation:
        return _denied("CONCURRENT_GENERATION_CONFLICT", True)

    matches = tuple(
        r for r in ledger.records
        if r.challenge.request_id == request_id
    )

    if not matches:
        return _denied("UNKNOWN_REQUEST")

    old = matches[0]

    if old.generation != expected_request_generation:
        return _denied("STALE_REQUEST_GENERATION", True)

    if old.generation == MAX_SAFE_INTEGER:
        return _denied("GENERATION_EXHAUSTED")

    if old.state in TERMINAL:
        return _denied(old.state + "_REQUEST", True)

    if action == "ISSUE":
        if response is not None or old.state != "RESERVED":
            return _denied("INVALID_TRANSITION")

        state, receipts, outcome = (
            "ISSUED",
            old.receipts,
            "PROPOSED_ISSUE",
        )

    elif action == "CONSUME":
        if old.state not in ("ISSUED", "COLLECTING"):
            return _denied("UNRESERVED_OR_UNISSUED_REQUEST")

        problem = _check_response(old, response)

        if problem is not None:
            return _denied(problem, True)

        prior = next(
            (r for r in old.receipts if r.role == response.role),
            None,
        )

        if prior is not None:
            if (
                prior.body_digest == response.body_digest
                and prior.envelope_digest == response.envelope_digest
            ):
                return _denied("DUPLICATE_RESPONSE", True)

            return _denied("CONFLICTING_ROLE_RESPONSE", True)

        receipt = RoleReceipt(
            response.role,
            response.body_digest,
            response.envelope_digest,
        )

        receipts = tuple(sorted(
            old.receipts + (receipt,),
            key=lambda r: ROLES.index(r.role),
        ))

        state, outcome = (
            "COLLECTING",
            "PROPOSED_ROLE_CONSUMPTION",
        )

    elif action == "COMPLETE":
        if (
            response is not None
            or old.state != "COLLECTING"
            or tuple(r.role for r in old.receipts) != ROLES
        ):
            return _denied("INCOMPLETE_RESPONSE_SET")

        state, receipts, outcome = (
            "COMPLETE",
            old.receipts,
            "PROPOSED_COMPLETION",
        )

    else:
        if response is not None:
            return _denied("INVALID_TRANSITION")

        state = {
            "EXPIRE": "EXPIRED",
            "ABORT": "ABORTED",
            "UNCERTAIN": "UNCERTAIN",
        }[action]

        receipts, outcome = old.receipts, "PROPOSED_" + state

    new = replace(
        old,
        state=state,
        receipts=receipts,
        generation=old.generation + 1,
    )

    snapshot = _advance(ledger, old, new)

    if type(snapshot) is ReplayLifecycleAssessment:
        return snapshot

    return _proposed(outcome, snapshot)


def classify_ledger_observation(previous, observed):
    """Compare untrusted snapshots; no authentic monotonic witness is consulted."""
    validate_replay_ledger(previous)

    if observed is None:
        return _denied("REPLAY_LEDGER_UNAVAILABLE")

    validate_replay_ledger(observed)

    if observed.generation < previous.generation:
        return _denied("LEDGER_ROLLBACK_SUSPECTED", True)

    if observed.generation == previous.generation:
        if (
            untrusted_ledger_commitment(observed)
            != untrusted_ledger_commitment(previous)
        ):
            return _denied("SAME_GENERATION_CONFLICT", True)

        return _denied("SAME_UNTRUSTED_LEDGER")

    return _denied("UNVERIFIED_FORWARD_LEDGER")
