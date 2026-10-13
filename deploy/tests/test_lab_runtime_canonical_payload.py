#!/usr/bin/env python3
"""Gate 4D.22C.3D.8 canonical payload security tests."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "releases"),
)

from lab_runtime_canonical_payload import (
    DOMAIN_PREFIX,
    MAX_DOCUMENT_BYTES,
    MAX_SAFE_INTEGER,
    canonical_json_bytes,
    canonical_signing_bytes,
    parse_canonical_json,
)

from lab_runtime_auth_envelope import (
    signing_payload,
    validate_envelope_bytes,
)

from test_lab_runtime_auth_envelope import (
    NOW,
    expected_binding,
    sample_envelope,
)


class CanonicalPayloadTests(unittest.TestCase):

    def assert_rejected(self, value):
        with self.assertRaises(ValueError):
            canonical_json_bytes(value)

    def assert_raw_rejected(self, value):
        with self.assertRaises(ValueError):
            parse_canonical_json(value)

    def test_exact_canonical_encoding(self):
        data = {
            "z": True,
            "a": {
                "x": 123,
                "nested": "yes",
            },
            "b": "a/b",
        }

        self.assertEqual(
            canonical_json_bytes(data),
            b'{"a":{"nested":"yes","x":123},'
            b'"b":"a/b","z":true}',
        )

    def test_dictionary_order_does_not_change_bytes(self):
        first = {"z": 1, "a": 2}
        second = {"a": 2, "z": 1}

        self.assertEqual(
            canonical_json_bytes(first),
            canonical_json_bytes(second),
        )

    def test_canonical_round_trip(self):
        data = sample_envelope()
        raw = canonical_json_bytes(data)

        self.assertEqual(
            parse_canonical_json(raw),
            data,
        )

    def test_signing_payload_has_domain_separation(self):
        payload = signing_payload(sample_envelope())

        self.assertTrue(
            payload.startswith(DOMAIN_PREFIX)
        )

    def test_signing_payload_excludes_signature(self):
        payload = signing_payload(sample_envelope())

        self.assertNotIn(
            b'"signature"',
            payload,
        )

    def test_subject_change_alters_signed_bytes(self):
        original = sample_envelope()
        modified = deepcopy(original)

        modified["evidence"]["subject"]["vm_id"] = (
            "another-vm"
        )

        self.assertNotEqual(
            signing_payload(original),
            signing_payload(modified),
        )

    def test_isolation_change_alters_signed_bytes(self):
        original = sample_envelope()
        modified = deepcopy(original)

        modified["evidence"]["isolation"]["controls"][
            "dedicated_vm"
        ] = False

        self.assertNotEqual(
            signing_payload(original),
            signing_payload(modified),
        )

    def test_raw_envelope_validation_is_non_authorizing(self):
        raw = canonical_json_bytes(
            sample_envelope()
        )

        result = validate_envelope_bytes(
            raw,
            expected_binding(),
            now=NOW,
        )

        self.assertTrue(result.structure_valid)
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

    def test_rejects_duplicate_top_level_key(self):
        self.assert_raw_rejected(
            b'{"a":1,"a":2}'
        )

    def test_rejects_nested_duplicate_key(self):
        self.assert_raw_rejected(
            b'{"a":{"x":1,"x":2}}'
        )

    def test_rejects_duplicate_after_escape_decoding(self):
        self.assert_raw_rejected(
            b'{"a":1,"\\u0061":2}'
        )

    def test_rejects_noncanonical_key_order(self):
        self.assert_raw_rejected(
            b'{"z":1,"a":2}'
        )

    def test_rejects_noncanonical_whitespace(self):
        self.assert_raw_rejected(
            b'{"a": 1}'
        )

    def test_rejects_escaped_ascii(self):
        self.assert_raw_rejected(
            b'{"a":"\\u0061"}'
        )

    def test_rejects_escaped_slash(self):
        self.assert_raw_rejected(
            b'{"a":"a\\/b"}'
        )

    def test_rejects_unicode_value(self):
        self.assert_rejected(
            {"a": "\u00e9"}
        )

    def test_rejects_unicode_escape(self):
        self.assert_raw_rejected(
            b'{"a":"\\u00e9"}'
        )

    def test_rejects_lone_surrogate(self):
        self.assert_raw_rejected(
            b'{"a":"\\ud800"}'
        )

    def test_rejects_control_character(self):
        self.assert_rejected(
            {"a": "line\nbreak"}
        )

    def test_rejects_fractional_number(self):
        self.assert_raw_rejected(
            b'{"a":1.5}'
        )

    def test_rejects_exponent_number(self):
        self.assert_raw_rejected(
            b'{"a":1e3}'
        )

    def test_rejects_nan(self):
        self.assert_raw_rejected(
            b'{"a":NaN}'
        )

    def test_rejects_negative_zero(self):
        self.assert_raw_rejected(
            b'{"a":-0}'
        )

    def test_rejects_negative_integer(self):
        self.assert_rejected(
            {"a": -1}
        )

    def test_rejects_unsafe_integer(self):
        self.assert_rejected(
            {"a": MAX_SAFE_INTEGER + 1}
        )

    def test_rejects_null(self):
        self.assert_raw_rejected(
            b'{"a":null}'
        )

    def test_rejects_arrays(self):
        self.assert_raw_rejected(
            b'{"a":[]}'
        )

    def test_rejects_non_string_keys(self):
        self.assert_rejected(
            {1: "value"}
        )

    def test_rejects_invalid_key_name(self):
        self.assert_rejected(
            {"unexpected-key": True}
        )

    def test_rejects_invalid_utf8(self):
        self.assert_raw_rejected(
            b'{"a":"\xff"}'
        )

    def test_rejects_utf8_bom(self):
        self.assert_raw_rejected(
            b'\xef\xbb\xbf{"a":1}'
        )

    def test_rejects_oversized_document(self):
        self.assert_raw_rejected(
            b'{"a":"'
            + b"x" * MAX_DOCUMENT_BYTES
            + b'"}'
        )

    def test_rejects_cyclic_object(self):
        data = {}
        data["self"] = data

        self.assert_rejected(data)

    def test_rejects_excessive_nesting(self):
        value = {"leaf": True}

        for _ in range(18):
            value = {"nested": value}

        self.assert_rejected(value)

    def test_rejects_non_bytes_raw_input(self):
        self.assert_raw_rejected(
            '{"a":1}'
        )

    def test_rejects_signed_object_at_unsigned_boundary(self):
        with self.assertRaises(ValueError):
            canonical_signing_bytes(
                sample_envelope()
            )

    def test_raw_entrypoint_rejects_duplicate_evidence(self):
        raw = canonical_json_bytes(
            sample_envelope()
        )

        raw = raw.replace(
            b'"vm_id":"vm-001"',
            b'"vm_id":"vm-001","vm_id":"vm-001"',
            1,
        )

        with self.assertRaises(ValueError):
            validate_envelope_bytes(
                raw,
                expected_binding(),
                now=NOW,
            )

    def test_raw_entrypoint_rejects_noncanonical_bytes(self):
        raw = canonical_json_bytes(
            sample_envelope()
        )

        with self.assertRaises(ValueError):
            validate_envelope_bytes(
                raw + b" ",
                expected_binding(),
                now=NOW,
            )

    def test_canonicalization_does_not_modify_input(self):
        data = sample_envelope()
        original = deepcopy(data)

        canonical_json_bytes(data)
        signing_payload(data)

        self.assertEqual(data, original)


if __name__ == "__main__":
    unittest.main()
