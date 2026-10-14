#!/usr/bin/env python3
"""Gate 4D.22C.3D.12H adversarial offline signature tests."""

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

from lab_authority_signature_verifier import (
    AuthorityResponseKey,
    AuthorityResponseKeyPolicy,
    SignedAuthorityResponse,
    POLICY_ID,
    PURPOSES,
    authority_response_signing_bytes,
    canonical_signed_authority_bytes,
    parse_signed_authority_bytes,
    validate_authority_response_key_policy,
    verify_authority_response_signatures,
)
from lab_runtime_auth_envelope import ALGORITHM
from test_lab_authority_evidence_contract import case

NOW = datetime(2026, 10, 14, 2, 0, tzinfo=timezone.utc)


class AuthoritySignatureTests(unittest.TestCase):
    def setUp(self):
        self.challenge, self.state, self.witness, self.admin = case()
        self.private = {}
        keys = []

        for role, evidence in (
            ("STATE", self.state),
            ("WITNESS", self.witness),
            ("ADMIN", self.admin),
        ):
            private = Ed25519PrivateKey.generate()
            self.private[role] = private
            keys.append(AuthorityResponseKey(
                role=role,
                authority_id=evidence.authority_id,
                key_id="test-key-" + role.lower(),
                public_key_hex=private.public_key().public_bytes(
                    Encoding.Raw, PublicFormat.Raw
                ).hex(),
                algorithm=ALGORITHM,
                purpose=PURPOSES[role],
                status="active",
                valid_from="2026-10-13T00:00:00Z",
                valid_until="2026-10-15T00:00:00Z",
            ))

        self.policy = AuthorityResponseKeyPolicy(POLICY_ID, tuple(keys))
        self.signed = tuple(
            self.sign(role, evidence)
            for role, evidence in (
                ("STATE", self.state),
                ("WITNESS", self.witness),
                ("ADMIN", self.admin),
            )
        )

    def sign(self, role, evidence):
        record = SignedAuthorityResponse(
            role=role,
            authority_id=evidence.authority_id,
            key_id="test-key-" + role.lower(),
            registry_id=evidence.registry_id,
            request_id=evidence.request_id,
            challenge_hex=evidence.challenge_hex,
            body_digest=evidence.body_digest,
            envelope_digest=evidence.envelope_digest,
            policy_epoch=self.state.body.position.policy_epoch,
            algorithm=ALGORITHM,
            purpose=PURPOSES[role],
            signature="",
        )
        signature = self.private[role].sign(
            authority_response_signing_bytes(record)
        )
        return replace(
            record,
            signature=base64.urlsafe_b64encode(
                signature
            ).decode("ascii").rstrip("="),
        )

    def verify(self, *, signed=None, policy=None, now=NOW, evidence=None):
        a, b, c = self.signed if signed is None else signed
        state, witness, admin = (
            (self.state, self.witness, self.admin)
            if evidence is None else evidence
        )
        return verify_authority_response_signatures(
            self.challenge, state, witness, admin,
            a, b, c,
            self.policy if policy is None else policy,
            now=now,
        )

    def reject(self, **kwargs):
        with self.assertRaises(ValueError):
            self.verify(**kwargs)

    def changed_key(self, role, **changes):
        return replace(
            self.policy,
            keys=tuple(
                replace(key, **changes) if key.role == role else key
                for key in self.policy.keys
            ),
        )

    def test_three_valid_ed25519_signatures(self):
        result = self.verify()
        self.assertTrue(result.state_signature_verified_under_supplied_key)
        self.assertTrue(result.witness_signature_verified_under_supplied_key)
        self.assertTrue(result.admin_signature_verified_under_supplied_key)

    def test_every_operational_trust_claim_remains_false(self):
        result = self.verify()
        for name in (
            "independent_authority_identity_authenticated",
            "administrative_policy_authenticated",
            "state_authority_authenticated",
            "rollback_witness_authenticated",
            "independently_trusted_key_provenance_verified",
            "trusted_time_verified",
            "challenge_uniqueness_verified",
            "replay_prevention_verified",
            "authoritative_currentness_verified",
            "protected_state_commit_verified",
            "rollback_prevention_verified",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "production_execution_enabled",
            "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, name), name)
        self.assertTrue(result.manual_verification_required)

    def test_immutable_result(self):
        result = self.verify()
        with self.assertRaises(FrozenInstanceError):
            result.revision = 2

    def test_signature_invalid_after_character_tamper(self):
        original = self.signed[0].signature
        changed = ("A" if original[0] != "A" else "B") + original[1:]
        bad = replace(self.signed[0], signature=changed)
        self.reject(signed=(bad, *self.signed[1:]))

    def test_signature_wrong_private_key(self):
        swapped = replace(
            self.signed[0], signature=self.signed[1].signature
        )
        self.reject(signed=(swapped, *self.signed[1:]))

    def test_wrong_signing_key_id(self):
        self.reject(signed=(
            replace(self.signed[0], key_id="other-key"),
            *self.signed[1:],
        ))

    def test_wrong_state_authority_id(self):
        self.reject(signed=(
            replace(self.signed[0], authority_id="fake-state"),
            *self.signed[1:],
        ))

    def test_wrong_role(self):
        self.reject(signed=(
            replace(self.signed[0], role="WITNESS"),
            *self.signed[1:],
        ))

    def test_wrong_signing_purpose(self):
        self.reject(signed=(
            replace(self.signed[0], purpose=PURPOSES["WITNESS"]),
            *self.signed[1:],
        ))

    def test_wrong_signing_algorithm(self):
        self.reject(signed=(
            replace(self.signed[0], algorithm="none"),
            *self.signed[1:],
        ))

    def test_wrong_registry_id(self):
        self.reject(signed=(
            replace(self.signed[0], registry_id="other"),
            *self.signed[1:],
        ))

    def test_wrong_request_id(self):
        self.reject(signed=(
            replace(self.signed[0], request_id="other-request"),
            *self.signed[1:],
        ))

    def test_wrong_challenge(self):
        self.reject(signed=(
            replace(self.signed[0], challenge_hex="b" * 64),
            *self.signed[1:],
        ))

    def test_modified_body_digest(self):
        self.reject(signed=(
            replace(self.signed[0], body_digest="c" * 64),
            *self.signed[1:],
        ))

    def test_modified_envelope_digest(self):
        other = (
            "c" * 64
            if self.signed[0].envelope_digest != "c" * 64
            else "d" * 64
        )
        self.reject(signed=(
            replace(self.signed[0], envelope_digest=other),
            *self.signed[1:],
        ))

    def test_modified_policy_epoch(self):
        self.reject(signed=(
            replace(self.signed[0], policy_epoch=2),
            *self.signed[1:],
        ))

    def test_boolean_policy_epoch(self):
        self.reject(signed=(
            replace(self.signed[0], policy_epoch=True),
            *self.signed[1:],
        ))

    def test_absent_signature(self):
        self.reject(signed=(
            replace(self.signed[0], signature=""),
            *self.signed[1:],
        ))

    def test_noncanonical_signature_encoding(self):
        self.reject(signed=(
            replace(
                self.signed[0],
                signature=self.signed[0].signature + "==",
            ),
            *self.signed[1:],
        ))

    def test_wrong_public_key(self):
        different = Ed25519PrivateKey.generate().public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        ).hex()
        self.reject(policy=self.changed_key(
            "STATE", public_key_hex=different
        ))

    def test_disabled_signing_key(self):
        self.reject(policy=self.changed_key(
            "STATE", status="disabled"
        ))

    def test_revoked_signing_key(self):
        self.reject(policy=self.changed_key(
            "WITNESS", status="revoked"
        ))

    def test_missing_signing_key(self):
        self.reject(policy=replace(
            self.policy, keys=self.policy.keys[1:]
        ))

    def test_unapproved_policy_id(self):
        self.reject(policy=replace(
            self.policy, policy_id="fake-policy"
        ))

    def test_duplicate_signer(self):
        self.reject(policy=replace(
            self.policy,
            keys=self.policy.keys + (self.policy.keys[0],),
        ))

    def test_reused_public_key_across_roles(self):
        self.reject(policy=self.changed_key(
            "WITNESS",
            public_key_hex=self.policy.keys[0].public_key_hex,
        ))

    def test_key_not_yet_valid(self):
        self.reject(now=datetime(
            2026, 10, 12, tzinfo=timezone.utc
        ))

    def test_key_expired(self):
        self.reject(now=datetime(
            2026, 10, 16, tzinfo=timezone.utc
        ))

    def test_naive_assessment_time(self):
        self.reject(now=datetime(2026, 10, 14))

    def test_missing_assessment_time(self):
        self.reject(now=None)

    def test_valid_signature_with_same_challenge_can_be_replayed(self):
        self.assertTrue(
            self.verify().state_signature_verified_under_supplied_key
        )
        self.assertFalse(self.verify().replay_prevention_verified)

    def test_self_selected_policy_not_independent_provenance(self):
        self.assertFalse(
            self.verify().independently_trusted_key_provenance_verified
        )

    def test_canonical_wire_round_trip(self):
        raw = canonical_signed_authority_bytes(self.signed[0])
        self.assertEqual(
            parse_signed_authority_bytes(raw),
            self.signed[0],
        )

    def test_noncanonical_wire_spacing_rejected(self):
        raw = canonical_signed_authority_bytes(self.signed[0])
        with self.assertRaises(ValueError):
            parse_signed_authority_bytes(
                raw.replace(b",", b", ", 1)
            )

    def test_duplicate_wire_key_rejected(self):
        raw = canonical_signed_authority_bytes(self.signed[0])
        bad = raw[:-1] + b',"role":"STATE"}'
        with self.assertRaises(ValueError):
            parse_signed_authority_bytes(bad)

    def test_unknown_wire_field_rejected(self):
        raw = canonical_signed_authority_bytes(self.signed[0])
        bad = raw[:-1] + b',"extra":"unapproved"}'
        with self.assertRaises(ValueError):
            parse_signed_authority_bytes(bad)

    def test_numeric_float_wire_rejected(self):
        raw = canonical_signed_authority_bytes(self.signed[0])
        bad = raw.replace(
            b'"policy_epoch":1',
            b'"policy_epoch":1.0',
        )
        with self.assertRaises(ValueError):
            parse_signed_authority_bytes(bad)

    def test_noncanonical_key_order_rejected(self):
        raw = canonical_signed_authority_bytes(self.signed[0])
        object_value = json.loads(raw)
        pairs = list(object_value.items())[::-1]

        reordered = b"{" + b",".join(
            json.dumps(k).encode("ascii")
            + b":"
            + json.dumps(v).encode("ascii")
            for k, v in pairs
        ) + b"}"

        with self.assertRaises(ValueError):
            parse_signed_authority_bytes(reordered)

    def test_oversized_wire_rejected(self):
        with self.assertRaises(ValueError):
            parse_signed_authority_bytes(b"a" * 5000)

    def test_tampered_evidence_even_when_signature_unchanged(self):
        changed = replace(
            self.state, request_id="other-request"
        )
        self.reject(evidence=(
            changed, self.witness, self.admin
        ))

    def test_signature_domain_separation(self):
        self.assertNotEqual(
            authority_response_signing_bytes(self.signed[0]),
            authority_response_signing_bytes(self.signed[1]),
        )

    def test_policy_schema_is_not_authentication(self):
        self.assertTrue(
            validate_authority_response_key_policy(self.policy)
        )
        self.assertFalse(
            self.verify().state_authority_authenticated
        )


if __name__ == "__main__":
    unittest.main()
