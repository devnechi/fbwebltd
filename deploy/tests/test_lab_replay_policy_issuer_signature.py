#!/usr/bin/env python3
"""Gate 4D.22C.3D.12S: adversarial offline issuer-signature tests."""

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

from lab_collector_trust_policy import REGISTRY_ID
from lab_replay_protected_contract import LEDGER_ID
from lab_replay_policy_continuity import (
    FORMAT_VERSION as SNAPSHOT_FORMAT_VERSION, GENESIS_DIGEST,
    ReplayPolicySnapshot, ReplayPolicyRoleBindings,
    untrusted_replay_policy_commitment,
)
from lab_replay_signature_verifier import (
    POLICY_ID, PURPOSES, ReplayResponseKey, ReplayResponseKeyPolicy,
)
from lab_replay_policy_issuer_signature import (
    ISSUER_KEY_POLICY_ID, ISSUER_PURPOSE, ISSUER_DOMAIN,
    FORMAT_VERSION, MAX_SIGNED_BYTES,
    ReplayPolicyIssuerKey, ReplayPolicyIssuerKeyPolicy,
    ReplayPolicyApprovalDeclaration, SignedReplayPolicyEnvelope,
    canonical_signed_issuer_bytes, issuer_signing_bytes,
    parse_signed_issuer_bytes, untrusted_approval_commitment,
    validate_approval_declaration, validate_issuer_key_policy,
    verify_replay_policy_issuer_signature,
)
from lab_runtime_auth_envelope import ALGORITHM

NOW = datetime(2026, 10, 14, 3, tzinfo=timezone.utc)


class ReplayPolicyIssuerTests(unittest.TestCase):
    def setUp(self):
        self.private = Ed25519PrivateKey.generate()
        self.issuer_key = ReplayPolicyIssuerKey(
            issuer_id="issuer-alpha", key_id="issuer-key-1",
            public_key_hex=self.private.public_key().public_bytes(
                Encoding.Raw, PublicFormat.Raw).hex(),
            algorithm=ALGORITHM, purpose=ISSUER_PURPOSE, status="active",
            valid_from="2026-10-13T00:00:00Z",
            valid_until="2026-10-15T00:00:00Z",
        )
        self.key_policy = ReplayPolicyIssuerKeyPolicy(
            ISSUER_KEY_POLICY_ID, (self.issuer_key,))
        keys = (
            ReplayResponseKey("REPLAY_STATE", "state-alpha", "state-key-1",
                              "a" * 64, ALGORITHM, PURPOSES["REPLAY_STATE"],
                              "active", "2026-10-13T00:00:00Z", "2026-11-13T00:00:00Z"),
            ReplayResponseKey("REPLAY_WITNESS", "witness-beta", "witness-key-1",
                              "b" * 64, ALGORITHM, PURPOSES["REPLAY_WITNESS"],
                              "active", "2026-10-13T00:00:00Z", "2026-11-13T00:00:00Z"),
        )
        self.snapshot = ReplayPolicySnapshot(
            registry_id=REGISTRY_ID, ledger_id=LEDGER_ID,
            format_version=SNAPSHOT_FORMAT_VERSION, policy_id=POLICY_ID,
            epoch=1, generation=1, recovery_epoch=1,
            previous_commitment=GENESIS_DIGEST, transition_id="bootstrap-1",
            issuer_id="issuer-alpha", approval_reference="approval-1",
            roles=ReplayPolicyRoleBindings("state-alpha", "witness-beta"),
            key_policy=ReplayResponseKeyPolicy(POLICY_ID, 1, keys),
        )
        self.approval = self.make_approval(self.snapshot)
        self.signed = self.sign(self.snapshot, self.approval)

    def make_approval(self, snapshot, **updates):
        approval = ReplayPolicyApprovalDeclaration(
            registry_id=snapshot.registry_id, ledger_id=snapshot.ledger_id,
            policy_id=snapshot.policy_id, issuer_id=snapshot.issuer_id,
            approval_reference=snapshot.approval_reference,
            transition_id=snapshot.transition_id,
            previous_commitment=snapshot.previous_commitment,
            proposed_commitment=untrusted_replay_policy_commitment(snapshot),
            epoch=snapshot.epoch, generation=snapshot.generation,
            recovery_epoch=snapshot.recovery_epoch,
            decision=("BOOTSTRAP_DECLARATION" if snapshot.epoch == 1
                      else "ROTATION_DECLARATION"),
            approver_ids=("approver-a", "approver-b"),
        )
        return replace(approval, **updates)

    def sign(self, snapshot, approval, **changes):
        record = SignedReplayPolicyEnvelope(
            format_version=FORMAT_VERSION,
            issuer_id=snapshot.issuer_id, key_id=self.issuer_key.key_id,
            registry_id=snapshot.registry_id, ledger_id=snapshot.ledger_id,
            policy_id=snapshot.policy_id, epoch=snapshot.epoch,
            generation=snapshot.generation, recovery_epoch=snapshot.recovery_epoch,
            previous_commitment=snapshot.previous_commitment,
            transition_id=snapshot.transition_id,
            approval_reference=snapshot.approval_reference,
            policy_commitment=untrusted_replay_policy_commitment(snapshot),
            approval_commitment=untrusted_approval_commitment(approval, snapshot),
            algorithm=ALGORITHM, purpose=ISSUER_PURPOSE, signature="",
        )
        record = replace(record, **changes)
        signature = self.private.sign(issuer_signing_bytes(record))
        return replace(record, signature=base64.urlsafe_b64encode(
            signature).decode("ascii").rstrip("="))

    def verify(self, *, snapshot=None, approval=None, signed=None,
               key_policy=None, issuer="issuer-alpha", now=NOW):
        return verify_replay_policy_issuer_signature(
            self.snapshot if snapshot is None else snapshot,
            self.approval if approval is None else approval,
            self.signed if signed is None else signed,
            self.key_policy if key_policy is None else key_policy,
            expected_issuer_id=issuer, now=now,
        )

    def reject(self, **kwargs):
        with self.assertRaises(ValueError):
            self.verify(**kwargs)

    def bad_header(self, **updates):
        self.reject(signed=replace(self.signed, **updates))

    def bad_approval(self, **updates):
        self.reject(approval=replace(self.approval, **updates))

    def bad_key(self, **updates):
        changed = replace(self.issuer_key, **updates)
        self.reject(key_policy=replace(self.key_policy, keys=(changed,)))

    def later(self):
        new_key = replace(self.snapshot.key_policy.keys[0],
                          status="disabled")
        replacement = replace(self.snapshot.key_policy.keys[0],
                              key_id="state-key-2", public_key_hex="c" * 64)
        keys = (new_key, replacement, self.snapshot.key_policy.keys[1])
        snapshot = replace(
            self.snapshot, epoch=2, generation=2,
            previous_commitment=untrusted_replay_policy_commitment(self.snapshot),
            transition_id="rotation-2", approval_reference="approval-2",
            key_policy=ReplayResponseKeyPolicy(POLICY_ID, 2, keys),
        )
        approval = self.make_approval(snapshot)
        return snapshot, approval, self.sign(snapshot, approval)

    def test_valid_issuer_signature_under_supplied_key(self):
        self.assertTrue(self.verify().issuer_signature_verified_under_supplied_key)

    def test_valid_approval_commitment(self):
        self.assertEqual(self.verify().approval_commitment,
                         untrusted_approval_commitment(self.approval, self.snapshot))

    def test_declared_approval_not_independent(self):
        self.assertFalse(self.verify().independent_policy_approval_verified)

    def test_caller_root_not_independent(self):
        self.assertFalse(self.verify().independent_root_provenance_verified)

    def test_no_operational_trust_flags(self):
        result = self.verify()
        for name in (
            "independent_issuer_authenticated", "independent_root_provenance_verified",
            "issuer_policy_currentness_verified", "independent_approver_identity_verified",
            "independent_policy_approval_verified", "protected_policy_currentness_verified",
            "independent_policy_witness_verified", "durable_policy_commit_verified",
            "trusted_time_verified", "replay_prevention_verified", "recovery_approved",
            "runtime_isolation_proven", "docker_execution_permitted",
            "automatic_retry_permitted", "production_execution_enabled",
        ):
            self.assertFalse(getattr(result, name), name)
        self.assertTrue(result.manual_verification_required)

    def test_immutable_assessment(self):
        with self.assertRaises(FrozenInstanceError):
            self.verify().issuer_id = "other"

    def test_canonical_signed_roundtrip(self):
        self.assertEqual(parse_signed_issuer_bytes(
            canonical_signed_issuer_bytes(self.signed)), self.signed)

    def test_correct_key_policy_structure(self):
        self.assertTrue(validate_issuer_key_policy(self.key_policy))

    def test_correct_approval_shape(self):
        self.assertTrue(validate_approval_declaration(self.approval, self.snapshot))

    def test_issuer_signing_domain_distinct(self):
        self.assertTrue(issuer_signing_bytes(self.signed).startswith(ISSUER_DOMAIN))
        self.assertNotEqual(ISSUER_DOMAIN, b"FBWEB-LAB-REPLAY-STATE-RESPONSE-SIGNATURE-V1\x00")

    def test_valid_rotation_signed_under_supplied_key(self):
        snapshot, approval, signed = self.later()
        self.assertEqual(self.verify(snapshot=snapshot, approval=approval,
                                     signed=signed).epoch, 2)

    def test_old_signature_cannot_verify_new_policy(self):
        snapshot, approval, _ = self.later()
        self.reject(snapshot=snapshot, approval=approval)

    def test_later_signature_does_not_prove_currentness(self):
        snapshot, approval, signed = self.later()
        self.assertFalse(self.verify(snapshot=snapshot, approval=approval,
                                     signed=signed).protected_policy_currentness_verified)

    def test_tampered_signature(self):
        self.bad_header(signature="A" * 86)

    def test_wrong_private_key_signature(self):
        alt = Ed25519PrivateKey.generate()
        forged = base64.urlsafe_b64encode(alt.sign(
            issuer_signing_bytes(self.signed))).decode("ascii").rstrip("=")
        self.bad_header(signature=forged)

    def test_registry_admin_purpose_substitution(self):
        self.bad_header(purpose="fbweb-lab-admin-authority-response-v1")

    def test_replay_state_purpose_substitution(self):
        self.bad_header(purpose=PURPOSES["REPLAY_STATE"])

    def test_replay_witness_purpose_substitution(self):
        self.bad_header(purpose=PURPOSES["REPLAY_WITNESS"])

    def test_wrong_algorithm(self):
        self.bad_header(algorithm="none")

    def test_wrong_key_id(self):
        self.bad_header(key_id="other-key")

    def test_wrong_issuer_id(self):
        self.bad_header(issuer_id="forged-issuer")

    def test_wrong_registry_id(self):
        self.bad_header(registry_id="other-registry")

    def test_wrong_ledger_id(self):
        self.bad_header(ledger_id="other-ledger")

    def test_wrong_policy_id(self):
        self.bad_header(policy_id="other-policy")

    def test_wrong_format_version(self):
        self.bad_header(format_version=2)

    def test_wrong_epoch(self):
        self.bad_header(epoch=2)

    def test_boolean_epoch(self):
        self.bad_header(epoch=True)

    def test_wrong_generation(self):
        self.bad_header(generation=2)

    def test_boolean_generation(self):
        self.bad_header(generation=True)

    def test_wrong_recovery_epoch(self):
        self.bad_header(recovery_epoch=2)

    def test_wrong_parent_digest(self):
        self.bad_header(previous_commitment="f" * 64)

    def test_wrong_transition_id(self):
        self.bad_header(transition_id="transition-other")

    def test_wrong_approval_reference(self):
        self.bad_header(approval_reference="approval-other")

    def test_wrong_policy_commitment(self):
        self.bad_header(policy_commitment="f" * 64)

    def test_wrong_approval_commitment(self):
        self.bad_header(approval_commitment="f" * 64)

    def test_invalid_signature_character(self):
        self.bad_header(signature="?")

    def test_invalid_signature_noncanonical(self):
        self.bad_header(signature="_" * 86)

    def test_wrong_expected_issuer(self):
        self.reject(issuer="forged-issuer")

    def test_declared_approval_wrong_policy(self):
        self.bad_approval(policy_id="wrong-policy")

    def test_declared_approval_wrong_issuer(self):
        self.bad_approval(issuer_id="other-issuer")

    def test_declared_approval_wrong_registry(self):
        self.bad_approval(registry_id="other-registry")

    def test_declared_approval_wrong_ledger(self):
        self.bad_approval(ledger_id="other-ledger")

    def test_declared_approval_wrong_epoch(self):
        self.bad_approval(epoch=2)

    def test_declared_approval_wrong_generation(self):
        self.bad_approval(generation=2)

    def test_declared_approval_wrong_recovery_epoch(self):
        self.bad_approval(recovery_epoch=2)

    def test_declared_approval_wrong_transition(self):
        self.bad_approval(transition_id="other-transition")

    def test_declared_approval_wrong_reference(self):
        self.bad_approval(approval_reference="other-ref")

    def test_declared_approval_wrong_previous_digest(self):
        self.bad_approval(previous_commitment="f" * 64)

    def test_declared_approval_wrong_proposed_digest(self):
        self.bad_approval(proposed_commitment="f" * 64)

    def test_declared_approval_wrong_decision(self):
        self.bad_approval(decision="APPROVED")

    def test_declared_approval_duplicate_approvers(self):
        self.bad_approval(approver_ids=("approver-a", "approver-a"))

    def test_declared_approval_unsorted_approvers(self):
        self.bad_approval(approver_ids=("approver-b", "approver-a"))

    def test_declared_approval_one_approver(self):
        self.bad_approval(approver_ids=("approver-a",))

    def test_declared_approval_issuer_self_approval(self):
        self.bad_approval(approver_ids=("approver-a", "issuer-alpha"))

    def test_declared_approval_replay_state_self_approval(self):
        self.bad_approval(approver_ids=("approver-a", "state-alpha"))

    def test_declared_approval_replay_witness_self_approval(self):
        self.bad_approval(approver_ids=("approver-a", "witness-beta"))

    def test_declared_approval_bad_approver_id(self):
        self.bad_approval(approver_ids=("approver-a", "not valid"))

    def test_policy_wrong_policy_id(self):
        self.reject(key_policy=replace(self.key_policy, policy_id="other"))

    def test_policy_wrong_type(self):
        self.reject(key_policy={})

    def test_policy_no_keys(self):
        self.reject(key_policy=replace(self.key_policy, keys=()))

    def test_policy_duplicate_key_id(self):
        self.reject(key_policy=replace(self.key_policy,
                                       keys=(self.issuer_key, self.issuer_key)))

    def test_policy_duplicate_key_material(self):
        second = replace(self.issuer_key, key_id="issuer-key-2")
        self.reject(key_policy=replace(self.key_policy,
                                       keys=(self.issuer_key, second)))

    def test_policy_wrong_key_purpose(self):
        self.bad_key(purpose=PURPOSES["REPLAY_STATE"])

    def test_policy_wrong_algorithm(self):
        self.bad_key(algorithm="RSA")

    def test_policy_revoked_key(self):
        self.bad_key(status="revoked")

    def test_policy_disabled_key(self):
        self.bad_key(status="disabled")

    def test_policy_invalid_public_key(self):
        self.bad_key(public_key_hex="!" * 64)

    def test_policy_zero_public_key(self):
        self.bad_key(public_key_hex="0" * 64)

    def test_policy_wrong_public_key(self):
        self.bad_key(public_key_hex="f" * 64)

    def test_policy_invalid_validity_window(self):
        self.bad_key(valid_from="2026-10-15T00:00:00Z")

    def test_supplied_time_before_window(self):
        self.reject(now=datetime(2026, 10, 12, tzinfo=timezone.utc))

    def test_supplied_time_at_expiry(self):
        self.reject(now=datetime(2026, 10, 15, tzinfo=timezone.utc))

    def test_naive_supplied_time(self):
        self.reject(now=datetime(2026, 10, 14))

    def test_time_not_trusted(self):
        self.assertFalse(self.verify().trusted_time_verified)

    def test_canonical_json_duplicate_key(self):
        raw = canonical_signed_issuer_bytes(self.signed)
        raw = raw.replace(b"{", b'{"epoch":1,', 1)
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(raw)

    def test_canonical_json_unknown_field(self):
        value = json.loads(canonical_signed_issuer_bytes(self.signed))
        value["extra"] = "invalid"
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(json.dumps(value, sort_keys=True,
                separators=(",", ":")).encode("ascii"))

    def test_canonical_json_missing_field(self):
        value = json.loads(canonical_signed_issuer_bytes(self.signed))
        del value["key_id"]
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(json.dumps(value, sort_keys=True,
                separators=(",", ":")).encode("ascii"))

    def test_canonical_json_whitespace(self):
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(json.dumps(
                json.loads(canonical_signed_issuer_bytes(self.signed)), indent=2
            ).encode("ascii"))

    def test_canonical_json_boolean_epoch(self):
        value = json.loads(canonical_signed_issuer_bytes(self.signed))
        value["epoch"] = True
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(json.dumps(value, sort_keys=True,
                separators=(",", ":")).encode("ascii"))

    def test_canonical_json_float_generation(self):
        value = json.loads(canonical_signed_issuer_bytes(self.signed))
        value["generation"] = 1.0
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(json.dumps(value, sort_keys=True,
                separators=(",", ":")).encode("ascii"))

    def test_canonical_json_invalid_bytes(self):
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(b"not-json")

    def test_canonical_json_exceeds_bound(self):
        with self.assertRaises(ValueError):
            parse_signed_issuer_bytes(b"x" * (MAX_SIGNED_BYTES + 1))

    def test_replay_key_material_overlap_denied(self):
        shared_key = replace(self.snapshot.key_policy.keys[0],
                             public_key_hex=self.issuer_key.public_key_hex)
        snapshot = replace(self.snapshot, key_policy=ReplayResponseKeyPolicy(
            POLICY_ID, 1, (shared_key, self.snapshot.key_policy.keys[1])))
        approval = self.make_approval(snapshot)
        signed = self.sign(snapshot, approval)
        self.reject(snapshot=snapshot, approval=approval, signed=signed)

    def test_signed_bootstrap_never_independent_bootstrap(self):
        self.assertFalse(self.verify().independent_issuer_authenticated)

    def test_replayed_valid_signature_not_proof_of_freshness(self):
        self.assertFalse(self.verify().protected_policy_currentness_verified)

    def test_issuer_policy_cannot_approve_own_replacement(self):
        self.assertFalse(self.verify().recovery_approved)

    def test_signed_old_policy_still_not_current(self):
        self.assertFalse(self.verify().issuer_policy_currentness_verified)


if __name__ == "__main__":
    unittest.main()
