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
        self.assertIn("2h ago", parsed["agenthood"][0])

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


class TestEventContext(unittest.TestCase):
    def test_push(self):
        ctx = u.event_context(
            {
                "type": "PushEvent",
                "payload": {
                    "ref": "refs/heads/feat/x",
                    "commits": [
                        {"message": "feat: wire builder\n\nbody", "sha": "a" * 40}
                    ],
                },
            }
        )
        self.assertIn("pushed 1 commit to branch x: feat: wire builder", ctx)

    def test_merged_pr(self):
        ctx = u.event_context(
            {
                "type": "PullRequestEvent",
                "payload": {
                    "action": "closed",
                    "pull_request": {
                        "number": 42,
                        "title": "harden eval",
                        "merged_at": "t",
                        "user": {"login": "fabio"},
                    },
                },
            }
        )
        self.assertIn("merged PR #42: harden eval by @fabio", ctx)

    def test_issue_with_labels(self):
        ctx = u.event_context(
            {
                "type": "IssuesEvent",
                "payload": {
                    "action": "opened",
                    "issue": {
                        "number": 7,
                        "title": "OG broken",
                        "user": {"login": "fabio"},
                        "labels": [{"name": "bug"}],
                    },
                },
            }
        )
        self.assertIn("opened issue #7: OG broken by @fabio labels: bug", ctx)


class TestPolishLines(unittest.TestCase):
    def resp(self, entries):
        content = json.dumps({"entries": entries})
        return {"choices": [{"message": {"content": content}}]}

    def entry(self, line="- a", summary=("On it", "Really on it.")):
        return {"line": line, "summary": list(summary)}

    def test_no_key_keeps_input(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": ""}, clear=False):
            lines, summaries = u.polish_lines([("- a", "ctx")])
        self.assertEqual(lines, ["- a"])
        self.assertEqual(summaries, [None])

    def test_valid_response_rewrites(self):
        entries = [
            self.entry("- A", ("\u26A1 Shipped it.", "The builder is live.")),
            self.entry("- B", ("Second line.", "More detail.")),
        ]
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp(entries)
        ):
            lines, summaries = u.polish_lines([("- a", "c1"), ("- b", "c2")])
        self.assertEqual(lines, ["- A", "- B"])
        self.assertEqual(
            summaries,
            [["\u26A1 Shipped it.", "The builder is live."], ["Second line.", "More detail."]],
        )

    def test_missing_dash_prefix_readded(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp([self.entry("A")])
        ):
            lines, summaries = u.polish_lines([("- a", "ctx")])
        self.assertEqual(lines, ["- A"])

    def test_bad_entry_shape_falls_back(self):
        bad = {"choices": [{"message": {"content": json.dumps({"entries": [{"line": "- x", "summary": ["only one"]}]})}}]}
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=bad
        ):
            lines, summaries = u.polish_lines([("- x", "ctx")])
        self.assertEqual(lines, ["- x"])
        self.assertEqual(summaries, [None])

    def test_entries_mismatch_falls_back(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp([self.entry()])
        ):
            lines, summaries = u.polish_lines([("- a", "c1"), ("- b", "c2")])
        self.assertEqual(lines, ["- a", "- b"])
        self.assertEqual(summaries, [None, None])

    def test_http_error_falls_back(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", side_effect=RuntimeError("curl failed: boom")
        ):
            lines, summaries = u.polish_lines([("- a", "ctx")])
        self.assertEqual(lines, ["- a"])
        self.assertEqual(summaries, [None])

    def test_invalid_json_falls_back(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", side_effect=ValueError("bad json")
        ):
            lines, summaries = u.polish_lines([("- a", "ctx")])
        self.assertEqual(lines, ["- a"])
        self.assertEqual(summaries, [None])

    def test_build_activity_lines_renders_summaries(self):
        block = u.build_activity_lines(
            {"a": "- a", "b": "- b"},
            [["Line one", "Line two."], None],
        )
        self.assertIn("- a\n  Line one\n  Line two.\n\n- b\n", block)


if __name__ == "__main__":
    unittest.main()
