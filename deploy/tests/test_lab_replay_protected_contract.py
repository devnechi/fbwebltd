#!/usr/bin/env python3
"""Gate 4D.22C.3D.12M adversarial replay position and recovery tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from lab_authority_evidence_contract import AuthorityReadChallenge
from lab_challenge_lifecycle import (
    ChallengeRecord, ReplayLedgerSnapshot, RoleReceipt,
    ROLES, untrusted_ledger_commitment,
)
from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER
from lab_replay_protected_contract import (
    LEDGER_ID, FORMAT_VERSION, ZERO_DIGEST,
    ReplayProtectedPosition, ReplayWitnessCheckpoint,
    ReplayProtectedReadBundle, ReplayConditionalTransitionIntent,
    assess_replay_conditional_transition, classify_replay_reconciliation,
    untrusted_operation_commitment, untrusted_position_commitment,
    validate_replay_position, validate_replay_protected_read,
)


def challenge(rid="request-1", nonce="a"):
    return AuthorityReadChallenge(
        registry_id=REGISTRY_ID,
        request_id=rid,
        challenge_hex=nonce * 64,
        state_authority_id="state-1",
        witness_authority_id="witness-1",
        admin_authority_id="admin-1",
    )


def empty_bundle():
    ledger = ReplayLedgerSnapshot(REGISTRY_ID, 0, ())
    position = ReplayProtectedPosition(
        registry_id=REGISTRY_ID,
        ledger_id=LEDGER_ID,
        format_version=FORMAT_VERSION,
        generation=0,
        ledger_digest=untrusted_ledger_commitment(ledger),
        policy_epoch=1,
        recovery_epoch=1,
        transition_id="bootstrap-0",
        previous_position_digest=ZERO_DIGEST,
    )
    return ReplayProtectedReadBundle(
        ledger, position, ReplayWitnessCheckpoint(position)
    )


def record(
    rid="request-1", *, nonce="a", state="RESERVED",
    generation=1, receipts=(), policy_epoch=1
):
    return ChallengeRecord(
        challenge(rid, nonce),
        "AUTHORITY_READ",
        policy_epoch,
        1,
        state,
        generation,
        receipts,
    )


def candidate(bundle, new_record):
    rows = {
        r.challenge.request_id: r
        for r in bundle.ledger.records
    }
    rows[new_record.challenge.request_id] = new_record

    return ReplayLedgerSnapshot(
        REGISTRY_ID,
        bundle.ledger.generation + 1,
        tuple(sorted(
            rows.values(),
            key=lambda r: r.challenge.request_id,
        )),
    )


def intent(bundle, proposed, action="RESERVE", rid="request-1", tid=None):
    name = tid or (
        "transition-" + str(bundle.ledger.generation + 1)
    )

    return ReplayConditionalTransitionIntent(
        expected_position=bundle.position,
        expected_witness=bundle.witness,
        candidate_ledger=proposed,
        action=action,
        request_id=rid,
        transition_id=name,
        operation_digest=untrusted_operation_commitment(
            bundle.position, proposed, action, rid, name,
        ),
    )


def simulated_advance(bundle, action, new_record, rid="request-1"):
    proposal = candidate(bundle, new_record)

    assessment = assess_replay_conditional_transition(
        bundle,
        intent(bundle, proposal, action, rid),
    )

    following = ReplayProtectedReadBundle(
        proposal,
        assessment.proposed_position,
        ReplayWitnessCheckpoint(assessment.proposed_position),
    )

    return following, assessment


class ReplayProtectedContractTests(unittest.TestCase):
    def setUp(self):
        self.base = empty_bundle()

        self.reserved, self.reservation = simulated_advance(
            self.base, "RESERVE", record()
        )

        self.issued, self.issue = simulated_advance(
            self.reserved,
            "ISSUE",
            record(state="ISSUED", generation=2),
        )

    def reject_position(self, **fields):
        with self.assertRaises(ValueError):
            validate_replay_position(
                replace(self.base.position, **fields)
            )

    def reject_read(self, **fields):
        with self.assertRaises(ValueError):
            validate_replay_protected_read(
                replace(self.base, **fields)
            )

    def reject_transition(
        self, new_record=None, action="ISSUE",
        old=None, rid="request-1", **changes
    ):
        source = self.reserved if old is None else old

        record_ = (
            new_record if new_record is not None
            else record(state="ISSUED", generation=2)
        )

        proposal = candidate(source, record_)

        with self.assertRaises(ValueError):
            assess_replay_conditional_transition(
                source,
                replace(
                    intent(source, proposal, action, rid),
                    **changes,
                ),
            )

    def collect(self):
        current = self.issued

        for index, role in enumerate(ROLES):
            receipts = current.ledger.records[0].receipts + (
                RoleReceipt(
                    role,
                    chr(97 + index) * 64,
                    chr(100 + index) * 64,
                ),
            )

            current, assessment = simulated_advance(
                current,
                "CONSUME",
                record(
                    state="COLLECTING",
                    generation=(
                        current.ledger.records[0].generation + 1
                    ),
                    receipts=receipts,
                ),
            )

        return current

    def test_genesis_position_shape(self):
        self.assertTrue(
            validate_replay_position(self.base.position)
        )

    def test_genesis_bundle_logical_consistency(self):
        self.assertTrue(
            validate_replay_protected_read(self.base)
        )

    def test_domain_separated_position_digest(self):
        import hashlib
        import json

        plain = hashlib.sha256(
            json.dumps(
                self.base.position.__dict__,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()

        self.assertNotEqual(
            untrusted_position_commitment(self.base.position),
            plain,
        )

    def test_digest_is_deterministic(self):
        self.assertEqual(
            untrusted_position_commitment(self.base.position),
            untrusted_position_commitment(
                deepcopy(self.base.position)
            ),
        )

    def test_wrong_position_type(self):
        with self.assertRaises(ValueError):
            validate_replay_position({})

    def test_wrong_registry_identity(self):
        self.reject_position(registry_id="other")

    def test_wrong_ledger_identity(self):
        self.reject_position(ledger_id="other")

    def test_wrong_format_version(self):
        self.reject_position(format_version=2)

    def test_boolean_generation(self):
        self.reject_position(generation=True)

    def test_negative_generation(self):
        self.reject_position(generation=-1)

    def test_policy_epoch_zero(self):
        self.reject_position(policy_epoch=0)

    def test_boolean_recovery_epoch(self):
        self.reject_position(recovery_epoch=True)

    def test_invalid_transition_id(self):
        self.reject_position(transition_id="bad transition!")

    def test_invalid_ledger_digest(self):
        self.reject_position(ledger_digest="n" * 64)

    def test_invalid_previous_digest(self):
        self.reject_position(previous_position_digest="0" * 63)

    def test_genesis_cannot_claim_nonzero_parent(self):
        self.reject_position(previous_position_digest="f" * 64)

    def test_nongenesis_cannot_claim_zero_parent(self):
        self.reject_position(generation=2)

    def test_generation_overflow(self):
        self.reject_position(generation=MAX_SAFE_INTEGER + 1)

    def test_wrong_bundle_type(self):
        with self.assertRaises(ValueError):
            validate_replay_protected_read(object())

    def test_ledger_position_generation_mismatch(self):
        self.reject_read(
            ledger=replace(self.base.ledger, generation=1)
        )

    def test_ledger_commitment_mismatch(self):
        self.reject_read(
            position=replace(
                self.base.position,
                ledger_digest="f" * 64,
            )
        )

    def test_witness_position_mismatch(self):
        self.reject_read(
            witness=ReplayWitnessCheckpoint(
                replace(self.base.position, policy_epoch=2)
            )
        )

    def test_wrong_witness_type(self):
        self.reject_read(witness={})

    def test_forged_matching_records_still_not_trusted(self):
        forged = deepcopy(self.base)

        self.assertTrue(
            validate_replay_protected_read(forged)
        )

        self.assertFalse(
            self.reservation.authority_identity_authenticated
        )

    def test_reservation_transition_proposed(self):
        self.assertEqual(
            self.reservation.classification,
            "PROPOSED_UNCOMMITTED_TRANSITION",
        )

    def test_reservation_generation_advanced(self):
        self.assertEqual(
            self.reservation.proposed_position.generation, 1
        )

    def test_parent_commitment_bound(self):
        self.assertEqual(
            self.reservation.proposed_position.previous_position_digest,
            untrusted_position_commitment(self.base.position),
        )

    def test_issue_after_reservation(self):
        self.assertEqual(
            self.issue.proposed_ledger.records[0].state,
            "ISSUED",
        )

    def test_new_reservation_must_start_reserved(self):
        self.reject_transition(
            new_record=record(state="ISSUED"),
            action="RESERVE",
            old=self.base,
        )

    def test_new_reservation_must_have_generation_one(self):
        self.reject_transition(
            new_record=record(generation=2),
            action="RESERVE",
            old=self.base,
        )

    def test_reservation_policy_epoch_must_match(self):
        self.reject_transition(
            new_record=record(policy_epoch=2),
            action="RESERVE",
            old=self.base,
        )

    def test_reused_transition_identifier(self):
        self.reject_transition(
            transition_id=self.reserved.position.transition_id
        )

    def test_stale_expected_position(self):
        self.reject_transition(
            expected_position=self.base.position
        )

    def test_stale_expected_witness(self):
        self.reject_transition(
            expected_witness=self.base.witness
        )

    def test_wrong_operation_digest(self):
        self.reject_transition(
            operation_digest="a" * 64
        )

    def test_wrong_intent_type(self):
        with self.assertRaises(ValueError):
            assess_replay_conditional_transition(
                self.reserved, {}
            )

    def test_missing_requested_action(self):
        self.reject_transition(action="RESERVE")

    def test_action_changes_unrelated_request(self):
        added, _ = simulated_advance(
            self.reserved,
            "RESERVE",
            record("request-2", nonce="b"),
            "request-2",
        )

        changes = []

        for r in added.ledger.records:
            if r.challenge.request_id == "request-1":
                changes.append(
                    replace(r, state="ISSUED", generation=2)
                )
            else:
                changes.append(
                    replace(r, policy_epoch=2)
                )

        forged = ReplayLedgerSnapshot(
            REGISTRY_ID,
            added.ledger.generation + 1,
            tuple(changes),
        )

        with self.assertRaises(ValueError):
            assess_replay_conditional_transition(
                added,
                intent(added, forged, "ISSUE"),
            )

    def test_incomplete_consumption_cannot_complete(self):
        self.reject_transition(
            old=self.issued,
            action="COMPLETE",
            new_record=record(
                state="COMPLETE", generation=3
            ),
        )

    def test_issue_cannot_change_receipts(self):
        bad = record(
            state="ISSUED",
            generation=2,
            receipts=(
                RoleReceipt("STATE", "a" * 64, "b" * 64),
            ),
        )

        self.reject_transition(new_record=bad)

    def test_consume_one_role(self):
        receipt = (
            RoleReceipt("STATE", "a" * 64, "b" * 64),
        )

        result, _ = simulated_advance(
            self.issued,
            "CONSUME",
            record(
                state="COLLECTING",
                generation=3,
                receipts=receipt,
            ),
        )

        self.assertEqual(
            result.ledger.records[0].receipts,
            receipt,
        )

    def test_duplicate_consume_denied(self):
        consumed, _ = simulated_advance(
            self.issued,
            "CONSUME",
            record(
                state="COLLECTING",
                generation=3,
                receipts=(
                    RoleReceipt("STATE", "a" * 64, "b" * 64),
                ),
            ),
        )

        self.reject_transition(
            old=consumed,
            action="CONSUME",
            new_record=record(
                state="COLLECTING",
                generation=4,
                receipts=(
                    RoleReceipt("STATE", "a" * 64, "b" * 64),
                ),
            ),
        )

    def test_changed_existing_receipt_denied(self):
        consumed, _ = simulated_advance(
            self.issued,
            "CONSUME",
            record(
                state="COLLECTING",
                generation=3,
                receipts=(
                    RoleReceipt("STATE", "a" * 64, "b" * 64),
                ),
            ),
        )

        self.reject_transition(
            old=consumed,
            action="CONSUME",
            new_record=record(
                state="COLLECTING",
                generation=4,
                receipts=(
                    RoleReceipt("STATE", "c" * 64, "d" * 64),
                    RoleReceipt("WITNESS", "e" * 64, "f" * 64),
                ),
            ),
        )

    def test_all_three_roles_then_complete(self):
        collecting = self.collect()
        current = collecting.ledger.records[0]

        closed, assessment = simulated_advance(
            collecting,
            "COMPLETE",
            replace(
                current,
                state="COMPLETE",
                generation=current.generation + 1,
            ),
        )

        self.assertEqual(
            closed.ledger.records[0].state,
            "COMPLETE",
        )
        self.assertFalse(
            assessment.durable_ledger_write_verified
        )

    def test_cannot_update_complete_request(self):
        collecting = self.collect()
        r = collecting.ledger.records[0]

        complete, _ = simulated_advance(
            collecting,
            "COMPLETE",
            replace(
                r,
                state="COMPLETE",
                generation=r.generation + 1,
            ),
        )

        self.reject_transition(
            old=complete,
            action="EXPIRE",
            new_record=replace(
                complete.ledger.records[0],
                state="EXPIRED",
                generation=r.generation + 2,
            ),
        )

    def test_expire_issued(self):
        expired, _ = simulated_advance(
            self.issued,
            "EXPIRE",
            record(state="EXPIRED", generation=3),
        )

        self.assertEqual(
            expired.ledger.records[0].state,
            "EXPIRED",
        )

    def test_abort_reserved(self):
        aborted, _ = simulated_advance(
            self.reserved,
            "ABORT",
            record(state="ABORTED", generation=2),
        )

        self.assertEqual(
            aborted.ledger.records[0].state,
            "ABORTED",
        )

    def test_uncertain_issued(self):
        uncertain, _ = simulated_advance(
            self.issued,
            "UNCERTAIN",
            record(state="UNCERTAIN", generation=3),
        )

        self.assertEqual(
            uncertain.ledger.records[0].state,
            "UNCERTAIN",
        )

    def test_policy_or_recovery_epoch_not_advanced(self):
        self.assertEqual(
            self.reservation.proposed_position.policy_epoch, 1
        )
        self.assertEqual(
            self.reservation.proposed_position.recovery_epoch, 1
        )

    def test_immutable_assessment(self):
        with self.assertRaises(FrozenInstanceError):
            self.reservation.classification = "COMMITTED"

    def test_input_not_mutated(self):
        saved = deepcopy(self.base)

        simulated_advance(
            self.base, "RESERVE", record()
        )

        self.assertEqual(saved, self.base)

    def test_all_trust_flags_remain_false(self):
        for field in (
            "authority_identity_authenticated",
            "witness_identity_authenticated",
            "independent_trust_roots_verified",
            "actual_conditional_commit_verified",
            "durable_ledger_write_verified",
            "witness_advanced",
            "atomic_two_authority_commit_verified",
            "independent_rollback_prevention_verified",
            "policy_currentness_verified",
            "trusted_time_verified",
            "replay_prevention_verified",
            "recovery_approved",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "automatic_retry_permitted",
            "production_execution_enabled",
        ):
            self.assertFalse(
                getattr(self.reservation, field), field
            )

        self.assertTrue(
            self.reservation.manual_verification_required
        )

    def reconcile(self, state, witness):
        return classify_replay_reconciliation(
            self.base.position,
            self.reservation.proposed_position,
            state,
            (
                ReplayWitnessCheckpoint(witness)
                if witness is not None
                else None
            ),
        )

    def test_both_previous(self):
        self.assertEqual(
            self.reconcile(
                self.base.position, self.base.position
            ).classification,
            "BOTH_PREVIOUS_UNTRUSTED",
        )

    def test_primary_ahead(self):
        self.assertEqual(
            self.reconcile(
                self.reservation.proposed_position,
                self.base.position,
            ).classification,
            "STATE_AHEAD_OF_WITNESS",
        )

    def test_witness_ahead(self):
        self.assertEqual(
            self.reconcile(
                self.base.position,
                self.reservation.proposed_position,
            ).classification,
            "WITNESS_AHEAD_OF_STATE",
        )

    def test_both_proposed_remain_untrusted(self):
        self.assertEqual(
            self.reconcile(
                self.reservation.proposed_position,
                self.reservation.proposed_position,
            ).classification,
            "BOTH_PROPOSED_UNTRUSTED",
        )

    def test_state_unavailable(self):
        self.assertEqual(
            self.reconcile(
                None, self.base.position
            ).classification,
            "REPLAY_AUTHORITY_UNAVAILABLE",
        )

    def test_witness_unavailable(self):
        self.assertEqual(
            self.reconcile(
                self.base.position, None
            ).classification,
            "REPLAY_WITNESS_UNAVAILABLE",
        )

    def test_both_unavailable(self):
        self.assertEqual(
            self.reconcile(None, None).classification,
            "BOTH_AUTHORITIES_UNAVAILABLE",
        )

    def test_state_rollback_suspected(self):
        self.assertEqual(
            classify_replay_reconciliation(
                self.reserved.position,
                self.issue.proposed_position,
                self.base.position,
                ReplayWitnessCheckpoint(
                    self.reserved.position
                ),
            ).classification,
            "REPLAY_STATE_ROLLBACK_SUSPECTED",
        )

    def test_witness_rollback_suspected(self):
        self.assertEqual(
            classify_replay_reconciliation(
                self.reserved.position,
                self.issue.proposed_position,
                self.reserved.position,
                ReplayWitnessCheckpoint(
                    self.base.position
                ),
            ).classification,
            "REPLAY_WITNESS_ROLLBACK_SUSPECTED",
        )

    def test_matching_unexpected_positions(self):
        unexpected = replace(
            self.base.position,
            ledger_digest="f" * 64,
        )

        self.assertEqual(
            self.reconcile(
                unexpected, unexpected
            ).classification,
            "CONFLICTING_OR_UNEXPECTED_POSITIONS",
        )

    def test_reconciliation_forged_parent_denied(self):
        with self.assertRaises(ValueError):
            classify_replay_reconciliation(
                self.base.position,
                replace(
                    self.reservation.proposed_position,
                    previous_position_digest="e" * 64,
                ),
                self.base.position,
                ReplayWitnessCheckpoint(
                    self.base.position
                ),
            )

    def test_reconciliation_wrong_witness_type_denied(self):
        with self.assertRaises(ValueError):
            classify_replay_reconciliation(
                self.base.position,
                self.reservation.proposed_position,
                self.base.position,
                {},
            )

    def test_reconciliation_flags_remain_false(self):
        result = self.reconcile(
            self.reservation.proposed_position,
            self.reservation.proposed_position,
        )

        for field in (
            "state_authority_authenticated",
            "witness_authority_authenticated",
            "protected_state_currentness_verified",
            "durable_commit_verified",
            "rollback_prevention_verified",
            "recovery_approved",
            "automatic_retry_permitted",
            "docker_execution_permitted",
            "production_execution_enabled",
        ):
            self.assertFalse(getattr(result, field), field)

        self.assertTrue(result.manual_verification_required)


if __name__ == "__main__":
    unittest.main()
