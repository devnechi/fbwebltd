#!/usr/bin/env python3
"""Gate 4D.22C.3D.12C non-authorizing contract tests."""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from lab_protected_state_contract import (
    ProtectedPosition,
    ProtectedReadBundle,
    ProtectedTransitionIntent,
    WitnessCheckpoint,
    assess_transition_contract,
    revocation_commitment,
    validate_position,
    validate_read_contract,
)
from lab_registry_revocation_continuity import (
    KeyLifecycleTombstone,
    RevocationHistoryProposal,
    RevocationHistorySnapshot,
)
from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER, REGISTRY_FORMAT_VERSION


def fixture(status="active", next_status="revoked"):
    old_marks = () if status == "active" else (
        KeyLifecycleTombstone("collector-1", "key-1", "c" * 64, status),
    )
    new_marks = () if next_status == "active" else (
        KeyLifecycleTombstone("collector-1", "key-1", "c" * 64, next_status),
    )
    old_history = RevocationHistorySnapshot(
        registry_id=REGISTRY_ID,
        revision=1,
        signing_digest="a" * 64,
        generation=1,
        tombstones=old_marks,
    )
    position = ProtectedPosition(
        registry_id=REGISTRY_ID,
        format_version=REGISTRY_FORMAT_VERSION,
        revision=1,
        signing_digest="a" * 64,
        generation=1,
        policy_epoch=1,
        recovery_epoch=1,
        revocation_digest=revocation_commitment(old_marks),
        transition_id="bootstrap-1",
    )
    bundle = ProtectedReadBundle(position, WitnessCheckpoint(position), old_history)
    proposal = RevocationHistoryProposal(
        registry_id=REGISTRY_ID,
        candidate_revision=2,
        candidate_signing_digest="d" * 64,
        tombstones=new_marks,
    )
    intent = ProtectedTransitionIntent(
        expected_position=position,
        candidate_revision=2,
        candidate_signing_digest="d" * 64,
        proposed_history=proposal,
        transition_id="update-2",
    )
    return bundle, intent


class ProtectedStateContractTests(unittest.TestCase):
    def test_read_structurally_consistent(self):
        bundle, _ = fixture()
        self.assertTrue(validate_read_contract(bundle))

    def test_transition_produces_uncommitted_proposal(self):
        bundle, intent = fixture()
        result = assess_transition_contract(bundle, intent)
        self.assertEqual(result.commit_status, "NOT_ATTEMPTED")
        self.assertEqual(result.proposed_position.revision, 2)
        self.assertEqual(result.proposed_position.generation, 2)
        self.assertEqual(result.proposed_position.policy_epoch, 1)
        self.assertEqual(result.proposed_position.recovery_epoch, 1)
        self.assertEqual(result.proposed_position.transition_id, "update-2")
        self.assertEqual(result.proposed_history.tombstones[0].status, "revoked")

    def test_no_authority_or_execution_claims(self):
        bundle, intent = fixture()
        assessment = assess_transition_contract(bundle, intent)
        for name in (
            "authority_identity_authenticated", "witness_identity_authenticated",
            "policy_provenance_authenticated", "snapshot_provenance_authenticated",
            "trusted_time_verified", "rollback_prevention_verified",
            "revocation_currentness_verified", "durable_state_commit_verified",
            "witness_advanced", "atomic_two_authority_commit_verified",
            "runtime_isolation_proven", "docker_execution_permitted",
            "production_execution_enabled", "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(assessment, name), name)
        self.assertTrue(assessment.manual_verification_required)

    def test_inputs_not_mutated(self):
        bundle, intent = fixture()
        assess_transition_contract(bundle, intent)
        self.assertEqual(bundle.position.revision, 1)
        self.assertEqual(bundle.history.tombstones, ())
        self.assertEqual(intent.candidate_revision, 2)

    def test_immutable_proposal(self):
        bundle, intent = fixture()
        result = assess_transition_contract(bundle, intent)
        with self.assertRaises(FrozenInstanceError):
            result.proposed_position = bundle.position

    def test_witness_revision_mismatch(self):
        bundle, _ = fixture()
        witness = WitnessCheckpoint(replace(bundle.position, revision=2))
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, witness=witness))

    def test_witness_digest_mismatch(self):
        bundle, _ = fixture()
        witness = WitnessCheckpoint(replace(bundle.position, signing_digest="b" * 64))
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, witness=witness))

    def test_witness_generation_mismatch(self):
        bundle, _ = fixture()
        witness = WitnessCheckpoint(replace(bundle.position, generation=2))
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, witness=witness))

    def test_witness_admin_policy_epoch_mismatch(self):
        bundle, _ = fixture()
        witness = WitnessCheckpoint(replace(bundle.position, policy_epoch=2))
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, witness=witness))

    def test_witness_recovery_epoch_mismatch(self):
        bundle, _ = fixture()
        witness = WitnessCheckpoint(replace(bundle.position, recovery_epoch=2))
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, witness=witness))

    def test_missing_witness(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, witness=None))

    def test_missing_history(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_read_contract(replace(bundle, history=None))

    def test_revocation_commitment_mismatch(self):
        bundle, _ = fixture()
        state = replace(bundle.position, revocation_digest="a" * 64)
        with self.assertRaises(ValueError):
            validate_read_contract(ProtectedReadBundle(
                state, WitnessCheckpoint(state), bundle.history,
            ))

    def test_history_revision_mismatch(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_read_contract(replace(
                bundle, history=replace(bundle.history, revision=3),
            ))

    def test_history_generation_mismatch(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_read_contract(replace(
                bundle, history=replace(bundle.history, generation=2),
            ))

    def test_bad_bundle_type(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_read_contract(bundle.__dict__)

    def test_boolean_policy_epoch_rejected(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_position(replace(bundle.position, policy_epoch=True))

    def test_zero_recovery_epoch_rejected(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_position(replace(bundle.position, recovery_epoch=0))

    def test_bad_transition_id_rejected(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_position(replace(bundle.position, transition_id="bad id"))

    def test_zero_signing_digest_rejected(self):
        bundle, _ = fixture()
        with self.assertRaises(ValueError):
            validate_position(replace(bundle.position, signing_digest="0" * 64))

    def test_stale_expected_generation_rejected(self):
        bundle, intent = fixture()
        altered = replace(intent.expected_position, generation=2)
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, expected_position=altered))

    def test_stale_expected_digest_rejected(self):
        bundle, intent = fixture()
        altered = replace(intent.expected_position, signing_digest="f" * 64)
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, expected_position=altered))

    def test_same_revision_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, candidate_revision=1))

    def test_revision_gap_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, candidate_revision=3))

    def test_boolean_candidate_revision_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, candidate_revision=True))

    def test_mismatched_proposal_revision_rejected(self):
        bundle, intent = fixture()
        bad = replace(intent.proposed_history, candidate_revision=3)
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=bad))

    def test_mismatched_proposal_digest_rejected(self):
        bundle, intent = fixture()
        bad = replace(intent.proposed_history, candidate_signing_digest="a" * 64)
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=bad))

    def test_empty_proposal_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=None))

    def test_missing_prior_revocation_tombstone_rejected(self):
        bundle, intent = fixture("revoked", "revoked")
        bad = replace(intent.proposed_history, tombstones=())
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=bad))

    def test_revoked_to_disabled_regression_rejected(self):
        bundle, intent = fixture("revoked", "revoked")
        prior = intent.proposed_history.tombstones[0]
        bad = replace(intent.proposed_history, tombstones=(replace(prior, status="disabled"),))
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=bad))

    def test_tombstone_key_material_change_rejected(self):
        bundle, intent = fixture("revoked", "revoked")
        prior = intent.proposed_history.tombstones[0]
        bad = replace(intent.proposed_history, tombstones=(replace(prior, public_key_hex="b" * 64),))
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=bad))

    def test_revocation_proposal_invalid_tombstone_rejected(self):
        bundle, intent = fixture()
        original = intent.proposed_history.tombstones[0]
        bad = replace(intent.proposed_history, tombstones=(replace(original, status="active"),))
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, proposed_history=bad))

    def test_same_transition_identifier_rejected(self):
        bundle, intent = fixture()
        with self.assertRaises(ValueError):
            assess_transition_contract(bundle, replace(intent, transition_id="bootstrap-1"))

    def test_generation_exhaustion_rejected(self):
        bundle, intent = fixture()
        pos = replace(bundle.position, generation=MAX_SAFE_INTEGER)
        oldhistory = replace(bundle.history, generation=MAX_SAFE_INTEGER)
        saturated = ProtectedReadBundle(pos, WitnessCheckpoint(pos), oldhistory)
        with self.assertRaises(ValueError):
            assess_transition_contract(saturated, replace(intent, expected_position=pos))

    def test_two_competing_intents_one_stale_in_fake_state(self):
        bundle, intent = fixture()
        first = assess_transition_contract(bundle, intent)
        # Test-only imitation of a successful commit to both authorities.
        after = ProtectedReadBundle(
            first.proposed_position,
            WitnessCheckpoint(first.proposed_position),
            first.proposed_history,
        )
        with self.assertRaises(ValueError):
            assess_transition_contract(after, replace(intent, transition_id="update-3"))

    def test_state_advanced_witness_stale_fails(self):
        bundle, intent = fixture()
        first = assess_transition_contract(bundle, intent)
        state_only = ProtectedReadBundle(
            first.proposed_position,
            bundle.witness,
            first.proposed_history,
        )
        with self.assertRaises(ValueError):
            validate_read_contract(state_only)

    def test_witness_advanced_state_stale_fails(self):
        bundle, intent = fixture()
        first = assess_transition_contract(bundle, intent)
        witness_only = replace(
            bundle, witness=WitnessCheckpoint(first.proposed_position),
        )
        with self.assertRaises(ValueError):
            validate_read_contract(witness_only)

    def test_undetermined_commit_never_implies_acceptance(self):
        bundle, intent = fixture()
        result = assess_transition_contract(bundle, intent)
        self.assertEqual(result.commit_status, "NOT_ATTEMPTED")
        self.assertFalse(result.durable_state_commit_verified)
        self.assertFalse(result.witness_advanced)

    def test_coordinated_forgery_not_authenticated(self):
        bundle, _ = fixture()
        # Identical caller-provided state and witness look consistent,
        # but validate_read_contract cannot authenticate either one.
        forged = replace(bundle.position, signing_digest="e" * 64)
        forged_history = replace(bundle.history, signing_digest="e" * 64)
        coordinated = ProtectedReadBundle(
            forged, WitnessCheckpoint(forged), forged_history,
        )
        self.assertTrue(validate_read_contract(coordinated))


if __name__ == "__main__":
    unittest.main()
