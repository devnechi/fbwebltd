#!/usr/bin/env python3
"""Gate 4D.22C.3D.11E pure revocation-continuity adversarial tests."""

from copy import deepcopy
from dataclasses import replace
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

from lab_registry_revocation_continuity import (
    KeyLifecycleTombstone,
    RevocationHistorySnapshot,
    assess_registry_revocation_bytes,
    validate_revocation_history,
)
from lab_registry_wire_format import canonical_registry_bytes
from test_lab_registry_signature_verifier import (
    public_hex,
    sample_case,
    sign_document,
)
from test_lab_registry_revision_continuity import (
    next_revision,
    snapshot_for,
)


def tombstone(record):
    return KeyLifecycleTombstone(
        collector_id=record["collector_id"],
        key_id=record["key_id"],
        public_key_hex=record["public_key_hex"],
        status=record["status"],
    )


def case(status="active"):
    raw, document, _, private = sample_case()

    if status != "active":
        document["keys"][0]["status"] = status
        raw = sign_document(document, private)

    state = snapshot_for(document)

    marks = (
        (tombstone(document["keys"][0]),)
        if status != "active"
        else ()
    )

    history = RevocationHistorySnapshot(
        registry_id=state.registry_id,
        revision=state.revision,
        signing_digest=state.signing_digest,
        generation=state.generation,
        tombstones=marks,
    )

    return raw, document, private, state, history


def advance(document, private, *, status=None, keys=None):
    _, updated = next_revision(document, private)

    if status is not None:
        updated["keys"][0]["status"] = status

    if keys is not None:
        updated["keys"] = keys

    return sign_document(updated, private), updated


def new_record(document, *, key_id="key-002", material=None):
    record = dict(document["keys"][0])
    record["key_id"] = key_id
    record["public_key_hex"] = (
        material
        or public_hex(Ed25519PrivateKey.generate())
    )
    record["status"] = "active"
    return record


def history_after(proposal, generation=2):
    return RevocationHistorySnapshot(
        registry_id=proposal.registry_id,
        revision=proposal.candidate_revision,
        signing_digest=proposal.candidate_signing_digest,
        generation=generation,
        tombstones=proposal.tombstones,
    )


class RegistryRevocationContinuityTests(unittest.TestCase):

    def evaluate(self, source, candidate, state, history):
        return assess_registry_revocation_bytes(
            source, candidate, state, history
        )

    def test_active_to_active(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        result = self.evaluate(old, raw, state, history)

        self.assertTrue(result.logical_lifecycle_continuity_valid)
        self.assertEqual(result.proposal.tombstones, ())

    def test_active_to_disabled_creates_tombstone(self):
        old, document, private, state, history = case()
        raw, updated = advance(
            document, private, status="disabled"
        )

        result = self.evaluate(old, raw, state, history)

        self.assertEqual(
            result.proposal.tombstones,
            (tombstone(updated["keys"][0]),),
        )
        self.assertEqual(result.proposal.candidate_revision, 2)

    def test_active_to_revoked_creates_tombstone(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private, status="revoked")

        result = self.evaluate(old, raw, state, history)

        self.assertEqual(
            result.proposal.tombstones[0].status,
            "revoked",
        )

    def test_disabled_to_disabled_preserves_tombstone(self):
        old, document, private, state, history = case("disabled")
        raw, _ = advance(document, private)

        self.assertEqual(
            self.evaluate(old, raw, state, history).proposal.tombstones,
            history.tombstones,
        )

    def test_disabled_to_revoked_upgrades_tombstone(self):
        old, document, private, state, history = case("disabled")
        raw, _ = advance(document, private, status="revoked")

        result = self.evaluate(old, raw, state, history)

        self.assertEqual(
            result.proposal.tombstones[0].status,
            "revoked",
        )

    def test_revoked_to_revoked_preserves_tombstone(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(document, private)

        self.assertEqual(
            self.evaluate(old, raw, state, history).proposal.tombstones,
            history.tombstones,
        )

    def test_disabled_to_active_rejected(self):
        old, document, private, state, history = case("disabled")
        raw, _ = advance(document, private, status="active")

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_revoked_to_active_rejected(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(document, private, status="active")

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_revoked_to_disabled_rejected(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(document, private, status="disabled")

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_active_removed_without_deactivation_rejected(self):
        old, document, private, state, history = case()
        raw, _ = advance(
            document,
            private,
            keys=[new_record(document)],
        )

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_disabled_removed_keeps_tombstone(self):
        old, document, private, state, history = case("disabled")
        raw, _ = advance(
            document,
            private,
            keys=[new_record(document)],
        )

        result = self.evaluate(old, raw, state, history)

        self.assertEqual(
            result.proposal.tombstones,
            history.tombstones,
        )

    def test_revoked_removed_keeps_tombstone(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(
            document,
            private,
            keys=[new_record(document)],
        )

        result = self.evaluate(old, raw, state, history)

        self.assertEqual(
            result.proposal.tombstones,
            history.tombstones,
        )

    def test_removed_revoked_identity_reintroduced_rejected(self):
        old, document, private, state, history = case("revoked")

        raw2, doc2 = advance(
            document,
            private,
            keys=[new_record(document)],
        )

        accepted = self.evaluate(old, raw2, state, history)

        replacement = new_record(
            document,
            key_id=document["keys"][0]["key_id"],
        )

        raw3, _ = advance(
            doc2,
            private,
            keys=sorted(
                [doc2["keys"][0], replacement],
                key=lambda r: (r["collector_id"], r["key_id"]),
            ),
        )

        with self.assertRaises(ValueError):
            self.evaluate(
                raw2,
                raw3,
                snapshot_for(doc2),
                history_after(accepted.proposal),
            )

    def test_removed_disabled_identity_reintroduced_rejected(self):
        old, document, private, state, history = case("disabled")

        raw2, doc2 = advance(
            document,
            private,
            keys=[new_record(document)],
        )

        accepted = self.evaluate(old, raw2, state, history)

        replacement = dict(document["keys"][0])

        raw3, _ = advance(
            doc2,
            private,
            keys=sorted(
                [replacement, doc2["keys"][0]],
                key=lambda r: (r["collector_id"], r["key_id"]),
            ),
        )

        with self.assertRaises(ValueError):
            self.evaluate(
                raw2,
                raw3,
                snapshot_for(doc2),
                history_after(accepted.proposal),
            )

    def test_tombstoned_material_reused_under_new_id_rejected(self):
        old, document, private, state, history = case("revoked")

        raw, _ = advance(
            document,
            private,
            keys=[
                new_record(
                    document,
                    material=document["keys"][0]["public_key_hex"],
                )
            ],
        )

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_existing_identity_key_material_substitution_rejected(self):
        old, document, private, state, history = case()

        replacement = dict(
            document["keys"][0],
            public_key_hex=public_hex(Ed25519PrivateKey.generate()),
        )

        raw, _ = advance(
            document, private, keys=[replacement]
        )

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_existing_scope_substitution_rejected(self):
        old, document, private, state, history = case()

        replacement = dict(
            document["keys"][0],
            vm_id="other-vm",
        )

        raw, _ = advance(
            document, private, keys=[replacement]
        )

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_existing_expiry_extension_rejected(self):
        old, document, private, state, history = case()

        replacement = dict(
            document["keys"][0],
            valid_until="2026-10-13T10:00:00Z",
        )

        raw, _ = advance(
            document, private, keys=[replacement]
        )

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_distinct_rotation_allowed(self):
        old, document, private, state, history = case()

        disabled = dict(
            document["keys"][0], status="disabled"
        )

        replacement = new_record(document)

        raw, updated = advance(
            document,
            private,
            keys=[disabled, replacement],
        )

        result = self.evaluate(old, raw, state, history)

        self.assertEqual(
            result.proposal.tombstones[0].status,
            "disabled",
        )
        self.assertEqual(len(updated["keys"]), 2)

    def test_missing_prior_disabled_tombstone_fails(self):
        old, document, private, state, history = case("disabled")
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, tombstones=()),
            )

    def test_missing_prior_revoked_tombstone_fails(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, tombstones=()),
            )

    def test_prior_tombstone_status_conflict_fails(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(document, private)

        fake = replace(
            history.tombstones[0],
            status="disabled",
        )

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, tombstones=(fake,)),
            )

    def test_prior_tombstone_material_conflict_fails(self):
        old, document, private, state, history = case("revoked")
        raw, _ = advance(document, private)

        fake = replace(
            history.tombstones[0],
            public_key_hex="a" * 64,
        )

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, tombstones=(fake,)),
            )

    def test_active_record_with_tombstone_fails(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        fake = replace(
            tombstone(document["keys"][0]),
            status="revoked",
        )

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, tombstones=(fake,)),
            )

    def test_history_revision_mismatch_fails(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, revision=2),
            )

    def test_history_digest_mismatch_fails(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, signing_digest="a" * 64),
            )

    def test_history_generation_mismatch_fails(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, generation=2),
            )

    def test_bad_history_registry_fails(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw,
                state,
                replace(history, registry_id="other"),
            )

    def test_history_dictionary_fails(self):
        _, _, _, state, history = case()

        with self.assertRaises(ValueError):
            validate_revocation_history(
                history.__dict__,
                state,
            )

    def test_tombstone_collection_must_be_tuple(self):
        _, _, _, state, history = case("disabled")

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=list(history.tombstones),
                ),
                state,
            )

    def test_non_dataclass_tombstone_fails(self):
        _, _, _, state, history = case("disabled")

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=(
                        history.tombstones[0].__dict__,
                    ),
                ),
                state,
            )

    def test_invalid_tombstone_status_fails(self):
        _, _, _, state, history = case("revoked")

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=(
                        replace(
                            history.tombstones[0],
                            status="active",
                        ),
                    ),
                ),
                state,
            )

    def test_invalid_tombstone_public_key_fails(self):
        _, _, _, state, history = case("revoked")

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=(
                        replace(
                            history.tombstones[0],
                            public_key_hex="0" * 64,
                        ),
                    ),
                ),
                state,
            )

    def test_unsorted_tombstones_fail(self):
        _, _, _, state, history = case("revoked")

        first = history.tombstones[0]
        second = replace(
            first,
            key_id="zzz",
            public_key_hex="b" * 64,
        )

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=(second, first),
                ),
                state,
            )

    def test_duplicate_tombstones_fail(self):
        _, _, _, state, history = case("revoked")

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=history.tombstones * 2,
                ),
                state,
            )

    def test_public_key_reused_between_tombstones_fails(self):
        _, _, _, state, history = case("revoked")

        second = replace(
            history.tombstones[0],
            key_id="zzz",
        )

        with self.assertRaises(ValueError):
            validate_revocation_history(
                replace(
                    history,
                    tombstones=history.tombstones + (second,),
                ),
                state,
            )

    def test_previous_registry_must_match_supplied_snapshot(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        changed = deepcopy(document)
        changed["keys"][0]["status"] = "disabled"
        changed_old = sign_document(changed, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                changed_old,
                raw,
                state,
                history,
            )

    def test_candidate_must_be_consecutive_revision(self):
        old, document, private, state, history = case()

        with self.assertRaises(ValueError):
            self.evaluate(old, old, state, history)

    def test_candidate_revision_gap_fails(self):
        old, document, private, state, history = case()

        changed = deepcopy(document)
        changed["revision"] = 3
        changed["previous_revision"] = 2
        changed["previous_digest"] = "a" * 64

        raw = sign_document(changed, private)

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_wrong_predecessor_digest_fails(self):
        old, document, private, state, history = case()
        _, changed = advance(document, private)

        changed["previous_digest"] = "a" * 64
        raw = sign_document(changed, private)

        with self.assertRaises(ValueError):
            self.evaluate(old, raw, state, history)

    def test_noncanonical_registry_fails(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        with self.assertRaises(ValueError):
            self.evaluate(
                old,
                raw + b" ",
                state,
                history,
            )

    def test_signature_is_not_cryptographically_verified_here(self):
        old, document, private, state, history = case()
        _, candidate = advance(document, private)

        candidate["signature"] = "A" * 86
        raw = canonical_registry_bytes(candidate)

        result = self.evaluate(
            old,
            raw,
            state,
            history,
        )

        self.assertTrue(result.logical_lifecycle_continuity_valid)
        self.assertFalse(result.registry_signature_verified)

    def test_positive_result_does_not_claim_trust_or_commit(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private)

        result = self.evaluate(
            old,
            raw,
            state,
            history,
        )

        for flag in (
            "registry_signature_verified",
            "administrative_policy_authenticated",
            "snapshot_provenance_authenticated",
            "revocation_history_authenticated",
            "revocation_currentness_verified",
            "rollback_prevention_verified",
            "trusted_time_source_verified",
            "state_commit_performed",
            "revocation_history_persisted",
            "atomic_update_authorized",
            "collector_authenticated",
            "runtime_isolation_proven",
            "docker_execution_permitted",
            "production_execution_enabled",
            "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, flag), flag)

        self.assertTrue(result.manual_verification_required)

    def test_proposal_is_not_committed_state(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private, status="revoked")

        result = self.evaluate(
            old,
            raw,
            state,
            history,
        )

        self.assertEqual(history.tombstones, ())
        self.assertEqual(result.proposal.candidate_revision, 2)
        self.assertFalse(hasattr(result.proposal, "generation"))

    def test_inputs_are_unchanged(self):
        old, document, private, state, history = case()
        raw, _ = advance(document, private, status="revoked")

        original = deepcopy(
            (old, raw, state, history, document)
        )

        self.evaluate(old, raw, state, history)

        self.assertEqual(
            (old, raw, state, history, document),
            original,
        )


if __name__ == "__main__":
    unittest.main()
