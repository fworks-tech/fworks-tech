#!/usr/bin/env python3
"""Unit tests for README Recent Activity generation."""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import update_readme as u  # noqa: E402


class _MockedClock(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 8, 19, 10, 0, tzinfo=timezone.utc)

    @classmethod
    def _patch(cls):
        _orig = u.datetime
        u.datetime = cls
        return _orig

    @classmethod
    def _unpatch(cls, orig):
        u.datetime = orig


class TestRelativeTime(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

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


class TestDescribeEvent(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

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


class TestFetchEvents(unittest.TestCase):
    def test_returns_none_on_api_failure(self):
        with mock.patch.object(u, "api_get", return_value=None):
            self.assertIsNone(u.fetch_events("token"))

    def test_returns_none_on_non_list_response(self):
        with mock.patch.object(u, "api_get", return_value={"message": "rate limited"}):
            self.assertIsNone(u.fetch_events("token"))

    def test_returns_empty_list_when_no_activity(self):
        with mock.patch.object(u, "api_get", return_value=[]):
            self.assertEqual(u.fetch_events("token"), [])

    def test_distinguishes_error_from_empty(self):
        with mock.patch.object(u, "api_get", side_effect=[None, []]):
            self.assertIsNone(u.fetch_events("token"))
            self.assertEqual(u.fetch_events("token"), [])


class TestEnrichEvent(unittest.TestCase):
    def pr_event(self):
        return {
            "type": "PullRequestEvent",
            "repo": {"name": "fworks-tech/agenthood"},
            "payload": {
                "action": "closed",
                "pull_request": {
                    "number": 9,
                    "title": "wire captcha widget",
                    "body": "Fixes #5",
                    "merged_at": "t",
                    "user": {"login": "fabio"},
                    "head": {"ref": "feat/x"},
                    "base": {"ref": "main"},
                },
            },
        }

    def test_pr_wires_commits_issues_and_prs(self):
        def api_get_side(url, token):
            if "/pulls/9/commits" in url:
                return [{"sha": "c" * 40, "commit": {"message": "feat: wire captcha (#9)"}}]
            if "/issues/5" in url:
                return {"title": "caption broken"}
            if "/issues/9" in url:
                return {"title": "captcha widget"}
            raise AssertionError(f"unexpected url: {url}")
        with mock.patch.object(u, "api_get", side_effect=api_get_side):
            detail = u.enrich_event(self.pr_event(), "token")
        self.assertEqual(detail["commits"], [("c" * 40, "feat: wire captcha (#9)")])
        self.assertEqual(detail["issues"], {5: "caption broken"})
        self.assertEqual(detail["prs"], {9: "captcha widget"})
        self.assertEqual(detail["pr"]["head"], "feat/x")

    def test_no_token_skips_network(self):
        with mock.patch.object(u, "fetch_pr_commits") as fpc, mock.patch.object(
            u, "fetch_issue_titles"
        ) as fit:
            detail = u.enrich_event(self.pr_event(), None)
        fpc.assert_not_called()
        fit.assert_not_called()
        self.assertEqual(detail["commits"], [])
        self.assertEqual(detail["issues"], {})
        self.assertEqual(detail["prs"], {})


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
        def api_get_side(url, token):
            if "/compare/abc123...def456" in url:
                return {"commits": [
                    {"sha": "a" * 40, "commit": {"message": "fix: wire captcha\nbody"}},
                    {"sha": "b" * 40, "commit": {"message": "feat: add toggle"}},
                ]}
            raise AssertionError(f"unexpected url: {url}")
        with mock.patch.object(u, "api_get", side_effect=api_get_side):
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


class TestFetchRecentMergedPrs(unittest.TestCase):
    def test_returns_only_merged_prs(self):
        api_response = [
            {"number": 1, "title": "merged", "merged_at": "2026-08-19T08:00:00Z",
             "user": {"login": "x"}, "head": {"ref": "h"}, "base": {"ref": "main"},
             "body": "done"},
            {"number": 2, "title": "closed not merged", "merged_at": None,
             "user": {"login": "y"}, "head": {"ref": "h"}, "base": {"ref": "main"},
             "body": ""},
        ]
        with mock.patch.object(u, "api_get", return_value=api_response):
            prs = u.fetch_recent_merged_prs("fworks-tech/agenthood", "token")
        self.assertEqual(len(prs), 1)
        self.assertEqual(prs[0]["number"], 1)

    def test_no_token_returns_empty(self):
        self.assertEqual(u.fetch_recent_merged_prs("fworks-tech/agenthood", None), [])

    def test_non_list_response_returns_empty(self):
        with mock.patch.object(u, "api_get", return_value={"error": "rate limited"}):
            self.assertEqual(u.fetch_recent_merged_prs("fworks-tech/agenthood", "token"), [])




class TestSignalHelpers(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

    def test_clean_pr_title_strips_prefix(self):
        self.assertEqual(
            u.clean_pr_title("feat(api): replay online turns"),
            "Replay online turns",
        )

    def test_clean_pr_title_keeps_version(self):
        self.assertEqual(u.clean_pr_title("chore(release): v4.5.0"), "v4.5.0")

    def test_is_noise_pr_rejects_bot(self):
        self.assertTrue(
            u.is_noise_pr(
                {"user": "dependabot[bot]", "title": "chore(deps): bump x"}
            )
        )

    def test_is_noise_pr_keeps_feature(self):
        self.assertFalse(
            u.is_noise_pr({"user": "fworks-tech", "title": "feat(api): replay turns"})
        )

    def test_automation_bot_is_allowed_for_open_prs(self):
        pr = {"user": "app/github-actions", "title": "chore(release): v4.5.0"}
        self.assertTrue(u.is_noise_pr(pr))
        self.assertFalse(u.is_noise_pr(pr, allow_automation=True))

    def test_first_sentence_trims_at_word_boundary(self):
        result = u.first_sentence("A long description " * 10, limit=40)
        self.assertLessEqual(len(result), 41)
        self.assertTrue(result.endswith("\u2026"))

    def test_within_window(self):
        self.assertTrue(u.within_window("2026-08-18T10:00:00Z"))
        self.assertFalse(u.within_window("2026-07-18T10:00:00Z"))


class TestCollectSignals(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

    def test_builds_ordered_signals_with_ids(self):
        prs = [
            {
                "number": 1,
                "title": "feat(api): wire cache",
                "body": "Adds a cache",
                "merged_at": "2026-08-17T10:00:00Z",
                "user": "fworks-tech",
            }
        ]
        open_prs = [
            {
                "number": 2,
                "title": "fix(ui): move button",
                "body": "",
                "updated_at": "2026-08-18T09:00:00Z",
                "user": "fworks-tech",
                "draft": False,
            }
        ]
        releases = [
            {
                "tag": "v1.2.0",
                "name": "",
                "body": "",
                "published_at": "2026-08-19T08:00:00Z",
            }
        ]
        with mock.patch.object(u, "fetch_recent_merged_prs", return_value=prs), \
                mock.patch.object(u, "fetch_open_prs", return_value=open_prs), \
                mock.patch.object(u, "fetch_recent_releases", return_value=releases):
            signals = u.collect_signals("fworks-tech/agenthood", "token")
        self.assertEqual([s["kind"] for s in signals], ["release", "open_pr", "pr"])
        self.assertEqual([s["id"] for s in signals], ["S1", "S2", "S3"])
        self.assertEqual(signals[2]["title"], "Wire cache")
        self.assertEqual(
            signals[0]["url"],
            "https://github.com/fworks-tech/agenthood/releases/tag/v1.2.0",
        )

    def test_skips_noise_and_old_prs(self):
        prs = [
            {
                "number": 1,
                "title": "chore(deps): bump",
                "body": "",
                "merged_at": "2026-08-18T09:00:00Z",
                "user": "dependabot[bot]",
            },
            {
                "number": 2,
                "title": "feat: old",
                "body": "",
                "merged_at": "2026-07-01T09:00:00Z",
                "user": "fworks-tech",
            },
            {
                "number": 3,
                "title": "feat: real",
                "body": "",
                "merged_at": "2026-08-18T09:00:00Z",
                "user": "fworks-tech",
            },
        ]
        with mock.patch.object(u, "fetch_recent_merged_prs", return_value=prs), \
                mock.patch.object(u, "fetch_open_prs", return_value=[]), \
                mock.patch.object(u, "fetch_recent_releases", return_value=[]):
            signals = u.collect_signals("fworks-tech/agenthood", "token")
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0]["title"], "Real")

    def test_draft_open_pr_is_marked(self):
        open_prs = [
            {
                "number": 7,
                "title": "chore(release): v4.5.0",
                "body": "",
                "updated_at": "2026-08-19T09:00:00Z",
                "user": "fworks-tech",
                "draft": True,
            }
        ]
        with mock.patch.object(u, "fetch_recent_merged_prs", return_value=[]), \
                mock.patch.object(u, "fetch_open_prs", return_value=open_prs), \
                mock.patch.object(u, "fetch_recent_releases", return_value=[]):
            signals = u.collect_signals("fworks-tech/agenthood", "token")
        self.assertEqual(signals[0]["title"], "v4.5.0 (draft)")

    def test_draft_release_keeps_its_notes(self):
        open_prs = [
            {
                "number": 1145,
                "title": "chore(release): v4.5.0",
                "body": "### Features\n- MCP cache per server",
                "updated_at": "2026-08-19T09:00:00Z",
                "user": "app/github-actions",
                "draft": True,
            }
        ]
        with mock.patch.object(u, "fetch_recent_merged_prs", return_value=[]), \
                mock.patch.object(u, "fetch_open_prs", return_value=open_prs), \
                mock.patch.object(u, "fetch_recent_releases", return_value=[]):
            signals = u.collect_signals("fworks-tech/agenthood", "token")
        self.assertEqual(signals[0]["title"], "v4.5.0 (draft)")
        self.assertIn("MCP cache per server", signals[0]["context"])


class TestBuildItems(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

    def event(self, repo):
        return {
            "type": "PushEvent",
            "repo": {"name": repo},
            "created_at": "2026-08-19T09:00:00Z",
            "payload": {},
        }

    def test_drops_repos_without_signals_and_passes_meta(self):
        events = [
            self.event("fworks-tech/a"),
            self.event("fworks-tech/b"),
            self.event("fworks-tech/fworks-tech"),
            self.event("BaaRai/ARTEX"),
        ]

        def fake_signals(repo_full, token):
            if repo_full.endswith("/a"):
                return [
                    {
                        "id": "S1",
                        "kind": "pr",
                        "title": "A",
                        "url": "u",
                        "date": "2026-08-19T09:00:00Z",
                        "context": "c",
                        "weight": 2,
                    }
                ]
            return []

        with mock.patch.object(u, "collect_signals", side_effect=fake_signals), \
                mock.patch.object(
                    u,
                    "fetch_repo_meta",
                    return_value={"description": "A repo", "topics": ["x"]},
                ):
            items = u.build_items(events, "token")
        self.assertEqual([item["repo"] for item in items], ["a"])
        self.assertEqual(items[0]["description"], "A repo")
        self.assertEqual(items[0]["topics"], ["x"])

    def test_caps_top_n_and_orders_newest_first(self):
        events = [self.event(f"fworks-tech/r{i}") for i in range(4)]

        def fake_signals(repo_full, token):
            index = int(repo_full[-1])
            return [
                {
                    "id": "S1",
                    "kind": "pr",
                    "title": "T",
                    "url": "u",
                    "date": f"2026-08-{15 + index}T09:00:00Z",
                    "context": "c",
                    "weight": 2,
                }
            ]

        with mock.patch.object(u, "collect_signals", side_effect=fake_signals), \
                mock.patch.object(
                    u, "fetch_repo_meta", return_value={"description": "", "topics": []}
                ):
            items = u.build_items(events, "token")
        self.assertEqual(len(items), u.TOP_N)
        self.assertEqual([item["repo"] for item in items], ["r3", "r2", "r1"])


class TestValidateEntry(unittest.TestCase):
    def item(self):
        return {"repo": "a", "signals": [{"id": "S1"}], "description": "", "topics": []}

    def entry(self, **kwargs):
        data = {
            "headline": "A calm headline",
            "body": "Two calm sentences.",
            "links": ["S1"],
        }
        data.update(kwargs)
        return data

    def test_valid_entry(self):
        self.assertEqual(u.validate_entry(self.item(), self.entry()), [])

    def test_missing_entry(self):
        self.assertEqual(u.validate_entry(self.item(), None), ["missing entry"])

    def test_rejects_pr_number(self):
        reasons = u.validate_entry(self.item(), self.entry(headline="Merged #42"))
        self.assertIn("PR/issue numbers are not allowed", reasons)

    def test_rejects_commit_hash(self):
        reasons = u.validate_entry(self.item(), self.entry(body="Fixed in a1b2c3d."))
        self.assertIn("commit hashes are not allowed", reasons)

    def test_rejects_marketing_word(self):
        reasons = u.validate_entry(self.item(), self.entry(body="A robust change."))
        self.assertIn("marketing filler: robust", reasons)

    def test_rejects_exclamation(self):
        reasons = u.validate_entry(self.item(), self.entry(headline="It works!"))
        self.assertIn("exclamation marks are not allowed", reasons)

    def test_rejects_we(self):
        reasons = u.validate_entry(self.item(), self.entry(body="We changed it."))
        self.assertIn("use first-person singular or neutral voice", reasons)

    def test_rejects_long_body(self):
        reasons = u.validate_entry(self.item(), self.entry(body="x " * 211))
        self.assertIn("body over 420 characters", reasons)

    def test_rejects_markdown(self):
        reasons = u.validate_entry(self.item(), self.entry(body="See [docs](x)."))
        self.assertIn("markdown is not allowed", reasons)


class TestRenderActivity(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

    def item(self):
        return {
            "repo": "wormage-demo",
            "url": "https://github.com/fworks-tech/wormage-demo",
            "description": (
                "A turn-based artillery duel in the browser with destructible "
                "terrain, dynamic wind, and teams of worms."
            ),
            "topics": [],
            "latest": "2026-08-19T09:00:00Z",
            "signals": [
                {
                    "id": "S1",
                    "kind": "pr",
                    "title": "Replay online turns",
                    "url": "https://x/pull/1",
                    "date": "2026-08-19T09:00:00Z",
                    "context": "c",
                    "weight": 2,
                },
                {
                    "id": "S2",
                    "kind": "release",
                    "title": "v4.4.0",
                    "url": "https://x/releases/v4.4.0",
                    "date": "2026-08-19T08:00:00Z",
                    "context": "c",
                    "weight": 3,
                },
            ],
        }

    def test_renders_headline_body_and_links(self):
        block = u.render_activity(
            [self.item()],
            [
                {
                    "headline": "Online duels catch up",
                    "body": "Both sides see the same battlefield.",
                    "links": ["S1", "S2"],
                }
            ],
        )
        self.assertIn(
            "- [**wormage-demo**](https://github.com/fworks-tech/wormage-demo) "
            "\u2014 Online duels catch up",
            block,
        )
        self.assertIn("\n  Both sides see the same battlefield.", block)
        self.assertIn(
            "[Replay online turns](https://x/pull/1) \u00B7 "
            "[v4.4.0](https://x/releases/v4.4.0)",
            block,
        )
        self.assertIn("1h ago", block)

    def test_fallback_uses_description_and_titles(self):
        block = u.render_activity([self.item()], [None])
        self.assertIn(
            "A turn-based artillery duel in the browser with destructible "
            "terrain, dynamic wind, and teams of worms.",
            block,
        )
        self.assertIn("[Replay online turns](https://x/pull/1)", block)
        self.assertNotIn("**Changes:**", block)
        self.assertNotIn("/commit/", block)

    def test_empty_items(self):
        self.assertEqual(u.render_activity([], []), "")


class TestWriteEntries(unittest.TestCase):
    def item(self, repo="agenthood"):
        return {
            "repo": repo,
            "description": "An AI engineering team.",
            "topics": ["ai"],
            "signals": [
                {
                    "id": "S1",
                    "kind": "pr",
                    "title": "Replay online turns",
                    "url": "u",
                    "date": "2026-08-19T09:00:00Z",
                    "context": "merged pull request #1: feat: replay turns",
                    "weight": 2,
                }
            ],
            "latest": "2026-08-19T09:00:00Z",
            "score": 2,
            "url": "https://github.com/fworks-tech/" + repo,
        }

    def resp(self, entries):
        return {"choices": [{"message": {"content": json.dumps({"entries": entries})}}]}

    def entry(self, **kwargs):
        data = {
            "index": 0,
            "headline": "A calm headline",
            "body": "Two calm sentences.",
            "links": ["S1"],
        }
        data.update(kwargs)
        return data

    def test_no_key_returns_nones(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": ""}, clear=False):
            self.assertEqual(u.write_entries([self.item()]), [None])

    def test_valid_response(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}, clear=False), \
                mock.patch.object(u, "MODELS", ["deepseek-v4.1-flash", "qwen3.8-flash"]), \
                mock.patch.object(
                    u, "llm_completions", return_value=self.resp([self.entry()])
                ) as llm:
            result = u.write_entries([self.item()])
        self.assertEqual(result[0]["headline"], "A calm headline")
        self.assertEqual(result[0]["links"], ["S1"])
        self.assertEqual(llm.call_args.args[0]["model"], "deepseek-v4.1-flash")

    def test_unknown_link_is_dropped(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}, clear=False), \
                mock.patch.object(
                    u,
                    "llm_completions",
                    return_value=self.resp([self.entry(links=["S9"])]),
                ):
            result = u.write_entries([self.item()])
        self.assertEqual(result[0]["links"], [])

    def test_primary_model_unavailable_uses_fallback(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}, clear=False), \
                mock.patch.object(u, "MODELS", ["deepseek-v4.1-flash", "qwen3.8-flash"]), \
                mock.patch.object(
                    u,
                    "llm_completions",
                    side_effect=[
                        RuntimeError("Model is unavailable"),
                        self.resp([self.entry()]),
                    ],
                ) as llm:
            result = u.write_entries([self.item()])
        self.assertEqual(result[0]["headline"], "A calm headline")
        self.assertEqual(
            [call.args[0]["model"] for call in llm.call_args_list],
            ["deepseek-v4.1-flash", "qwen3.8-flash"],
        )

    def test_invalid_entry_is_retried(self):
        bad = self.entry(headline="Merged #42")
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}, clear=False), \
                mock.patch.object(
                    u,
                    "llm_completions",
                    side_effect=[self.resp([bad]), self.resp([self.entry()])],
                ) as llm:
            result = u.write_entries([self.item()])
        self.assertEqual(result[0]["headline"], "A calm headline")
        self.assertEqual(llm.call_count, 2)

    def test_failed_retry_returns_none(self):
        bad = self.entry(headline="Merged #42")
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}, clear=False), \
                mock.patch.object(
                    u,
                    "llm_completions",
                    side_effect=[self.resp([bad]), self.resp([bad])],
                ):
            result = u.write_entries([self.item()])
        self.assertEqual(result, [None])

    def test_unavailable_models_return_none(self):
        with mock.patch.dict(os.environ, {"OPENCODE_API_KEY": "k"}, clear=False), \
                mock.patch.object(
                    u,
                    "llm_completions",
                    side_effect=[RuntimeError("boom"), RuntimeError("boom")],
                ):
            result = u.write_entries([self.item()])
        self.assertEqual(result, [None])


class TestRenderPrBody(unittest.TestCase):
    def test_with_activity_has_sections(self):
        block = "- [**agenthood**](u) \u2014 Headline\n  Body."
        body = u.render_pr_body(["agenthood"], block, "Aug 19, 2026")
        text = "\n".join(body)
        self.assertIn("## What", text)
        self.assertIn("## Why", text)
        self.assertIn("## How to test", text)
        self.assertIn("1 entry: agenthood", text)
        self.assertIn(block, text)
        self.assertIn("Last updated bumped to Aug 19, 2026.", text)

    def test_without_activity_is_explicit(self):
        text = "\n".join(u.render_pr_body([], "", "Aug 19, 2026"))
        self.assertIn("No substantive public activity", text)
        self.assertNotIn("## Recent activity", text)


class TestMain(unittest.TestCase):
    def setUp(self):
        self._clock = _MockedClock._patch()

    def tearDown(self):
        _MockedClock._unpatch(self._clock)

    def readme(self, block="- old entry\n"):
        return (
            "# Test\n\n"
            "## Recent Activity\n\n"
            "<!-- recent-activity:start -->\n"
            + block
            + "<!-- recent-activity:end -->\n\n"
            "---\n\n"
            "*Last updated: Sep 1, 2026\n"
        )

    def run_main(self, content, new_rows, events=None, items=None):
        with tempfile.TemporaryDirectory() as d:
            readme = os.path.join(d, "README.md")
            summary = os.path.join(d, "update_summary.txt")
            with open(readme, "w", encoding="utf-8") as f:
                f.write(content)
            with open(summary, "w", encoding="utf-8") as f:
                f.write("")
            items = items if items is not None else [{"repo": "agenthood"}]
            with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "tok"}, clear=False), \
                    mock.patch.object(u, "fetch_events", return_value=events), \
                    mock.patch.object(u, "build_items", return_value=items) as build, \
                    mock.patch.object(
                        u, "write_entries", return_value=[None] * len(items)
                    ), \
                    mock.patch.object(u, "render_activity", return_value=new_rows), \
                    mock.patch.object(u, "README_PATH", readme), \
                    mock.patch.object(u, "SUMMARY_PATH", summary), \
                    mock.patch.object(u, "set_output") as set_output:
                u.main()
            with open(readme, encoding="utf-8") as f:
                result = f.read()
            with open(summary, encoding="utf-8") as f:
                summary_text = f.read()
        return result, summary_text, set_output, build

    def test_changed_block_writes_and_bumps_footer(self):
        result, summary, set_output, _ = self.run_main(
            self.readme(), "- new entry\n", events=[{}]
        )
        set_output.assert_called_once_with(1)
        self.assertIn("- new entry", result)
        self.assertIn("Last updated: Aug 19, 2026", result)
        self.assertIn("agenthood", summary)

    def test_unchanged_block_does_not_write(self):
        result, summary, set_output, _ = self.run_main(
            self.readme("- new entry\n"), "- new entry\n", events=[{}]
        )
        set_output.assert_called_once_with(0)
        self.assertIn("Last updated: Sep 1, 2026", result)
        self.assertEqual(summary, "")

    def test_events_unavailable_keeps_section(self):
        result, _, set_output, build = self.run_main(self.readme(), "", events=None)
        set_output.assert_called_once_with(0)
        build.assert_not_called()
        self.assertIn("- old entry", result)

    def test_no_signals_keeps_section(self):
        result, _, set_output, _ = self.run_main(
            self.readme(), "", events=[], items=[]
        )
        set_output.assert_called_once_with(0)
        self.assertIn("- old entry", result)

    def test_missing_markers_skips(self):
        result, _, set_output, _ = self.run_main(
            "# Test\n", "- new entry\n", events=[{}]
        )
        set_output.assert_called_once_with(0)
        self.assertEqual(result, "# Test\n")

    def test_missing_token_skips(self):
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": ""}, clear=False), \
                mock.patch.object(u, "fetch_events") as fetch, \
                mock.patch.object(u, "set_output") as set_output:
            u.main()
        fetch.assert_not_called()
        set_output.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
