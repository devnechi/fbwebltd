#!/usr/bin/env python3
"""Gate 4D.21A: release intent canonicalization and rejection tests."""

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1] / "releases"
sys.path.insert(0, str(ROOT))

from release_authorization_intent import ReleaseIntent
from rollback_planner import ImagePair


def fixture():
    return ReleaseIntent(
        source_commit="740befa2d06bb3728c2ef98f58eca4c989293a26",
        environment="production",
        candidate=ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:"
            "4d23170ebfb0bdb92bbeec96a30458ca921d4559f371ec14853ce0e15117d497",
            "ghcr.io/devnechi/fbwebltd-web@sha256:"
            "45a58f99e97b0554eeddb5fcbdd1f6a074d5f4798d6dee94334e80edb686a1bd",
        ),
        rollback=ImagePair(
            "ghcr.io/devnechi/fbwebltd-app@sha256:"
            "5174e318474c8658c81b5fc3723df3549305086e389347b2666c19e33cee1f5a",
            "ghcr.io/devnechi/fbwebltd-web@sha256:"
            "964eef5c4a5e718bb919a24240580180115a49ce5392406e41afbe5f7e672cf4",
        ),
        window_start="2026-11-02T20:00:00Z",
        window_end="2026-11-02T21:00:00Z",
        change_reference="CHG-2026-021",
    )


class ReleaseAuthorizationIntentTests(unittest.TestCase):
    def test_canonical_fingerprint_is_stable(self):
        request = fixture()
        self.assertTrue(request.validate())
        self.assertEqual(request.fingerprint(), request.fingerprint())
        self.assertEqual(len(request.fingerprint()), 64)

    def test_changed_source_commit_changes_fingerprint(self):
        original = fixture()
        changed = replace(original, source_commit="a" * 40)
        self.assertNotEqual(original.fingerprint(), changed.fingerprint())

    def test_changed_candidate_digest_changes_fingerprint(self):
        original = fixture()
        changed = replace(
            original,
            candidate=ImagePair(
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "a" * 64,
                original.candidate.web,
            ),
        )
        self.assertNotEqual(original.fingerprint(), changed.fingerprint())

    def test_changed_rollback_digest_changes_fingerprint(self):
        original = fixture()
        changed = replace(
            original,
            rollback=ImagePair(
                "ghcr.io/devnechi/fbwebltd-app@sha256:" + "b" * 64,
                original.rollback.web,
            ),
        )
        self.assertNotEqual(original.fingerprint(), changed.fingerprint())

    def test_changed_window_changes_fingerprint(self):
        original = fixture()
        changed = replace(original, window_end="2026-11-02T21:30:00Z")
        self.assertNotEqual(original.fingerprint(), changed.fingerprint())

    def test_changed_environment_rejected(self):
        with self.assertRaises(ValueError):
            replace(fixture(), environment="development").validate()

    def test_mutable_image_tag_rejected(self):
        original = fixture()
        changed = replace(
            original,
            candidate=ImagePair(
                "ghcr.io/devnechi/fbwebltd-app:latest",
                original.candidate.web,
            ),
        )
        with self.assertRaises(ValueError):
            changed.validate()

    def test_same_candidate_and_rollback_rejected(self):
        original = fixture()
        with self.assertRaises(ValueError):
            replace(original, rollback=original.candidate).validate()

    def test_invalid_change_reference_rejected(self):
        with self.assertRaises(ValueError):
            replace(fixture(), change_reference="../../unsafe").validate()

    def test_excessive_window_rejected(self):
        with self.assertRaises(ValueError):
            replace(
                fixture(),
                window_end="2026-11-03T01:00:00Z",
            ).validate()

    def test_non_utc_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            replace(
                fixture(),
                window_start="2026-11-02T23:00:00+03:00",
            ).validate()

    def test_window_open_close(self):
        request = fixture()

        before = datetime(2026, 11, 2, 19, 59, tzinfo=timezone.utc)
        during = datetime(2026, 11, 2, 20, 30, tzinfo=timezone.utc)
        after = datetime(2026, 11, 2, 21, 0, tzinfo=timezone.utc)

        self.assertFalse(request.window_contains(before))
        self.assertTrue(request.window_contains(during))
        self.assertFalse(request.window_contains(after))

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            fixture().window_contains(datetime(2026, 11, 2, 20, 30))

    def test_fingerprint_is_not_approval(self):
        request = fixture()
        self.assertEqual(
            set(request.document()),
            {
                "schema_version",
                "repository",
                "source_ref",
                "source_commit",
                "environment",
                "candidate",
                "rollback",
                "window_start",
                "window_end",
                "change_reference",
            },
        )

        self.assertNotIn("approved", request.document())
        self.assertNotIn("approver", request.document())
        self.assertNotIn("authorization", request.document())


if __name__ == "__main__":
    unittest.main()
