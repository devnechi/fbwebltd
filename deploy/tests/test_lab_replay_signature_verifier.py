#!/usr/bin/env python3
"""Gate 4D.22C.3D.12O adversarial OFFLINE replay-signature tests."""

from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import base64
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from lab_challenge_lifecycle import ReplayLedgerSnapshot, untrusted_ledger_commitment
from lab_collector_trust_policy import REGISTRY_ID
from lab_replay_protected_contract import (
    LEDGER_ID, FORMAT_VERSION, ZERO_DIGEST,
    ReplayProtectedPosition, ReplayWitnessCheckpoint,
    untrusted_position_commitment,
)
from lab_replay_signature_verifier import (
    POLICY_ID, PURPOSES, DOMAINS, BODY_DOMAINS, REQUEST_PURPOSE,
    ROLES, STATUS, PROTOCOL_VERSION, MAX_SIGNED_BYTES,
    ReplayReadChallenge, ReplayStateReadBody, ReplayReadEvidence,
    ReplayResponseKey, ReplayResponseKeyPolicy, SignedReplayResponse,
    replay_response_signing_bytes, canonical_signed_replay_bytes,
    parse_signed_replay_bytes, untrusted_replay_body_commitment,
    validate_replay_read_challenge, validate_replay_response_key_policy,
    verify_replay_read_signatures,
)
from lab_runtime_auth_envelope import ALGORITHM

NOW = datetime(2026, 10, 14, 2, 0, tzinfo=timezone.utc)


class ReplaySignatureTests(unittest.TestCase):
    def setUp(self):
        self.challenge = ReplayReadChallenge(
            registry_id=REGISTRY_ID, ledger_id=LEDGER_ID,
            request_id="read-100", challenge_hex="a" * 64,
            state_authority_id="replay-state-1",
            witness_authority_id="replay-witness-1",
            policy_epoch=1, recovery_epoch=1,
        )
        self.ledger = ReplayLedgerSnapshot(REGISTRY_ID, 0, ())
        self.position = ReplayProtectedPosition(
            registry_id=REGISTRY_ID, ledger_id=LEDGER_ID,
            format_version=FORMAT_VERSION, generation=0,
            ledger_digest=untrusted_ledger_commitment(self.ledger),
            policy_epoch=1, recovery_epoch=1,
            transition_id="bootstrap-0", previous_position_digest=ZERO_DIGEST,
        )
        self.state_body = ReplayStateReadBody(self.ledger, self.position)
        self.witness_body = ReplayWitnessCheckpoint(self.position)
        self.state = self.evidence("REPLAY_STATE", self.state_body)
        self.witness = self.evidence("REPLAY_WITNESS", self.witness_body)
        self.private = {}
        keys = []
        for role, authority in (
            ("REPLAY_STATE", self.challenge.state_authority_id),
            ("REPLAY_WITNESS", self.challenge.witness_authority_id),
        ):
            private = Ed25519PrivateKey.generate()
            self.private[role] = private
            keys.append(ReplayResponseKey(
                role=role, authority_id=authority,
                key_id="key-" + role.lower(),
                public_key_hex=private.public_key().public_bytes(
                    Encoding.Raw, PublicFormat.Raw
                ).hex(),
                algorithm=ALGORITHM, purpose=PURPOSES[role],
                status="active",
                valid_from="2026-10-13T00:00:00Z",
                valid_until="2026-10-15T00:00:00Z",
            ))
        self.policy = ReplayResponseKeyPolicy(POLICY_ID, 1, tuple(keys))
        self.signed = (
            self.sign("REPLAY_STATE", self.state),
            self.sign("REPLAY_WITNESS", self.witness),
        )

    def evidence(self, role, body):
        return ReplayReadEvidence(
            role=role,
            authority_id=(
                self.challenge.state_authority_id
                if role == "REPLAY_STATE"
                else self.challenge.witness_authority_id
            ),
            registry_id=self.challenge.registry_id,
            ledger_id=self.challenge.ledger_id,
            request_id=self.challenge.request_id,
            challenge_hex=self.challenge.challenge_hex,
            body_digest=untrusted_replay_body_commitment(role, body),
            body=body,
        )

    def sign(self, role, evidence):
        position = evidence.body.position
        unsigned = SignedReplayResponse(
            protocol_version=PROTOCOL_VERSION,
            role=role, authority_id=evidence.authority_id,
            key_id="key-" + role.lower(),
            registry_id=evidence.registry_id,
            ledger_id=evidence.ledger_id,
            request_id=evidence.request_id,
            challenge_hex=evidence.challenge_hex,
            response_status=STATUS,
            body_digest=evidence.body_digest,
            position_digest=untrusted_position_commitment(position),
            ledger_digest=position.ledger_digest,
            generation=position.generation,
            policy_epoch=position.policy_epoch,
            recovery_epoch=position.recovery_epoch,
            transition_id=position.transition_id,
            algorithm=ALGORITHM, purpose=PURPOSES[role], signature="",
        )
        signature = self.private[role].sign(
            replay_response_signing_bytes(unsigned)
        )
        return replace(unsigned, signature=base64.urlsafe_b64encode(
            signature
        ).decode("ascii").rstrip("="))

    def verify(self, signed=None, evidence=None, policy=None, now=NOW,
               challenge=None):
        a, b = self.signed if signed is None else signed
        state, witness = ((self.state, self.witness) if evidence is None
                          else evidence)
        return verify_replay_read_signatures(
            self.challenge if challenge is None else challenge,
            state, witness, a, b,
            self.policy if policy is None else policy, now=now,
        )

    def reject(self, **kwargs):
        with self.assertRaises(ValueError):
            self.verify(**kwargs)

    def change_key(self, role, **changes):
        return replace(self.policy, keys=tuple(
            replace(k, **changes) if k.role == role else k
            for k in self.policy.keys
        ))

    def test_two_valid_signatures(self):
        result = self.verify()
        self.assertTrue(result.state_signature_verified_under_supplied_key)
        self.assertTrue(result.witness_signature_verified_under_supplied_key)
        self.assertEqual(result.reconciliation_classification, "MATCHING_UNTRUSTED")

    def test_all_trust_claims_remain_false(self):
        result = self.verify()
        for field in (
            "independent_authority_identity_authenticated",
            "independent_trust_roots_verified", "state_authority_authenticated",
            "witness_authority_authenticated", "key_policy_currentness_verified",
            "challenge_randomness_verified", "challenge_uniqueness_verified",
            "replay_prevention_verified", "trusted_time_verified",
            "protected_state_currentness_verified", "durable_state_commit_verified",
            "witness_advancement_verified", "independent_rollback_prevention_verified",
            "recovery_approved", "runtime_isolation_proven",
            "automatic_retry_permitted", "docker_execution_permitted",
            "production_execution_enabled",
        ):
            self.assertFalse(getattr(result, field), field)
        self.assertTrue(result.manual_verification_required)

    def test_immutable_assessment(self):
        with self.assertRaises(FrozenInstanceError):
            self.verify().reconciliation_classification = "AUTHORIZED"

    def test_valid_canonical_round_trip(self):
        raw = canonical_signed_replay_bytes(self.signed[0])
        self.assertEqual(parse_signed_replay_bytes(raw), self.signed[0])

    def test_role_separated_domains(self):
        self.assertNotEqual(DOMAINS[ROLES[0]], DOMAINS[ROLES[1]])
        self.assertNotEqual(BODY_DOMAINS[ROLES[0]], BODY_DOMAINS[ROLES[1]])
        self.assertNotEqual(
            replay_response_signing_bytes(self.signed[0])[:36],
            replay_response_signing_bytes(self.signed[1])[:36],
        )

    def test_correct_supplied_policy_shape(self):
        self.assertTrue(validate_replay_response_key_policy(self.policy))

    def test_correct_supplied_challenge_shape(self):
        self.assertTrue(validate_replay_read_challenge(self.challenge))

    def test_signatures_under_attacker_supplied_keys_do_not_create_trust(self):
        self.assertFalse(self.verify().independent_trust_roots_verified)

    def test_invalid_signature(self):
        self.reject(signed=(replace(self.signed[0], signature="A" * 86),
                            self.signed[1]))

    def test_wrong_private_key_signature(self):
        self.reject(signed=(replace(self.signed[0],
            signature=self.signed[1].signature), self.signed[1]))

    def test_swapped_replay_role(self):
        self.reject(signed=(replace(self.signed[0],
            role="REPLAY_WITNESS"), self.signed[1]))

    def test_registry_role_cannot_be_replay_role(self):
        self.reject(signed=(replace(self.signed[0], role="STATE"), self.signed[1]))

    def test_wrong_key_id(self):
        self.reject(signed=(replace(self.signed[0], key_id="missing"),
                            self.signed[1]))

    def test_wrong_authority_id(self):
        self.reject(signed=(replace(self.signed[0],
            authority_id="other-replay-state"), self.signed[1]))

    def test_wrong_registry(self):
        self.reject(signed=(replace(self.signed[0], registry_id="other"),
                            self.signed[1]))

    def test_wrong_ledger(self):
        self.reject(signed=(replace(self.signed[0], ledger_id="other"),
                            self.signed[1]))

    def test_wrong_request(self):
        self.reject(signed=(replace(self.signed[0], request_id="other"),
                            self.signed[1]))

    def test_wrong_challenge(self):
        self.reject(signed=(replace(self.signed[0], challenge_hex="b" * 64),
                            self.signed[1]))

    def test_wrong_response_status(self):
        self.reject(signed=(replace(self.signed[0],
            response_status="COMMITTED"), self.signed[1]))

    def test_wrong_body_commitment(self):
        self.reject(signed=(replace(self.signed[0], body_digest="b" * 64),
                            self.signed[1]))

    def test_wrong_position_commitment(self):
        self.reject(signed=(replace(self.signed[0],
            position_digest="b" * 64), self.signed[1]))

    def test_wrong_ledger_commitment(self):
        self.reject(signed=(replace(self.signed[0], ledger_digest="b" * 64),
                            self.signed[1]))

    def test_wrong_generation(self):
        self.reject(signed=(replace(self.signed[0], generation=2),
                            self.signed[1]))

    def test_wrong_policy_epoch(self):
        self.reject(signed=(replace(self.signed[0], policy_epoch=2),
                            self.signed[1]))

    def test_wrong_recovery_epoch(self):
        self.reject(signed=(replace(self.signed[0], recovery_epoch=2),
                            self.signed[1]))

    def test_wrong_transition_id(self):
        self.reject(signed=(replace(self.signed[0], transition_id="wrong"),
                            self.signed[1]))

    def test_wrong_algorithm(self):
        self.reject(signed=(replace(self.signed[0], algorithm="none"),
                            self.signed[1]))

    def test_wrong_purpose(self):
        self.reject(signed=(replace(self.signed[0],
            purpose=PURPOSES["REPLAY_WITNESS"]), self.signed[1]))

    def test_wrong_protocol_version(self):
        self.reject(signed=(replace(self.signed[0], protocol_version=2),
                            self.signed[1]))

    def test_invalid_signature_encoding(self):
        self.reject(signed=(replace(self.signed[0], signature="!") ,
                            self.signed[1]))

    def test_invalid_signature_noncanonical(self):
        self.reject(signed=(replace(self.signed[0], signature="_" * 86),
                            self.signed[1]))

    def test_disabled_key(self):
        self.reject(policy=self.change_key("REPLAY_STATE", status="disabled"))

    def test_revoked_key(self):
        self.reject(policy=self.change_key("REPLAY_STATE", status="revoked"))

    def test_wrong_key_purpose(self):
        self.reject(policy=self.change_key(
            "REPLAY_STATE", purpose=PURPOSES["REPLAY_WITNESS"]))

    def test_duplicate_key_identity(self):
        self.reject(policy=replace(self.policy,
            keys=self.policy.keys + (self.policy.keys[0],)))

    def test_cross_role_key_reuse(self):
        self.reject(policy=self.change_key(
            "REPLAY_WITNESS",
            public_key_hex=self.policy.keys[0].public_key_hex))

    def test_invalid_key_material(self):
        self.reject(policy=self.change_key("REPLAY_STATE", public_key_hex="0" * 64))

    def test_wrong_key_policy_epoch(self):
        self.reject(policy=replace(self.policy, epoch=2))

    def test_wrong_key_policy_id(self):
        self.reject(policy=replace(self.policy, policy_id="registry-policy"))

    def test_early_supplied_time(self):
        self.reject(now=datetime(2026, 10, 12, tzinfo=timezone.utc))

    def test_expired_supplied_time(self):
        self.reject(now=datetime(2026, 10, 15, tzinfo=timezone.utc))

    def test_naive_time(self):
        self.reject(now=datetime(2026, 10, 14))

    def test_time_is_not_independently_trusted(self):
        self.assertFalse(self.verify().trusted_time_verified)

    def test_wrong_evidence_authority(self):
        self.reject(evidence=(replace(self.state, authority_id="impostor"),
                              self.witness))

    def test_wrong_evidence_role(self):
        self.reject(evidence=(replace(self.state, role="REPLAY_WITNESS"),
                              self.witness))

    def test_wrong_evidence_challenge(self):
        self.reject(evidence=(replace(self.state, challenge_hex="b" * 64),
                              self.witness))

    def test_wrong_evidence_body_digest(self):
        self.reject(evidence=(replace(self.state, body_digest="f" * 64),
                              self.witness))

    def test_wrong_evidence_ledger_commitment(self):
        forged = replace(self.state_body,
                         position=replace(self.position, ledger_digest="f" * 64))
        self.reject(evidence=(replace(self.state, body=forged), self.witness))

    def test_wrong_evidence_policy_epoch(self):
        bad = replace(self.position, policy_epoch=2)
        self.reject(evidence=(replace(self.state,
            body=ReplayStateReadBody(self.ledger, bad)), self.witness))

    def test_wrong_evidence_recovery_epoch(self):
        bad = replace(self.position, recovery_epoch=2)
        self.reject(evidence=(replace(self.state,
            body=ReplayStateReadBody(self.ledger, bad)), self.witness))

    def test_wrong_challenge_purpose(self):
        self.reject(challenge=replace(self.challenge, purpose="DEPLOY"))

    def test_wrong_challenge_authority(self):
        self.reject(challenge=replace(self.challenge,
            state_authority_id="other"))

    def test_duplicate_challenge_authorities(self):
        self.reject(challenge=replace(self.challenge,
            witness_authority_id=self.challenge.state_authority_id))

    def test_duplicate_signed_json_key(self):
        raw = canonical_signed_replay_bytes(self.signed[0]).decode("ascii")
        duplicate = raw.replace('{', '{"role":"REPLAY_STATE",', 1).encode()
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(duplicate)

    def test_unknown_signed_json_key(self):
        value = json.loads(canonical_signed_replay_bytes(self.signed[0]))
        value["extra"] = "bogus"
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(json.dumps(value, sort_keys=True,
                separators=(",", ":")).encode())

    def test_missing_signed_json_key(self):
        value = json.loads(canonical_signed_replay_bytes(self.signed[0]))
        del value["role"]
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(json.dumps(value, sort_keys=True,
                separators=(",", ":")).encode())

    def test_noncanonical_signed_json(self):
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(json.dumps(
                json.loads(canonical_signed_replay_bytes(self.signed[0])),
                indent=2,
            ).encode())

    def test_invalid_json_bytes(self):
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(b"not-json")

    def test_oversized_wire_message(self):
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(b"x" * (MAX_SIGNED_BYTES + 1))

    def test_boolean_generation_on_wire(self):
        value = json.loads(canonical_signed_replay_bytes(self.signed[0]))
        value["generation"] = True
        raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        with self.assertRaises(ValueError):
            parse_signed_replay_bytes(raw)

    def test_cross_request_replay(self):
        self.reject(challenge=replace(self.challenge, request_id="other"))

    def test_fresh_signed_state_may_be_behind_witness(self):
        # A self-consistent, but independently UNTRUSTED, witness can be ahead.
        ahead = replace(self.position,
            generation=1, previous_position_digest="b" * 64,
            transition_id="transition-1")
        ev = self.evidence("REPLAY_WITNESS", ReplayWitnessCheckpoint(ahead))
        signed = self.sign("REPLAY_WITNESS", ev)
        result = self.verify(signed=(self.signed[0], signed),
                             evidence=(self.state, ev))
        self.assertEqual(result.reconciliation_classification,
                         "REPLAY_WITNESS_AHEAD_UNTRUSTED")
        self.assertFalse(result.protected_state_currentness_verified)

    def test_fresh_signed_state_ahead_of_witness(self):
        ledger = ReplayLedgerSnapshot(REGISTRY_ID, 1, ())
        ahead = replace(self.position, generation=1,
            ledger_digest=untrusted_ledger_commitment(ledger),
            previous_position_digest="b" * 64,
            transition_id="transition-1")
        ev = self.evidence("REPLAY_STATE", ReplayStateReadBody(ledger, ahead))
        signed = self.sign("REPLAY_STATE", ev)
        result = self.verify(signed=(signed, self.signed[1]),
                             evidence=(ev, self.witness))
        self.assertEqual(result.reconciliation_classification,
                         "REPLAY_STATE_AHEAD_UNTRUSTED")

    def test_matching_generation_conflicting_position(self):
        different = replace(self.position, transition_id="alternate-0")
        ev = self.evidence("REPLAY_WITNESS", ReplayWitnessCheckpoint(different))
        signed = self.sign("REPLAY_WITNESS", ev)
        result = self.verify(signed=(self.signed[0], signed),
                             evidence=(self.state, ev))
        self.assertEqual(result.reconciliation_classification,
                         "CONFLICTING_UNTRUSTED")


if __name__ == "__main__":
    unittest.main()
