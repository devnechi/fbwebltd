#!/usr/bin/env python3
"""Gate 4D.22C.3D.12I adversarial pure policy continuity tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from lab_authority_policy_continuity import (
    AuthorityRoleBindings,
    AuthorityPolicySnapshot,
    GENESIS_DIGEST,
    assess_authority_policy_transition,
    untrusted_policy_commitment,
    validate_authority_policy_snapshot,
    validate_policy_binding,
)
from lab_authority_signature_verifier import (
    AuthorityResponseKey,
    AuthorityResponseKeyPolicy,
    POLICY_ID,
    PURPOSES,
)
from lab_authority_evidence_contract import AuthorityReadChallenge
from lab_collector_trust_policy import REGISTRY_ID
from lab_protected_state_contract import ProtectedPosition, revocation_commitment
from lab_registry_wire_format import MAX_SAFE_INTEGER, REGISTRY_FORMAT_VERSION
from lab_runtime_auth_envelope import ALGORITHM


def key(role, number=1, *, status="active", material=None):
    authority = {"ADMIN": "authority-admin", "STATE": "authority-state",
                 "WITNESS": "authority-witness"}[role]
    hex_char = material or {"ADMIN": "a", "STATE": "b", "WITNESS": "c"}[role]
    if number > 1 and material is None:
        hex_char = "d"
    return AuthorityResponseKey(
        role=role, authority_id=authority, key_id="key-" + role.lower() + "-" + str(number),
        public_key_hex=hex_char * 64, algorithm=ALGORITHM,
        purpose=PURPOSES[role], status=status,
        valid_from="2026-10-13T00:00:00Z", valid_until="2026-11-13T00:00:00Z",
    )


def policy(keys):
    return AuthorityResponseKeyPolicy(
        POLICY_ID, tuple(sorted(keys, key=lambda k: (k.role, k.authority_id, k.key_id)))
    )


def genesis():
    return AuthorityPolicySnapshot(
        registry_id=REGISTRY_ID, policy_id=POLICY_ID, epoch=1, generation=1,
        recovery_epoch=1, previous_commitment=GENESIS_DIGEST,
        transition_id="bootstrap-1",
        roles=AuthorityRoleBindings("authority-state", "authority-witness", "authority-admin"),
        key_policy=policy([key("STATE"), key("WITNESS"), key("ADMIN")]),
    )


def future(old, keys, **updates):
    result = replace(
        old, epoch=old.epoch + 1, generation=old.generation + 1,
        previous_commitment=untrusted_policy_commitment(old),
        transition_id="rotation-" + str(old.epoch + 1), key_policy=policy(keys),
    )
    return replace(result, **updates)


def with_state_rotation(old=None, *, retired="disabled"):
    old = genesis() if old is None else old
    keys = [replace(k, status=retired) if k.role == "STATE" else k
            for k in old.key_policy.keys]
    keys.append(key("STATE", 2))
    return old, future(old, keys)


class AuthorityPolicyContinuityTests(unittest.TestCase):
    def setUp(self):
        self.old = genesis()
        self.after = future(self.old, list(self.old.key_policy.keys) + [key("STATE", 2)])

    def reject(self, candidate, previous=None):
        with self.assertRaises(ValueError):
            assess_authority_policy_transition(self.old if previous is None else previous, candidate)

    def test_genesis_shape_valid(self):
        self.assertTrue(validate_authority_policy_snapshot(self.old))

    def test_genesis_is_not_independently_authenticated(self):
        # A caller can fabricate a fully self-consistent bootstrap declaration.
        self.assertTrue(validate_authority_policy_snapshot(genesis()))

    def test_deterministic_commitment(self):
        self.assertEqual(untrusted_policy_commitment(self.old), untrusted_policy_commitment(genesis()))

    def test_commitment_is_not_plain_json_hash(self):
        import hashlib, json
        from dataclasses import asdict
        plain = hashlib.sha256(json.dumps(asdict(self.old), sort_keys=True,
            separators=(",", ":")).encode("ascii")).hexdigest()
        self.assertNotEqual(plain, untrusted_policy_commitment(self.old))

    def test_add_new_state_key(self):
        result = assess_authority_policy_transition(self.old, self.after)
        self.assertEqual(result.new_keys, (("STATE", "authority-state", "key-state-2"),))
        self.assertEqual(result.proposed_epoch, 2)

    def test_disable_old_key_during_rotation(self):
        old, new = with_state_rotation()
        result = assess_authority_policy_transition(old, new)
        self.assertEqual(result.status_changes[0][-2:], ("active", "disabled"))

    def test_revoke_old_key_during_rotation(self):
        old, new = with_state_rotation(retired="revoked")
        self.assertEqual(assess_authority_policy_transition(old, new).status_changes[0][-1], "revoked")

    def test_disabled_to_revoked(self):
        old, middle = with_state_rotation()
        newest = future(middle, [replace(k, status="revoked") if k.key_id == "key-state-1" else k
                                 for k in middle.key_policy.keys])
        self.assertTrue(assess_authority_policy_transition(middle, newest).logical_continuity_valid)

    def test_disabled_to_active_denied(self):
        old, middle = with_state_rotation()
        newest = future(middle, [replace(k, status="active") if k.key_id == "key-state-1" else k
                                 for k in middle.key_policy.keys])
        self.reject(newest, middle)

    def test_revoked_to_disabled_denied(self):
        old, middle = with_state_rotation(retired="revoked")
        newest = future(middle, [replace(k, status="disabled") if k.key_id == "key-state-1" else k
                                 for k in middle.key_policy.keys])
        self.reject(newest, middle)

    def test_revoked_to_active_denied(self):
        old, middle = with_state_rotation(retired="revoked")
        newest = future(middle, [replace(k, status="active") if k.key_id == "key-state-1" else k
                                 for k in middle.key_policy.keys])
        self.reject(newest, middle)

    def test_disabled_record_deletion_denied(self):
        old, middle = with_state_rotation()
        newest = future(middle, [k for k in middle.key_policy.keys if k.key_id != "key-state-1"] + [key("ADMIN", 2, material="e")])
        self.reject(newest, middle)

    def test_revoked_record_deletion_denied(self):
        old, middle = with_state_rotation(retired="revoked")
        newest = future(middle, [k for k in middle.key_policy.keys if k.key_id != "key-state-1"] + [key("ADMIN", 2, material="e")])
        self.reject(newest, middle)

    def test_key_material_rebinding_denied(self):
        modified = [replace(k, public_key_hex="e" * 64) if k.role == "STATE" else k
                    for k in self.old.key_policy.keys]
        self.reject(future(self.old, modified))

    def test_validity_window_mutation_denied(self):
        changed = [replace(k, valid_until="2027-11-13T00:00:00Z") if k.role == "ADMIN" else k
                   for k in self.old.key_policy.keys]
        self.reject(future(self.old, changed))

    def test_key_id_rebinding_denied(self):
        keys = [replace(k, key_id="key-state-replaced") if k.role == "STATE" else k
                for k in self.old.key_policy.keys]
        self.reject(future(self.old, keys))

    def test_reused_material_across_roles_denied(self):
        keys = list(self.old.key_policy.keys) + [key("STATE", 2, material="a")]
        self.reject(future(self.old, keys))

    def test_unapproved_extra_authority_label_denied(self):
        keys = list(self.old.key_policy.keys) + [replace(key("STATE", 2), authority_id="new-state")]
        self.reject(future(self.old, keys))

    def test_changed_role_binding_denied(self):
        candidate = replace(self.after, roles=replace(self.after.roles, state_authority_id="new-state"))
        self.reject(candidate)

    def test_changed_recovery_epoch_denied(self):
        self.reject(replace(self.after, recovery_epoch=2))

    def test_skipped_epoch_denied(self):
        self.reject(replace(self.after, epoch=3))

    def test_repeated_epoch_denied(self):
        self.reject(replace(self.after, epoch=1))

    def test_skipped_generation_denied(self):
        self.reject(replace(self.after, generation=3))

    def test_repeated_generation_denied(self):
        self.reject(replace(self.after, generation=1))

    def test_wrong_parent_digest_denied(self):
        self.reject(replace(self.after, previous_commitment="f" * 64))

    def test_repeated_transition_identifier_denied(self):
        self.reject(replace(self.after, transition_id=self.old.transition_id))

    def test_empty_rotation_denied(self):
        empty = future(self.old, self.old.key_policy.keys)
        self.reject(empty)

    def test_wrong_registry_denied(self):
        self.reject(replace(self.after, registry_id="other"))

    def test_wrong_policy_identity_denied(self):
        self.reject(replace(self.after, policy_id="other"))

    def test_boolean_epoch_denied(self):
        self.reject(replace(self.after, epoch=True))

    def test_zero_epoch_denied(self):
        self.reject(replace(self.after, epoch=0))

    def test_bootstrap_parent_nonzero_denied(self):
        with self.assertRaises(ValueError):
            validate_authority_policy_snapshot(replace(self.old, previous_commitment="f" * 64))

    def test_nonbootstrap_parent_zero_denied(self):
        self.reject(replace(self.after, previous_commitment=GENESIS_DIGEST))

    def test_self_consistent_unanchored_parent_not_trusted(self):
        fake = replace(self.after, previous_commitment="f" * 64)
        self.assertTrue(validate_authority_policy_snapshot(fake))
        self.reject(fake)

    def test_duplicate_role_bindings_denied(self):
        with self.assertRaises(ValueError):
            validate_authority_policy_snapshot(replace(self.old, roles=replace(self.old.roles,
                admin_authority_id=self.old.roles.state_authority_id)))

    def test_missing_active_role_denied(self):
        all_disabled = [replace(k, status="disabled") if k.role == "STATE" else k
                        for k in self.old.key_policy.keys]
        self.reject(future(self.old, all_disabled))

    def test_unsorted_policy_keys_denied(self):
        with self.assertRaises(ValueError):
            validate_authority_policy_snapshot(replace(self.old,
                key_policy=AuthorityResponseKeyPolicy(POLICY_ID, self.old.key_policy.keys[::-1])))

    def test_empty_key_policy_denied(self):
        with self.assertRaises(ValueError):
            validate_authority_policy_snapshot(replace(self.old,
                key_policy=AuthorityResponseKeyPolicy(POLICY_ID, ())))

    def test_invalid_key_status_denied(self):
        changed = [replace(k, status="retired") if k.role == "STATE" else k
                   for k in self.old.key_policy.keys]
        self.reject(future(self.old, changed))

    def test_zero_key_denied(self):
        changed = [replace(k, public_key_hex="0" * 64) if k.role == "STATE" else k
                   for k in self.old.key_policy.keys]
        self.reject(future(self.old, changed))

    def test_new_disabled_key_denied(self):
        self.reject(future(self.old,
            list(self.old.key_policy.keys) + [key("STATE", 2, status="disabled")]))

    def test_existing_status_unchanged_plus_new_key_allowed(self):
        self.assertEqual(assess_authority_policy_transition(self.old, self.after).status_changes, ())

    def test_bad_snapshot_type_denied(self):
        with self.assertRaises(ValueError):
            validate_authority_policy_snapshot({})

    def test_policy_binding_structurally_agrees(self):
        challenge, position = self._binding_inputs()
        self.assertTrue(validate_policy_binding(self.old, challenge, position))

    def test_policy_binding_epoch_conflict_denied(self):
        challenge, position = self._binding_inputs()
        with self.assertRaises(ValueError):
            validate_policy_binding(self.old, challenge, replace(position, policy_epoch=2))

    def test_policy_binding_authority_conflict_denied(self):
        challenge, position = self._binding_inputs()
        with self.assertRaises(ValueError):
            validate_policy_binding(self.old, replace(challenge,
                witness_authority_id="other-witness"), position)

    def _binding_inputs(self):
        from test_lab_protected_state_contract import fixture
        bundle, _ = fixture()
        challenge = AuthorityReadChallenge(
            registry_id=REGISTRY_ID, request_id="request-1",
            challenge_hex="a" * 64,
            state_authority_id=self.old.roles.state_authority_id,
            witness_authority_id=self.old.roles.witness_authority_id,
            admin_authority_id=self.old.roles.admin_authority_id,
        )
        return challenge, bundle.position

    def test_flags_all_remain_non_authorizing(self):
        result = assess_authority_policy_transition(self.old, self.after)
        for field in (
            "independently_trusted_policy", "policy_approval_authenticated",
            "independent_bootstrap_verified", "protected_epoch_committed",
            "policy_provenance_authenticated", "protected_storage_verified",
            "recovery_authorized", "authority_identity_authenticated",
            "trusted_time_verified", "replay_prevention_verified",
            "rollback_prevention_verified", "durable_commit_verified",
            "runtime_isolation_proven", "docker_execution_permitted",
            "production_execution_enabled", "automatic_retry_permitted",
        ):
            self.assertFalse(getattr(result, field), field)
        self.assertTrue(result.manual_verification_required)

    def test_frozen_assessment(self):
        result = assess_authority_policy_transition(self.old, self.after)
        with self.assertRaises(FrozenInstanceError):
            result.proposed_epoch = 99

    def test_inputs_not_mutated(self):
        saved = deepcopy((self.old, self.after))
        assess_authority_policy_transition(self.old, self.after)
        self.assertEqual((self.old, self.after), saved)

    def test_epoch_exhaustion_denied(self):
        saturated = replace(self.old, epoch=MAX_SAFE_INTEGER,
            generation=MAX_SAFE_INTEGER, previous_commitment="f" * 64)
        self.reject(self.after, saturated)

    def test_generation_exhaustion_denied(self):
        saturated = replace(self.old, generation=MAX_SAFE_INTEGER)
        self.reject(self.after, saturated)


if __name__ == "__main__":
    unittest.main()
