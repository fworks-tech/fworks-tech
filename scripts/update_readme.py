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
    """Extract one human-readable line per repo from recent events.

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
        seen[repo_short] = describe_event(event, repo_short, repo_full)
        if len(seen) >= TOP_N:
            break
    return seen


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


def build_activity_lines(event_map, summary):
    """Build the markdown block: summary quote lines followed by bullets."""
    quote = "\n".join(f"> {line}" for line in summary)
    return f"{quote}\n\n" + "\n".join(event_map.values()) + "\n"


def default_summary(lines):
    """Deterministic 3-line summary used when the LLM is unavailable."""
    count = len(lines)
    noun = "repos" if count != 1 else "repo"
    return [
        f"\u26A1 {count} {noun} just moved in the fworks-tech workshop.",
        "Fresh branches, commits and PRs \u2014 all public, all recent.",
        "Explore the repos below to see what is shipping today.",
    ]


def polish_lines(lines):
    """Reword bullets and write a short summary via OpenCode Go.

    Returns (summary, lines) where summary is a list of 2-3 quote lines.
    Falls back to the deterministic summary and the original bullets on
    any failure.
    """
    key = os.environ.get("OPENCODE_API_KEY")
    if not key:
        return default_summary(lines), lines
    try:
        payload = {
            "model": MODEL,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You summarize GitHub activity for a developer's README. "
                        "Keep every repo name and markdown link in the bullets "
                        "exactly as-is, one line per bullet, concise and slightly "
                        "more engaging. Write a short 2-3 line summary in plain "
                        "prose (one emoji allowed, no markdown headings) that "
                        "explains the activity and catches a recruiter's eye; each "
                        "line becomes a blockquote line and must stand on its own. "
                        "Reply with JSON only: "
                        '{"summary": ["...", "...", "..."], "lines": ["...", "..."]}.'
                    ),
                },
                {"role": "user", "content": "\n".join(lines)},
            ],
            "response_format": {"type": "json_object"},
        }
        req = urllib.request.Request(
            f"{API_BASE}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        result = json.loads(data["choices"][0]["message"]["content"])
        items = result.get("lines")
        summary = result.get("summary")
        if (
            isinstance(items, list)
            and len(items) == len(lines)
            and isinstance(summary, list)
            and 2 <= len(summary) <= 3
        ):
            polished = [
                item if str(item).lstrip().startswith("-") else f"- {item}"
                for item in items
            ]
            return [str(line).strip() for line in summary], polished
    except Exception as e:
        print(f"LLM polish unavailable, keeping fallback text: {e}")
    return default_summary(lines), lines


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
    summary = None
    if event_map:
        summary, polished = polish_lines(list(event_map.values()))
        event_map = dict(zip(event_map.keys(), polished))

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    m = ACTIVITY_RE.search(content)
    if not m:
        print("Could not find Recent Activity section in README.md")
        set_output(0)
        return

    new_rows = build_activity_lines(event_map, summary) if event_map else "\n"
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
        body_lines.append("Summary:")
        body_lines.extend(summary)
        body_lines.append("Recent activity:")
        for line in event_map.values():
            body_lines.append(line)
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
