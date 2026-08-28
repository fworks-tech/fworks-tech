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
    def push_event(self):
        return {
            "type": "PushEvent",
            "payload": {"ref": "refs/heads/feat/x", "commits": []},
        }

    def test_push(self):
        ctx = u.event_context(
            self.push_event(),
            {"commits": [("a" * 40, "feat: wire builder")], "ref": "feat/x"},
        )
        self.assertIn("pushed 1 commit to branch feat/x: feat: wire builder", ctx)

    def test_push_empty_commits_is_ambiguous_not_zero(self):
        ctx = u.event_context(self.push_event(), {"ref": "feat/x"})
        self.assertIn("pushed to branch feat/x", ctx)
        self.assertIn("did not include commit details", ctx)
        self.assertNotIn("0 commits", ctx)

    def test_push_context_includes_fetched_messages(self):
        ctx = u.event_context(
            self.push_event(),
            {
                "ref": "feat/x",
                "commits": [
                    ("4" * 40, "fix: wire captcha"),
                    ("9" * 40, "feat: add visibility toggle"),
                ],
            },
        )
        self.assertIn(
            "pushed 2 commits to branch feat/x: fix: wire captcha; feat: add visibility toggle",
            ctx,
        )
        self.assertNotIn("did not include", ctx)

    def test_push_many_commits(self):
        ctx = u.event_context(
            self.push_event(),
            {"commits": [("1" * 40, "one"), ("2" * 40, "two")], "ref": "feat/x"},
        )
        self.assertIn("pushed 2 commits to branch feat/x: one; two", ctx)

    def test_push_lists_linked_issues_and_prs(self):
        ctx = u.event_context(
            self.push_event(),
            {
                "commits": [("1" * 40, "fix: bump deps (#42)")],
                "issues": {5: "OG broken"},
                "prs": {42: "bump deps"},
            },
        )
        self.assertIn("linked issues: #5 OG broken", ctx)
        self.assertIn("referenced PRs: #42 bump deps", ctx)

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
            },
            {"pr": {"number": 42, "title": "harden eval", "author": "fabio", "merged_at": "t"}},
        )
        self.assertIn("merged PR #42: harden eval by @fabio", ctx)

    def test_pr_includes_commits_body_and_linked_issues(self):
        ctx = u.event_context(
            {
                "type": "PullRequestEvent",
                "payload": {
                    "action": "closed",
                    "pull_request": {"number": 42, "merged_at": "t"},
                },
            },
            {
                "pr": {
                    "number": 42,
                    "title": "harden eval",
                    "body": "closes #5",
                    "head": "feat/x",
                    "base": "main",
                    "merged_at": "t",
                    "author": "fabio",
                },
                "commits": [("c9c3b0a" + "0" * 33, "fix: wire captcha")],
                "issues": {5: "OG broken"},
                "prs": {},
            },
        )
        self.assertIn("PR body excerpt: closes #5", ctx)
        self.assertIn("head branch: feat/x, base branch: main", ctx)
        self.assertIn("PR commits: fix: wire captcha", ctx)
        self.assertIn("linked issues: #5 OG broken", ctx)

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
            },
            {"issue": {"number": 7, "title": "OG broken", "labels": ["bug"]}},
        )
        self.assertIn("opened issue #7: OG broken by @fabio labels: bug", ctx)


class TestFetchPushCommits(unittest.TestCase):
    class FakeResp:
        def __init__(self, data):
            self._data = json.dumps(data).encode()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return self._data

    def event(self):
        return {
            "type": "PushEvent",
            "repo": {"name": "fworks-tech/agenthood-site"},
            "payload": {
                "ref": "refs/heads/89-studio-captcha-widget-visibility",
                "before": "abc123",
                "head": "def456",
                "commits": [],
            },
        }

    def resp(self):
        return {
            "commits": [
                {"sha": "a" * 40, "commit": {"message": "fix: wire captcha\nbody"}},
                {"sha": "b" * 40, "commit": {"message": "feat: add toggle"}},
            ]
        }

    def test_returns_commit_shas_and_subjects(self):
        with mock.patch(
            "urllib.request.urlopen", return_value=self.FakeResp(self.resp())
        ):
            commits = u.fetch_push_commits(
                "fworks-tech/agenthood-site", "abc123", "def456", "token"
            )
        self.assertEqual(
            commits, [("a" * 40, "fix: wire captcha"), ("b" * 40, "feat: add toggle")]
        )

    def test_failure_returns_empty(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("boom")):
            self.assertEqual(u.fetch_push_commits("r/o", "a", "b", "token"), [])

    def test_no_token_returns_empty(self):
        self.assertEqual(u.fetch_push_commits("r/o", "a", "b", None), [])

    def test_parse_events_feeds_fetched_commits_to_context_and_refs(self):
        with mock.patch(
            "urllib.request.urlopen", return_value=self.FakeResp(self.resp())
        ):
            parsed = u.parse_events([self.event()], "token")
        bullet, ctx, refs = parsed["agenthood-site"]
        self.assertIn(
            "pushed 2 commits to branch 89-studio-captcha-widget-visibility: "
            "fix: wire captcha; feat: add toggle",
            ctx,
        )
        commit_refs = [r for r in refs if r["kind"] == "commit"]
        self.assertGreaterEqual(len(commit_refs), 2)
        self.assertTrue(commit_refs[0]["url"].startswith("https://github.com/"))


class TestLinkedRefs(unittest.TestCase):
    def test_keyword_refs_map_to_issues(self):
        issues, prs = u.linked_refs("Fixes #5\nCloses #12")
        self.assertEqual(issues, [5, 12])
        self.assertEqual(prs, [])

    def test_squash_suffix_maps_to_prs(self):
        issues, prs = u.linked_refs("chore: bump deps (#42)")
        self.assertEqual(prs, [42])
        self.assertEqual(issues, [])

    def test_commit_subjects_scanned(self):
        issues, prs = u.linked_refs("", "fix: resolve issue #8", "feat: add panel (#9)")
        self.assertEqual(issues, [8])
        self.assertEqual(prs, [9])


class TestCollectRefs(unittest.TestCase):
    def test_pr_event_has_commit_issue_and_pr_refs(self):
        event = {"type": "PullRequestEvent", "repo": {"name": "fworks-tech/agenthood"}, "payload": {}}
        detail = {
            "commits": [("c9c3b0a1234567890", "fix: wire captcha")],
            "issues": {5: "OG broken"},
            "prs": {},
            "pr": {"number": 42, "title": "harden eval"},
        }
        refs = u.collect_refs(event, detail)
        self.assertEqual([r["kind"] for r in refs], ["commit", "issue", "pr"])
        self.assertEqual(refs[0]["sha"], "c9c3b0a")
        self.assertIn("/commit/c9c3b0a1234567890", refs[0]["url"])
        self.assertIn("/issues/5", refs[1]["url"])
        self.assertEqual(refs[2]["number"], "42")

    def test_pr_ref_deduped_when_already_in_prs(self):
        event = {"type": "PullRequestEvent", "repo": {"name": "fworks-tech/agenthood"}, "payload": {}}
        detail = {
            "commits": [],
            "issues": {},
            "prs": {42: "harden eval"},
            "pr": {"number": 42, "title": "harden eval"},
        }
        refs = u.collect_refs(event, detail)
        prs = [r for r in refs if r["kind"] == "pr"]
        self.assertEqual(len(prs), 1)

    def test_branch_ref_for_create_event(self):
        event = {"type": "CreateEvent", "repo": {"name": "fworks-tech/agenthood"}, "payload": {}}
        detail = {"ref_type": "branch", "ref": "chore/auto-update", "commits": [], "issues": {}, "prs": {}}
        refs = u.collect_refs(event, detail)
        branch = [r for r in refs if r["kind"] == "branch"]
        self.assertEqual(len(branch), 1)
        self.assertIn("/tree/chore/auto-update", branch[0]["url"])


class TestChangesAndRelatedLines(unittest.TestCase):
    def test_changes_line_lists_commits(self):
        refs = [
            {"kind": "commit", "sha": "c9c3b0a", "url": "u1", "subject": "fix: wire captcha"},
            {"kind": "commit", "sha": "cc193f8", "url": "u2", "subject": "feat: add toggle"},
        ]
        line = u._changes_line(refs)
        self.assertTrue(line.startswith("**Changes:** "))
        self.assertIn("[`c9c3b0a`](u1) fix: wire captcha", line)
        self.assertIn(" \u00B7 ", line)

    def test_changes_line_many_commits_says_more(self):
        refs = [
            {"kind": "commit", "sha": f"{i:07d}", "url": f"u{i}", "subject": f"s{i}"}
            for i in range(5)
        ]
        line = u._changes_line(refs)
        self.assertIn("and 2 more commits", line)

    def test_changes_line_empty_without_commits(self):
        self.assertEqual(u._changes_line([{"kind": "issue", "number": "5", "url": "u", "title": "t"}]), "")

    def test_related_line_links_issues_and_prs(self):
        refs = [
            {"kind": "issue", "number": "5", "url": "https://github.com/fworks-tech/agenthood/issues/5", "title": "OG broken"},
            {"kind": "pr", "number": "42", "url": "https://github.com/fworks-tech/agenthood/pull/42", "title": "harden eval"},
        ]
        line = u._related_line(refs)
        self.assertIn("[issue #5](https://github.com/fworks-tech/agenthood/issues/5) — OG broken", line)
        self.assertIn("[PR #42](https://github.com/fworks-tech/agenthood/pull/42) — harden eval", line)

    def test_related_line_empty_without_issues(self):
        refs = [{"kind": "pr", "number": "42", "url": "u", "title": "t"}]
        self.assertEqual(u._related_line(refs), "")


class TestRenderPrBody(unittest.TestCase):
    def test_with_activity_has_scribe_sections(self):
        blocks = "- \U0001F680 **agenthood**\n  **Brief:** Real line.\n  Second line."
        body = u.render_pr_body(["agenthood"], blocks, "Aug 19, 2026")
        text = "\n".join(body)
        self.assertIn("## What", text)
        self.assertIn("## Why", text)
        self.assertIn("## How to test", text)
        self.assertIn("1 entry: agenthood", text)
        self.assertIn("- \U0001F680 **agenthood**\n  **Brief:** Real line.\n  Second line.", text)
        self.assertIn("Last updated bumped to Aug 19, 2026.", text)

    def test_without_activity_is_explicit(self):
        body = u.render_pr_body([], "", "Aug 19, 2026")
        text = "\n".join(body)
        self.assertIn("No qualifying public events", text)
        self.assertNotIn("Recent activity", text)


class TestPolishLines(unittest.TestCase):
    def resp(self, entries):
        content = json.dumps({"entries": entries})
        return {"choices": [{"message": {"content": content}}]}

    def entry(self, line="- a", brief=("On it", "Really on it.")):
        return {"line": line, "brief": list(brief)}

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

    def test_accepts_three_line_brief(self):
        entries = [self.entry("- A", ("First.", "Second.", "Third."))]
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp(entries)
        ):
            lines, summaries = u.polish_lines([("- a", "ctx")])
        self.assertEqual(summaries, [["First.", "Second.", "Third."]])

    def test_missing_dash_prefix_readded(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp([self.entry("A")])
        ):
            lines, summaries = u.polish_lines([("- a", "ctx")])
        self.assertEqual(lines, ["- A"])

    def test_bad_entry_shape_degrades_only_that_entry(self):
        bad = {"choices": [{"message": {"content": json.dumps({"entries": [{"line": "", "brief": ["a", "b"]}]})}}]}
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=bad
        ):
            lines, summaries = u.polish_lines([("- x", "ctx")])
        self.assertEqual(lines, ["- x"])
        self.assertEqual(summaries, [[]])

    def test_fewer_entries_degrades_missing(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp([self.entry("- A", ("On it", "Keep calm."))])
        ):
            lines, summaries = u.polish_lines([("- a", "c1"), ("- b", "c2")])
        self.assertEqual(lines, ["- A", "- b"])
        self.assertEqual(summaries, [["On it", "Keep calm."], []])

    def test_partial_bad_entry_keeps_good_ones(self):
        entries = [self.entry("- A", ("Good line.", "Second good.")), {"line": "x"}]
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}), mock.patch.object(
            u, "llm_completions", return_value=self.resp(entries)
        ):
            lines, summaries = u.polish_lines([("- a", "c1"), ("- b", "c2")])
        self.assertEqual(lines, ["- A", "- b"])
        self.assertEqual(summaries, [["Good line.", "Second good."], []])

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

    def test_system_prompt_grounds_against_invention(self):
        self.assertIn("never invent", u.SYSTEM_PROMPT)
        self.assertIn("REAL brief", u.SYSTEM_PROMPT)
        self.assertIn("exactly 3", u.SYSTEM_PROMPT)
        self.assertIn("NAME THE ARTIFACTS", u.SYSTEM_PROMPT)
        self.assertIn("foundation", u.SYSTEM_PROMPT)
        self.assertIn("could apply to any repo", u.SYSTEM_PROMPT)
        self.assertIn("confident", u.SYSTEM_PROMPT)
        self.assertIn("never clinical or robotic", u.SYSTEM_PROMPT)
        self.assertIn("zero commits", u.SYSTEM_PROMPT)
        self.assertIn("NO NEGATIVE CLAIMS", u.SYSTEM_PROMPT)

    def test_build_activity_lines_renders_brief(self):
        block = u.build_activity_lines(
            {"a": "- a", "b": "- b"},
            [["Line one", "Line two."], None],
        )
        self.assertIn("- a\n  **Brief:** Line one\n  Line two.\n\n- b\n", block)

    def test_build_activity_lines_appends_changes_and_related(self):
        refs = [
            [
                {"kind": "commit", "sha": "c9c3b0a", "url": "u1", "subject": "fix: wire captcha"},
                {"kind": "issue", "number": "5", "url": "u2", "title": "OG broken"},
            ]
        ]
        block = u.build_activity_lines({"a": "- a"}, [None], refs)
        self.assertIn("**Changes:** [`c9c3b0a`](u1) fix: wire captcha", block)
        self.assertIn("**Related:** [issue #5](u2) — OG broken", block)


if __name__ == "__main__":
    unittest.main()
