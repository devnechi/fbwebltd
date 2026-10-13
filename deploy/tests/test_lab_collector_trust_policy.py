#!/usr/bin/env python3
"""Gate 4D.22C.3D.9 collector trust-policy tests."""

from dataclasses import replace
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import sys
import unittest


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_collector_trust_policy import (
    CollectorKeyRecord,
    CollectorTrustRegistry,
    REGISTRY_ID,
    MAX_KEYS,
    assess_collector_policy,
    assess_collector_policy_bytes,
    validate_registry,
)

from lab_runtime_auth_envelope import (
    PURPOSE,
)

from lab_runtime_canonical_payload import (
    canonical_json_bytes,
)

from test_lab_runtime_auth_envelope import (
    NOW,
    expected_binding,
    sample_envelope,
)


def sample_key():
    return CollectorKeyRecord(
        collector_id="offline-collector",
        key_id="key-001",
        algorithm="Ed25519",
        public_key_hex="a" * 64,
        purpose=PURPOSE,
        vm_id="vm-001",
        daemon_id="daemon-001",
        valid_from="2026-10-13T07:30:00Z",
        valid_until="2026-10-13T09:00:00Z",
        status="active",
    )


def sample_registry():
    return CollectorTrustRegistry(
        registry_id=REGISTRY_ID,
        revision=1,
        keys=(sample_key(),),
    )


class CollectorTrustPolicyTests(unittest.TestCase):

    def assess(self, registry=None, envelope=None, now=NOW):
        return assess_collector_policy(
            sample_envelope() if envelope is None else envelope,
            expected_binding(),
            sample_registry() if registry is None else registry,
            now=now,
        )

    def change_key(self, **changes):
        registry = sample_registry()

        return replace(
            registry,
            keys=(
                replace(sample_key(), **changes),
            ),
        )

    def test_policy_eligibility_never_authenticates(self):
        result = self.assess()

        self.assertTrue(result.registry_structure_valid)
        self.assertTrue(result.collector_key_binding_matches)
        self.assertTrue(result.subject_scope_matches)
        self.assertTrue(
            result.key_eligible_for_future_verification
        )

        self.assertFalse(result.registry_authenticity_verified)
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

    def test_raw_canonical_envelope_is_supported(self):
        raw = canonical_json_bytes(sample_envelope())

        result = assess_collector_policy_bytes(
            raw,
            expected_binding(),
            sample_registry(),
            now=NOW,
        )

        self.assertTrue(
            result.key_eligible_for_future_verification
        )
        self.assertFalse(result.signature_verified)

    def test_unknown_key_is_rejected(self):
        registry = self.change_key(key_id="key-other")

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_unknown_collector_is_rejected(self):
        registry = self.change_key(
            collector_id="unknown-collector"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_revoked_key_is_rejected(self):
        registry = self.change_key(status="revoked")

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_disabled_key_is_rejected(self):
        registry = self.change_key(status="disabled")

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_unknown_status_is_rejected(self):
        registry = self.change_key(status="trusted")

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_vm_scope_substitution_is_rejected(self):
        registry = self.change_key(vm_id="other-vm")

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_daemon_scope_substitution_is_rejected(self):
        registry = self.change_key(
            daemon_id="other-daemon"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_wrong_purpose_is_rejected(self):
        registry = self.change_key(
            purpose="production-deployment"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_algorithm_substitution_is_rejected(self):
        registry = self.change_key(algorithm="none")

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_expired_key_is_rejected(self):
        registry = self.change_key(
            valid_until="2026-10-13T08:00:20Z"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_not_yet_valid_key_is_rejected(self):
        registry = self.change_key(
            valid_from="2026-10-13T08:00:20Z"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_expired_key_remains_rejected_for_old_evidence(self):
        registry = self.change_key(
            valid_until="2026-10-13T08:00:20Z"
        )

        with self.assertRaises(ValueError):
            self.assess(
                registry,
                now=datetime(
                    2026, 10, 13, 8, 0, 30,
                    tzinfo=timezone.utc,
                ),
            )

    def test_key_must_cover_envelope_expiry(self):
        registry = self.change_key(
            valid_until="2026-10-13T08:02:00Z"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_key_must_cover_collection(self):
        registry = self.change_key(
            valid_from="2026-10-13T08:00:05Z"
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_invalid_key_validity_interval(self):
        registry = self.change_key(
            valid_from="2026-10-13T09:00:00Z"
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_invalid_public_key_length(self):
        registry = self.change_key(
            public_key_hex="a" * 62
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_uppercase_public_key_is_rejected(self):
        registry = self.change_key(
            public_key_hex="A" * 64
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_all_zero_public_key_is_rejected(self):
        registry = self.change_key(
            public_key_hex="0" * 64
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_boolean_revision_is_rejected(self):
        registry = replace(
            sample_registry(),
            revision=True,
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_wrong_registry_identity_is_rejected(self):
        registry = replace(
            sample_registry(),
            registry_id="untrusted-registry",
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_empty_registry_is_rejected(self):
        registry = replace(
            sample_registry(),
            keys=(),
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_duplicate_collector_key_is_rejected(self):
        registry = replace(
            sample_registry(),
            keys=(sample_key(), sample_key()),
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_reused_public_key_is_rejected(self):
        second = replace(
            sample_key(),
            key_id="key-002",
        )

        registry = replace(
            sample_registry(),
            keys=(sample_key(), second),
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_invalid_unselected_record_fails_closed(self):
        second = replace(
            sample_key(),
            key_id="key-002",
            public_key_hex="b" * 64,
            status="unexpected",
        )

        registry = replace(
            sample_registry(),
            keys=(sample_key(), second),
        )

        with self.assertRaises(ValueError):
            self.assess(registry)

    def test_distinct_rotation_keys_are_permitted(self):
        second = replace(
            sample_key(),
            key_id="key-002",
            public_key_hex="b" * 64,
            status="disabled",
        )

        registry = replace(
            sample_registry(),
            keys=(sample_key(), second),
        )

        result = self.assess(registry)

        self.assertTrue(
            result.key_eligible_for_future_verification
        )
        self.assertFalse(result.signature_verified)

    def test_oversized_registry_is_rejected(self):
        records = tuple(
            replace(
                sample_key(),
                key_id="key-" + str(index),
                public_key_hex=f"{index + 1:064x}",
            )
            for index in range(MAX_KEYS + 1)
        )

        registry = replace(
            sample_registry(),
            keys=records,
        )

        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_embedded_public_key_claim_is_rejected(self):
        envelope = sample_envelope()
        envelope["public_key_hex"] = "a" * 64

        with self.assertRaises(ValueError):
            self.assess(envelope=envelope)

    def test_duplicate_raw_json_key_is_rejected(self):
        raw = canonical_json_bytes(sample_envelope())

        raw = raw.replace(
            b'"key_id":"key-001"',
            b'"key_id":"key-001","key_id":"key-001"',
            1,
        )

        with self.assertRaises(ValueError):
            assess_collector_policy_bytes(
                raw,
                expected_binding(),
                sample_registry(),
                now=NOW,
            )

    def test_registry_is_not_mutated(self):
        registry = sample_registry()
        original = deepcopy(registry)

        self.assess(registry)

        self.assertEqual(registry, original)

    def test_envelope_is_not_mutated(self):
        envelope = sample_envelope()
        original = deepcopy(envelope)

        self.assess(envelope=envelope)

        self.assertEqual(envelope, original)


if __name__ == "__main__":
    unittest.main()
