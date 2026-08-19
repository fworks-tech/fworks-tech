#!/usr/bin/env python3
"""Auto-update the Recent Activity section in README.md.

Fetches recent public events from the GitHub Events API (pushes, PRs,
issues, releases) and regenerates the bullet-point list under the
``## Recent Activity`` heading. Bullets link to repos, commits, PRs and
issues, show authors and relative age, and can be reworded via OpenCode
Go when OPENCODE_API_KEY is set. Always bumps the "Last updated" footer
so the workflow always has a diff to commit and opens a PR every day.

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


def fetch_events(token):
    """Fetch recent public events for the user."""
    url = f"https://api.github.com/users/{ORG}/events/public?per_page=100"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "update-readme-script")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


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


def parse_events(events):
    """Extract one (bullet, context) pair per repo from recent events.

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
        seen[repo_short] = (
            describe_event(event, repo_short, repo_full),
            event_context(event),
        )
        if len(seen) >= TOP_N:
            break
    return seen


def event_context(event):
    """Structured one-line digest of an event, used for the LLM prompt."""
    etype = event.get("type", "")
    payload = event.get("payload", {})

    if etype == "PushEvent":
        commits = payload.get("commits", [])
        ref = payload.get("ref", "").split("/")[-1]
        if len(commits) == 1:
            msg = commits[0].get("message", "").split("\n")[0][:80]
            return f"pushed 1 commit to branch {ref}: {msg}"
        return f"pushed {len(commits)} commits to branch {ref}"

    if etype == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        verb = "merged" if pr.get("merged_at") else payload.get("action", "opened")
        title = pr.get("title", "")[:80]
        author = pr.get("user", {}).get("login", "")
        return f"{verb} PR #{pr.get('number', '')}: {title} by @{author}"

    if etype == "IssuesEvent":
        issue = payload.get("issue", {})
        labels = [label.get("name") for label in issue.get("labels", [])][:2]
        label_part = f" labels: {', '.join(labels)}" if labels else ""
        author = issue.get("user", {}).get("login", "")
        return (
            f"{payload.get('action', 'opened')} issue #{issue.get('number', '')}: "
            f"{issue.get('title', '')[:80]} by @{author}{label_part}"
        )

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


def build_activity_lines(event_map, summaries):
    """Build the bullet list, each bullet followed by an indented summary."""
    blocks = []
    for i, line in enumerate(event_map.values()):
        block = line
        if summaries and summaries[i]:
            block += "\n  " + "\n  ".join(summaries[i])
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
    "exactly as-is. Then write a short summary of exactly 2 lines to place "
    "under the bullet. STRICT RULES: "
    "(1) GROUNDING — write a REAL summary. State only facts present in the "
    "CONTEXT; never invent features, fixes, motivations or code you cannot "
    "see. A 1-commit push is a small change, not a milestone. Write in "
    "natural, confident, human language — never clinical or robotic — while "
    "staying limited to the stated facts. "
    f"(2) NO BOILERPLATE — never use these words: {', '.join(FORBIDDEN_WORDS)}. "
    "If a summary could apply to any repo, rewrite it. "
    "(3) BE SPECIFIC — name the concrete artifact: repo, branch, PR number, "
    "tag or commit subject. "
    "(4) VARY — no two summaries may share their opening words or sentence "
    "structure; rotate the angle (what, why, technical detail). "
    "(5) SHORT — each line must fit one line and be scannable. "
    "Reply with JSON only: "
    '{"entries": [{"line": "...", "summary": ["...", "..."]}, ...]}, '
    "one entry per ITEM."
)


def polish_lines(items):
    """Reword bullets and write a per-item quick summary via OpenCode Go.

    items: list of (bullet_line, context_text). Returns (lines, summaries)
    where summaries[i] is a list of 1-2 summary lines for lines[i]. Falls
    back to the original bullets and empty summaries on any failure; a
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
        summaries = []
        for i, (bullet, _) in enumerate(items):
            entry = entries_by_index.get(i)
            line = str(entry.get("line", "")).strip() if entry else ""
            summary = entry.get("summary") if entry else None
            if not line or not isinstance(summary, list) or not 1 <= len(summary) <= 2:
                lines.append(bullet)
                summaries.append([])
                continue
            lines.append(line if line.lstrip().startswith("-") else f"- {line}")
            summaries.append([str(s).strip() for s in summary])
        return lines, summaries
    except Exception as e:
        print(f"LLM polish unavailable, keeping fallback text: {e}")
        return [bullet for bullet, _ in items], [None] * len(items)


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

    event_map = parse_events(events)
    summaries = []
    if event_map:
        items = list(event_map.values())
        lines, summaries = polish_lines(items)
        event_map = dict(zip(event_map.keys(), lines))

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    m = ACTIVITY_RE.search(content)
    if not m:
        print("Could not find Recent Activity section in README.md")
        set_output(0)
        return

    new_rows = build_activity_lines(event_map, summaries) if event_map else "\n"
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
    body_lines = ["Auto-generated by update-readme workflow", ""]
    if event_map:
        body_lines.append("Recent activity:")
        for i, line in enumerate(event_map.values()):
            body_lines.append(line)
            if summaries[i]:
                body_lines.extend("  " + s for s in summaries[i])
    else:
        body_lines.append("No contribution events found.")
    body_lines.append(f"\nLast updated bumped to {today}.")

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(body_lines) + "\n")

    change_desc = ", ".join(repos) if repos else "date bump only"
    print(f"README updated. Changes: {change_desc}")
    set_output(1)


if __name__ == "__main__":
    main()
