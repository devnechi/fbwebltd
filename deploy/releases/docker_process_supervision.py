#!/usr/bin/env python3
"""Read-only Linux process supervision for recovery investigations.

A process observation is not deployment authorization, a termination
request, or proof that Docker daemon-side operations have settled.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import os
import re


PID_LIMIT = 4194304
TICKS_PATTERN = re.compile(r"^[0-9]+$")


class ProcessStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXITED = "EXITED"
    MISSING = "MISSING"
    PID_REUSED = "PID_REUSED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ProcessIdentity:
    pid: int
    start_ticks: int

    def validate(self):
        if type(self.pid) is not int or not 1 <= self.pid <= PID_LIMIT:
            raise ValueError("Invalid process PID")

        if type(self.start_ticks) is not int or self.start_ticks <= 0:
            raise ValueError("Invalid process start time")

        return True


@dataclass(frozen=True)
class ProcessAssessment:
    status: ProcessStatus
    original_process_active: bool
    docker_operation_settled: bool
    automatic_retry_permitted: bool
    manual_reconciliation_required: bool
    reason: str


def parse_proc_stat(content):
    """Parse Linux /proc/PID/stat, including spaced command names."""
    if not isinstance(content, str):
        raise ValueError("Invalid process stat content")

    left = content.find("(")
    right = content.rfind(")")

    if left < 1 or right <= left:
        raise ValueError("Malformed Linux process stat")

    pid_text = content[:left].strip()

    if not pid_text.isdecimal():
        raise ValueError("Invalid PID in process stat")

    pid = int(pid_text)

    # After the closing parenthesis the first field is field 3,
    # followed by fields 4 through 52.
    fields = content[right + 1:].split()

    if len(fields) < 20:
        raise ValueError("Incomplete Linux process stat")

    state = fields[0]
    ticks_text = fields[19]  # Original /proc field 22.

    if (
        len(state) != 1
        or state not in "RSDTtZXIKPW"
        or not TICKS_PATTERN.fullmatch(ticks_text)
    ):
        raise ValueError("Invalid Linux process state or start time")

    identity = ProcessIdentity(pid, int(ticks_text))
    identity.validate()

    return identity, state


def assess_process(identity, stat_content=None, *, unreadable=False):
    """Classify evidence without treating process exit as Docker quiescence."""
    if not isinstance(identity, ProcessIdentity):
        raise ValueError("ProcessIdentity required")

    identity.validate()

    if unreadable:
        status = ProcessStatus.UNKNOWN
        reason = "Process identity could not be inspected"
    elif stat_content is None:
        status = ProcessStatus.MISSING
        reason = "Original PID is absent; Docker state remains uncertain"
    else:
        try:
            observed, state = parse_proc_stat(stat_content)
        except ValueError:
            status = ProcessStatus.UNKNOWN
            reason = "Process record could not be validated"
        else:
            if observed.pid != identity.pid:
                status = ProcessStatus.UNKNOWN
                reason = "Observed process PID does not match request"
            elif observed.start_ticks != identity.start_ticks:
                status = ProcessStatus.PID_REUSED
                reason = "PID was reused; original process not observed"
            elif state in ("Z", "X"):
                status = ProcessStatus.EXITED
                reason = "Original process exited; Docker may remain active"
            else:
                status = ProcessStatus.ACTIVE
                reason = "Original process is still active"

    return ProcessAssessment(
        status=status,
        original_process_active=(status == ProcessStatus.ACTIVE),
        docker_operation_settled=False,
        automatic_retry_permitted=False,
        manual_reconciliation_required=True,
        reason=reason,
    )


def observe_linux_process(identity, *, proc_root=Path("/proc")):
    """Inspect a process read-only; fail closed on access or format errors."""
    if not isinstance(identity, ProcessIdentity):
        raise ValueError("ProcessIdentity required")

    identity.validate()

    root = Path(proc_root)

    try:
        stat_content = (root / str(identity.pid) / "stat").read_text(
            encoding="utf-8"
        )
    except FileNotFoundError:
        return assess_process(identity)
    except (OSError, UnicodeError):
        return assess_process(identity, unreadable=True)

    return assess_process(identity, stat_content)


def capture_linux_identity(pid, *, proc_root=Path("/proc")):
    """Capture kernel PID/start ticks; never invent missing evidence."""
    if type(pid) is not int or not 1 <= pid <= PID_LIMIT:
        raise ValueError("Invalid PID")

    try:
        content = (
            Path(proc_root) / str(pid) / "stat"
        ).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError("Cannot capture process identity") from exc

    identity, state = parse_proc_stat(content)

    if identity.pid != pid or state in ("Z", "X"):
        raise ValueError("Process is absent, exited or mismatched")

    return identity
