#!/usr/bin/env python3
"""Auto-update the Recent Activity section in README.md.

Fetches recent public events from the GitHub Events API (pushes, PRs,
issues, releases) and regenerates the bullet-point list under the
``## Recent Activity`` heading. Always bumps the "Last updated" footer
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
TOP_N = 6
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


def parse_events(events):
    """Extract one human-readable line per repo from recent events.

    Deduplicates by repo, keeping only the most recent event for each.
    Skips noise events (WatchEvent, ForkEvent, MemberEvent).
    """
    skip_types = {"WatchEvent", "ForkEvent", "MemberEvent", "GollumEvent"}
    seen = {}
    for event in events:
        repo_name = event.get("repo", {}).get("name", "").split("/")[-1]
        if not repo_name or repo_name == ORG:
            continue
        if event.get("type") in skip_types:
            continue
        if repo_name in seen:
            continue
        seen[repo_name] = describe_event(event)
        if len(seen) >= TOP_N:
            break
    return seen


def describe_event(event):
    """Return a single bullet-point line describing a GitHub event."""
    repo = event.get("repo", {}).get("name", "").split("/")[-1]
    etype = event.get("type", "")
    payload = event.get("payload", {})

    if etype == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        action = payload.get("action", "opened")
        title = pr.get("title", "update")[:60]
        number = pr.get("number", "")
        return f"**{repo}** — {action} PR #{number}: {title}"

    if etype == "IssuesEvent":
        issue = payload.get("issue", {})
        action = payload.get("action", "opened")
        title = issue.get("title", "issue")[:60]
        number = issue.get("number", "")
        return f"**{repo}** — {action} issue #{number}: {title}"

    if etype == "PushEvent":
        commits = payload.get("commits", [])
        ref = payload.get("ref", "").split("/")[-1]
        if len(commits) == 1:
            msg = commits[0].get("message", "").split("\n")[0][:60]
            return f"**{repo}** — pushed to {ref}: {msg}"
        if len(commits) > 1:
            return f"**{repo}** — pushed {len(commits)} commits to {ref}"
        return f"**{repo}** — pushed to {ref}"

    if etype == "ReleaseEvent":
        release = payload.get("release", {})
        tag = release.get("tag_name", "release")
        action = payload.get("action", "published")
        return f"**{repo}** — {action} release {tag}"

    if etype == "IssueCommentEvent":
        issue = payload.get("issue", {})
        number = issue.get("number", "")
        return f"**{repo}** — commented on issue #{number}"

    if etype == "PullRequestReviewEvent":
        pr = payload.get("pull_request", {})
        number = pr.get("number", "")
        return f"**{repo}** — reviewed PR #{number}"

    if etype == "CreateEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        return f"**{repo}** — created {ref_type} {ref}"

    if etype == "DeleteEvent":
        ref_type = payload.get("ref_type", "resource")
        ref = payload.get("ref", "")
        return f"**{repo}** — deleted {ref_type} {ref}"

    return f"**{repo}** — activity"


def build_activity_lines(event_map):
    """Build the markdown bullet list."""
    return "\n".join(f"- {line}" for line in event_map.values()) + "\n"


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

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    m = ACTIVITY_RE.search(content)
    if not m:
        print("Could not find Recent Activity section in README.md")
        set_output(0)
        return

    new_rows = build_activity_lines(event_map) if event_map else "\n"
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
    summary_lines = ["Auto-generated by update-readme workflow", ""]
    if event_map:
        summary_lines.append("Recent activity:")
        for repo, line in event_map.items():
            summary_lines.append(f"- {line}")
    else:
        summary_lines.append("No contribution events found.")
    summary_lines.append(f"\nLast updated bumped to {today}.")

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines) + "\n")

    change_desc = ", ".join(repos) if repos else "date bump only"
    print(f"README updated. Changes: {change_desc}")
    set_output(1)


if __name__ == "__main__":
    main()
