#!/usr/bin/env python3
"""Gate 4D.22C.3D.12Q adversarial NON-AUTHORIZING policy tests."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))

from lab_collector_trust_policy import REGISTRY_ID
from lab_registry_wire_format import MAX_SAFE_INTEGER
from lab_replay_protected_contract import (
    LEDGER_ID, FORMAT_VERSION as POSITION_VERSION,
    ReplayProtectedPosition, ZERO_DIGEST,
)
from lab_replay_signature_verifier import (
    POLICY_ID, PURPOSES, ReplayReadChallenge, ReplayResponseKey,
    ReplayResponseKeyPolicy,
)
from lab_replay_policy_continuity import (
    FORMAT_VERSION, GENESIS_DIGEST,
    ReplayPolicyRoleBindings, ReplayPolicySnapshot,
    ReplayPolicyCheckpoint, assess_replay_policy_transition,
    classify_replay_policy_reconciliation, replay_policy_checkpoint,
    untrusted_replay_policy_commitment, validate_replay_policy_binding,
    validate_replay_policy_checkpoint, validate_replay_policy_snapshot,
)
from lab_runtime_auth_envelope import ALGORITHM

ROLE_IDS = {"REPLAY_STATE": "replay-state-1", "REPLAY_WITNESS": "replay-witness-1"}


def key(role, suffix="1", *, material=None, status="active"):
    return ReplayResponseKey(
        role=role, authority_id=ROLE_IDS[role], key_id="key-" + role.lower() + suffix,
        public_key_hex=(material or ("a" if role == "REPLAY_STATE" else "b")) * 64,
        algorithm=ALGORITHM, purpose=PURPOSES[role], status=status,
        valid_from="2026-10-13T00:00:00Z", valid_until="2026-11-13T00:00:00Z",
    )


def policy(keys, epoch=1):
    return ReplayResponseKeyPolicy(POLICY_ID, epoch, tuple(sorted(
        keys, key=lambda k: (k.role, k.authority_id, k.key_id),
    )))


def genesis():
    return ReplayPolicySnapshot(
        registry_id=REGISTRY_ID, ledger_id=LEDGER_ID,
        format_version=FORMAT_VERSION, policy_id=POLICY_ID,
        epoch=1, generation=1, recovery_epoch=1,
        previous_commitment=GENESIS_DIGEST, transition_id="bootstrap-1",
        issuer_id="policy-issuer-1", approval_reference="approval-1",
        roles=ReplayPolicyRoleBindings(ROLE_IDS["REPLAY_STATE"],
                                       ROLE_IDS["REPLAY_WITNESS"]),
        key_policy=policy([key("REPLAY_STATE"), key("REPLAY_WITNESS")]),
    )


def future(previous, keys, **changes):
    epoch = previous.epoch + 1
    result = replace(
        previous, epoch=epoch, generation=previous.generation + 1,
        previous_commitment=untrusted_replay_policy_commitment(previous),
        transition_id="rotate-" + str(epoch),
        approval_reference="approval-" + str(epoch),
        key_policy=policy(keys, epoch),
    )
    return replace(result, **changes)


def state_rotation(previous=None, retire="disabled"):
    previous = genesis() if previous is None else previous
    keys = [replace(k, status=retire) if k.role == "REPLAY_STATE" else k
            for k in previous.key_policy.keys]
    keys.append(key("REPLAY_STATE", "2", material="c"))
    return previous, future(previous, keys)


def challenge(epoch=1, recovery=1):
    return ReplayReadChallenge(
        REGISTRY_ID, LEDGER_ID, "read-1", "a" * 64,
        ROLE_IDS["REPLAY_STATE"], ROLE_IDS["REPLAY_WITNESS"], epoch, recovery,
    )


def position(epoch=1, recovery=1):
    return ReplayProtectedPosition(
        REGISTRY_ID, LEDGER_ID, POSITION_VERSION, 0, "c" * 64,
        epoch, recovery, "bootstrap-0", ZERO_DIGEST,
    )


class ReplayPolicyContinuityTests(unittest.TestCase):
    def setUp(self):
        self.old = genesis()
        self.new = future(self.old, self.old.key_policy.keys + (
            key("REPLAY_STATE", "2", material="c"),
        ))

    def reject(self, candidate, old=None):
        with self.assertRaises(ValueError):
            assess_replay_policy_transition(
                self.old if old is None else old, candidate,
            )

    def reject_shape(self, **changes):
        with self.assertRaises(ValueError):
            validate_replay_policy_snapshot(replace(self.old, **changes))

    def test_genesis_valid_shape(self):
        self.assertTrue(validate_replay_policy_snapshot(self.old))

    def test_genesis_does_not_authenticate_root(self):
        self.assertTrue(validate_replay_policy_snapshot(deepcopy(self.old)))
        self.assertFalse(assess_replay_policy_transition(self.old, self.new).independent_bootstrap_verified)

    def test_deterministic_policy_digest(self):
        self.assertEqual(untrusted_replay_policy_commitment(self.old),
                         untrusted_replay_policy_commitment(genesis()))

    def test_policy_digest_is_domain_separated(self):
        import hashlib
        import json
        from dataclasses import asdict
        raw = json.dumps(asdict(self.old), sort_keys=True,
                         separators=(",", ":")).encode()
        self.assertNotEqual(untrusted_replay_policy_commitment(self.old),
                            hashlib.sha256(raw).hexdigest())

    def test_normal_enrollment(self):
        result = assess_replay_policy_transition(self.old, self.new)
        self.assertEqual(result.proposed_epoch, 2)
        self.assertEqual(result.proposed_generation, 2)
        self.assertEqual(result.new_keys,
                         (("REPLAY_STATE", ROLE_IDS["REPLAY_STATE"],
                           "key-replay_state2"),))

    def test_normal_witness_enrollment(self):
        candidate = future(self.old, self.old.key_policy.keys + (
            key("REPLAY_WITNESS", "2", material="d"),
        ))
        self.assertEqual(len(assess_replay_policy_transition(
            self.old, candidate).new_keys), 1)

    def test_disable_state_key_with_replacement(self):
        old, new = state_rotation()
        result = assess_replay_policy_transition(old, new)
        self.assertEqual(result.status_changes[0][-2:], ("active", "disabled"))

    def test_revoke_state_key_with_replacement(self):
        old, new = state_rotation(retire="revoked")
        self.assertEqual(assess_replay_policy_transition(old, new).status_changes[0][-1],
                         "revoked")

    def test_disabled_to_revoked(self):
        old, middle = state_rotation()
        later = future(middle, [replace(k, status="revoked")
                                if k.key_id == "key-replay_state1" else k
                                for k in middle.key_policy.keys])
        self.assertEqual(len(assess_replay_policy_transition(middle, later).status_changes), 1)

    def test_disabled_to_active_rejected(self):
        old, middle = state_rotation()
        later = future(middle, [replace(k, status="active")
                                if k.key_id == "key-replay_state1" else k
                                for k in middle.key_policy.keys])
        self.reject(later, middle)

    def test_revoked_to_disabled_rejected(self):
        old, middle = state_rotation(retire="revoked")
        later = future(middle, [replace(k, status="disabled")
                                if k.key_id == "key-replay_state1" else k
                                for k in middle.key_policy.keys])
        self.reject(later, middle)

    def test_revoked_to_active_rejected(self):
        old, middle = state_rotation(retire="revoked")
        later = future(middle, [replace(k, status="active")
                                if k.key_id == "key-replay_state1" else k
                                for k in middle.key_policy.keys])
        self.reject(later, middle)

    def test_revoked_key_deletion_rejected(self):
        old, middle = state_rotation(retire="revoked")
        keys = [k for k in middle.key_policy.keys if k.key_id != "key-replay_state1"]
        keys.append(key("REPLAY_WITNESS", "2", material="d"))
        self.reject(future(middle, keys), middle)

    def test_disabled_key_deletion_rejected(self):
        old, middle = state_rotation()
        keys = [k for k in middle.key_policy.keys if k.key_id != "key-replay_state1"]
        keys.append(key("REPLAY_WITNESS", "2", material="d"))
        self.reject(future(middle, keys), middle)

    def test_active_key_deletion_rejected(self):
        keys = [k for k in self.old.key_policy.keys if k.role != "REPLAY_STATE"]
        keys.append(key("REPLAY_STATE", "2", material="c"))
        self.reject(future(self.old, keys))

    def test_rebind_key_material_rejected(self):
        keys = [replace(k, public_key_hex="e" * 64)
                if k.role == "REPLAY_STATE" else k for k in self.old.key_policy.keys]
        self.reject(future(self.old, keys))

    def test_rebind_key_purpose_rejected(self):
        keys = [replace(k, purpose=PURPOSES["REPLAY_WITNESS"])
                if k.role == "REPLAY_STATE" else k for k in self.old.key_policy.keys]
        self.reject(future(self.old, keys))

    def test_rebind_key_validity_start_rejected(self):
        keys = [replace(k, valid_from="2026-10-14T00:00:00Z")
                if k.role == "REPLAY_STATE" else k for k in self.old.key_policy.keys]
        self.reject(future(self.old, keys))

    def test_rebind_key_validity_end_rejected(self):
        keys = [replace(k, valid_until="2026-12-13T00:00:00Z")
                if k.role == "REPLAY_STATE" else k for k in self.old.key_policy.keys]
        self.reject(future(self.old, keys))

    def test_rebind_key_id_rejected(self):
        keys = [replace(k, key_id="replacement-state-key")
                if k.role == "REPLAY_STATE" else k for k in self.old.key_policy.keys]
        self.reject(future(self.old, keys))

    def test_reenroll_old_material_rejected(self):
        new = future(self.old, self.old.key_policy.keys + (
            key("REPLAY_STATE", "2", material="a"),
        ))
        self.reject(new)

    def test_duplicate_material_cross_role_rejected(self):
        new = future(self.old, self.old.key_policy.keys + (
            key("REPLAY_WITNESS", "2", material="a"),
        ))
        self.reject(new)

    def test_new_key_must_start_active(self):
        new = future(self.old, self.old.key_policy.keys + (
            key("REPLAY_STATE", "2", material="c", status="disabled"),
        ))
        self.reject(new)

    def test_pinned_state_authority_change_rejected(self):
        self.reject(replace(self.new, roles=replace(
            self.new.roles, replay_state_authority_id="alternate-state")))

    def test_pinned_witness_authority_change_rejected(self):
        self.reject(replace(self.new, roles=replace(
            self.new.roles, replay_witness_authority_id="alternate-witness")))

    def test_issuer_change_rejected(self):
        self.reject(replace(self.new, issuer_id="alternate-issuer"))

    def test_recovery_epoch_change_rejected(self):
        self.reject(replace(self.new, recovery_epoch=2))

    def test_epoch_skip_rejected(self):
        self.reject(replace(self.new, epoch=3,
                            key_policy=replace(self.new.key_policy, epoch=3)))

    def test_epoch_repeat_rejected(self):
        self.reject(replace(self.new, epoch=1,
                            key_policy=replace(self.new.key_policy, epoch=1)))

    def test_generation_skip_rejected(self):
        self.reject(replace(self.new, generation=3))

    def test_generation_repeat_rejected(self):
        self.reject(replace(self.new, generation=1))

    def test_parent_digest_mismatch_rejected(self):
        self.reject(replace(self.new, previous_commitment="f" * 64))

    def test_transition_id_reuse_rejected(self):
        self.reject(replace(self.new, transition_id=self.old.transition_id))

    def test_approval_reference_reuse_rejected(self):
        self.reject(replace(self.new, approval_reference=self.old.approval_reference))

    def test_empty_rotation_rejected(self):
        self.reject(future(self.old, self.old.key_policy.keys))

    def test_wrong_registry_rejected(self):
        self.reject(replace(self.new, registry_id="other-registry"))

    def test_wrong_ledger_rejected(self):
        self.reject(replace(self.new, ledger_id="other-ledger"))

    def test_wrong_policy_id_rejected(self):
        self.reject(replace(self.new, policy_id="other-policy"))

    def test_wrong_format_rejected(self):
        self.reject(replace(self.new, format_version=2))

    def test_boolean_epoch_rejected(self):
        self.reject_shape(epoch=True)

    def test_zero_epoch_rejected(self):
        self.reject_shape(epoch=0)

    def test_boolean_generation_rejected(self):
        self.reject_shape(generation=True)

    def test_epoch_overflow_rejected(self):
        self.reject_shape(epoch=MAX_SAFE_INTEGER + 1)

    def test_generation_overflow_rejected(self):
        self.reject_shape(generation=MAX_SAFE_INTEGER + 1)

    def test_missing_genesis_parent_rejected(self):
        self.reject_shape(previous_commitment="f" * 64)

    def test_non_genesis_with_zero_parent_rejected(self):
        self.reject(replace(self.new, previous_commitment=GENESIS_DIGEST))

    def test_invalid_role_bindings_type_rejected(self):
        self.reject_shape(roles={})

    def test_duplicate_role_labels_rejected(self):
        self.reject_shape(roles=ReplayPolicyRoleBindings("shared", "shared"))

    def test_role_key_outside_pinned_identity_rejected(self):
        keys = [replace(k, authority_id="outside") if k.role == "REPLAY_STATE" else k
                for k in self.old.key_policy.keys]
        self.reject_shape(key_policy=policy(keys))

    def test_key_policy_epoch_mismatch_rejected(self):
        self.reject_shape(key_policy=replace(self.old.key_policy, epoch=2))

    def test_unsorted_keys_rejected(self):
        self.reject_shape(key_policy=replace(
            self.old.key_policy, keys=tuple(reversed(self.old.key_policy.keys))))

    def test_no_active_state_key_rejected(self):
        keys = [replace(k, status="revoked") if k.role == "REPLAY_STATE" else k
                for k in self.old.key_policy.keys]
        self.reject_shape(key_policy=policy(keys))

    def test_no_active_witness_key_rejected(self):
        keys = [replace(k, status="disabled") if k.role == "REPLAY_WITNESS" else k
                for k in self.old.key_policy.keys]
        self.reject_shape(key_policy=policy(keys))

    def test_invalid_issuer_rejected(self):
        self.reject_shape(issuer_id="!bad")

    def test_invalid_approval_reference_rejected(self):
        self.reject_shape(approval_reference="bad reference")

    def test_caller_supplied_policy_binding_valid(self):
        self.assertTrue(validate_replay_policy_binding(
            self.old, challenge(), position()))

    def test_policy_binding_old_epoch_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_binding(self.new, challenge(), position())

    def test_policy_binding_wrong_recovery_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_binding(self.old, challenge(recovery=2), position())

    def test_policy_binding_wrong_state_role_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_binding(self.old,
                replace(challenge(), state_authority_id="other"), position())

    def test_policy_binding_wrong_witness_role_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_binding(self.old,
                replace(challenge(), witness_authority_id="other"), position())

    def test_checkpoint_logical_shape(self):
        self.assertTrue(validate_replay_policy_checkpoint(
            replay_policy_checkpoint(self.old)))

    def test_checkpoint_wrong_type_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_checkpoint({})

    def test_checkpoint_wrong_policy_id_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_checkpoint(replace(
                replay_policy_checkpoint(self.old), policy_id="other"))

    def test_checkpoint_boolean_epoch_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_checkpoint(replace(
                replay_policy_checkpoint(self.old), epoch=True))

    def test_checkpoint_bad_commitment_rejected(self):
        with self.assertRaises(ValueError):
            validate_replay_policy_checkpoint(replace(
                replay_policy_checkpoint(self.old), policy_commitment="g" * 64))

    def classify(self, state, witness):
        return classify_replay_policy_reconciliation(self.old, self.new, state, witness)

    def test_both_old_untrusted(self):
        self.assertEqual(self.classify(self.old, replay_policy_checkpoint(self.old)).classification,
                         "BOTH_PREVIOUS_UNTRUSTED")

    def test_state_ahead_witness_old(self):
        self.assertEqual(self.classify(self.new, replay_policy_checkpoint(self.old)).classification,
                         "POLICY_STATE_AHEAD_OF_WITNESS")

    def test_witness_ahead_state_old(self):
        self.assertEqual(self.classify(self.old, replay_policy_checkpoint(self.new)).classification,
                         "POLICY_WITNESS_AHEAD_OF_STATE")

    def test_both_new_still_untrusted(self):
        self.assertEqual(self.classify(self.new, replay_policy_checkpoint(self.new)).classification,
                         "BOTH_PROPOSED_UNTRUSTED")

    def test_state_unavailable(self):
        self.assertEqual(self.classify(None, replay_policy_checkpoint(self.new)).classification,
                         "POLICY_STATE_UNAVAILABLE")

    def test_witness_unavailable(self):
        self.assertEqual(self.classify(self.new, None).classification,
                         "POLICY_WITNESS_UNAVAILABLE")

    def test_both_unavailable(self):
        self.assertEqual(self.classify(None, None).classification,
                         "BOTH_POLICY_AUTHORITIES_UNAVAILABLE")

    def test_state_rollback_suspected(self):
        old, middle = state_rotation()
        newest = future(middle, middle.key_policy.keys + (
            key("REPLAY_WITNESS", "2", material="d"),
        ))
        result = classify_replay_policy_reconciliation(
            middle, newest, old, replay_policy_checkpoint(middle))
        self.assertEqual(result.classification, "POLICY_STATE_ROLLBACK_SUSPECTED")

    def test_witness_rollback_suspected(self):
        old, middle = state_rotation()
        newest = future(middle, middle.key_policy.keys + (
            key("REPLAY_WITNESS", "2", material="d"),
        ))
        result = classify_replay_policy_reconciliation(
            middle, newest, middle, replay_policy_checkpoint(old))
        self.assertEqual(result.classification, "POLICY_WITNESS_ROLLBACK_SUSPECTED")

    def test_conflicting_checkpoint(self):
        fake = replace(replay_policy_checkpoint(self.new), policy_commitment="f" * 64)
        self.assertEqual(self.classify(self.new, fake).classification,
                         "CONFLICTING_OR_UNEXPECTED_POLICY_POSITIONS")

    def test_same_generation_forged_state(self):
        fake = replace(self.new, issuer_id="other-issuer")
        self.assertEqual(self.classify(fake, replay_policy_checkpoint(self.new)).classification,
                         "CONFLICTING_OR_UNEXPECTED_POLICY_POSITIONS")

    def test_untrusted_policy_forgery_not_authenticated(self):
        forged = deepcopy(self.new)
        result = self.classify(forged, replay_policy_checkpoint(forged))
        self.assertEqual(result.classification, "BOTH_PROPOSED_UNTRUSTED")
        self.assertFalse(result.state_and_witness_authenticated)

    def test_reconciliation_rejects_invalid_target(self):
        with self.assertRaises(ValueError):
            classify_replay_policy_reconciliation(
                self.old, replace(self.new, previous_commitment="f" * 64),
                self.old, replay_policy_checkpoint(self.old))

    def test_reconciliation_rejects_invalid_checkpoint(self):
        with self.assertRaises(ValueError):
            self.classify(self.new, {})

    def test_assessment_is_immutable(self):
        result = assess_replay_policy_transition(self.old, self.new)
        with self.assertRaises(FrozenInstanceError):
            result.proposed_epoch = 9

    def test_all_transition_trust_flags_false(self):
        result = assess_replay_policy_transition(self.old, self.new)
        for field in (
            "independent_issuer_authenticated", "independent_trust_root_verified",
            "independent_bootstrap_verified", "independent_policy_approval_verified",
            "protected_policy_storage_verified", "policy_currentness_verified",
            "trusted_time_verified", "durable_policy_commit_verified",
            "independent_witness_verified", "rollback_prevention_verified",
            "recovery_approved", "replay_prevention_verified", "runtime_isolation_proven",
            "automatic_retry_permitted", "docker_execution_permitted",
            "production_execution_enabled",
        ):
            self.assertFalse(getattr(result, field), field)
        self.assertTrue(result.manual_verification_required)

    def test_all_reconciliation_trust_flags_false(self):
        result = self.classify(self.new, replay_policy_checkpoint(self.new))
        for field in (
            "state_and_witness_authenticated", "independent_trust_root_verified",
            "protected_policy_currentness_verified", "durable_policy_commit_verified",
            "independent_rollback_prevention_verified", "recovery_approved",
            "automatic_retry_permitted", "docker_execution_permitted",
            "production_execution_enabled",
        ):
            self.assertFalse(getattr(result, field), field)
        self.assertTrue(result.manual_verification_required)

    def test_inputs_not_mutated(self):
        old = deepcopy(self.old)
        new = deepcopy(self.new)
        assess_replay_policy_transition(self.old, self.new)
        self.assertEqual((old, new), (self.old, self.new))


if __name__ == "__main__":
    unittest.main()
