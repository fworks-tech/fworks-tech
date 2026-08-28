#!/usr/bin/env python3
"""Auto-update the Recent Activity section in README.md.

Fetches recent public events from the GitHub Events API (pushes, PRs,
issues, releases) and regenerates the activity entries under the
``## Recent Activity`` heading. Each entry carries a bullet headline
that links to the repo, PR, commit or issue, a grounded LLM ``Brief``
(when OPENCODE_API_KEY is set), and deterministic ``Changes`` /
``Related`` reference lines built from real GitHub API data — commit
SHAs, PR commit lists and linked-issue titles — so the references stay
valid even when the LLM is unavailable. Always bumps the "Last updated"
footer so the workflow always has a diff to commit and opens a PR daily.

Outputs ``changed=1`` via $GITHUB_OUTPUT, or ``changed=0`` if the
section is missing or the API call fails.
"""

import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone

ORG = "fworks-tech"
TOP_N = 3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
README_PATH = os.path.join(REPO_ROOT, "README.md")
SUMMARY_PATH = os.path.join(SCRIPT_DIR, "update_summary.txt")

ACTIVITY_RE = re.compile(
    r"<!-- recent-activity:start -->\n"
    r"(.*?)"
    r"<!-- recent-activity:end -->",
    re.DOTALL,
)

EMOJI = {
    "PushEvent": "\U0001F680",
    "PullRequestEvent": "\U0001F500",
    "IssuesEvent": "\U0001F41B",
    "IssueCommentEvent": "\U0001F4AC",
    "PullRequestReviewEvent": "\u2705",
    "ReleaseEvent": "\U0001F4E6",
    "CreateEvent": "\U0001F331",
    "DeleteEvent": "\U0001F5D1\uFE0F",
}

SKIP_TYPES = {"WatchEvent", "ForkEvent", "MemberEvent", "GollumEvent"}

API_BASE = os.environ.get(
    "OPENCODE_README_BASE_URL", "https://opencode.ai/zen/go/v1"
)
MODEL = os.environ.get("OPENCODE_README_MODEL", "deepseek-v4-flash")


def api_get(url, token):
    """GET a GitHub API URL, returning decoded JSON or None on failure."""
    if not token:
        return None
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "update-readme-script")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def fetch_events(token):
    """Fetch recent public events; None when the API call fails.

    A failure returns None (not []) so callers can distinguish a broken
    API from genuinely empty activity instead of wiping the section.
    """
    url = f"https://api.github.com/users/{ORG}/events/public?per_page=100"
    data = api_get(url, token)
    return data if isinstance(data, list) else None


def fetch_pr_commits(repo_full, pr_number, token):
    """Commit (sha, subject) list for a pull request."""
    if not token:
        return []
    url = f"https://api.github.com/repos/{repo_full}/pulls/{pr_number}/commits"
    commits = []
    for c in (api_get(url, token) or [])[:10]:
        sha = c.get("sha", "")
        subject = c.get("commit", {}).get("message", "").split("\n")[0][:80]
        if sha:
            commits.append((sha, subject))
    return commits


def fetch_push_commits(repo_full, before, head, token):
    """Commit (sha, subject) list for a push via the compare endpoint."""
    if not token:
        return []
    url = f"https://api.github.com/repos/{repo_full}/compare/{before}...{head}"
    commits = []
    for c in (api_get(url, token) or {}).get("commits", [])[:10]:
        sha = c.get("sha", "")
        subject = c.get("commit", {}).get("message", "").split("\n")[0][:80]
        if sha:
            commits.append((sha, subject))
    return commits


def fetch_issue_titles(repo_full, numbers, token):
    """Map issue/PR numbers to their titles via the issues endpoint."""
    titles = {}
    for number in numbers[:5]:
        data = api_get(f"https://api.github.com/repos/{repo_full}/issues/{number}", token)
        if data:
            titles[number] = data.get("title", "")
    return titles


def linked_refs(body, *subjects):
    """Split referenced numbers into (issue_numbers, pr_numbers).

    Keyword patterns like 'closes #4' map to issues; the squash-merge
    suffix '(#42)' maps to the PR the commits came through.
    """
    issues, prs = set(), set()
    text = "\n".join([body or "", *subjects])
    for m in re.finditer(
        r"(?:closes?|fix(?:es|ed)?|resolves?|refs?|references?|implements?|see|relates?\s+to)\s+(?:issue\s+)?#\s*(\d+)",
        text,
        re.IGNORECASE,
    ):
        issues.add(int(m.group(1)))
    for m in re.finditer(r"\(\s*(?:#|issue\s+#)\s*(\d+)\s*\)", text):
        prs.add(int(m.group(1)))
    return sorted(issues), sorted(prs)


def format_date(iso_ts):
    """Convert ISO 8601 timestamp to 'Mon D, YYYY' (no leading zero)."""
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def relative_time(iso_ts):
    """Human-friendly age, falling back to a full date beyond 30 days."""
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    delta = datetime.now(timezone.utc) - dt
    days = delta.days
    if days < 1:
        hours = int(delta.total_seconds() // 3600)
        return "just now" if hours < 1 else f"{hours}h ago"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days}d ago"
    return format_date(iso_ts)


def repo_url(repo_full):
    """Full repo name 'owner/name' to its github.com URL."""
    return f"https://github.com/{repo_full}"


def clean_text(text):
    """Strip markdown metacharacters that would break a bullet's rendering."""
    return text.replace("[", "").replace("]", "").replace("`", "")


def enrich_event(event, token=None):
    """Network-fill event details: PR commits, push commits, linked issues.

    Returns a plain dict consumed by both ``event_context`` (LLM digest)
    and ``collect_refs`` (deterministic reference links). Never raises;
    a missing detail simply degrades that entry.
    """
    etype = event.get("type", "")
    payload = event.get("payload", {})
    repo_full = event.get("repo", {}).get("name", "")
    info = {"commits": [], "issues": {}, "prs": {}}

    if etype == "PushEvent":
        info["ref"] = payload.get("ref", "").split("/")[-1]
        commits = [
            (c.get("sha", ""), c.get("message", "").split("\n")[0][:80])
            for c in payload.get("commits", [])
            if c.get("sha")
        ]
        if (
            not commits
            and token
            and payload.get("before")
            and payload.get("head")
        ):
            commits = fetch_push_commits(
                repo_full, payload["before"], payload["head"], token
            )
        info["commits"] = commits

    elif etype == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        info["pr"] = {
            "number": pr.get("number"),
            "title": pr.get("title", ""),
            "body": pr.get("body", ""),
            "head": pr.get("head", {}).get("ref", ""),
            "base": pr.get("base", {}).get("ref", ""),
            "merged_at": pr.get("merged_at"),
            "author": pr.get("user", {}).get("login", ""),
        }
        info["commits"] = fetch_pr_commits(repo_full, pr.get("number"), token) if token else []

    elif etype == "IssuesEvent":
        issue = payload.get("issue", {})
        info["issue"] = {
            "number": issue.get("number"),
            "title": issue.get("title", ""),
            "body": issue.get("body", ""),
            "labels": [l.get("name", "") for l in issue.get("labels", [])],
        }

    elif etype == "PullRequestReviewEvent":
        pr = payload.get("pull_request", {})
        info["pr"] = {"number": pr.get("number"), "title": pr.get("title", "")}

    elif etype == "IssueCommentEvent":
        issue = payload.get("issue", {})
        info["issue"] = {"number": issue.get("number"), "title": issue.get("title", "")}

    elif etype == "ReleaseEvent":
        release = payload.get("release", {})
        info["release"] = {
            "tag": release.get("tag_name", ""),
            "name": release.get("name", ""),
        }

    elif etype in ("CreateEvent", "DeleteEvent"):
        info["ref_type"] = payload.get("ref_type", "")
        info["ref"] = payload.get("ref", "")

    subjects = [s for _, s in info["commits"]]
    issue_nums, pr_nums = linked_refs(
        info.get("pr", {}).get("body", "")
        if "pr" in info
        else info.get("issue", {}).get("body", ""),
        *subjects,
    )
    info["issues"] = fetch_issue_titles(repo_full, issue_nums, token) if token else {}
    info["prs"] = fetch_issue_titles(repo_full, pr_nums, token) if token else {}
    return info


def _commit_ref(repo_full, sha, subject):
    return {
        "kind": "commit",
        "sha": sha[:7],
        "url": f"{repo_url(repo_full)}/commit/{sha}",
        "subject": subject,
    }


def _issue_ref(repo_full, number, title):
    return {
        "kind": "issue",
        "number": str(number),
        "url": f"{repo_url(repo_full)}/issues/{number}",
        "title": title,
    }


def _pr_ref(repo_full, number, title):
    return {
        "kind": "pr",
        "number": str(number),
        "url": f"{repo_url(repo_full)}/pull/{number}",
        "title": title,
    }


def collect_refs(event, detail):
    """Deterministic reference links (commits, issues, PRs) for an event.

    Built solely from API data so every URL is valid; the LLM never
    generates these links.
    """
    repo_full = event.get("repo", {}).get("name", "")
    refs = [_commit_ref(repo_full, sha, subj) for sha, subj in detail.get("commits", [])]
    refs.extend(
        _issue_ref(repo_full, n, t) for n, t in detail.get("issues", {}).items()
    )
    refs.extend(_pr_ref(repo_full, n, t) for n, t in detail.get("prs", {}).items())
    pr = detail.get("pr") or {}
    number = pr.get("number")
    if number and not any(
        r["kind"] == "pr" and r["number"] == str(number) for r in refs
    ):
        refs.append(_pr_ref(repo_full, number, pr.get("title", "")))
    if detail.get("ref_type") == "branch" and detail.get("ref"):
        refs.append(
            {
                "kind": "branch",
                "name": detail["ref"],
                "url": f"{repo_url(repo_full)}/tree/{detail['ref']}",
            }
        )
    return refs


def parse_events(events, token=None):
    """Extract one (bullet, context, refs) triple per repo from events.

    Deduplicates by repo, keeping only the most recent event for each.
    Skips noise events (WatchEvent, ForkEvent, MemberEvent).
    """
    seen = {}
    for event in events:
        repo_full = event.get("repo", {}).get("name", "")
        repo_short = repo_full.split("/")[-1]
        if not repo_short or repo_short == ORG:
            continue
        if event.get("type") in SKIP_TYPES:
            continue
        if repo_short in seen:
            continue
        detail = enrich_event(event, token)
        seen[repo_short] = (
            describe_event(event, repo_short, repo_full),
            event_context(event, detail),
            collect_refs(event, detail),
        )
        if len(seen) >= TOP_N:
            break
    return seen


def event_context(event, detail=None):
    """Structured multi-line digest of an event, used for the LLM prompt."""
    etype = event.get("type", "")
    payload = event.get("payload", {})
    detail = detail or {}

    if etype == "PushEvent":
        ref = detail.get("ref") or payload.get("ref", "").split("/")[-1]
        commits = detail.get("commits", [])
        if commits:
            if len(commits) == 1:
                heads = f": {commits[0][1]}"
            else:
                heads = f": {'; '.join(s for _, s in commits[:10])[:300]}"
            lines = [f"pushed {len(commits)} commit{'s' if len(commits) != 1 else ''} to branch {ref}{heads}"]
        else:
            lines = [
                f"pushed to branch {ref} (GitHub did not include commit details)"
            ]
        if detail.get("issues"):
            lines.append(
                "linked issues: "
                + "; ".join(f"#{n} {t}" for n, t in detail["issues"].items())
            )
        if detail.get("prs"):
            lines.append(
                "referenced PRs: "
                + "; ".join(f"#{n} {t}" for n, t in detail["prs"].items())
            )
        return "\n".join(lines)

    if etype == "PullRequestEvent":
        pr = detail.get("pr", {}) or {}
        verb = "merged" if pr.get("merged_at") else payload.get("action", "opened")
        title = pr.get("title") or payload.get("pull_request", {}).get("title", "")
        author = pr.get("author") or payload.get("pull_request", {}).get("user", {}).get("login", "")
        lines = [f"{verb} PR #{pr.get('number', '')}: {title} by @{author}"]
        if pr.get("body"):
            lines.append("PR body excerpt: " + clean_text(pr["body"]).strip()[:500])
        if pr.get("head"):
            lines.append(f"head branch: {pr['head']}, base branch: {pr.get('base', '')}")
        commits = detail.get("commits", [])
        if commits:
            lines.append("PR commits: " + "; ".join(s for _, s in commits[:10])[:300])
        if detail.get("issues"):
            lines.append(
                "linked issues: "
                + "; ".join(f"#{n} {t}" for n, t in detail["issues"].items())
            )
        return "\n".join(lines)

    if etype == "IssuesEvent":
        issue = detail.get("issue", {}) or {}
        number = issue.get("number") or payload.get("issue", {}).get("number", "")
        title = issue.get("title") or payload.get("issue", {}).get("title", "")
        labels = issue.get("labels") or [
            label.get("name") for label in payload.get("issue", {}).get("labels", [])
        ][:2]
        author = payload.get("issue", {}).get("user", {}).get("login", "")
        label_part = f" labels: {', '.join(labels)}" if labels else ""
        lines = [
            f"{payload.get('action', 'opened')} issue #{number}: {title} by @{author}{label_part}"
        ]
        if issue.get("body"):
            lines.append("issue body excerpt: " + clean_text(issue["body"]).strip()[:500])
        return "\n".join(lines)

    if etype == "ReleaseEvent":
        release = payload.get("release", {})
        return f"{payload.get('action', 'published')} release {release.get('tag_name', '')}"

    if etype == "PullRequestReviewEvent":
        pr = payload.get("pull_request", {})
        state = payload.get("review", {}).get("state", "reviewed")
        return f"{state} PR #{pr.get('number', '')}"

    if etype == "IssueCommentEvent":
        issue = payload.get("issue", {})
        return f"commented on issue #{issue.get('number', '')}"

    if etype in ("CreateEvent", "DeleteEvent"):
        return f"{etype.replace('Event', '').lower()} {payload.get('ref_type', '')} {payload.get('ref', '')}"

    return etype.replace("Event", "")


def describe_event(event, repo_short, repo_full):
    """Return a single bullet-point line describing a GitHub event."""
    etype = event.get("type", "")
    payload = event.get("payload", {})
    base = repo_url(repo_full)
    emoji = EMOJI.get(etype, "\u2B50")
    created_at = event.get("created_at", "")
    age = f" \u00B7 {relative_time(created_at)}" if created_at else ""

    if etype == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        action = payload.get("action", "opened")
        title = clean_text(pr.get("title", ""))[:60]
        number = pr.get("number", "")
        author = pr.get("user", {}).get("login", "")
        merged = pr.get("merged_at")
        verb = "merged" if merged else action
        link = f"[PR #{number}]({base}/pull/{number})"
        text = f"{verb} {link}"
        if title:
            text += f": {title}"
        if author:
            text += f" by @{author}"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 {text}{age}"

    if etype == "IssuesEvent":
        issue = payload.get("issue", {})
        action = payload.get("action", "opened")
        title = clean_text(issue.get("title", ""))[:60]
        number = issue.get("number", "")
        author = issue.get("user", {}).get("login", "")
        labels = [label.get("name") for label in issue.get("labels", [])][:2]
        link = f"[issue #{number}]({base}/issues/{number})"
        text = f"{action} {link}"
        if title:
            text += f": {title}"
        if author:
            text += f" by @{author}"
        if labels:
            text += f" ({', '.join(labels)})"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 {text}{age}"

    if etype == "PushEvent":
        commits = payload.get("commits", [])
        ref = payload.get("ref", "").split("/")[-1]
        if len(commits) == 1:
            sha = commits[0].get("sha", "")
            msg = clean_text(commits[0].get("message", "").split("\n")[0])[:60]
            if sha:
                short = sha[:7]
                sha_link = f"[`{short}`]({base}/commit/{sha})"
                return f"- {emoji} [**{repo_short}**]({base}) \u2014 pushed {sha_link} to `{ref}`: {msg}{age}"
            return f"- {emoji} [**{repo_short}**]({base}) \u2014 pushed to `{ref}`: {msg}{age}"
        if len(commits) > 1:
            return f"- {emoji} [**{repo_short}**]({base}) \u2014 pushed {len(commits)} commits to `{ref}`{age}"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 pushed to `{ref}`{age}"

    if etype == "ReleaseEvent":
        release = payload.get("release", {})
        tag = release.get("tag_name", "release")
        action = payload.get("action", "published")
        tag_link = f"[{tag}]({base}/releases/tag/{tag})"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 {action} release {tag_link}{age}"

    if etype == "IssueCommentEvent":
        issue = payload.get("issue", {})
        number = issue.get("number", "")
        link = f"[issue #{number}]({base}/issues/{number})"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 commented on {link}{age}"

    if etype == "PullRequestReviewEvent":
        pr = payload.get("pull_request", {})
        number = pr.get("number", "")
        state = payload.get("review", {}).get("state", "reviewed")
        link = f"[PR #{number}]({base}/pull/{number})"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 {state} {link}{age}"

    if etype == "CreateEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        if ref_type == "branch":
            ref_link = f"[`{ref}`]({base}/tree/{ref})"
            return f"- {emoji} [**{repo_short}**]({base}) \u2014 created branch {ref_link}{age}"
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 created {ref_type} {ref}{age}"

    if etype == "DeleteEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        return f"- {emoji} [**{repo_short}**]({base}) \u2014 deleted {ref_type} {ref}{age}"

    return f"- {emoji} [**{repo_short}**]({base}) \u2014 activity{age}"


def _changes_line(refs):
    """Deterministic '**Changes:**' line linking commit SHAs."""
    commits = [r for r in refs if r["kind"] == "commit"]
    if not commits:
        return ""
    parts = []
    for r in commits[:3]:
        label = f"[`{r['sha']}`]({r['url']})"
        if r.get("subject"):
            label += " " + clean_text(r["subject"])[:40].rstrip()
        parts.append(label)
    if len(commits) > 3:
        parts.append(f"and {len(commits) - 3} more commits")
    return "**Changes:** " + " \u00B7 ".join(parts)


def _related_line(refs):
    """Deterministic '**Related:**' line linking issues (and PRs)."""
    related = [r for r in refs if r["kind"] in ("issue", "pr")][:3]
    if not any(r["kind"] == "issue" for r in related):
        return ""
    pieces = []
    for r in related:
        if r["kind"] == "issue":
            label = f"[issue #{r['number']}]({r['url']})"
        else:
            label = f"[PR #{r['number']}]({r['url']})"
        if r.get("title"):
            label += " \u2014 " + clean_text(r["title"])[:40]
        pieces.append(label)
    return "**Related:** " + " \u00B7 ".join(pieces)


def build_activity_lines(event_map, summaries, refs_list=None):
    """Build entry blocks: bullet headline, brief, and deterministic refs."""
    summary_list = summaries or []
    blocks = []
    for i, line in enumerate(event_map.values()):
        block = line
        summary = summary_list[i] if i < len(summary_list) and summary_list[i] else []
        if summary:
            block += "\n  **Brief:** " + summary[0]
            for extra in summary[1:]:
                block += "\n  " + extra
        if refs_list and refs_list[i]:
            changes = _changes_line(refs_list[i])
            if changes:
                block += "\n  " + changes
            related = _related_line(refs_list[i])
            if related:
                block += "\n  " + related
        blocks.append(block)
    return "\n\n".join(blocks) + "\n"


def llm_completions(payload):
    """POST a chat completion to the LLM gateway via curl.

    Uses curl instead of urllib because the gateway sits behind Cloudflare
    and rejects urllib's TLS fingerprint (HTTP 1010).
    """
    proc = subprocess.run(
        [
            "curl", "-sS", "-m", "30", "-X", "POST",
            f"{API_BASE}/chat/completions",
            "-H", f"Authorization: Bearer {os.environ['OPENCODE_API_KEY']}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ],
        capture_output=True,
        text=True,
        timeout=35,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"curl failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


FORBIDDEN_WORDS = [
    "foundation",
    "critical",
    "essential",
    "seamless",
    "establishing",
    "single source of truth",
    "robust",
    "streamline",
    "ensures",
    "empowers",
]

SYSTEM_PROMPT = (
    "You polish GitHub activity for a developer's README profile. "
    "For every ITEM keep the repo name, markdown links and the action verb "
    "exactly as-is. Then write a BRIEF of exactly 3 short scannable lines "
    "that explains the change and names its concrete artifacts. "
    "STRICT RULES: "
    "(1) GROUNDING — write a REAL brief. State only facts present in the "
    "CONTEXT; never invent features, fixes, motivations or code you cannot "
    "see. A 1-commit push is a small change, not a milestone. Write in "
    "natural, confident, human language — never clinical or robotic — while "
    "staying limited to the stated facts. "
    f"(2) NO BOILERPLATE — never use these words: {', '.join(FORBIDDEN_WORDS)}. "
    "If a brief could apply to any repo, rewrite it. "
    "(3) NAME THE ARTIFACTS — reference the concrete PR number, commit "
    "SHAs, issue numbers, branch names and tags from the CONTEXT so the "
    "reader can trace the change. Never use meta-labels like 'Artifacts:', "
    "'Summary:', 'Overview:' or 'Reference:' — fold the references directly "
    "into the sentences. "
    "(4) NO NEGATIVE CLAIMS — never assert \"zero commits\", \"no changes\" "
    "or similar absent facts. An empty or missing commits list only means "
    "details were not included; say so if relevant. "
    "(5) VARY — no two briefs may share their opening words or sentence "
    "structure; rotate the angle (what, why, technical detail). "
    "(6) SHORT — each line must fit one line and be scannable. "
    "Reply with JSON only: "
    '{"entries": [{"line": "...", "brief": ["...", "...", "..."]}, ...]}, '
    "one entry per ITEM."
)


def polish_lines(items):
    """Reword bullets and write a per-item brief via OpenCode Go.

    items: list of (bullet_line, context_text). Returns (lines, briefs)
    where briefs[i] is a list of 1-3 brief lines for lines[i]. Falls
    back to the original bullets and empty briefs on any failure; a
    single malformed entry degrades only that entry, not the whole list.
    """
    key = os.environ.get("OPENCODE_API_KEY")
    if not key:
        return [bullet for bullet, _ in items], [None] * len(items)
    try:
        numbered = "\n".join(
            f"ITEM {i + 1}: {bullet}\nCONTEXT {i + 1}: {context}"
            for i, (bullet, context) in enumerate(items)
        )
        payload = {
            "model": MODEL,
            "temperature": 0.5,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": numbered},
            ],
            "response_format": {"type": "json_object"},
        }
        data = llm_completions(payload)
        entries = json.loads(data["choices"][0]["message"]["content"]).get("entries")
        if not isinstance(entries, list):
            raise ValueError("entries not a list")
        entries_by_index = {
            i: entry for i, entry in enumerate(entries[: len(items)]) if isinstance(entry, dict)
        }
        lines = []
        briefs = []
        for i, (bullet, _) in enumerate(items):
            entry = entries_by_index.get(i)
            line = str(entry.get("line", "")).strip() if entry else ""
            brief = entry.get("brief") if entry else None
            if not line or not isinstance(brief, list) or not 1 <= len(brief) <= 3:
                lines.append(bullet)
                briefs.append([])
                continue
            lines.append(line if line.lstrip().startswith("-") else f"- {line}")
            briefs.append([str(b).strip() for b in brief])
        return lines, briefs
    except Exception as e:
        print(f"LLM polish unavailable, keeping fallback text: {e}")
        return [bullet for bullet, _ in items], [None] * len(items)


def render_pr_body(repos, blocks, today):
    """Build the Scribe-style body for the auto-update pull request."""
    body_lines = ["Auto-generated by update-readme workflow", ""]
    if blocks:
        noun = "entries" if len(repos) != 1 else "entry"
        body_lines.append("## What")
        body_lines.append(
            f"Updated the Recent Activity section in README.md with the latest "
            f"public activity \u2014 {len(repos)} {noun}: {', '.join(repos)}."
        )
        body_lines.append("")
        body_lines.append("## Why")
        body_lines.append(
            "Keeps the profile's Recent Activity current so visitors see live "
            "work at a glance, grounded in real events with PR/commit and "
            "linked-issue references."
        )
        body_lines.append("")
        body_lines.append("## How to test")
        body_lines.append("1. Diff this PR and confirm the briefs are factual and the refs link correctly.")
        body_lines.append("2. Re-run the Update README workflow to refresh the section tomorrow.")
        body_lines.append("")
        body_lines.append("## Recent activity")
        body_lines.extend(blocks.rstrip("\n").split("\n"))
    else:
        body_lines.append("## What")
        body_lines.append(
            "No qualifying public events found; only the Last updated footer was bumped."
        )
        body_lines.append("")
        body_lines.append("## Why")
        body_lines.append(
            "Keeps the date footer honest on days with no qualifying activity."
        )
    body_lines.append(f"\nLast updated bumped to {today}.")
    return body_lines


def set_output(value):
    """Write step output for GitHub Actions and print to stdout."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"changed={value}\n")
    print(f"changed={value}")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set, skipping.")
        set_output(0)
        return

    try:
        events = fetch_events(token)
    except Exception as e:
        print(f"Failed to fetch events: {e}")
        set_output(0)
        return
    if events is None:
        print("Failed to fetch events: API returned an error, leaving README untouched.")
        set_output(0)
        return

    event_map = parse_events(events, token)
    summaries = []
    refs_list = None
    if event_map:
        entries = list(event_map.values())
        lines, summaries = polish_lines([(b, c) for b, c, _ in entries])
        refs_list = [r for _, _, r in entries]
        event_map = dict(zip(event_map.keys(), lines))

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    m = ACTIVITY_RE.search(content)
    if not m:
        print("Could not find Recent Activity section in README.md")
        set_output(0)
        return

    new_rows = build_activity_lines(event_map, summaries, refs_list) if event_map else "\n"
    old_activity = m.group(1).strip()
    old_date = re.search(r"Last updated: (.+)", content)
    old_date_str = old_date.group(1) if old_date else ""

    today = format_date(datetime.now(timezone.utc).isoformat())
    date_changed = old_date_str != today
    activity_changed = old_activity != new_rows.strip()

    if not date_changed and not activity_changed:
        print("No changes detected — date and activity are current.")
        set_output(0)
        return

    new_content = content[: m.start(1)] + new_rows + content[m.end(1) :]
    new_content = re.sub(
        r"Last updated: .+", f"Last updated: {today}", new_content
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    repos = list(event_map.keys())
    body_lines = render_pr_body(repos, new_rows, today)

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:


        f.write("\n".join(body_lines) + "\n")

    change_desc = ", ".join(repos) if repos else "date bump only"
    print(f"README updated. Changes: {change_desc}")
    set_output(1)


if __name__ == "__main__":
    main()
