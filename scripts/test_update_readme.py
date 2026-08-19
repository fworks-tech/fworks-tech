#!/usr/bin/env python3
"""Unit tests for the README activity bullet formatters."""

import json
import os
import sys
import unittest
import urllib.request
from datetime import datetime, timezone
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import update_readme as u  # noqa: E402


class FrozenNow(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc)


class _FrozenClock:
    def setUp(self):
        self._real = u.datetime
        u.datetime = FrozenNow

    def tearDown(self):
        u.datetime = self._real


class TestRelativeTime(_FrozenClock, unittest.TestCase):

    def test_hours_ago(self):
        self.assertEqual(u.relative_time("2026-08-19T09:00:00Z"), "1h ago")

    def test_just_now(self):
        self.assertEqual(u.relative_time("2026-08-19T09:59:59Z"), "just now")

    def test_yesterday(self):
        self.assertEqual(u.relative_time("2026-08-18T10:00:00Z"), "yesterday")

    def test_days_ago(self):
        self.assertEqual(u.relative_time("2026-08-16T10:00:00Z"), "3d ago")

    def test_beyond_30_days(self):
        self.assertEqual(u.relative_time("2026-07-01T10:00:00Z"), "Jul 1, 2026")


class TestCleanText(unittest.TestCase):
    def test_strips_markdown_metacharacters(self):
        self.assertEqual(u.clean_text("fix [x] `y`"), "fix x y")


class TestDescribeEvent(_FrozenClock, unittest.TestCase):
    def event(self, etype, payload, created="2026-08-19T09:00:00Z"):
        return {
            "type": etype,
            "repo": {"name": "fworks-tech/agenthood"},
            "created_at": created,
            "payload": payload,
        }

    def test_push_with_commit(self):
        line = u.describe_event(
            self.event(
                "PushEvent",
                {
                    "ref": "refs/heads/main",
                    "commits": [
                        {
                            "sha": "9f8a7b6c5d",
                            "message": "feat: add builder\n\nbody",
                        }
                    ],
                },
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("\U0001F680", line)
        self.assertIn("[**agenthood**](https://github.com/fworks-tech/agenthood)", line)
        self.assertIn("[`9f8a7b6`](https://github.com/fworks-tech/agenthood/commit/9f8a7b6c5d)", line)
        self.assertIn("to `main`: feat: add builder", line)
        self.assertIn("1h ago", line)

    def test_push_without_sha_skips_link(self):
        line = u.describe_event(
            self.event(
                "PushEvent",
                {"ref": "refs/heads/main", "commits": [{"sha": "", "message": "no sha"}]},
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertNotIn("/commit/", line)
        self.assertIn("no sha", line)

    def test_push_multiple_commits(self):
        line = u.describe_event(
            self.event(
                "PushEvent",
                {
                    "ref": "refs/heads/feat/x",
                    "commits": [{"sha": "a" * 40}, {"sha": "b" * 40}],
                },
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("pushed 2 commits to `x`", line)

    def test_merged_pr(self):
        line = u.describe_event(
            self.event(
                "PullRequestEvent",
                {
                    "action": "closed",
                    "pull_request": {
                        "number": 42,
                        "title": "harden eval",
                        "user": {"login": "fabio"},
                        "merged_at": "2026-08-18T11:00:00Z",
                    },
                },
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("merged [PR #42](https://github.com/fworks-tech/agenthood/pull/42)", line)
        self.assertIn("by @fabio", line)

    def test_opened_pr_title_sanitized(self):
        line = u.describe_event(
            self.event(
                "PullRequestEvent",
                {
                    "action": "opened",
                    "pull_request": {
                        "number": 3,
                        "title": "add [`x`] panel",
                        "user": {"login": "fabio"},
                    },
                },
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("add x panel", line)
        self.assertNotIn("[`x`]", line)

    def test_issue_with_labels(self):
        line = u.describe_event(
            self.event(
                "IssuesEvent",
                {
                    "action": "opened",
                    "issue": {
                        "number": 7,
                        "title": "OG broken",
                        "user": {"login": "fabio"},
                        "labels": [{"name": "bug"}, {"name": "priority: high"}],
                    },
                },
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("[issue #7](https://github.com/fworks-tech/agenthood/issues/7)", line)
        self.assertIn("(bug, priority: high)", line)

    def test_release(self):
        line = u.describe_event(
            self.event(
                "ReleaseEvent",
                {"action": "published", "release": {"tag_name": "v2.1.0"}},
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("[v2.1.0](https://github.com/fworks-tech/agenthood/releases/tag/v2.1.0)", line)

    def test_review(self):
        line = u.describe_event(
            self.event(
                "PullRequestReviewEvent",
                {"review": {"state": "approved"}, "pull_request": {"number": 12}},
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("approved [PR #12]", line)

    def test_create_branch(self):
        line = u.describe_event(
            self.event(
                "CreateEvent",
                {"ref_type": "branch", "ref": "chore/auto-update"},
            ),
            "agenthood",
            "fworks-tech/agenthood",
        )
        self.assertIn("[`chore/auto-update`](https://github.com/fworks-tech/agenthood/tree/chore/auto-update)", line)

    def test_unknown_event(self):
        line = u.describe_event(self.event("SomethingEvent", {}), "agenthood", "fworks-tech/agenthood")
        self.assertIn("\u2014 activity", line)


class TestParseEvents(_FrozenClock, unittest.TestCase):
    def event(self, etype, repo, created):
        return {
            "type": etype,
            "repo": {"name": repo},
            "created_at": created,
            "payload": {},
        }

    def test_dedupes_first_wins(self):
        events = [
            self.event("PushEvent", "fworks-tech/agenthood", "2026-08-19T08:00:00Z"),
            self.event("PushEvent", "fworks-tech/agenthood", "2026-08-19T09:00:00Z"),
        ]
        parsed = u.parse_events(events)
        self.assertEqual(len(parsed), 1)
        self.assertIn("2h ago", parsed["agenthood"])

    def test_skips_noise_and_org_repo(self):
        events = [
            self.event("WatchEvent", "fworks-tech/agenthood", "2026-08-19T08:00:00Z"),
            self.event("ForkEvent", "fworks-tech/agenthood", "2026-08-19T08:00:00Z"),
            self.event("PushEvent", "fworks-tech/fworks-tech", "2026-08-19T08:00:00Z"),
        ]
        self.assertEqual(u.parse_events(events), {})

    def test_respects_top_n(self):
        events = [
            self.event("PushEvent", f"fworks-tech/repo{i}", "2026-08-19T08:00:00Z")
            for i in range(6)
        ]
        parsed = u.parse_events(events)
        self.assertEqual(len(parsed), u.TOP_N)


class TestPolishLines(unittest.TestCase):
    class FakeResp:
        def __init__(self, data):
            self._data = data

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return self._data

    def content(self, lines, summary=("\u26A1 Moving fast", "Second summary line.")):
        body = json.dumps({"summary": list(summary), "lines": lines})
        return json.dumps({"choices": [{"message": {"content": body}}]}).encode()

    def test_no_key_uses_default_summary(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": ""}, clear=False):
            summary, lines = u.polish_lines(["- a", "- b"])
        self.assertEqual(lines, ["- a", "- b"])
        self.assertEqual(len(summary), 3)
        self.assertIn("2", summary[0])

    def test_default_summary_singular(self):
        self.assertIn("1 repo", u.default_summary(["- a"])[0])

    def test_valid_response_rewrites(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch(
            "urllib.request.urlopen",
            return_value=self.FakeResp(
                self.content(["- A", "- B"], ("\u26A1 On a roll", "Two lines."))
            ),
        ):
            summary, lines = u.polish_lines(["- a", "- b"])
        self.assertEqual(lines, ["- A", "- B"])
        self.assertEqual(summary, ["\u26A1 On a roll", "Two lines."])

    def test_missing_dash_prefix_readded(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch(
            "urllib.request.urlopen",
            return_value=self.FakeResp(self.content(["A", "B"])),
        ):
            summary, lines = u.polish_lines(["- a", "- b"])
        self.assertEqual(lines, ["- A", "- B"])

    def test_bad_summary_shape_falls_back(self):
        bad = json.dumps({"summary": "not a list", "lines": ["- x"]})
        body = json.dumps({"choices": [{"message": {"content": bad}}]}).encode()
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch(
            "urllib.request.urlopen", return_value=self.FakeResp(body)
        ):
            summary, lines = u.polish_lines(["- x"])
        self.assertEqual(lines, ["- x"])
        self.assertEqual(len(summary), 3)
        self.assertIn("1", summary[0])

    def test_bad_payload_falls_back(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch(
            "urllib.request.urlopen", return_value=self.FakeResp(b"not json")
        ):
            summary, lines = u.polish_lines(["- a"])
        self.assertEqual(lines, ["- a"])
        self.assertEqual(len(summary), 3)

    def test_network_error_falls_back(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch(
            "urllib.request.urlopen", side_effect=OSError("boom")
        ):
            summary, lines = u.polish_lines(["- a"])
        self.assertEqual(lines, ["- a"])
        self.assertEqual(len(summary), 3)

    def test_build_activity_lines_renders_summary(self):
        block = u.build_activity_lines(
            {"a": "- a", "b": "- b"}, ["\u26A1 Ho", "Second line."]
        )
        self.assertIn("> \u26A1 Ho\n> Second line.\n\n- a\n- b\n", block)


if __name__ == "__main__":
    unittest.main()
