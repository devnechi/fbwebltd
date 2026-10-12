#!/usr/bin/env python3
"""Gate 4D.22C.3C.2: read-only Linux Docker socket assessment.

Linux socket and process evidence supports investigation only.
It cannot prove daemon isolation or authorize Docker execution.

No socket connection, Docker API request, mutation or subprocess.
"""

from dataclasses import dataclass
from pathlib import Path
import os
import re
import stat


SOCKET_LINK = re.compile(r"^socket:\[([0-9]+)\]$")
PID_NAME = re.compile(r"^[1-9][0-9]*$")
INODE_NAME = re.compile(r"^[1-9][0-9]*$")


@dataclass(frozen=True)
class SocketHolder:
    pid: int
    fd: int


@dataclass(frozen=True)
class DaemonIdentityAssessment:
    socket_path: str
    socket_inode: int
    holders: tuple
    socket_record_count: int
    evidence_consistent: bool
    daemon_identity_proven: bool = False
    daemon_isolation_proven: bool = False
    docker_execution_permitted: bool = False
    automatic_retry_permitted: bool = False
    manual_verification_required: bool = True


def parse_unix_table(content, socket_path):
    """Find a socket path in /proc/net/unix.

    Return its inode records. Duplicate records remain visible,
    rather than silently selecting one.
    """
    if not isinstance(content, str):
        raise ValueError("Invalid Unix socket table")

    matches = []
    lines = content.splitlines()

    if not lines or not lines[0].startswith("Num "):
        raise ValueError("Invalid Unix socket table header")

    for line in lines[1:]:
        fields = line.split(None, 7)

        if len(fields) < 7:
            raise ValueError("Malformed Unix socket table entry")

        if len(fields) != 8 or fields[7] != socket_path:
            continue

        inode_text = fields[6]

        if not INODE_NAME.fullmatch(inode_text):
            raise ValueError("Invalid socket inode")

        matches.append(int(inode_text))

    return tuple(matches)


def find_socket_holders(proc_root, inode):
    """List readable /proc/PID/fd links to a socket inode.

    Unreadable entries and concurrent process changes are not
    evidence that no other holders exist.
    """
    if type(inode) is not int or inode <= 0:
        raise ValueError("Invalid socket inode")

    proc_root = Path(proc_root)
    holders = []
    incomplete = False

    try:
        entries = list(proc_root.iterdir())
    except OSError as exc:
        raise ValueError("Cannot enumerate procfs") from exc

    for entry in entries:
        if not PID_NAME.fullmatch(entry.name):
            continue

        fd_dir = entry / "fd"

        try:
            descriptors = list(fd_dir.iterdir())
        except (PermissionError, OSError):
            incomplete = True
            continue

        for descriptor in descriptors:
            try:
                target = os.readlink(descriptor)
            except (PermissionError, OSError):
                incomplete = True
                continue

            matched = SOCKET_LINK.fullmatch(target)

            if matched and int(matched.group(1)) == inode:
                try:
                    holders.append(
                        SocketHolder(
                            pid=int(entry.name),
                            fd=int(descriptor.name),
                        )
                    )
                except ValueError:
                    incomplete = True

    return (
        tuple(sorted(set(holders), key=lambda h: (h.pid, h.fd))),
        incomplete,
    )


def assess_lab_daemon_identity(
    socket_path,
    *,
    proc_root="/proc",
    unix_table_content=None,
):
    """Assess kernel-visible socket evidence without authorization."""
    socket_path = Path(socket_path)

    if (
        not socket_path.is_absolute()
        or socket_path.is_symlink()
        or socket_path.name != "docker-lab.sock"
    ):
        raise ValueError("Unexpected laboratory socket path")

    info = socket_path.lstat()

    if (
        not stat.S_ISSOCK(info.st_mode)
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o600
    ):
        raise ValueError("Private owned laboratory socket required")

    if unix_table_content is None:
        unix_table_content = (
            Path(proc_root) / "net" / "unix"
        ).read_text(encoding="utf-8")

    records = parse_unix_table(
        unix_table_content, str(socket_path)
    )

    # Ambiguous or missing kernel records fail closed.
    if len(records) != 1:
        return DaemonIdentityAssessment(
            socket_path=str(socket_path),
            socket_inode=0,
            holders=(),
            socket_record_count=len(records),
            evidence_consistent=False,
        )

    inode = records[0]
    holders, incomplete = find_socket_holders(
        proc_root, inode
    )

    return DaemonIdentityAssessment(
        socket_path=str(socket_path),
        socket_inode=inode,
        holders=holders,
        socket_record_count=1,
        evidence_consistent=bool(holders) and not incomplete,
    )
