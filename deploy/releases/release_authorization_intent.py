#!/usr/bin/env python3
"""Canonical, non-executing release intent. Not an approval authority."""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import re

try:
    from .rollback_planner import ImagePair
except ImportError:
    from rollback_planner import ImagePair


REPOSITORY = "devnechi/fbwebltd"
SOURCE_REF = "refs/heads/feature/docker-cicd-deployment"
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
CHANGE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{2,79}$")


def parse_utc(value):
    """Accept only canonical UTC timestamps, without fractional seconds."""
    if not isinstance(value, str):
        raise ValueError("UTC timestamp must be a string")

    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value
    ):
        raise ValueError("Timestamp must be ISO-8601 UTC ending in Z")

    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("Invalid UTC timestamp") from exc

    return parsed.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class ReleaseIntent:
    source_commit: str
    environment: str
    candidate: ImagePair
    rollback: ImagePair
    window_start: str
    window_end: str
    change_reference: str

    def validate(self):
        if not isinstance(self.source_commit, str):
            raise ValueError("Source commit must be a string")

        if not SHA_PATTERN.fullmatch(self.source_commit):
            raise ValueError("Invalid full source commit SHA")

        if self.environment != "production":
            raise ValueError("Unexpected target environment")

        if not isinstance(self.candidate, ImagePair):
            raise ValueError("Candidate image pair required")

        if not isinstance(self.rollback, ImagePair):
            raise ValueError("Rollback image pair required")

        self.candidate.validate()
        self.rollback.validate()

        if self.candidate == self.rollback:
            raise ValueError("Candidate and rollback images are identical")

        start = parse_utc(self.window_start)
        end = parse_utc(self.window_end)

        if end <= start:
            raise ValueError("Maintenance window must have positive duration")

        if (end - start).total_seconds() > 4 * 3600:
            raise ValueError("Maintenance window exceeds four hours")

        if not isinstance(self.change_reference, str):
            raise ValueError("Change reference must be a string")

        if not CHANGE_PATTERN.fullmatch(self.change_reference):
            raise ValueError("Invalid change-control reference")

        return True

    def document(self):
        self.validate()

        return {
            "schema_version": 1,
            "repository": REPOSITORY,
            "source_ref": SOURCE_REF,
            "source_commit": self.source_commit,
            "environment": self.environment,
            "candidate": {
                "app": self.candidate.app,
                "web": self.candidate.web,
            },
            "rollback": {
                "app": self.rollback.app,
                "web": self.rollback.web,
            },
            "window_start": self.window_start,
            "window_end": self.window_end,
            "change_reference": self.change_reference,
        }

    def canonical_bytes(self):
        return json.dumps(
            self.document(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")

    def fingerprint(self):
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def window_contains(self, now):
        """Check timing only. This does not verify authorization."""
        self.validate()

        if not isinstance(now, datetime):
            raise ValueError("Current time must be a datetime")

        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Current time must have timezone information")

        instant = now.astimezone(timezone.utc)

        return (
            parse_utc(self.window_start)
            <= instant
            < parse_utc(self.window_end)
        )
