#!/usr/bin/env python3
"""Gate 4D.22C.3D.11D pure registry revision continuity tests."""

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import hashlib
import sys
import unittest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_registry_wire_format import (
    canonical_registry_bytes,
    registry_signing_bytes,
)
from lab_registry_revision_continuity import (
    RevisionStateSnapshot,
    assess_registry_revision_bytes,
    validate_revision_snapshot,
)
from test_lab_registry_signature_verifier import (
    sample_case,
    sign_document,
)


def digest(document):
    return hashlib.sha256(
        registry_signing_bytes(document)
    ).hexdigest()


def snapshot_for(document):
    return RevisionStateSnapshot(
        registry_id=document["registry_id"],
        format_version=document["registry_format_version"],
        revision=document["revision"],
        signing_digest=digest(document),
        generation=1,
    )


def next_revision(document, private):
    updated = deepcopy(document)
    updated["revision"] = document["revision"] + 1
    updated["previous_revision"] = document["revision"]
    updated["previous_digest"] = digest(document)
    return sign_document(updated, private), updated


class RegistryRevisionContinuityTests(unittest.TestCase):

    def test_existing_revision_same_digest_is_recognized(self):
        raw, document, _, _ = sample_case()
        result = assess_registry_revision_bytes(
            raw, snapshot_for(document)
        )
        self.assertTrue(result.logical_continuity_valid)
        self.assertTrue(result.matches_existing_revision)
        self.assertEqual(
            result.relationship,
            "same_revision_same_digest",
        )

    def test_consecutive_revision_is_logically_valid(self):
        _, document, _, private = sample_case()
        raw, _ = next_revision(document, private)

        result = assess_registry_revision_bytes(
            raw, snapshot_for(document)
        )

        self.assertEqual(result.candidate_revision, 2)
        self.assertTrue(result.logical_continuity_valid)
        self.assertFalse(result.matches_existing_revision)
        self.assertEqual(
            result.relationship,
            "consecutive_revision",
        )

    def test_success_does_not_claim_authorization(self):
        _, document, _, private = sample_case()
        raw, _ = next_revision(document, private)
        result = assess_registry_revision_bytes(
            raw, snapshot_for(document)
        )

        for field in (
            "registry_signature_verified",
            "administrative_policy_authenticated",
            "snapshot_provenance_authenticated",
            "registry_currentness_verified",
            "rollback_prevention_verified",
            "revocation_history_verified",
            "trusted_time_source_verified",
            "state_commit_performed",
            "atomic_update_authorized",
            "collector_authenticated",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "production_execution_enabled",
            "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, field), field)

        self.assertTrue(result.manual_verification_required)

    def test_lower_revision_rejected(self):
        raw, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document),
            revision=2,
            signing_digest="b" * 64,
        )
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, state)

    def test_same_revision_conflicting_digest_rejected(self):
        _, document, _, private = sample_case()
        state = snapshot_for(document)
        document["keys"][0]["status"] = "disabled"
        changed = sign_document(document, private)

        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(changed, state)

    def test_missing_intermediate_revision_rejected(self):
        _, document, _, private = sample_case()
        state = snapshot_for(document)

        document["revision"] = 3
        document["previous_revision"] = 2
        document["previous_digest"] = "a" * 64

        raw = sign_document(document, private)

        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, state)

    def test_wrong_predecessor_digest_rejected(self):
        _, document, _, private = sample_case()
        state = snapshot_for(document)
        raw, updated = next_revision(document, private)

        updated["previous_digest"] = "f" * 64
        raw = sign_document(updated, private)

        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, state)

    def test_wrong_predecessor_revision_rejected(self):
        _, document, _, private = sample_case()
        state = snapshot_for(document)
        _, updated = next_revision(document, private)
        updated["previous_revision"] = 0

        # Existing wire-format checks reject this before comparison.
        with self.assertRaises(ValueError):
            sign_document(updated, private)

    def test_unexpected_snapshot_registry_identity_rejected(self):
        raw, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document),
            registry_id="attacker-registry",
        )
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, state)

    def test_wrong_snapshot_format_rejected(self):
        raw, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document),
            format_version=2,
        )
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, state)

    def test_wrong_candidate_format_rejected(self):
        _, document, _, _ = sample_case()
        document["registry_format_version"] = 2

        with self.assertRaises(ValueError):
            canonical_registry_bytes(document)

    def test_missing_snapshot_rejected(self):
        raw, _, _, _ = sample_case()
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, None)

    def test_snapshot_dictionary_rejected(self):
        raw, document, _, _ = sample_case()
        state = snapshot_for(document).__dict__

        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, state)

    def test_boolean_revision_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document), revision=True
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_negative_revision_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document), revision=-1
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_oversized_revision_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document), revision=1 << 53
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_zero_digest_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document),
            signing_digest="0" * 64,
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_uppercase_digest_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document),
            signing_digest="A" * 64,
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_non_string_digest_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document), signing_digest=123
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_boolean_generation_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document), generation=True
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_zero_generation_rejected(self):
        _, document, _, _ = sample_case()
        state = replace(
            snapshot_for(document), generation=0
        )
        with self.assertRaises(ValueError):
            validate_revision_snapshot(state)

    def test_snapshot_generation_is_not_advanced(self):
        _, document, _, private = sample_case()
        state = replace(
            snapshot_for(document), generation=8
        )
        raw, _ = next_revision(document, private)

        result = assess_registry_revision_bytes(raw, state)

        self.assertEqual(result.snapshot_generation, 8)
        self.assertFalse(result.state_commit_performed)

    def test_non_byte_registry_input_rejected(self):
        _, document, _, _ = sample_case()
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(
                document, snapshot_for(document)
            )

    def test_noncanonical_registry_bytes_rejected(self):
        raw, document, _, _ = sample_case()
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(
                raw + b" ", snapshot_for(document)
            )

    def test_duplicate_json_fields_rejected(self):
        raw, document, _, _ = sample_case()
        modified = raw.replace(
            b'"revision":1',
            b'"revision":1,"revision":1',
            1,
        )

        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(
                modified, snapshot_for(document)
            )

    def test_continuity_does_not_verify_registry_signature(self):
        _, document, _, _ = sample_case()
        state = snapshot_for(document)

        # This is a structurally valid but cryptographically
        # invalid Ed25519 signature. Continuity alone cannot
        # identify the invalid cryptographic authentication.
        document["signature"] = "A" * 86
        raw = canonical_registry_bytes(document)

        result = assess_registry_revision_bytes(raw, state)

        self.assertTrue(result.logical_continuity_valid)
        self.assertFalse(result.registry_signature_verified)
        self.assertFalse(result.registry_currentness_verified)
        self.assertFalse(result.atomic_update_authorized)

    def test_digest_uses_domain_separated_unsigned_bytes(self):
        raw, document, _, _ = sample_case()
        result = assess_registry_revision_bytes(
            raw, snapshot_for(document)
        )
        self.assertEqual(
            result.candidate_signing_digest,
            digest(document),
        )

    def test_inputs_are_not_mutated(self):
        raw, document, _, _ = sample_case()
        state = snapshot_for(document)
        original_state = deepcopy(state)
        original_raw = bytes(raw)

        assess_registry_revision_bytes(raw, state)

        self.assertEqual(state, original_state)
        self.assertEqual(raw, original_raw)

    def test_genesis_cannot_bootstrap_without_state(self):
        raw, _, _, _ = sample_case()

        # There is deliberately no automatic revision-zero
        # state or implicit bootstrap authority.
        with self.assertRaises(ValueError):
            assess_registry_revision_bytes(raw, None)


if __name__ == "__main__":
    unittest.main()
