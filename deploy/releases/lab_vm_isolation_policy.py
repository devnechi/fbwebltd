#!/usr/bin/env python3
"""Gate 4D.22C.3D.2: isolated Docker laboratory VM policy.

Validates an untrusted declaration of intended VM isolation.
Does not provision VMs, execute Docker, read secrets or authorize
any deployment.

A valid declaration is NOT independently verified runtime evidence.
"""

from dataclasses import dataclass
from ipaddress import ip_address, ip_network
from pathlib import PurePosixPath


REQUIRED_CONTROLS = frozenset({
    "dedicated_vm",
    "no_production_credentials",
    "no_host_docker_socket",
    "no_host_filesystem_passthrough",
    "dedicated_docker_data_root",
    "dedicated_lab_socket",
    "no_production_network_route",
    "no_shared_container_runtime",
    "snapshot_before_experiments",
    "disposable_vm",
    "independent_runtime_verification",
})

FORBIDDEN_DATA_ROOTS = frozenset({
    "/", "/var", "/var/lib", "/var/lib/docker",
    "/run", "/home", "/root",
})

ALLOWED_DOCKER_DATA_ROOT = "/var/lib/fbweb-lab-docker"
ALLOWED_DOCKER_SOCKET = "/run/fbweb-lab/docker-lab.sock"
ALLOWED_DAEMON_NAME = "fbweb-dedicated-lab"


@dataclass(frozen=True)
class LabVMBaseline:
    vm_name: str
    environment: str
    network_mode: str
    guest_address: str
    docker_data_root: str
    docker_socket: str
    host_socket_shared: bool
    host_paths_shared: bool
    production_credentials_present: bool
    production_network_reachable: bool
    snapshot_policy: str
    controls: tuple


@dataclass(frozen=True)
class LabVMAssessment:
    declaration_valid: bool
    missing_controls: tuple
    reason: str
    runtime_evidence_verified: bool = False
    isolation_proven: bool = False
    docker_execution_permitted: bool = False
    production_execution_enabled: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def validate_absolute_path(value):
    if not isinstance(value, str) or not value.startswith("/"):
        raise ValueError("Absolute Unix path required")

    path = PurePosixPath(value)

    if (
        ".." in value.split("/")
        or "//" in value
        or str(path) != value
    ):
        raise ValueError("Noncanonical path prohibited")

    return value


def assess_vm_baseline(value):
    """Validate a proposed, not independently verified, VM baseline."""
    if not isinstance(value, LabVMBaseline):
        raise ValueError("LabVMBaseline required")

    if value.vm_name != ALLOWED_DAEMON_NAME:
        raise ValueError("Unexpected laboratory VM identity")

    if value.environment != "isolated-laboratory":
        raise ValueError("Non-laboratory environment prohibited")

    # Offline guest networking is mandatory for the initial
    # destructive Docker execution experiments.
    if value.network_mode != "internal-only":
        raise ValueError("Guest network must be internal-only")

    try:
        guest_ip = ip_address(value.guest_address)
    except ValueError as exc:
        raise ValueError("Invalid guest network address") from exc

    allowed_network = ip_network("192.0.2.0/24")

    # Documentation-only TEST-NET-1 addresses avoid silently
    # choosing a real production or public network.
    if guest_ip not in allowed_network:
        raise ValueError("Guest address must use the test network")

    validate_absolute_path(value.docker_data_root)
    validate_absolute_path(value.docker_socket)

    if value.docker_data_root in FORBIDDEN_DATA_ROOTS:
        raise ValueError("Host Docker data root prohibited")

    if value.docker_data_root != ALLOWED_DOCKER_DATA_ROOT:
        raise ValueError("Unexpected laboratory Docker data root")

    if value.docker_socket != ALLOWED_DOCKER_SOCKET:
        raise ValueError("Unexpected laboratory Docker socket")

    for field in (
        "host_socket_shared",
        "host_paths_shared",
        "production_credentials_present",
        "production_network_reachable",
    ):
        setting = getattr(value, field)

        if type(setting) is not bool:
            raise ValueError("Explicit boolean isolation value required")

        if setting:
            raise ValueError("Unsafe shared production or host resource")

    if value.snapshot_policy != "snapshot-before-each-experiment":
        raise ValueError("Snapshot and rollback policy required")

    if (
        type(value.controls) is not tuple
        or any(type(item) is not str for item in value.controls)
        or len(value.controls) != len(set(value.controls))
    ):
        raise ValueError("Invalid control declarations")

    supplied = frozenset(value.controls)

    if supplied - REQUIRED_CONTROLS:
        raise ValueError("Unknown isolation control")

    missing = tuple(sorted(REQUIRED_CONTROLS - supplied))

    return LabVMAssessment(
        declaration_valid=not missing,
        missing_controls=missing,
        reason=(
            "Baseline declarations accepted; VM runtime isolation "
            "has not been independently verified"
            if not missing
            else "Mandatory VM isolation declarations are missing"
        ),
    )
