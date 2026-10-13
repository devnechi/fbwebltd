#!/usr/bin/env python3
"""Gate 4D.22C.3D.8: restricted canonical JSON for lab evidence.

This is not general-purpose RFC 8785 canonicalization.

No signature verification, filesystem access, Docker, subprocess,
network interaction, replay consumption or authorization.
"""

import json
import re


DOMAIN_PREFIX = b"FBWEB-LAB-RUNTIME-EVIDENCE-SIGNATURE-V1\x00"

MAX_DOCUMENT_BYTES = 65536
MAX_DEPTH = 16
MAX_SAFE_INTEGER = (1 << 53) - 1

KEY_NAME = re.compile(
    r"[A-Za-z][A-Za-z0-9_]*\Z",
    re.ASCII,
)


def _validate(value, depth=0, ancestors=None):
    """Reject ambiguous and unsupported JSON values."""
    if depth > MAX_DEPTH:
        raise ValueError("Canonical JSON nesting limit exceeded")

    if value is True or value is False:
        return

    if type(value) is int:
        if not 0 <= value <= MAX_SAFE_INTEGER:
            raise ValueError("Unsafe canonical JSON integer")
        return

    if type(value) is str:
        if not all(
            0x20 <= ord(character) <= 0x7E
            for character in value
        ):
            raise ValueError(
                "Only printable ASCII strings are permitted"
            )
        return

    if type(value) is not dict:
        raise ValueError(
            "Unsupported canonical JSON value type"
        )

    if ancestors is None:
        ancestors = set()

    identity = id(value)

    if identity in ancestors:
        raise ValueError("Cyclic JSON object prohibited")

    ancestors.add(identity)

    try:
        for key, item in value.items():
            if (
                type(key) is not str
                or len(key) > 80
                or not KEY_NAME.fullmatch(key)
            ):
                raise ValueError(
                    "Unsupported canonical JSON object key"
                )

            _validate(
                item,
                depth + 1,
                ancestors,
            )
    finally:
        ancestors.remove(identity)


def canonical_json_bytes(value):
    """Encode one strictly restricted JSON object."""
    if type(value) is not dict:
        raise ValueError(
            "Top-level canonical JSON object required"
        )

    _validate(value)

    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")

    if len(encoded) > MAX_DOCUMENT_BYTES:
        raise ValueError(
            "Canonical JSON document too large"
        )

    return encoded


def _unique_pairs(pairs):
    """Reject duplicate object keys at every nesting level."""
    result = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(
                "Duplicate JSON object key"
            )

        result[key] = value

    return result


def _reject_number(value):
    raise ValueError(
        "Unsupported JSON numeric form"
    )


def parse_canonical_json(raw):
    """Parse exact canonical bytes, rejecting ambiguous encodings.

    This function must operate on original input bytes, before
    an ordinary JSON parser can discard duplicate-key evidence.
    """
    if (
        type(raw) is not bytes
        or not 0 < len(raw) <= MAX_DOCUMENT_BYTES
    ):
        raise ValueError(
            "Bounded raw JSON bytes required"
        )

    try:
        text = raw.decode(
            "utf-8",
            errors="strict",
        )

        value = json.loads(
            text,
            object_pairs_hook=_unique_pairs,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )

        expected = canonical_json_bytes(value)

    except (
        UnicodeError,
        json.JSONDecodeError,
        RecursionError,
    ) as exc:
        raise ValueError(
            "Invalid canonical JSON encoding"
        ) from exc

    if expected != raw:
        raise ValueError(
            "Noncanonical JSON bytes"
        )

    return value


def canonical_signing_bytes(unsigned_envelope):
    """Return domain-separated signed bytes, without signing."""
    if (
        type(unsigned_envelope) is not dict
        or "signature" in unsigned_envelope
    ):
        raise ValueError(
            "Unsigned envelope required"
        )

    return (
        DOMAIN_PREFIX
        + canonical_json_bytes(unsigned_envelope)
    )
