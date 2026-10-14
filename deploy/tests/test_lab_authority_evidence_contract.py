#!/usr/bin/env python3
"""Gate 4D.22C.3D.12F adversarial response binding tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from lab_authority_evidence_contract import (
    AdminPolicyReadBody,
    AuthorityReadChallenge,
    AuthorityReadEvidence,
    StateReadBody,
    assess_authority_evidence,
    untrusted_body_commitment,
    untrusted_envelope_commitment,
    validate_authority_challenge,
)
from lab_protected_state_contract import WitnessCheckpoint
from lab_registry_signature_verifier import (
    ADMIN_POLICY_ID,
    AdministrativeKeyPolicy,
    AdministrativeKeyRecord,
)
from lab_registry_wire_format import REGISTRY_PURPOSE
from lab_runtime_auth_envelope import ALGORITHM
from test_lab_protected_state_contract import fixture


def _policy(key="d" * 64, status="active"):
    return AdministrativeKeyPolicy(
        policy_id=ADMIN_POLICY_ID,
        keys=(AdministrativeKeyRecord(
            key_id="admin-1",
            public_key_hex=key,
            algorithm=ALGORITHM,
            purpose=REGISTRY_PURPOSE,
            valid_from="2026-10-13T07:00:00Z",
            valid_until="2026-10-15T09:00:00Z",
            status=status,
        ),),
    )


def _challenge():
    bundle, _ = fixture()
    return AuthorityReadChallenge(
        registry_id=bundle.position.registry_id,
        request_id="request-001",
        challenge_hex="a" * 64,
        state_authority_id="independent-state",
        witness_authority_id="independent-witness",
        admin_authority_id="independent-admin",
    )


def _evidence(challenge, role, body):
    authority_id = {
        "STATE": challenge.state_authority_id,
        "WITNESS": challenge.witness_authority_id,
        "ADMIN": challenge.admin_authority_id,
    }[role]
    digest = untrusted_body_commitment(role, body)
    envelope = untrusted_envelope_commitment(
        role, authority_id, challenge.registry_id,
        challenge.request_id, challenge.challenge_hex, digest,
    )
    return AuthorityReadEvidence(
        role, authority_id, challenge.registry_id,
        challenge.request_id, challenge.challenge_hex,
        digest, envelope, body,
    )


def case():
    bundle, _ = fixture()
    challenge = _challenge()
    state = _evidence(challenge, "STATE", StateReadBody(
        bundle.position, bundle.history,
    ))
    witness = _evidence(challenge, "WITNESS", bundle.witness)
    admin = _evidence(challenge, "ADMIN", AdminPolicyReadBody(
        _policy(), bundle.position.policy_epoch,
    ))
    return challenge, state, witness, admin


class AuthorityEvidenceContractTests(unittest.TestCase):
    def evaluate(self, data=None):
        return assess_authority_evidence(*(case() if data is None else data))

    def assert_rejected(self, data):
        with self.assertRaises(ValueError):
            self.evaluate(data)

    def test_consistent_payloads_pass_structural_assessment(self):
        result = self.evaluate()
        self.assertEqual((result.revision, result.generation, result.policy_epoch), (1, 1, 1))
        self.assertTrue(result.logical_response_binding_valid)
        self.assertTrue(result.local_body_commitments_match)

    def test_no_authentication_or_execution_claims(self):
        result = self.evaluate()
        for field in (
            "independent_authority_identity_authenticated",
            "administrative_policy_authenticated",
            "state_authority_authenticated",
            "rollback_witness_authenticated",
            "transport_authenticated",
            "response_signature_verified",
            "challenge_uniqueness_verified",
            "replay_prevention_verified",
            "authoritative_currentness_verified",
            "trusted_time_verified",
            "revocation_currentness_verified",
            "durable_state_commit_verified",
            "rollback_prevention_verified",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "production_execution_enabled",
            "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, field), field)
        self.assertTrue(result.manual_verification_required)

    def test_assessment_is_immutable(self):
        result = self.evaluate()
        with self.assertRaises(FrozenInstanceError):
            result.revision = 42

    def test_inputs_unchanged(self):
        data = case()
        copy = deepcopy(data)
        self.evaluate(data)
        self.assertEqual(data, copy)

    def test_wrong_challenge_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, challenge_hex="b" * 64), state, witness, admin))

    def test_wrong_request_id_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, request_id="request-002"), state, witness, admin))

    def test_wrong_registry_id_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, registry_id="other-registry"), state, witness, admin))

    def test_zero_challenge_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, challenge_hex="0" * 64), state, witness, admin))

    def test_invalid_challenge_case_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, challenge_hex="A" * 64), state, witness, admin))

    def test_challenge_wrong_type_rejected(self):
        _, state, witness, admin = case()
        self.assert_rejected(({}, state, witness, admin))

    def test_duplicate_expected_authorities_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, admin_authority_id=challenge.state_authority_id), state, witness, admin))

    def test_invalid_expected_authority_label_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((replace(challenge, state_authority_id="wrong host"), state, witness, admin))

    def test_identity_substitution_state_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, replace(state, authority_id="attacker"), witness, admin))

    def test_identity_substitution_witness_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, state, replace(witness, authority_id="attacker"), admin))

    def test_identity_substitution_admin_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, state, witness, replace(admin, authority_id="attacker")))

    def test_cross_role_substitution_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, witness, state, admin))

    def test_declared_wrong_role_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, replace(state, role="WITNESS"), witness, admin))

    def test_response_request_id_mismatch(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, replace(state, request_id="request-002"), witness, admin))

    def test_response_nonce_mismatch(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, state, replace(witness, challenge_hex="c" * 64), admin))

    def test_response_registry_mismatch(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, state, witness, replace(admin, registry_id="bad-registry")))

    def test_body_tampering_without_digest_rejected(self):
        challenge, state, witness, admin = case()
        tampered = StateReadBody(replace(state.body.position, revision=2), state.body.history)
        self.assert_rejected((challenge, replace(state, body=tampered), witness, admin))

    def test_envelope_digest_tamper_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, replace(state, envelope_digest="f" * 64), witness, admin))

    def test_body_digest_tamper_rejected(self):
        challenge, state, witness, admin = case()
        self.assert_rejected((challenge, state, replace(witness, body_digest="f" * 64), admin))

    def test_partial_state_history_rejected(self):
        challenge, state, witness, admin = case()
        altered = replace(state, body=StateReadBody(state.body.position, None))
        self.assert_rejected((challenge, altered, witness, admin))

    def test_wrong_revocation_commitment_rejected(self):
        challenge, state, witness, admin = case()
        altered = replace(state, body=StateReadBody(
            replace(state.body.position, revocation_digest="e" * 64), state.body.history,
        ))
        self.assert_rejected((challenge, altered, witness, admin))

    def test_witness_position_mismatch_rejected(self):
        challenge, state, witness, admin = case()
        other = WitnessCheckpoint(replace(state.body.position, generation=2))
        changed = _evidence(challenge, "WITNESS", other)
        self.assert_rejected((challenge, state, changed, admin))

    def test_policy_epoch_mismatch_rejected(self):
        challenge, state, witness, admin = case()
        changed = _evidence(challenge, "ADMIN", replace(admin.body, policy_epoch=2))
        self.assert_rejected((challenge, state, witness, changed))

    def test_invalid_policy_epoch_boolean_rejected(self):
        challenge, state, witness, admin = case()
        changed = replace(admin, body=replace(admin.body, policy_epoch=True))
        self.assert_rejected((challenge, state, witness, changed))

    def test_invalid_admin_policy_rejected(self):
        challenge, state, witness, admin = case()
        altered = replace(admin.body, policy=replace(admin.body.policy, policy_id="wrong"))
        self.assert_rejected((challenge, state, witness, replace(admin, body=altered)))

    def test_state_body_under_witness_role_rejected(self):
        challenge, state, witness, admin = case()
        altered = replace(witness, body=state.body)
        self.assert_rejected((challenge, state, altered, admin))

    def test_missing_evidence_rejected(self):
        challenge, state, witness, _ = case()
        self.assert_rejected((challenge, state, witness, None))

    def test_stale_response_rejected_under_new_request_challenge(self):
        challenge, state, witness, admin = case()
        changed = replace(challenge, request_id="request-999", challenge_hex="e" * 64)
        self.assert_rejected((changed, state, witness, admin))

    def test_reused_caller_challenge_is_not_detected_as_replay(self):
        # Reusing the same request ID and challenge allows replay.
        data = case()
        self.assertTrue(self.evaluate(data).logical_response_binding_valid)
        self.assertFalse(self.evaluate(data).replay_prevention_verified)

    def test_alternate_self_consistent_forged_admin_policy_not_proven(self):
        challenge, state, witness, admin = case()
        forged = _evidence(challenge, "ADMIN", AdminPolicyReadBody(_policy("e" * 64), 1))
        result = self.evaluate((challenge, state, witness, forged))
        self.assertFalse(result.administrative_policy_authenticated)

    def test_alternate_self_consistent_forged_state_not_proven(self):
        challenge, state, witness, admin = case()
        tampered_position = replace(state.body.position, signing_digest="f" * 64)
        tampered_history = replace(state.body.history, signing_digest="f" * 64)
        new_state = _evidence(challenge, "STATE", StateReadBody(tampered_position, tampered_history))
        new_witness = _evidence(challenge, "WITNESS", WitnessCheckpoint(tampered_position))
        result = self.evaluate((challenge, new_state, new_witness, admin))
        self.assertFalse(result.state_authority_authenticated)
        self.assertFalse(result.rollback_prevention_verified)

    def test_wrong_administrative_key_status_structurally_allowed(self):
        # Actual administrator authorization is a separate gate.
        challenge, state, witness, admin = case()
        disabled = _evidence(challenge, "ADMIN", AdminPolicyReadBody(_policy(status="disabled"), 1))
        result = self.evaluate((challenge, state, witness, disabled))
        self.assertFalse(result.administrative_policy_authenticated)

    def test_response_wrong_type_rejected(self):
        challenge, _, witness, admin = case()
        self.assert_rejected((challenge, {}, witness, admin))

    def test_body_commitment_domain_separated_by_role(self):
        _, state, _, _ = case()
        with self.assertRaises(ValueError):
            untrusted_body_commitment("ADMIN", state.body)

    def test_challenge_validator_only_checks_structure(self):
        challenge, _, _, _ = case()
        self.assertTrue(validate_authority_challenge(challenge))


if __name__ == "__main__":
    unittest.main()
