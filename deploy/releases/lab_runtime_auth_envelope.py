#!/usr/bin/env python3
"""Gate 4D.22C.3D.6: pure laboratory authentication-envelope contract.

Untrusted envelope validation only. Signature bytes are format-checked,
not cryptographically verified. No filesystem, Docker, subprocess,
network, signing keys, replay store or execution authorization.
"""

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import base64
import binascii
import hashlib
import json
import re

from lab_runtime_evidence_schema import (
    parse_timestamp,
    validate_evidence,
)


ENVELOPE_VERSION = 1
PURPOSE = "fbweb-lab-runtime-evidence"
ALGORITHM = "Ed25519"
MAX_VALIDITY_SECONDS = 300
MAX_COLLECTION_LAG_SECONDS = 60

IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")
CHALLENGE = re.compile(r"^[0-9a-f]{64}$")
SIGNATURE = re.compile(r"^[A-Za-z0-9_-]{86}$")

ENVELOPE_FIELDS = frozenset({
    "envelope_version",
    "purpose",
    "algorithm",
    "collector_id",
    "key_id",
    "challenge",
    "issued_at",
    "expires_at",
    "evidence",
    "signature",
})


@dataclass(frozen=True)
class ExpectedBinding:
    collector_id: str
    key_id: str
    vm_id: str
    daemon_id: str
    challenge: str
    collection_id: str


@dataclass(frozen=True)
class EnvelopeAssessment:
    structure_valid: bool
    expected_binding_matches: bool
    timestamp_window_valid: bool
    signature_verified: bool = False
    collector_authenticated: bool = False
    freshness_verified: bool = False
    replay_prevention_verified: bool = False
    runtime_evidence_verified: bool = False
    isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def canonical_bytes(value):
    """Deterministic representation; not proof of authenticity."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def signing_payload(envelope):
    """Construct the proposed signed payload, excluding signature.

    The encoding is a provisional contract. It must be separately
    reviewed before integration with a real signing implementation.
    """
    if type(envelope) is not dict:
        raise ValueError("Envelope object required")

    if set(envelope) != ENVELOPE_FIELDS:
        raise ValueError("Invalid envelope fields")

    return canonical_bytes({
        key: value
        for key, value in envelope.items()
        if key != "signature"
    })


def _identifier(value, label):
    if type(value) is not str or not IDENTIFIER.fullmatch(value):
        raise ValueError("Invalid " + label)


def _challenge(value):
    if type(value) is not str or not CHALLENGE.fullmatch(value):
        raise ValueError("Invalid challenge")


def _signature_format(value):
    if type(value) is not str or not SIGNATURE.fullmatch(value):
        raise ValueError("Invalid signature encoding")

    try:
        raw = base64.b64decode(
            value + "==",
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid signature encoding") from exc

    if len(raw) != 64:
        raise ValueError("Invalid Ed25519 signature length")

    canonical = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    if canonical != value:
        raise ValueError("Noncanonical signature encoding")


def validate_envelope(envelope, expected, *, now):
    """Validate structure and verifier-supplied identity bindings.

    No signature verification, replay consumption or authorization.
    The caller must independently obtain expected and trusted time.
    """
    if type(envelope) is not dict or set(envelope) != ENVELOPE_FIELDS:
        raise ValueError("Invalid authentication envelope")

    if not isinstance(expected, ExpectedBinding):
        raise ValueError("ExpectedBinding required")

    for label in (
        "collector_id", "key_id", "vm_id",
        "daemon_id", "collection_id",
    ):
        _identifier(getattr(expected, label), "expected " + label)

    _challenge(expected.challenge)

    if (
        type(envelope["envelope_version"]) is not int
        or envelope["envelope_version"] != ENVELOPE_VERSION
    ):
        raise ValueError("Unsupported envelope version")

    if envelope["purpose"] != PURPOSE:
        raise ValueError("Invalid verification purpose")

    if envelope["algorithm"] != ALGORITHM:
        raise ValueError("Unsupported signature algorithm")

    _identifier(envelope["collector_id"], "collector")
    _identifier(envelope["key_id"], "key")
    _challenge(envelope["challenge"])
    _signature_format(envelope["signature"])

    if (
        envelope["collector_id"] != expected.collector_id
        or envelope["key_id"] != expected.key_id
        or envelope["challenge"] != expected.challenge
    ):
        raise ValueError("Untrusted collector, key or challenge binding")

    evidence = envelope["evidence"]
    validate_evidence(evidence)

    if (
        evidence["subject"]["vm_id"] != expected.vm_id
        or evidence["subject"]["daemon_id"] != expected.daemon_id
        or evidence["provenance"]["collector_id"]
            != expected.collector_id
        or evidence["provenance"]["collection_id"]
            != expected.collection_id
    ):
        raise ValueError("Evidence subject or collection mismatch")

    if (
        not isinstance(now, datetime)
        or now.tzinfo is None
        or now.utcoffset() is None
    ):
        raise ValueError("Trusted timezone-aware time required")

    instant = now.astimezone(timezone.utc)
    issued = parse_timestamp(envelope["issued_at"])
    expires = parse_timestamp(envelope["expires_at"])
    collected = parse_timestamp(
        evidence["provenance"]["collected_at"]
    )

    if not issued < expires:
        raise ValueError("Invalid authentication validity window")

    if expires - issued > timedelta(seconds=MAX_VALIDITY_SECONDS):
        raise ValueError("Authentication validity window too long")

    if not collected <= issued:
        raise ValueError("Evidence collection occurs after issuance")

    if issued - collected > timedelta(
        seconds=MAX_COLLECTION_LAG_SECONDS
    ):
        raise ValueError("Evidence collection too old at issuance")

    if not issued <= instant < expires:
        raise ValueError("Envelope outside assessment validity window")

    if instant - collected > timedelta(
        seconds=MAX_VALIDITY_SECONDS
    ):
        raise ValueError("Evidence exceeds maximum age")

    # Ensure the proposed signing representation is serializable.
    signing_payload(envelope)

    return EnvelopeAssessment(
        structure_valid=True,
        expected_binding_matches=True,
        timestamp_window_valid=True,
    )
