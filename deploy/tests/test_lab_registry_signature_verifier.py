#!/usr/bin/env python3
"""Gate 4D.22C.3D.11B: offline admin registry signature tests."""

import base64
from copy import deepcopy
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from lab_registry_wire_format import (
    REGISTRY_DOMAIN_PREFIX,
    REGISTRY_PURPOSE,
    canonical_registry_bytes,
    parse_signed_registry_bytes,
    registry_signing_bytes,
)
from lab_registry_signature_verifier import (
    ADMIN_POLICY_ID,
    AdministrativeKeyRecord,
    AdministrativeKeyPolicy,
    validate_administrative_policy,
    verify_registry_signature_bytes,
)
from test_lab_collector_trust_policy import sample_key

NOW = datetime(2026, 10, 13, 8, 0, 30, tzinfo=timezone.utc)


def public_hex(private):
    return private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()


def sign_document(document, private):
    document["signature"] = base64.urlsafe_b64encode(
        private.sign(registry_signing_bytes(document))
    ).decode("ascii").rstrip("=")
    return canonical_registry_bytes(document)


def sample_case():
    admin_private = Ed25519PrivateKey.generate()
    collector_private = Ed25519PrivateKey.generate()
    admin = AdministrativeKeyRecord(
        key_id="admin-001", public_key_hex=public_hex(admin_private),
        algorithm="Ed25519", purpose=REGISTRY_PURPOSE,
        valid_from="2026-10-13T07:00:00Z",
        valid_until="2026-10-13T09:00:00Z", status="active",
    )
    policy = AdministrativeKeyPolicy(
        policy_id=ADMIN_POLICY_ID, keys=(admin,),
    )
    collector = replace(sample_key(), public_key_hex=public_hex(collector_private))
    document = {
        "registry_format_version": 1,
        "registry_id": "fbweb-lab-collector-registry-v1",
        "revision": 1,
        "previous_revision": 0,
        "previous_digest": "0" * 64,
        "issuer_key_id": "admin-001",
        "purpose": REGISTRY_PURPOSE,
        "algorithm": "Ed25519",
        "issued_at": "2026-10-13T08:00:00Z",
        "expires_at": "2026-10-13T08:04:00Z",
        "keys": [asdict(collector)],
        "signature": "A" * 86,
    }
    raw = sign_document(document, admin_private)
    return raw, document, policy, admin_private


class OfflineRegistrySignatureTests(unittest.TestCase):
    def verify(self, raw, policy, now=NOW):
        return verify_registry_signature_bytes(raw, policy, now=now)

    def test_valid_signature_remains_non_authorizing(self):
        raw, _, policy, _ = sample_case()
        result = self.verify(raw, policy)
        self.assertTrue(result.registry_structure_valid)
        self.assertTrue(result.registry_signature_verified)
        self.assertTrue(result.administrative_key_policy_eligible)
        self.assertTrue(result.declared_window_matches)
        self.assertEqual(result.registry_revision, 1)
        self.assertEqual(len(result.registry_signing_digest), 64)
        self.assertEqual(len(result.registry_declaration.keys), 1)
        for name in (
            "registry_provenance_authenticated", "administrative_identity_authenticated",
            "trusted_time_source_verified", "registry_revision_current",
            "registry_freshness_verified", "rollback_prevention_verified",
            "collector_authenticated", "evidence_signature_verified",
            "replay_prevention_verified", "runtime_evidence_verified",
            "isolation_proven", "docker_execution_permitted",
            "production_execution_enabled", "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, name), name)
        self.assertTrue(result.manual_verification_required)

    def test_signed_bytes_have_separate_domain(self):
        _, document, _, _ = sample_case()
        self.assertTrue(registry_signing_bytes(document).startswith(REGISTRY_DOMAIN_PREFIX))
        self.assertNotIn(b'"signature"', registry_signing_bytes(document))
        self.assertNotEqual(REGISTRY_DOMAIN_PREFIX, b"FBWEB-LAB-RUNTIME-EVIDENCE-SIGNATURE-V1\x00")

    def test_original_json_round_trip(self):
        raw, document, _, _ = sample_case()
        self.assertEqual(parse_signed_registry_bytes(raw), document)

    def test_modified_collector_status_without_resigning_fails(self):
        _, document, policy, _ = sample_case()
        document["keys"][0]["status"] = "revoked"
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_modified_collector_public_key_without_resigning_fails(self):
        _, document, policy, _ = sample_case()
        document["keys"][0]["public_key_hex"] = "a" * 64
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_signature_from_wrong_private_key_fails(self):
        _, document, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(sign_document(document, Ed25519PrivateKey.generate()), policy)

    def test_wrong_public_key_fails(self):
        raw, _, policy, _ = sample_case()
        wrong_key = replace(policy.keys[0], public_key_hex=public_hex(Ed25519PrivateKey.generate()))
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(wrong_key,)))

    def test_unknown_issuer_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(replace(policy.keys[0], key_id="different"),)))

    def test_disabled_admin_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(replace(policy.keys[0], status="disabled"),)))

    def test_revoked_admin_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(replace(policy.keys[0], status="revoked"),)))

    def test_wrong_admin_purpose_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(replace(policy.keys[0], purpose="fbweb-lab-runtime-evidence"),)))

    def test_wrong_admin_algorithm_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(replace(policy.keys[0], algorithm="none"),)))

    def test_admin_role_overlap_collector_key_fails(self):
        _, document, policy, private = sample_case()
        document["keys"][0]["public_key_hex"] = public_hex(private)
        with self.assertRaises(ValueError):
            self.verify(sign_document(document, private), policy)

    def test_wrong_registry_purpose_fails(self):
        _, document, policy, _ = sample_case()
        document["purpose"] = "fbweb-lab-runtime-evidence"
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_algorithm_substitution_fails(self):
        _, document, policy, _ = sample_case()
        document["algorithm"] = "none"
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_unknown_wire_version_fails(self):
        _, document, policy, _ = sample_case()
        document["registry_format_version"] = 2
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_extra_trust_anchor_field_fails(self):
        _, document, policy, _ = sample_case()
        document["trusted_public_key"] = "a" * 64
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_wrong_registry_identity_fails(self):
        _, document, policy, _ = sample_case()
        document["registry_id"] = "untrusted"
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_duplicate_top_level_json_key_fails(self):
        raw, _, policy, _ = sample_case()
        raw = raw.replace(b'"revision":1', b'"revision":1,"revision":1', 1)
        with self.assertRaises(ValueError):
            self.verify(raw, policy)

    def test_duplicate_nested_json_key_fails(self):
        raw, _, policy, _ = sample_case()
        raw = raw.replace(b'"status":"active"', b'"status":"active","status":"active"', 1)
        with self.assertRaises(ValueError):
            self.verify(raw, policy)

    def test_noncanonical_whitespace_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw + b" ", policy)

    def test_malformed_signature_fails(self):
        _, document, policy, _ = sample_case()
        document["signature"] = "invalid"
        with self.assertRaises(ValueError):
            self.verify(canonical_registry_bytes(document), policy)

    def test_bad_raw_input_fails(self):
        _, document, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(document, policy)

    def test_expired_registry_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, policy, now=datetime(2026, 10, 13, 8, 5, tzinfo=timezone.utc))

    def test_future_issued_registry_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, policy, now=datetime(2026, 10, 13, 7, 59, tzinfo=timezone.utc))

    def test_naive_time_fails(self):
        raw, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            self.verify(raw, policy, now=datetime(2026, 10, 13, 8, 0))

    def test_admin_expiry_before_registry_expiry_fails(self):
        raw, _, policy, _ = sample_case()
        key = replace(policy.keys[0], valid_until="2026-10-13T08:02:00Z")
        with self.assertRaises(ValueError):
            self.verify(raw, replace(policy, keys=(key,)))

    def test_duplicate_admin_key_id_fails(self):
        _, _, policy, _ = sample_case()
        second = replace(policy.keys[0], public_key_hex=public_hex(Ed25519PrivateKey.generate()))
        with self.assertRaises(ValueError):
            validate_administrative_policy(replace(policy, keys=(policy.keys[0], second)))

    def test_admin_public_key_reuse_fails(self):
        _, _, policy, _ = sample_case()
        second = replace(policy.keys[0], key_id="admin-002")
        with self.assertRaises(ValueError):
            validate_administrative_policy(replace(policy, keys=(policy.keys[0], second)))

    def test_bad_admin_policy_identity_fails(self):
        _, _, policy, _ = sample_case()
        with self.assertRaises(ValueError):
            validate_administrative_policy(replace(policy, policy_id="attacker"))

    def test_unsorted_registry_keys_fail(self):
        _, document, policy, private = sample_case()
        first = document["keys"][0]
        second = dict(first, key_id="key-000", public_key_hex="b" * 64)
        document["keys"] = [first, second]
        with self.assertRaises(ValueError):
            sign_document(document, private)

    def test_duplicate_collector_key_identity_fails(self):
        _, document, policy, private = sample_case()
        document["keys"].append(dict(document["keys"][0]))
        with self.assertRaises(ValueError):
            sign_document(document, private)

    def test_previous_revision_mismatch_fails(self):
        _, document, policy, private = sample_case()
        document["revision"] = 2
        document["previous_revision"] = 0
        document["previous_digest"] = "a" * 64
        with self.assertRaises(ValueError):
            sign_document(document, private)

    def test_nonzero_genesis_digest_fails(self):
        _, document, policy, private = sample_case()
        document["previous_digest"] = "b" * 64
        with self.assertRaises(ValueError):
            sign_document(document, private)

    def test_valid_higher_revision_does_not_prove_currentness(self):
        _, document, policy, private = sample_case()
        document["revision"] = 2
        document["previous_revision"] = 1
        document["previous_digest"] = "c" * 64
        result = self.verify(sign_document(document, private), policy)
        self.assertEqual(result.registry_revision, 2)
        self.assertTrue(result.registry_signature_verified)
        self.assertFalse(result.registry_revision_current)
        self.assertFalse(result.rollback_prevention_verified)

    def test_reverification_does_not_prevent_replay(self):
        raw, _, policy, _ = sample_case()
        self.assertFalse(self.verify(raw, policy).replay_prevention_verified)
        self.assertFalse(self.verify(raw, policy).replay_prevention_verified)

    def test_inputs_are_not_mutated(self):
        raw, document, policy, _ = sample_case()
        policy_copy = deepcopy(policy)
        document_copy = deepcopy(document)
        self.verify(raw, policy)
        self.assertEqual(policy, policy_copy)
        self.assertEqual(document, document_copy)


if __name__ == "__main__":
    unittest.main()
