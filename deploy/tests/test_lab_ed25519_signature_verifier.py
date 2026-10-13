#!/usr/bin/env python3
"""Gate 4D.22C.3D.10 Ed25519 verification security tests."""

from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
import base64
import sys
import unittest


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from lab_ed25519_signature_verifier import (
    verify_lab_signature_bytes,
)
from lab_runtime_auth_envelope import signing_payload
from lab_runtime_canonical_payload import (
    DOMAIN_PREFIX,
    canonical_json_bytes,
)
from test_lab_runtime_auth_envelope import (
    NOW,
    expected_binding,
    sample_envelope,
)
from test_lab_collector_trust_policy import (
    sample_key,
    sample_registry,
)


def make_signed_case():
    """Create one ephemeral, test-only signing context."""
    private_key = Ed25519PrivateKey.generate()

    public_key_hex = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()

    key_record = replace(
        sample_key(),
        public_key_hex=public_key_hex,
    )

    registry = replace(
        sample_registry(),
        keys=(key_record,),
    )

    envelope = sample_envelope()

    signature = private_key.sign(
        signing_payload(envelope)
    )

    envelope["signature"] = (
        base64.urlsafe_b64encode(signature)
        .decode("ascii")
        .rstrip("=")
    )

    return (
        canonical_json_bytes(envelope),
        expected_binding(),
        registry,
        private_key,
        envelope,
    )


class Ed25519SignatureVerificationTests(unittest.TestCase):

    def verify(self, raw, expected, registry, now=NOW):
        return verify_lab_signature_bytes(
            raw,
            expected,
            registry,
            now=now,
        )

    def test_valid_signature_does_not_authorize_execution(self):
        raw, expected, registry, _, _ = make_signed_case()

        result = self.verify(raw, expected, registry)

        self.assertTrue(result.schema_valid)
        self.assertTrue(result.envelope_valid)
        self.assertTrue(result.collector_key_policy_eligible)
        self.assertTrue(result.signature_verified)
        self.assertTrue(result.expected_binding_matches)

        self.assertFalse(result.registry_authenticity_verified)
        self.assertFalse(result.collector_authenticated)
        self.assertFalse(result.trusted_time_source_verified)
        self.assertFalse(result.freshness_verified)
        self.assertFalse(result.replay_prevention_verified)
        self.assertFalse(result.runtime_evidence_verified)
        self.assertFalse(result.vm_identity_proven)
        self.assertFalse(result.daemon_identity_proven)
        self.assertFalse(result.isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.production_execution_enabled)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_valid_signature_over_claims_is_not_isolation_proof(self):
        raw, expected, registry, _, _ = make_signed_case()

        result = self.verify(raw, expected, registry)

        self.assertTrue(result.signature_verified)
        self.assertFalse(result.isolation_proven)

    def test_zero_signature_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["signature"] = (
            base64.urlsafe_b64encode(bytes(64))
            .decode("ascii")
            .rstrip("=")
        )

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_modified_evidence_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["evidence"]["provenance"][
            "source_digest"
        ] = "b" * 64

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_modified_configuration_digest_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["evidence"]["vm"][
            "configuration_digest"
        ] = "c" * 64

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_modified_challenge_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["challenge"] = "d" * 64
        modified_expected = replace(
            expected,
            challenge="d" * 64,
        )

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                modified_expected,
                registry,
            )

    def test_wrong_private_key_signature_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        other_key = Ed25519PrivateKey.generate()

        envelope["signature"] = (
            base64.urlsafe_b64encode(
                other_key.sign(signing_payload(envelope))
            )
            .decode("ascii")
            .rstrip("=")
        )

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_substituted_registry_key_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        other_key = Ed25519PrivateKey.generate()

        other_public = other_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()

        modified_registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    public_key_hex=other_public,
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(
                raw,
                expected,
                modified_registry,
            )

    def test_revoked_key_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    status="revoked",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_disabled_key_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    status="disabled",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_unknown_collector_key_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    key_id="unknown-key",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_wrong_vm_scope_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    vm_id="another-vm",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_wrong_daemon_scope_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    daemon_id="another-daemon",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_expired_envelope_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        with self.assertRaises(ValueError):
            self.verify(
                raw,
                expected,
                registry,
                now=datetime(
                    2026, 10, 13, 8, 5,
                    tzinfo=timezone.utc,
                ),
            )

    def test_future_dated_envelope_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["issued_at"] = "2026-10-13T08:01:00Z"

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_wrong_purpose_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["purpose"] = "production-deployment"

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_algorithm_substitution_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        envelope["algorithm"] = "none"

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_duplicate_json_key_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        raw = raw.replace(
            b'"key_id":"key-001"',
            b'"key_id":"key-001","key_id":"key-001"',
            1,
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_noncanonical_json_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        with self.assertRaises(ValueError):
            self.verify(raw + b" ", expected, registry)

    def test_preparsed_dictionary_is_rejected(self):
        raw, expected, registry, _, envelope = make_signed_case()

        with self.assertRaises(ValueError):
            self.verify(envelope, expected, registry)

    def test_invalid_public_key_encoding_is_rejected(self):
        raw, expected, registry, _, _ = make_signed_case()

        registry = replace(
            registry,
            keys=(
                replace(
                    registry.keys[0],
                    public_key_hex="bad",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self.verify(raw, expected, registry)

    def test_non_domain_separated_signature_is_rejected(self):
        raw, expected, registry, private_key, envelope = (
            make_signed_case()
        )

        message = signing_payload(envelope)

        self.assertTrue(message.startswith(DOMAIN_PREFIX))

        signature = private_key.sign(
            message[len(DOMAIN_PREFIX):]
        )

        envelope["signature"] = (
            base64.urlsafe_b64encode(signature)
            .decode("ascii")
            .rstrip("=")
        )

        with self.assertRaises(ValueError):
            self.verify(
                canonical_json_bytes(envelope),
                expected,
                registry,
            )

    def test_crypto_library_failure_fails_closed(self):
        raw, expected, registry, _, _ = make_signed_case()

        with patch(
            "lab_ed25519_signature_verifier."
            "Ed25519PublicKey.from_public_bytes",
            side_effect=ValueError("invalid public key"),
        ):
            with self.assertRaises(ValueError):
                self.verify(raw, expected, registry)

    def test_repeated_verification_does_not_claim_replay_protection(self):
        raw, expected, registry, _, _ = make_signed_case()

        first = self.verify(raw, expected, registry)
        second = self.verify(raw, expected, registry)

        self.assertTrue(first.signature_verified)
        self.assertTrue(second.signature_verified)

        self.assertFalse(first.replay_prevention_verified)
        self.assertFalse(second.replay_prevention_verified)

    def test_caller_controlled_registry_is_not_authenticated(self):
        # This deliberately demonstrates the remaining trust gap.
        raw, expected, registry, _, _ = make_signed_case()

        result = self.verify(raw, expected, registry)

        self.assertTrue(result.signature_verified)
        self.assertFalse(result.registry_authenticity_verified)
        self.assertFalse(result.collector_authenticated)

    def test_input_is_not_mutated(self):
        raw, expected, registry, _, _ = make_signed_case()

        original_registry = deepcopy(registry)
        original_raw = bytes(raw)

        self.verify(raw, expected, registry)

        self.assertEqual(registry, original_registry)
        self.assertEqual(raw, original_raw)


if __name__ == "__main__":
    unittest.main()
