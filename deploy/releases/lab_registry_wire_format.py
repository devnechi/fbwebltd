#!/usr/bin/env python3
"""Gate 4D.22C.3D.11B: canonical offline registry wire format.

The registry JSON profile is separate from laboratory evidence JSON.
Only the 'keys' field permits an array. No filesystem, network or signing.
"""

import base64
import binascii
import json
import re

from lab_collector_trust_policy import (
    CollectorKeyRecord,
    CollectorTrustRegistry,
    MAX_KEYS,
    REGISTRY_ID,
    validate_registry,
)
from lab_runtime_auth_envelope import ALGORITHM
from lab_runtime_evidence_schema import parse_timestamp

REGISTRY_FORMAT_VERSION = 1
REGISTRY_PURPOSE = "fbweb-lab-collector-registry-admin"
REGISTRY_DOMAIN_PREFIX = b"FBWEB-LAB-COLLECTOR-REGISTRY-SIGNATURE-V1\x00"
MAX_REGISTRY_BYTES = 131072
MAX_SAFE_INTEGER = (1 << 53) - 1
HEX_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
BASE64_SIGNATURE = re.compile(r"[A-Za-z0-9_-]{86}\Z")

WIRE_FIELDS = frozenset({
    "registry_format_version", "registry_id", "revision",
    "previous_revision", "previous_digest", "issuer_key_id",
    "purpose", "algorithm", "issued_at", "expires_at",
    "keys", "signature",
})
KEY_FIELDS = frozenset(CollectorKeyRecord.__dataclass_fields__)


def _valid_signature_encoding(value):
    if type(value) is not str or not BASE64_SIGNATURE.fullmatch(value):
        raise ValueError("Invalid registry signature encoding")
    try:
        decoded = base64.b64decode(value + "==", altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid registry signature encoding") from exc
    if len(decoded) != 64 or base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=") != value:
        raise ValueError("Noncanonical registry signature")
    return decoded


def _unique_object_keys(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError("Duplicate registry JSON key")
        output[key] = value
    return output


def _invalid_numeric(_value):
    raise ValueError("Unsupported registry JSON number")


def _encoded(value):
    result = json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")
    if len(result) > MAX_REGISTRY_BYTES:
        raise ValueError("Registry document too large")
    return result


def validate_registry_wire(document):
    """Validate exact wire fields; return an untrusted policy declaration."""
    if type(document) is not dict or set(document) != WIRE_FIELDS:
        raise ValueError("Unexpected signed registry fields")
    if type(document["registry_format_version"]) is not int or document["registry_format_version"] != REGISTRY_FORMAT_VERSION:
        raise ValueError("Unsupported registry wire version")
    if document["registry_id"] != REGISTRY_ID:
        raise ValueError("Unexpected registry identity")
    if document["purpose"] != REGISTRY_PURPOSE or document["algorithm"] != ALGORITHM:
        raise ValueError("Wrong registry signature purpose or algorithm")
    issuer = document["issuer_key_id"]
    if type(issuer) is not str or not IDENTIFIER.fullmatch(issuer):
        raise ValueError("Invalid registry issuer identifier")
    revision = document["revision"]
    previous = document["previous_revision"]
    if (type(revision) is not int or type(previous) is not int
            or not 1 <= revision <= MAX_SAFE_INTEGER
            or previous != revision - 1):
        raise ValueError("Invalid registry revision relationship")
    digest = document["previous_digest"]
    if type(digest) is not str or not HEX_DIGEST.fullmatch(digest):
        raise ValueError("Invalid previous registry digest")
    if (revision == 1 and digest != "0" * 64) or (revision > 1 and digest == "0" * 64):
        raise ValueError("Invalid registry genesis/previous digest")
    issued = parse_timestamp(document["issued_at"])
    expires = parse_timestamp(document["expires_at"])
    if not issued < expires:
        raise ValueError("Invalid registry issue/expiry window")
    keys = document["keys"]
    if type(keys) is not list or not 1 <= len(keys) <= MAX_KEYS:
        raise ValueError("Invalid registry key array")
    records = []
    previous_identity = None
    for item in keys:
        if type(item) is not dict or set(item) != KEY_FIELDS:
            raise ValueError("Invalid registry collector record fields")
        record = CollectorKeyRecord(**item)
        identity = (record.collector_id, record.key_id)
        if previous_identity is not None and identity <= previous_identity:
            raise ValueError("Registry keys must be strictly sorted")
        previous_identity = identity
        records.append(record)
    registry = CollectorTrustRegistry(
        registry_id=document["registry_id"],
        revision=revision,
        keys=tuple(records),
    )
    validate_registry(registry)
    _valid_signature_encoding(document["signature"])
    return registry


def canonical_registry_bytes(document):
    """Canonicalize a strictly validated complete registry document."""
    validate_registry_wire(document)
    return _encoded(document)


def registry_signing_bytes(document):
    """Exact admin-domain signed bytes; excludes registry signature."""
    canonical_registry_bytes(document)
    unsigned = {key: value for key, value in document.items() if key != "signature"}
    return REGISTRY_DOMAIN_PREFIX + _encoded(unsigned)


def parse_signed_registry_bytes(raw):
    """Parse original bytes without losing duplicate-key evidence."""
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_REGISTRY_BYTES:
        raise ValueError("Bounded registry bytes required")
    try:
        document = json.loads(
            raw.decode("utf-8", errors="strict"),
            object_pairs_hook=_unique_object_keys,
            parse_float=_invalid_numeric,
            parse_constant=_invalid_numeric,
        )
        canonical = canonical_registry_bytes(document)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("Invalid registry JSON bytes") from exc
    if raw != canonical:
        raise ValueError("Noncanonical registry JSON bytes")
    return document
