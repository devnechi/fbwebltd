#!/usr/bin/env python3
"""Gate 4D.22C.3D.10: Ed25519 laboratory evidence verification.

Verifies canonical evidence signatures using a public key selected
from a caller-supplied collector registry.

IMPORTANT:
- Registry authenticity is not established here.
- A valid signature does not prove collector trust or runtime isolation.
- Trusted time and expected bindings are caller responsibilities.
- Replay prevention is not implemented.
- No private keys, Docker access, subprocess, network or deployment.
"""

from dataclasses import dataclass
import base64
import binascii

from cryptography.exceptions import (
    InvalidSignature,
    UnsupportedAlgorithm,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey,
)

from lab_collector_trust_policy import assess_collector_policy
from lab_runtime_auth_envelope import signing_payload
from lab_runtime_canonical_payload import parse_canonical_json


@dataclass(frozen=True)
class SignatureVerificationAssessment:
    schema_valid: bool
    envelope_valid: bool
    collector_key_policy_eligible: bool
    signature_verified: bool
    expected_binding_matches: bool
    registry_revision: int
    reason: str

    registry_authenticity_verified: bool = False
    collector_authenticated: bool = False
    trusted_time_source_verified: bool = False
    freshness_verified: bool = False
    replay_prevention_verified: bool = False
    runtime_evidence_verified: bool = False
    vm_identity_proven: bool = False
    daemon_identity_proven: bool = False
    isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def _decode_signature(value):
    """Decode a canonical, format-validated Ed25519 signature."""
    if type(value) is not str:
        raise ValueError("Invalid signature value")

    try:
        signature = base64.b64decode(
            value + "==",
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, binascii.Error) as exc:
        raise ValueError(
            "Invalid Ed25519 signature encoding"
        ) from exc

    if len(signature) != 64:
        raise ValueError(
            "Invalid Ed25519 signature length"
        )

    return signature


def verify_lab_signature_bytes(
    raw,
    expected,
    registry,
    *,
    now,
):
    """Verify an Ed25519 signature over original canonical JSON.

    Verification is against the public key in the supplied registry.
    This function does NOT authenticate the registry itself.

    A successful result establishes signature validity under the
    supplied key only; it does not authorize Docker execution.
    """
    # Reject duplicate JSON keys, noncanonical bytes and
    # unsupported JSON representations before evaluating trust.
    envelope = parse_canonical_json(raw)

    # Enforce existing envelope, subject, timestamp and key policy.
    policy = assess_collector_policy(
        envelope,
        expected,
        registry,
        now=now,
    )

    if not policy.key_eligible_for_future_verification:
        raise ValueError(
            "Collector key is ineligible for verification"
        )

    # The registry validator already prohibits duplicate
    # collector/key pairs and malformed records.
    matching = tuple(
        record
        for record in registry.keys
        if (
            record.collector_id == expected.collector_id
            and record.key_id == expected.key_id
        )
    )

    if len(matching) != 1:
        raise ValueError(
            "Ambiguous collector verification key"
        )

    record = matching[0]

    signature = _decode_signature(
        envelope["signature"]
    )

    # Gate 3D.8 defines these exact domain-separated bytes.
    message = signing_payload(envelope)

    try:
        public_key = Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(record.public_key_hex)
        )

        public_key.verify(
            signature,
            message,
        )

    except (
        InvalidSignature,
        UnsupportedAlgorithm,
        ValueError,
        TypeError,
    ) as exc:
        raise ValueError(
            "Ed25519 evidence signature verification failed"
        ) from exc

    return SignatureVerificationAssessment(
        schema_valid=True,
        envelope_valid=True,
        collector_key_policy_eligible=True,
        signature_verified=True,
        expected_binding_matches=True,
        registry_revision=registry.revision,
        reason=(
            "Ed25519 signature verifies under the supplied public "
            "key. Registry provenance, collector authenticity, "
            "replay resistance and runtime isolation remain "
            "independently unverified."
        ),
    )
