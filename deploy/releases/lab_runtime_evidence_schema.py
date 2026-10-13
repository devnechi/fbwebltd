#!/usr/bin/env python3
"""Gate 4D.22C.3D.4: pure laboratory evidence schema validation.

Validates untrusted, versioned evidence declarations.

No filesystem access, subprocess, Docker API, network connection,
runtime attestation, execution authorization or deployment.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import re


SCHEMA_VERSION = 1
LAB_NAME = "fbweb-dedicated-lab"
LAB_SOCKET = "/run/fbweb-lab/docker-lab.sock"
LAB_DATA_ROOT = "/var/lib/fbweb-lab-docker"

IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
UTC_FORMAT = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)

REQUIRED_CONTROLS = frozenset({
    "dedicated_vm",
    "dedicated_daemon",
    "private_unix_socket",
    "separate_data_root",
    "no_host_docker_socket",
    "no_host_filesystem_passthrough",
    "no_production_credentials",
    "no_production_network_route",
    "no_shared_container_runtime",
    "independent_lifecycle",
})


@dataclass(frozen=True)
class RuntimeEvidenceAssessment:
    schema_valid: bool
    declaration_consistent: bool
    reason: str
    runtime_evidence_verified: bool = False
    vm_identity_proven: bool = False
    daemon_identity_proven: bool = False
    daemon_isolation_proven: bool = False
    isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def require_fields(value, expected, label):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError("Invalid " + label + " fields")


def require_identifier(value, label):
    if type(value) is not str or not IDENTIFIER.fullmatch(value):
        raise ValueError("Invalid " + label)


def require_hash(value, label):
    if type(value) is not str or not HEX64.fullmatch(value):
        raise ValueError("Invalid " + label)


def parse_timestamp(value):
    if type(value) is not str or not UTC_FORMAT.fullmatch(value):
        raise ValueError("Canonical UTC timestamp required")

    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("Invalid UTC timestamp") from exc

    return parsed.replace(tzinfo=timezone.utc)


def validate_evidence(value):
    """Validate structure and internal consistency only.

    Valid evidence is still untrusted. The supplied provenance,
    configuration and isolation claims are not independently proven.
    """
    require_fields(
        value,
        {
            "schema_version",
            "evidence_id",
            "subject",
            "provenance",
            "vm",
            "daemon",
            "isolation",
        },
        "runtime evidence",
    )

    if type(value["schema_version"]) is not int:
        raise ValueError("Invalid schema version type")

    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported schema version")

    require_identifier(value["evidence_id"], "evidence identity")

    subject = value["subject"]
    require_fields(
        subject,
        {"vm_id", "daemon_id"},
        "subject",
    )

    require_identifier(subject["vm_id"], "subject VM identity")
    require_identifier(subject["daemon_id"], "subject daemon identity")

    provenance = value["provenance"]
    require_fields(
        provenance,
        {
            "collector_id",
            "collection_id",
            "collected_at",
            "source_type",
            "source_digest",
        },
        "provenance",
    )

    require_identifier(provenance["collector_id"], "collector")
    require_identifier(provenance["collection_id"], "collection")
    require_hash(provenance["source_digest"], "source digest")

    parse_timestamp(provenance["collected_at"])

    if provenance["source_type"] not in (
        "declared",
        "offline-record",
    ):
        raise ValueError("Unsupported evidence source type")

    vm = value["vm"]
    require_fields(
        vm,
        {
            "vm_id",
            "vm_name",
            "configuration_digest",
            "lifecycle",
        },
        "VM",
    )

    require_identifier(vm["vm_id"], "VM identity")
    require_hash(vm["configuration_digest"], "VM configuration digest")

    if vm["vm_id"] != subject["vm_id"]:
        raise ValueError("VM subject mismatch")

    if vm["vm_name"] != LAB_NAME:
        raise ValueError("Unexpected laboratory VM")

    if vm["lifecycle"] != "declared-isolated":
        raise ValueError("Unacceptable VM lifecycle declaration")

    daemon = value["daemon"]
    require_fields(
        daemon,
        {
            "vm_id",
            "daemon_id",
            "daemon_name",
            "pid",
            "start_ticks",
            "socket_path",
            "data_root",
        },
        "daemon",
    )

    require_identifier(daemon["vm_id"], "daemon VM identity")
    require_identifier(daemon["daemon_id"], "daemon identity")

    if (
        daemon["vm_id"] != subject["vm_id"]
        or daemon["daemon_id"] != subject["daemon_id"]
    ):
        raise ValueError("Daemon subject mismatch")

    if daemon["daemon_name"] != LAB_NAME:
        raise ValueError("Unexpected daemon name")

    if (
        type(daemon["pid"]) is not int
        or daemon["pid"] <= 0
        or type(daemon["start_ticks"]) is not int
        or daemon["start_ticks"] <= 0
    ):
        raise ValueError("Invalid declared daemon process identity")

    if daemon["socket_path"] != LAB_SOCKET:
        raise ValueError("Unexpected laboratory socket")

    if daemon["data_root"] != LAB_DATA_ROOT:
        raise ValueError("Unexpected laboratory data root")

    isolation = value["isolation"]
    require_fields(
        isolation,
        {"vm_id", "daemon_id", "controls"},
        "isolation",
    )

    if (
        isolation["vm_id"] != subject["vm_id"]
        or isolation["daemon_id"] != subject["daemon_id"]
    ):
        raise ValueError("Isolation subject mismatch")

    controls = isolation["controls"]

    if type(controls) is not dict or set(controls) != REQUIRED_CONTROLS:
        raise ValueError("Missing or unexpected isolation controls")

    for name, setting in controls.items():
        if type(setting) is not bool or setting is not True:
            raise ValueError("Unsafe or invalid control: " + name)

    return RuntimeEvidenceAssessment(
        schema_valid=True,
        declaration_consistent=True,
        reason=(
            "Evidence structure and declarations are consistent; "
            "provenance, freshness and runtime isolation remain "
            "independently unverified"
        ),
    )
