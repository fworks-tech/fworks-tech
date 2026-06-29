#!/usr/bin/env python3
"""Auto-update the Recent Activity table in README.md.

Fetches the 6 most recently pushed non-fork, non-archived repos from the
GitHub API and regenerates the table block. Curated descriptions live in
REPO_DESCRIPTIONS at the top of this file; unmapped repos fall back to the
GitHub description (truncated).

Outputs ``changed=1`` or ``changed=0`` via $GITHUB_OUTPUT for the workflow.
"""

import json
import os
import re
import urllib.request
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Curated short descriptions for the Recent Activity table.
# Edit this dict to tweak the wording for a specific repo.
# Repos not listed here fall back to the GitHub ``description`` field.
# ---------------------------------------------------------------------------
REPO_DESCRIPTIONS = {
    "agenthood": "Society of AI agents — SKILL.md open standard · TS framework · VS Code extension · Academy",
    "flabs.tech": "Next.js 16 portfolio — Vitest, Playwright E2E, visual snapshots, CI",
    "agenthood-site": "Agenthood landing page — agent-agnostic SKILL.md skills, SEO-optimized, Studio playground",
    "logroute": "FMCSA ELD logbook & route planner — Django + React, live at logroute-app.vercel.app",
    "Jupyter-Crypto-Wizard": "Streamlit crypto dashboard — KPIs, trends, risk panels, alerts, news",
    "ApolloDroid": "100% Python voice assistant for Android powered by Claude AI",
    "verihire": "GenAI / RAG recruiter tool — Chroma vector search, Claude AI",
    "pagination-with-ssg": "Next.js pagination with static site generation",
    "fabionismos-blog": "Next.js + Markdown blog deployed on Vercel",
    "devices-manager": "Full-stack device management demo",
    "blockchain-explorer": "Blockchain explorer UI experiments (React)",
    "fashionista": "E-commerce storefront — React, Redux, Sass",
}

ORG = "fworks-tech"
TOP_N = 6
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
README_PATH = os.path.join(REPO_ROOT, "README.md")
SUMMARY_PATH = os.path.join(SCRIPT_DIR, "update_summary.txt")

TABLE_RE = re.compile(
    r"(\| Repository \| Description \|\n\|---\|---\|\n)"
    r"((?:\|.*\n)*)"
)


def fetch_repos(token):
    """Fetch all non-fork, non-archived repos for the user/org."""
    url = f"https://api.github.com/users/{ORG}/repos?per_page=100&type=owner"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "update-readme-script")
    with urllib.request.urlopen(req) as resp:
        repos = json.loads(resp.read())
    return [r for r in repos if not r["archived"] and not r["fork"] and r["name"] != ORG]


def format_date(iso_ts):
    """Convert ISO 8601 timestamp to 'Mon D, YYYY' (no leading zero)."""
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def get_description(repo):
    """Curated description or fallback to GitHub description (truncated)."""
    name = repo["name"]
    if name in REPO_DESCRIPTIONS:
        return REPO_DESCRIPTIONS[name]
    desc = (repo.get("description") or "").strip()
    if len(desc) > 80:
        desc = desc[:77].rstrip() + "..."
    return desc or name


def build_table(top_repos):
    """Build the markdown table rows."""
    rows = []
    for repo in top_repos:
        name = repo["name"]
        url = repo["html_url"]
        desc = get_description(repo)
        rows.append(f"| [{name}]({url}) | {desc} |")
    return "\n".join(rows) + "\n"


def parse_old_rows(content):
    """Extract ordered list of repo names from existing table."""
    m = TABLE_RE.search(content)
    if not m:
        return []
    name_re = re.compile(r"\[([^\]]+)\]")
    names = []
    for line in m.group(2).splitlines():
        nm = name_re.search(line)
        if nm:
            names.append(nm.group(1))
    return names


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

    repos = fetch_repos(token)
    repos.sort(key=lambda r: r["pushed_at"], reverse=True)
    top = repos[:TOP_N]

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    old_names = parse_old_rows(content)
    new_names = [r["name"] for r in top]
    new_rows = build_table(top)

    m = TABLE_RE.search(content)
    if not m:
        print("Could not find table block in README.md")
        set_output(0)
        return

    old_rows = m.group(2)
    changed = old_rows.strip() != new_rows.strip()

    if not changed:
        print("No changes detected — table is up to date.")
        set_output(0)
        return

    new_content = content[: m.start(2)] + new_rows + content[m.end(2) :]

    today = format_date(datetime.now(timezone.utc).isoformat())
    new_content = re.sub(
        r"Last updated: .+", f"Last updated: {today}", new_content
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    added = [n for n in new_names if n not in old_names]
    removed = [n for n in old_names if n not in new_names]
    moved = [
        (old_names.index(n), new_names.index(n), n)
        for n in new_names
        if n in old_names and old_names.index(n) != new_names.index(n)
    ]

    summary_lines = ["Auto-generated by update-readme workflow", ""]
    if added:
        summary_lines.append("Added:")
        for n in added:
            summary_lines.append(f"- {n} entered top {TOP_N}")
    if removed:
        summary_lines.append("Removed:")
        for n in removed:
            summary_lines.append(f"- {n} dropped out of top {TOP_N}")
    if moved:
        summary_lines.append("Reordered:")
        for old_i, new_i, n in moved:
            summary_lines.append(f"- {n}: #{old_i + 1} -> #{new_i + 1}")
    summary_lines.append(f"\nLast updated bumped to {today}.")

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines) + "\n")

    print(f"Table updated. Changes: {', '.join(added + removed) or 'reorder only'}")
    set_output(1)


if __name__ == "__main__":
    main()
