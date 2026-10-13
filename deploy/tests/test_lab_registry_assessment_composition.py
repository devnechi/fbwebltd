#!/usr/bin/env python3
"""Gate 4D.22C.3D.11F registry composition security tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from lab_registry_assessment_composition import (
    RegistryCompositionAssessment,
    assess_registry_composition_bytes,
)
from lab_registry_signature_verifier import (
    ADMIN_POLICY_ID,
    AdministrativeKeyRecord,
    AdministrativeKeyPolicy,
)
from lab_registry_wire_format import (
    REGISTRY_PURPOSE,
    canonical_registry_bytes,
)
from test_lab_registry_signature_verifier import (
    NOW,
    public_hex,
    sign_document,
)
from test_lab_registry_revocation_continuity import (
    advance,
    case,
    new_record,
)


def admin_policy(private):
    return AdministrativeKeyPolicy(
        policy_id=ADMIN_POLICY_ID,
        keys=(
            AdministrativeKeyRecord(
                key_id="admin-001",
                public_key_hex=public_hex(private),
                algorithm="Ed25519",
                purpose=REGISTRY_PURPOSE,
                valid_from="2026-10-13T07:00:00Z",
                valid_until="2026-10-13T09:00:00Z",
                status="active",
            ),
        ),
    )


def fixture(status="active", next_status=None):
    old, document, private, state, history = case(status)
    candidate, updated = advance(
        document,
        private,
        status=next_status,
    )
    return (
        old, candidate, document, updated,
        admin_policy(private), state, history, private,
    )


class RegistryAssessmentCompositionTests(unittest.TestCase):

    def assess(
        self,
        old,
        candidate,
        policy,
        state,
        history,
        now=NOW,
    ):
        return assess_registry_composition_bytes(
            old,
            candidate,
            policy,
            state,
            history,
            now=now,
        )

    def test_valid_composition(self):
        old, raw, doc, updated, policy, state, history, _ = fixture()
        result = self.assess(old, raw, policy, state, history)
        self.assertIsInstance(result, RegistryCompositionAssessment)
        self.assertEqual(result.previous_revision, 1)
        self.assertEqual(result.candidate_revision, 2)
        self.assertEqual(result.snapshot_generation, 1)
        self.assertEqual(result.proposed_history.tombstones, ())

    def test_all_three_local_checks_pass(self):
        old, raw, _, _, policy, state, history, _ = fixture()
        result = self.assess(old, raw, policy, state, history)
        self.assertTrue(result.signature_matches_supplied_admin_key)
        self.assertTrue(result.revision_matches_supplied_snapshot)
        self.assertTrue(result.lifecycle_matches_supplied_history)
        self.assertEqual(
            result.candidate_signing_digest,
            result.proposed_history.candidate_signing_digest,
        )

    def test_positive_result_never_claims_authorization(self):
        old, raw, _, _, policy, state, history, _ = fixture()
        result = self.assess(old, raw, policy, state, history)
        for name in (
            "registry_provenance_authenticated",
            "previous_registry_authenticated",
            "administrative_identity_authenticated",
            "administrative_policy_authenticated",
            "snapshot_provenance_authenticated",
            "revocation_history_authenticated",
            "registry_currentness_verified",
            "revocation_currentness_verified",
            "trusted_time_source_verified",
            "rollback_prevention_verified",
            "replay_prevention_verified",
            "state_commit_performed",
            "revocation_history_persisted",
            "atomic_update_authorized",
            "collector_authenticated",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "production_execution_enabled",
            "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, name), name)
        self.assertTrue(result.manual_verification_required)

    def test_active_to_disabled_proposal(self):
        args = fixture(next_status="disabled")
        result = self.assess(args[0], args[1], args[4], args[5], args[6])
        self.assertEqual(result.proposed_history.tombstones[0].status, "disabled")

    def test_active_to_revoked_proposal(self):
        args = fixture(next_status="revoked")
        result = self.assess(args[0], args[1], args[4], args[5], args[6])
        self.assertEqual(result.proposed_history.tombstones[0].status, "revoked")

    def test_disabled_to_revoked_proposal(self):
        args = fixture(status="disabled", next_status="revoked")
        result = self.assess(args[0], args[1], args[4], args[5], args[6])
        self.assertEqual(result.proposed_history.tombstones[0].status, "revoked")

    def test_distinct_key_rotation(self):
        old, _, document, _, policy, state, history, private = fixture()
        original = dict(document["keys"][0], status="disabled")
        rotated = new_record(document)
        keys = sorted(
            [original, rotated],
            key=lambda item: (item["collector_id"], item["key_id"]),
        )
        candidate, _ = advance(document, private, keys=keys)
        result = self.assess(old, candidate, policy, state, history)
        self.assertEqual(len(result.proposed_history.tombstones), 1)

    def test_invalid_candidate_signature_rejected(self):
        old, _, _, updated, policy, state, history, _ = fixture()
        updated["signature"] = "A" * 86
        bad = canonical_registry_bytes(updated)
        with self.assertRaises(ValueError):
            self.assess(old, bad, policy, state, history)

    def test_candidate_tampering_after_signing_rejected(self):
        old, _, _, updated, policy, state, history, _ = fixture()
        updated["keys"][0]["status"] = "disabled"
        with self.assertRaises(ValueError):
            self.assess(
                old, canonical_registry_bytes(updated),
                policy, state, history,
            )

    def test_unknown_administrator_rejected(self):
        args = fixture()
        policy = replace(
            args[4],
            keys=(replace(args[4].keys[0], key_id="unknown"),),
        )
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], policy, args[5], args[6])

    def test_disabled_administrator_rejected(self):
        args = fixture()
        policy = replace(
            args[4],
            keys=(replace(args[4].keys[0], status="disabled"),),
        )
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], policy, args[5], args[6])

    def test_revoked_administrator_rejected(self):
        args = fixture()
        policy = replace(
            args[4],
            keys=(replace(args[4].keys[0], status="revoked"),),
        )
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], policy, args[5], args[6])

    def test_wrong_administrator_purpose_rejected(self):
        args = fixture()
        policy = replace(
            args[4],
            keys=(replace(args[4].keys[0], purpose="wrong-purpose"),),
        )
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], policy, args[5], args[6])

    def test_wrong_administrator_public_key_rejected(self):
        args = fixture()
        replacement = public_hex(Ed25519PrivateKey.generate())
        policy = replace(
            args[4],
            keys=(replace(args[4].keys[0], public_key_hex=replacement),),
        )
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], policy, args[5], args[6])

    def test_expired_candidate_rejected(self):
        args = fixture()
        expired = datetime(
            2026, 10, 13, 8, 5, tzinfo=timezone.utc,
        )
        with self.assertRaises(ValueError):
            self.assess(
                args[0], args[1], args[4],
                args[5], args[6], now=expired,
            )

    def test_future_dated_candidate_rejected(self):
        args = fixture()
        earlier = datetime(
            2026, 10, 13, 7, 59, tzinfo=timezone.utc,
        )
        with self.assertRaises(ValueError):
            self.assess(
                args[0], args[1], args[4],
                args[5], args[6], now=earlier,
            )

    def test_naive_assessment_time_rejected(self):
        args = fixture()
        with self.assertRaises(ValueError):
            self.assess(
                args[0], args[1], args[4], args[5], args[6],
                now=datetime(2026, 10, 13, 8, 0),
            )

    def test_wrong_revision_snapshot_digest_rejected(self):
        args = fixture()
        state = replace(args[5], signing_digest="a" * 64)
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], args[4], state, args[6])

    def test_missing_disabled_tombstone_rejected(self):
        args = fixture(status="disabled")
        history = replace(args[6], tombstones=())
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], args[4], args[5], history)

    def test_mismatched_revocation_history_generation_rejected(self):
        args = fixture()
        history = replace(args[6], generation=2)
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], args[4], args[5], history)

    def test_revoked_key_reactivation_rejected(self):
        args = fixture(status="revoked", next_status="active")
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], args[4], args[5], args[6])

    def test_disabled_key_reactivation_rejected(self):
        args = fixture(status="disabled", next_status="active")
        with self.assertRaises(ValueError):
            self.assess(args[0], args[1], args[4], args[5], args[6])

    def test_existing_key_scope_substitution_rejected(self):
        old, _, doc, _, policy, state, history, private = fixture()
        changed = dict(doc["keys"][0], vm_id="different-vm")
        candidate, _ = advance(doc, private, keys=[changed])
        with self.assertRaises(ValueError):
            self.assess(old, candidate, policy, state, history)

    def test_revoked_key_material_reuse_rejected(self):
        old, _, doc, _, policy, state, history, private = fixture(
            status="revoked"
        )
        replacement = new_record(
            doc,
            material=doc["keys"][0]["public_key_hex"],
        )
        candidate, _ = advance(
            doc, private, keys=[replacement],
        )
        with self.assertRaises(ValueError):
            self.assess(old, candidate, policy, state, history)

    def test_revision_gap_rejected(self):
        old, _, doc, updated, policy, state, history, private = fixture()
        updated["revision"] = 3
        updated["previous_revision"] = 2
        updated["previous_digest"] = "a" * 64
        candidate = sign_document(updated, private)
        with self.assertRaises(ValueError):
            self.assess(old, candidate, policy, state, history)

    def test_same_revision_is_not_new_transition(self):
        old, _, _, _, policy, state, history, _ = fixture()
        with self.assertRaises(ValueError):
            self.assess(old, old, policy, state, history)

    def test_altered_previous_registry_rejected(self):
        old, raw, doc, _, policy, state, history, private = fixture()
        previous = deepcopy(doc)
        previous["keys"][0]["status"] = "disabled"
        wrong_previous = sign_document(previous, private)
        with self.assertRaises(ValueError):
            self.assess(
                wrong_previous, raw, policy, state, history,
            )

    def test_noncanonical_candidate_rejected(self):
        args = fixture()
        with self.assertRaises(ValueError):
            self.assess(
                args[0], args[1] + b" ",
                args[4], args[5], args[6],
            )

    def test_noncanonical_previous_rejected(self):
        args = fixture()
        with self.assertRaises(ValueError):
            self.assess(
                args[0] + b" ", args[1],
                args[4], args[5], args[6],
            )

    def test_duplicate_candidate_field_rejected(self):
        args = fixture()
        bad = args[1].replace(
            b'"revision":2',
            b'"revision":2,"revision":2',
            1,
        )
        with self.assertRaises(ValueError):
            self.assess(
                args[0], bad, args[4], args[5], args[6],
            )

    def test_missing_snapshot_rejected(self):
        args = fixture()
        with self.assertRaises(ValueError):
            self.assess(
                args[0], args[1], args[4], None, args[6],
            )

    def test_previous_signature_is_not_authenticated(self):
        args = fixture()
        previous = deepcopy(args[2])
        previous["signature"] = "A" * 86
        old_with_invalid_signature = canonical_registry_bytes(previous)

        # Signing digest excludes the signature. This demonstrates
        # the deliberately limited previous-registry trust boundary.
        result = self.assess(
            old_with_invalid_signature,
            args[1], args[4], args[5], args[6],
        )
        self.assertTrue(result.revision_matches_supplied_snapshot)
        self.assertFalse(result.previous_registry_authenticated)

    def test_caller_controlled_admin_policy_is_not_proven(self):
        args = fixture()
        attacker_private = Ed25519PrivateKey.generate()
        forged_policy = admin_policy(attacker_private)
        attacker_signed_candidate = sign_document(
            deepcopy(args[3]), attacker_private,
        )

        # Cryptography cannot determine whether the caller was
        # entitled to replace the administrator trust policy.
        result = self.assess(
            args[0], attacker_signed_candidate,
            forged_policy, args[5], args[6],
        )
        self.assertTrue(result.signature_matches_supplied_admin_key)
        self.assertFalse(result.administrative_policy_authenticated)
        self.assertFalse(result.registry_provenance_authenticated)

    def test_inputs_remain_unchanged(self):
        args = fixture(next_status="revoked")
        inputs = deepcopy(args[:7])
        self.assess(
            args[0], args[1], args[4], args[5], args[6],
        )
        self.assertEqual(args[:7], inputs)

    def test_result_is_immutable(self):
        args = fixture()
        result = self.assess(
            args[0], args[1], args[4], args[5], args[6],
        )
        with self.assertRaises(FrozenInstanceError):
            result.candidate_revision = 999


if __name__ == "__main__":
    unittest.main()
