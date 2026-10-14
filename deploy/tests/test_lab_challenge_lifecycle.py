#!/usr/bin/env python3
"""Gate 4D.22C.3D.12K adversarial, non-authorizing lifecycle tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from lab_challenge_lifecycle import (
    ChallengeRecord,
    ReplayLedgerSnapshot,
    RoleReceipt,
    ROLES,
    assess_request_action,
    assess_reservation,
    classify_ledger_observation,
    untrusted_ledger_commitment,
    validate_replay_ledger,
)
from lab_collector_trust_policy import REGISTRY_ID
from test_lab_authority_evidence_contract import case, _evidence
from lab_authority_evidence_contract import StateReadBody


class ChallengeLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.challenge, self.state, self.witness, self.admin = case()
        self.empty = ReplayLedgerSnapshot(REGISTRY_ID, 0, ())

        self.reservation = assess_reservation(
            self.empty,
            self.challenge,
            purpose="AUTHORITY_READ",
            policy_epoch=1,
            state_generation=1,
            expected_ledger_generation=0,
        )

        self.reserved = self.reservation.proposed_snapshot
        self.issued = self.action(
            self.reserved, "ISSUE"
        ).proposed_snapshot

    def action(
        self,
        ledger,
        name,
        response=None,
        request_id=None,
        expected_ledger_generation=None,
        expected_request_generation=None,
    ):
        record = next(
            (
                r for r in ledger.records
                if r.challenge.request_id == (
                    request_id or self.challenge.request_id
                )
            ),
            None,
        )

        return assess_request_action(
            ledger,
            request_id or self.challenge.request_id,
            name,
            expected_ledger_generation=(
                ledger.generation
                if expected_ledger_generation is None
                else expected_ledger_generation
            ),
            expected_request_generation=(
                record.generation
                if expected_request_generation is None
                and record is not None
                else expected_request_generation
            ),
            response=response,
        )

    def collect(self, ledger=None):
        ledger = self.issued if ledger is None else ledger

        for response in (
            self.state,
            self.witness,
            self.admin,
        ):
            assessment = self.action(
                ledger, "CONSUME", response
            )

            self.assertEqual(
                assessment.classification,
                "PROPOSED_ROLE_CONSUMPTION",
            )

            ledger = assessment.proposed_snapshot

        return ledger

    def denied(self, result, expected):
        self.assertEqual(result.classification, expected)
        self.assertFalse(result.logical_transition_proposed)
        self.assertIsNone(result.proposed_snapshot)

    def test_empty_ledger_valid(self):
        self.assertTrue(validate_replay_ledger(self.empty))

    def test_reservation_proposed(self):
        self.assertEqual(
            self.reservation.classification,
            "PROPOSED_RESERVATION",
        )
        self.assertEqual(
            self.reserved.records[0].state,
            "RESERVED",
        )

    def test_ledger_not_mutated_by_reservation(self):
        self.assertEqual(self.empty.generation, 0)
        self.assertEqual(self.empty.records, ())

    def test_reservation_generation_advances(self):
        self.assertEqual(self.reserved.generation, 1)
        self.assertEqual(self.reserved.records[0].generation, 1)

    def test_issue_from_reservation(self):
        self.assertEqual(self.issued.records[0].state, "ISSUED")

    def test_issue_without_reservation_denied(self):
        self.denied(
            self.action(
                self.empty,
                "ISSUE",
                expected_request_generation=1,
            ),
            "UNKNOWN_REQUEST",
        )

    def test_consume_before_issue_denied(self):
        self.denied(
            self.action(
                self.reserved, "CONSUME", self.state
            ),
            "UNRESERVED_OR_UNISSUED_REQUEST",
        )

    def test_second_issue_denied(self):
        self.denied(
            self.action(self.issued, "ISSUE"),
            "INVALID_TRANSITION",
        )

    def test_receive_state(self):
        proposed = self.action(
            self.issued, "CONSUME", self.state
        )
        self.assertEqual(
            proposed.proposed_snapshot.records[0].state,
            "COLLECTING",
        )

    def test_receive_roles_in_different_order(self):
        ledger = self.issued

        for response in (
            self.admin,
            self.witness,
            self.state,
        ):
            ledger = self.action(
                ledger, "CONSUME", response
            ).proposed_snapshot

        self.assertEqual(
            tuple(x.role for x in ledger.records[0].receipts),
            ROLES,
        )

    def test_complete_requires_three_roles(self):
        one = self.action(
            self.issued, "CONSUME", self.state
        ).proposed_snapshot

        self.denied(
            self.action(one, "COMPLETE"),
            "INCOMPLETE_RESPONSE_SET",
        )

    def test_complete_after_three_roles(self):
        full = self.collect()
        result = self.action(full, "COMPLETE")

        self.assertEqual(
            result.classification,
            "PROPOSED_COMPLETION",
        )
        self.assertEqual(
            result.proposed_snapshot.records[0].state,
            "COMPLETE",
        )

    def test_complete_cannot_repeat(self):
        complete = self.action(
            self.collect(), "COMPLETE"
        ).proposed_snapshot

        self.denied(
            self.action(complete, "COMPLETE"),
            "COMPLETE_REQUEST",
        )

    def test_same_role_response_is_duplicate(self):
        one = self.action(
            self.issued, "CONSUME", self.state
        ).proposed_snapshot

        result = self.action(
            one, "CONSUME", self.state
        )

        self.denied(result, "DUPLICATE_RESPONSE")
        self.assertTrue(result.replay_or_conflict_detected)

    def test_different_response_same_role_conflicts(self):
        one = self.action(
            self.issued, "CONSUME", self.state
        ).proposed_snapshot

        position = replace(
            self.state.body.position,
            signing_digest="f" * 64,
        )

        history = replace(
            self.state.body.history,
            signing_digest="f" * 64,
        )

        substitute = _evidence(
            self.challenge,
            "STATE",
            StateReadBody(position, history),
        )

        self.denied(
            self.action(one, "CONSUME", substitute),
            "CONFLICTING_ROLE_RESPONSE",
        )

    def test_response_wrong_challenge_denied(self):
        bad = replace(
            self.state, challenge_hex="f" * 64
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "CHALLENGE_MISMATCH",
        )

    def test_response_wrong_request_denied(self):
        bad = replace(
            self.state, request_id="other-request"
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "CHALLENGE_MISMATCH",
        )

    def test_response_wrong_registry_denied(self):
        bad = replace(
            self.state, registry_id="other-registry"
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "CHALLENGE_MISMATCH",
        )

    def test_response_wrong_authority_denied(self):
        bad = replace(
            self.state, authority_id="impostor"
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "ROLE_MISMATCH",
        )

    def test_response_wrong_role_denied(self):
        bad = replace(
            self.state, role="UNAPPROVED"
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "ROLE_MISMATCH",
        )

    def test_response_body_digest_mismatch_denied(self):
        bad = replace(
            self.state, body_digest="e" * 64
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "RESPONSE_COMMITMENT_MISMATCH",
        )

    def test_response_envelope_digest_mismatch_denied(self):
        bad = replace(
            self.state, envelope_digest="e" * 64
        )
        self.denied(
            self.action(self.issued, "CONSUME", bad),
            "RESPONSE_COMMITMENT_MISMATCH",
        )

    def test_bad_response_type_denied(self):
        with self.assertRaises(ValueError):
            self.action(
                self.issued, "CONSUME", object()
            )

    def test_policy_epoch_mismatch_denied(self):
        altered = _evidence(
            self.challenge,
            "ADMIN",
            replace(self.admin.body, policy_epoch=2),
        )
        self.denied(
            self.action(self.issued, "CONSUME", altered),
            "POLICY_EPOCH_MISMATCH",
        )

    def test_state_generation_mismatch_denied(self):
        altered = _evidence(
            self.challenge,
            "WITNESS",
            replace(
                self.witness.body,
                position=replace(
                    self.witness.body.position,
                    generation=2,
                ),
            ),
        )
        self.denied(
            self.action(self.issued, "CONSUME", altered),
            "STATE_GENERATION_MISMATCH",
        )

    def test_reservation_duplicate_request_id(self):
        newer = replace(
            self.challenge,
            challenge_hex="b" * 64,
        )

        result = assess_reservation(
            self.reserved,
            newer,
            purpose="AUTHORITY_READ",
            policy_epoch=1,
            state_generation=1,
            expected_ledger_generation=1,
        )
        self.denied(result, "REQUEST_ID_REUSE")

    def test_reservation_duplicate_challenge(self):
        newer = replace(
            self.challenge,
            request_id="request-222",
        )

        result = assess_reservation(
            self.reserved,
            newer,
            purpose="AUTHORITY_READ",
            policy_epoch=1,
            state_generation=1,
            expected_ledger_generation=1,
        )
        self.denied(result, "CHALLENGE_REUSE")

    def test_second_distinct_reservation(self):
        newer = replace(
            self.challenge,
            request_id="request-222",
            challenge_hex="b" * 64,
        )

        result = assess_reservation(
            self.reserved,
            newer,
            purpose="AUTHORITY_READ",
            policy_epoch=1,
            state_generation=1,
            expected_ledger_generation=1,
        )

        self.assertEqual(
            len(result.proposed_snapshot.records), 2
        )

    def test_reservation_old_ledger_generation(self):
        self.denied(
            assess_reservation(
                self.reserved,
                self.challenge,
                purpose="AUTHORITY_READ",
                policy_epoch=1,
                state_generation=1,
                expected_ledger_generation=0,
            ),
            "CONCURRENT_GENERATION_CONFLICT",
        )

    def test_action_old_ledger_generation(self):
        self.denied(
            self.action(
                self.issued,
                "CONSUME",
                self.state,
                expected_ledger_generation=1,
            ),
            "CONCURRENT_GENERATION_CONFLICT",
        )

    def test_action_old_request_generation(self):
        self.denied(
            self.action(
                self.issued,
                "CONSUME",
                self.state,
                expected_request_generation=1,
            ),
            "STALE_REQUEST_GENERATION",
        )

    def test_aborted_request_terminal(self):
        aborted = self.action(
            self.issued, "ABORT"
        ).proposed_snapshot

        self.denied(
            self.action(
                aborted, "CONSUME", self.state
            ),
            "ABORTED_REQUEST",
        )

    def test_expired_request_terminal(self):
        expired = self.action(
            self.issued, "EXPIRE"
        ).proposed_snapshot

        self.denied(
            self.action(
                expired, "CONSUME", self.state
            ),
            "EXPIRED_REQUEST",
        )

    def test_uncertain_request_terminal(self):
        uncertain = self.action(
            self.issued, "UNCERTAIN"
        ).proposed_snapshot

        self.denied(
            self.action(uncertain, "ISSUE"),
            "UNCERTAIN_REQUEST",
        )

    def test_aborted_challenge_not_reusable(self):
        aborted = self.action(
            self.issued, "ABORT"
        ).proposed_snapshot

        changed_id = replace(
            self.challenge,
            request_id="request-333",
        )

        self.denied(
            assess_reservation(
                aborted,
                changed_id,
                purpose="AUTHORITY_READ",
                policy_epoch=1,
                state_generation=1,
                expected_ledger_generation=aborted.generation,
            ),
            "CHALLENGE_REUSE",
        )

    def test_unknown_request(self):
        self.denied(
            self.action(
                self.issued,
                "CONSUME",
                self.state,
                request_id="missing",
                expected_request_generation=1,
            ),
            "UNKNOWN_REQUEST",
        )

    def test_ledger_observation_unavailable(self):
        self.denied(
            classify_ledger_observation(
                self.issued, None
            ),
            "REPLAY_LEDGER_UNAVAILABLE",
        )

    def test_ledger_rollback_suspected(self):
        self.denied(
            classify_ledger_observation(
                self.issued, self.reserved
            ),
            "LEDGER_ROLLBACK_SUSPECTED",
        )

    def test_ledger_same_untrusted(self):
        self.denied(
            classify_ledger_observation(
                self.issued, deepcopy(self.issued)
            ),
            "SAME_UNTRUSTED_LEDGER",
        )

    def test_ledger_forward_unverified(self):
        self.denied(
            classify_ledger_observation(
                self.reserved, self.issued
            ),
            "UNVERIFIED_FORWARD_LEDGER",
        )

    def test_ledger_same_generation_conflicting_content(self):
        corrupted = replace(
            self.issued,
            records=(
                replace(
                    self.issued.records[0],
                    purpose="AUTHORITY_READ",
                    policy_epoch=2,
                ),
            ),
        )

        self.denied(
            classify_ledger_observation(
                self.issued, corrupted
            ),
            "SAME_GENERATION_CONFLICT",
        )

    def test_deterministic_untrusted_checksum(self):
        self.assertEqual(
            untrusted_ledger_commitment(self.issued),
            untrusted_ledger_commitment(deepcopy(self.issued)),
        )

    def test_ledger_duplicate_requests_denied(self):
        with self.assertRaises(ValueError):
            validate_replay_ledger(
                replace(
                    self.issued,
                    records=self.issued.records * 2,
                )
            )

    def test_ledger_duplicate_challenges_denied(self):
        duplicate = replace(
            self.issued.records[0],
            challenge=replace(
                self.challenge,
                request_id="request-222",
            ),
        )

        with self.assertRaises(ValueError):
            validate_replay_ledger(
                replace(
                    self.issued,
                    records=self.issued.records + (duplicate,),
                )
            )

    def test_ledger_invalid_receipt_denied(self):
        forged = replace(
            self.issued.records[0],
            state="COLLECTING",
            receipts=(
                RoleReceipt(
                    "STATE", "a" * 64, "b" * 64
                ),
                RoleReceipt(
                    "STATE", "c" * 64, "d" * 64
                ),
            ),
        )

        with self.assertRaises(ValueError):
            validate_replay_ledger(
                replace(self.issued, records=(forged,))
            )

    def test_ledger_complete_without_receipts_denied(self):
        forged = replace(
            self.issued.records[0],
            state="COMPLETE",
        )

        with self.assertRaises(ValueError):
            validate_replay_ledger(
                replace(self.issued, records=(forged,))
            )

    def test_replay_classification_never_authorizes(self):
        result = self.action(
            self.issued, "CONSUME", self.state
        )

        for name in (
            "independent_authority_authenticated",
            "response_signatures_verified",
            "challenge_randomness_verified",
            "protected_reservation_verified",
            "role_consumption_durable",
            "replay_prevention_verified",
            "trusted_time_verified",
            "state_currentness_verified",
            "independent_rollback_witness_verified",
            "protected_storage_verified",
            "automatic_retry_permitted",
            "docker_execution_permitted",
            "production_execution_enabled",
        ):
            self.assertFalse(getattr(result, name), name)

        self.assertTrue(result.manual_verification_required)

    def test_immutable_result_and_snapshots(self):
        with self.assertRaises(FrozenInstanceError):
            self.reservation.classification = "AUTHORIZED"

        with self.assertRaises(FrozenInstanceError):
            self.issued.generation = 999

    def test_inputs_unchanged(self):
        before = deepcopy(self.issued)
        self.action(
            self.issued, "CONSUME", self.state
        )
        self.assertEqual(self.issued, before)

    def test_wrong_reservation_purpose_denied(self):
        with self.assertRaises(ValueError):
            assess_reservation(
                self.empty,
                self.challenge,
                purpose="DEPLOY",
                policy_epoch=1,
                state_generation=1,
                expected_ledger_generation=0,
            )

    def test_boolean_generation_denied(self):
        with self.assertRaises(ValueError):
            assess_reservation(
                self.empty,
                self.challenge,
                purpose="AUTHORITY_READ",
                policy_epoch=True,
                state_generation=1,
                expected_ledger_generation=0,
            )

    def test_invalid_action_denied(self):
        with self.assertRaises(ValueError):
            self.action(self.issued, "DEPLOY")

    def test_challenge_supplied_does_not_prove_randomness(self):
        self.assertFalse(
            self.reservation.challenge_randomness_verified
        )


if __name__ == "__main__":
    unittest.main()
