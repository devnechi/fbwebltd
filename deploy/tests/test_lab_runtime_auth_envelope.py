#!/usr/bin/env python3
"""Gate 4D.22C.3D.6 authentication-envelope contract tests."""

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import base64
import sys
import unittest


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_runtime_auth_envelope import (
    ExpectedBinding,
    PURPOSE,
    signing_payload,
    validate_envelope,
)
from test_lab_runtime_evidence_schema import sample_evidence


NOW = datetime(2026, 10, 13, 8, 0, 30, tzinfo=timezone.utc)
CHALLENGE = "c" * 64


def expected_binding():
    return ExpectedBinding(
        collector_id="offline-collector",
        key_id="key-001",
        vm_id="vm-001",
        daemon_id="daemon-001",
        challenge=CHALLENGE,
        collection_id="collection-001",
    )


def sample_envelope():
    evidence = sample_evidence()
    evidence["provenance"]["collected_at"] = "2026-10-13T08:00:00Z"

    return {
        "envelope_version": 1,
        "purpose": PURPOSE,
        "algorithm": "Ed25519",
        "collector_id": "offline-collector",
        "key_id": "key-001",
        "challenge": CHALLENGE,
        "issued_at": "2026-10-13T08:00:10Z",
        "expires_at": "2026-10-13T08:04:10Z",
        "evidence": evidence,
        # Format-valid placeholder, never a verified signature.
        "signature": base64.urlsafe_b64encode(
            bytes(64)
        ).decode("ascii").rstrip("="),
    }


class AuthenticationEnvelopeTests(unittest.TestCase):

    def check_rejected(self, modify, *, now=NOW):
        envelope = sample_envelope()
        modify(envelope)

        with self.assertRaises(ValueError):
            validate_envelope(
                envelope,
                expected_binding(),
                now=now,
            )

    def test_valid_structure_never_establishes_authenticity(self):
        result = validate_envelope(
            sample_envelope(),
            expected_binding(),
            now=NOW,
        )

        self.assertTrue(result.structure_valid)
        self.assertTrue(result.expected_binding_matches)
        self.assertTrue(result.timestamp_window_valid)
        self.assertFalse(result.signature_verified)
        self.assertFalse(result.collector_authenticated)
        self.assertFalse(result.freshness_verified)
        self.assertFalse(result.replay_prevention_verified)
        self.assertFalse(result.runtime_evidence_verified)
        self.assertFalse(result.isolation_proven)
        self.assertFalse(result.docker_execution_permitted)
        self.assertFalse(result.production_execution_enabled)
        self.assertFalse(result.automatic_retry_permitted)
        self.assertTrue(result.manual_verification_required)

    def test_rejects_wrong_version(self):
        self.check_rejected(
            lambda e: e.update(envelope_version=2)
        )

    def test_rejects_boolean_version(self):
        self.check_rejected(
            lambda e: e.update(envelope_version=True)
        )

    def test_rejects_wrong_purpose(self):
        self.check_rejected(
            lambda e: e.update(purpose="production-deployment")
        )

    def test_rejects_algorithm_substitution(self):
        self.check_rejected(
            lambda e: e.update(algorithm="none")
        )

    def test_rejects_collector_substitution(self):
        self.check_rejected(
            lambda e: e.update(collector_id="attacker")
        )

    def test_rejects_key_substitution(self):
        self.check_rejected(
            lambda e: e.update(key_id="attacker-key")
        )

    def test_rejects_wrong_challenge(self):
        self.check_rejected(
            lambda e: e.update(challenge="d" * 64)
        )

    def test_rejects_malformed_signature(self):
        self.check_rejected(
            lambda e: e.update(signature="invalid")
        )

    def test_rejects_subject_substitution(self):
        self.check_rejected(
            lambda e: e["evidence"]["subject"].update(
                vm_id="vm-other"
            )
        )

    def test_rejects_collection_substitution(self):
        self.check_rejected(
            lambda e: e["evidence"]["provenance"].update(
                collection_id="collection-other"
            )
        )

    def test_rejects_expired_envelope(self):
        self.check_rejected(
            lambda e: None,
            now=datetime(
                2026, 10, 13, 8, 5,
                tzinfo=timezone.utc,
            ),
        )

    def test_rejects_future_issued_envelope(self):
        self.check_rejected(
            lambda e: e.update(
                issued_at="2026-10-13T08:01:00Z"
            )
        )

    def test_rejects_excessive_validity(self):
        self.check_rejected(
            lambda e: e.update(
                expires_at="2026-10-13T08:10:00Z"
            )
        )

    def test_rejects_stale_collection(self):
        self.check_rejected(
            lambda e: e["evidence"]["provenance"].update(
                collected_at="2026-10-13T07:00:00Z"
            )
        )

    def test_rejects_naive_assessment_time(self):
        self.check_rejected(
            lambda e: None,
            now=datetime(2026, 10, 13, 8, 0, 30),
        )

    def test_rejects_extra_fields(self):
        self.check_rejected(
            lambda e: e.update(execution_permitted=True)
        )

    def test_signing_payload_excludes_signature(self):
        envelope = sample_envelope()
        payload = signing_payload(envelope)

        self.assertNotIn(b'"signature"', payload)
        self.assertIn(b'"challenge"', payload)
        self.assertIn(b'"evidence"', payload)

    def test_signing_payload_changes_with_subject(self):
        original = sample_envelope()
        modified = deepcopy(original)
        modified["evidence"]["subject"]["vm_id"] = "vm-other"

        self.assertNotEqual(
            signing_payload(original),
            signing_payload(modified),
        )

    def test_input_remains_unchanged(self):
        envelope = sample_envelope()
        original = deepcopy(envelope)

        validate_envelope(
            envelope,
            expected_binding(),
            now=NOW,
        )

        self.assertEqual(envelope, original)


if __name__ == "__main__":
    unittest.main()
