#!/usr/bin/env python3
"""Gate 4D.22C.3D.12E adversarial pure-reconciliation tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_registry_reconciliation import (
    ReconciliationObservation,
    assess_reconciliation,
)
from lab_protected_state_contract import (
    ProtectedReadBundle,
    WitnessCheckpoint,
    assess_transition_contract,
)
from test_lab_protected_state_contract import fixture


def observation(
    bundle,
    intent,
    state="previous",
    witness="previous",
    state_report="NOT_ATTEMPTED",
    witness_report="NOT_ATTEMPTED",
):
    proposal = assess_transition_contract(bundle, intent)

    state_positions = {
        "previous": bundle.position,
        "proposed": proposal.proposed_position,
        "missing": None,
    }
    histories = {
        "previous": bundle.history,
        "proposed": proposal.proposed_history,
        "missing": None,
    }

    position = state_positions[state]
    witness_position = state_positions[witness]

    return ReconciliationObservation(
        state_position=position,
        state_history=histories[state],
        witness_checkpoint=(
            WitnessCheckpoint(witness_position)
            if witness_position is not None
            else None
        ),
        state_commit_report=state_report,
        witness_advance_report=witness_report,
    )


class RegistryReconciliationTests(unittest.TestCase):

    def evaluate(
        self,
        state="previous",
        witness="previous",
        **kwargs,
    ):
        bundle, intent = fixture()
        result = assess_reconciliation(
            bundle,
            intent,
            observation(
                bundle, intent, state, witness, **kwargs
            ),
        )
        return result

    def test_both_previous(self):
        self.assertEqual(
            self.evaluate().classification,
            "BOTH_PREVIOUS",
        )

    def test_state_ahead(self):
        result = self.evaluate("proposed", "previous")
        self.assertEqual(
            result.classification,
            "STATE_AHEAD",
        )

    def test_witness_ahead(self):
        result = self.evaluate("previous", "proposed")
        self.assertEqual(
            result.classification,
            "WITNESS_AHEAD",
        )

    def test_both_proposed_remain_untrusted(self):
        result = self.evaluate("proposed", "proposed")
        self.assertEqual(
            result.classification,
            "BOTH_PROPOSED_UNTRUSTED",
        )
        self.assertTrue(result.logical_pair_matches_proposal)
        self.assertFalse(result.durable_state_commit_verified)

    def test_unavailable_state(self):
        result = self.evaluate("missing", "proposed")
        self.assertEqual(
            result.classification,
            "AUTHORITY_UNAVAILABLE",
        )
        self.assertEqual(result.state_relation, "UNAVAILABLE")

    def test_unavailable_witness(self):
        result = self.evaluate("proposed", "missing")
        self.assertEqual(
            result.classification,
            "AUTHORITY_UNAVAILABLE",
        )

    def test_both_unavailable(self):
        self.assertEqual(
            self.evaluate(
                "missing", "missing"
            ).classification,
            "AUTHORITY_UNAVAILABLE",
        )

    def test_acknowledged_but_unavailable_is_contradictory(self):
        result = self.evaluate(
            "missing",
            "previous",
            state_report="ACKNOWLEDGED",
        )
        self.assertEqual(
            result.classification,
            "AUTHORITY_UNAVAILABLE",
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )

    def test_default_unknown_reports(self):
        bundle, intent = fixture()
        observed = observation(bundle, intent)
        observed = replace(
            observed,
            state_commit_report="UNKNOWN",
            witness_advance_report="UNKNOWN",
        )
        result = assess_reconciliation(
            bundle, intent, observed
        )
        self.assertTrue(result.reported_outcome_uncertain)
        self.assertEqual(
            result.classification,
            "BOTH_PREVIOUS",
        )

    def test_unknown_state_report_even_when_both_new(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            state_report="UNKNOWN",
            witness_report="ACKNOWLEDGED",
        )
        self.assertTrue(result.reported_outcome_uncertain)
        self.assertFalse(
            result.authoritative_currentness_verified
        )

    def test_unknown_witness_report(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            state_report="ACKNOWLEDGED",
            witness_report="UNKNOWN",
        )
        self.assertTrue(result.reported_outcome_uncertain)

    def test_acknowledgement_not_proof(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            state_report="ACKNOWLEDGED",
            witness_report="ACKNOWLEDGED",
        )
        self.assertFalse(result.durable_state_commit_verified)
        self.assertFalse(result.witness_commit_verified)

    def test_ack_state_but_old_state_reports_contradict(self):
        result = self.evaluate(
            state_report="ACKNOWLEDGED"
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )
        self.assertEqual(
            result.classification,
            "BOTH_PREVIOUS",
        )

    def test_ack_witness_but_old_witness_reports_contradict(self):
        result = self.evaluate(
            witness_report="ACKNOWLEDGED"
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )

    def test_rejected_state_but_new_state_reports_contradict(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            state_report="REJECTED",
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )

    def test_rejected_witness_but_new_witness_reports_contradict(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            witness_report="REJECTED",
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )

    def test_not_attempted_state_but_new_state(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            state_report="NOT_ATTEMPTED",
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )

    def test_not_attempted_witness_but_new_witness(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            witness_report="NOT_ATTEMPTED",
        )
        self.assertFalse(
            result.reports_consistent_with_observations
        )

    def test_matching_reports_are_consistent_not_authenticated(self):
        result = self.evaluate(
            "proposed",
            "proposed",
            state_report="ACKNOWLEDGED",
            witness_report="ACKNOWLEDGED",
        )
        self.assertTrue(
            result.reports_consistent_with_observations
        )
        self.assertFalse(
            result.authority_identity_authenticated
        )

    def test_invalid_state_report_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            state_commit_report="SUCCESS",
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_invalid_witness_report_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            witness_advance_report=True,
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_invalid_observation_type_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, {})

    def test_invalid_intent_type_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_reconciliation(
                bundle, None, observation(bundle, intent)
            )

    def test_mismatched_previous_expectation_rejected(self):
        bundle, intent = fixture()
        bad = replace(
            intent,
            expected_position=replace(
                bundle.position, generation=3
            ),
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(
                bundle,
                bad,
                observation(bundle, intent),
            )

    def test_invalid_previous_bundle_rejected(self):
        bundle, intent = fixture()
        bad = replace(
            bundle,
            witness=WitnessCheckpoint(
                replace(bundle.position, generation=2)
            ),
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(
                bad,
                intent,
                observation(bundle, intent),
            )

    def test_half_observed_state_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            state_history=None,
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_history_without_position_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            state_position=None,
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_wrong_observed_history_digest_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            state_history=replace(
                bundle.history,
                signing_digest="e" * 64,
            ),
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_wrong_revocation_commitment_rejected(self):
        bundle, intent = fixture()
        wrong = replace(
            bundle.position,
            revocation_digest="e" * 64,
        )
        obs = replace(
            observation(bundle, intent),
            state_position=wrong,
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_malformed_observed_witness_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            witness_checkpoint="fake",
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_malformed_observed_state_rejected(self):
        bundle, intent = fixture()
        obs = replace(
            observation(bundle, intent),
            state_position="fake",
        )
        with self.assertRaises(ValueError):
            assess_reconciliation(bundle, intent, obs)

    def test_conflicting_forward_position(self):
        bundle, intent = fixture()
        obs = observation(bundle, intent)

        other = replace(
            bundle.position,
            revision=5,
            generation=5,
            signing_digest="e" * 64,
            transition_id="later-5",
        )
        history = replace(
            bundle.history,
            revision=5,
            generation=5,
            signing_digest="e" * 64,
        )

        obs = replace(
            obs,
            state_position=other,
            state_history=history,
        )

        result = assess_reconciliation(
            bundle, intent, obs
        )
        self.assertEqual(
            result.classification,
            "CONFLICTING_POSITION",
        )

    def test_transition_identifier_collision(self):
        bundle, intent = fixture()
        proposal = assess_transition_contract(
            bundle, intent
        )

        other = replace(
            proposal.proposed_position,
            signing_digest="e" * 64,
        )
        history = replace(
            proposal.proposed_history,
            signing_digest="e" * 64,
        )

        obs = replace(
            observation(bundle, intent),
            state_position=other,
            state_history=history,
        )

        result = assess_reconciliation(
            bundle, intent, obs
        )
        self.assertEqual(
            result.classification,
            "TRANSITION_ID_CONFLICT",
        )

    def test_witness_transition_identifier_collision(self):
        bundle, intent = fixture()
        proposal = assess_transition_contract(
            bundle, intent
        )
        other = replace(
            proposal.proposed_position,
            signing_digest="e" * 64,
        )
        obs = replace(
            observation(bundle, intent),
            witness_checkpoint=WitnessCheckpoint(other),
        )
        self.assertEqual(
            assess_reconciliation(
                bundle, intent, obs
            ).classification,
            "TRANSITION_ID_CONFLICT",
        )

    def test_policy_epoch_rollback_suspected(self):
        bundle, intent = fixture()
        old = replace(
            bundle.position, policy_epoch=2
        )
        previous = ProtectedReadBundle(
            old,
            WitnessCheckpoint(old),
            bundle.history,
        )
        updated_intent = replace(
            intent, expected_position=old
        )
        stale = replace(old, policy_epoch=1)
        obs = replace(
            observation(previous, updated_intent),
            witness_checkpoint=WitnessCheckpoint(stale),
        )
        result = assess_reconciliation(
            previous, updated_intent, obs
        )
        self.assertEqual(
            result.classification,
            "ROLLBACK_SUSPECTED",
        )

    def test_recovery_epoch_rollback_suspected(self):
        bundle, intent = fixture()
        old = replace(
            bundle.position, recovery_epoch=2
        )
        previous = ProtectedReadBundle(
            old,
            WitnessCheckpoint(old),
            bundle.history,
        )
        updated_intent = replace(
            intent, expected_position=old
        )
        stale = replace(old, recovery_epoch=1)
        obs = replace(
            observation(previous, updated_intent),
            witness_checkpoint=WitnessCheckpoint(stale),
        )
        self.assertEqual(
            assess_reconciliation(
                previous, updated_intent, obs
            ).classification,
            "ROLLBACK_SUSPECTED",
        )

    def test_old_generation_rollback_suspected(self):
        bundle, intent = fixture()
        old = replace(
            bundle.position, generation=3
        )
        history = replace(
            bundle.history, generation=3
        )
        previous = ProtectedReadBundle(
            old,
            WitnessCheckpoint(old),
            history,
        )
        updated_intent = replace(
            intent, expected_position=old
        )
        stale = replace(
            old, generation=2
        )
        stale_history = replace(
            history, generation=2
        )
        obs = replace(
            observation(previous, updated_intent),
            state_position=stale,
            state_history=stale_history,
        )
        self.assertEqual(
            assess_reconciliation(
                previous, updated_intent, obs
            ).classification,
            "ROLLBACK_SUSPECTED",
        )

    def test_competing_candidate_cannot_be_inferred_accepted(self):
        bundle, intent = fixture()
        other_intent = replace(
            intent,
            candidate_signing_digest="e" * 64,
            proposed_history=replace(
                intent.proposed_history,
                candidate_signing_digest="e" * 64,
            ),
            transition_id="update-3",
        )
        obs = observation(
            bundle, intent, "proposed", "proposed"
        )
        result = assess_reconciliation(
            bundle, other_intent, obs
        )
        self.assertEqual(
            result.classification,
            "CONFLICTING_POSITION",
        )
        self.assertFalse(
            result.authoritative_currentness_verified
        )

    def test_duplicate_transition_binding_conflict(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_reconciliation(
                bundle,
                replace(
                    intent,
                    transition_id=bundle.position.transition_id,
                ),
                observation(bundle, intent),
            )

    def test_all_security_and_execution_flags_false(self):
        result = self.evaluate("proposed", "proposed")
        for field in (
            "authority_identity_authenticated",
            "witness_identity_authenticated",
            "administrative_policy_authenticated",
            "snapshot_provenance_authenticated",
            "state_response_freshness_verified",
            "witness_response_freshness_verified",
            "trusted_time_verified",
            "authoritative_currentness_verified",
            "durable_state_commit_verified",
            "witness_commit_verified",
            "two_authority_atomicity_verified",
            "rollback_prevention_verified",
            "revocation_currentness_verified",
            "collector_authenticated",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "production_execution_enabled",
            "automatic_retry_permitted",
        ):
            self.assertFalse(
                getattr(result, field), field
            )
        self.assertTrue(
            result.manual_verification_required
        )

    def test_result_is_frozen(self):
        result = self.evaluate()
        with self.assertRaises(FrozenInstanceError):
            result.classification = "ACCEPTED"

    def test_input_records_are_unchanged(self):
        bundle, intent = fixture()
        obs = observation(
            bundle, intent, "proposed", "previous"
        )
        saved = deepcopy((bundle, intent, obs))
        assess_reconciliation(bundle, intent, obs)
        self.assertEqual(
            (bundle, intent, obs), saved
        )

    def test_simulated_authorship_does_not_establish_authority(self):
        result = self.evaluate("proposed", "proposed")
        self.assertTrue(
            result.logical_pair_matches_proposal
        )
        self.assertFalse(
            result.authority_identity_authenticated
        )
        self.assertFalse(
            result.witness_identity_authenticated
        )


if __name__ == "__main__":
    unittest.main()
