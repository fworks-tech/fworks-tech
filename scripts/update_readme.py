#!/usr/bin/env python3
"""Auto-update Featured Projects dates and Recent Activity in README.md.

Discovers active repos from the org's public events, collects the
substantive signals from the last two weeks (merged PRs, releases and
open PRs, excluding bot and dependency noise), and asks an LLM to write
one short, reader-friendly entry per repo. The LLM only picks signal
ids; every link is rendered from GitHub API data, so an unavailable
model degrades to a deterministic description-plus-titles fallback
instead of breaking the section.

Outputs ``changed=1`` via $GITHUB_OUTPUT when either generated section
changes; the workflow reuses one pull request across runs.
"""

import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timedelta, timezone

ORG = "fworks-tech"
TOP_N = 3
CANDIDATE_N = 6
WINDOW_DAYS = 14
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
PROJECT_ROW_RE = re.compile(
    r"^\| \[(?P<repo>[^\]]+)\]\(https://github\.com/fworks-tech/[^)]+\)"
    r" \| .*? \| (?P<date>\d{2}/\d{2}/\d{4}) \|$",
    re.MULTILINE,
)

API_BASE = os.environ.get(
    "OPENCODE_README_BASE_URL", "https://opencode.ai/zen/v1"
)
MODEL = os.environ.get("OPENCODE_README_MODEL", "deepseek-v4.1-flash")
FALLBACK_MODELS = ["qwen3.8-flash"]
MODELS = [MODEL] + [m for m in FALLBACK_MODELS if m != MODEL]
SESSION_ID = os.environ.get("OPENCODE_SESSION_ID", "agenthood-readme-briefs")


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
            remaining = resp.headers.get("X-RateLimit-Remaining")
            if remaining is not None and int(remaining) < 5:
                print(f"GitHub API rate limit low: {remaining} remaining ({url})")
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


PRS_PER_REPO = 20


def fetch_recent_merged_prs(repo_full, token, limit=PRS_PER_REPO):
    """Fetch the last N PRs merged into main for a repo.

    Returns a list of PR dicts with number, title, body, merged_at,
    user, head, base. Empty list when no merged PRs or on failure.
    """
    if not token:
        return []
    url = (
        f"https://api.github.com/repos/{repo_full}/pulls"
        f"?state=closed&base=main&sort=updated&direction=desc&per_page={limit}"
    )
    data = api_get(url, token)
    if not isinstance(data, list):
        return []
    merged = []
    for pr in data:
        if not pr.get("merged_at"):
            continue
        merged.append({
            "number": pr.get("number"),
            "title": pr.get("title", ""),
            "body": pr.get("body", "") or "",
            "merged_at": pr.get("merged_at", ""),
            "user": pr.get("user", {}).get("login", ""),
            "head": pr.get("head", {}).get("ref", ""),
            "base": pr.get("base", {}).get("ref", ""),
        })
    return merged


def fetch_repo_meta(repo_full, token):
    """Short repo description and topics, used to ground the prose."""
    data = api_get(f"https://api.github.com/repos/{repo_full}", token)
    if not isinstance(data, dict):
        return {}
    return {
        "description": data.get("description") or "",
        "topics": data.get("topics") or [],
    }


def fetch_latest_commit_date(repo_full, token):
    """Latest default-branch commit date, or None when unavailable."""
    if not token:
        return None
    data = api_get(
        f"https://api.github.com/repos/{repo_full}/commits?per_page=1", token
    )
    if not isinstance(data, list) or not data:
        return None
    commit = data[0].get("commit") if isinstance(data[0], dict) else None
    if not isinstance(commit, dict):
        return None
    committer = commit.get("committer")
    if not isinstance(committer, dict):
        return None
    return committer.get("date") or None


def format_short_date(iso_ts):
    """Convert ISO 8601 timestamp to MM/DD/YYYY."""
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    return dt.strftime("%m/%d/%Y")


def update_project_dates(content, token):
    """Refresh Featured Projects date cells and return changed repo names."""
    matches = list(PROJECT_ROW_RE.finditer(content))
    if not matches:
        raise RuntimeError("Could not find Featured Projects rows in README.md")

    updates = []
    missing = []
    for match in matches:
        repo = match.group("repo")
        iso_ts = fetch_latest_commit_date(f"{ORG}/{repo}", token)
        if not iso_ts:
            missing.append(repo)
            continue
        updates.append((match.span("date"), format_short_date(iso_ts), repo))

    if missing:
        raise RuntimeError(
            "Could not fetch Featured Projects update dates: " + ", ".join(missing)
        )

    changed = [
        repo
        for match, (_, date, repo) in zip(matches, updates)
        if match.group("date") != date
    ]
    for (start, end), date, _ in reversed(updates):
        content = content[:start] + date + content[end:]
    return content, changed


def fetch_recent_releases(repo_full, token, limit=5):
    """Releases for a repo, newest first."""
    if not token:
        return []
    data = api_get(
        f"https://api.github.com/repos/{repo_full}/releases?per_page={limit}",
        token,
    )
    if not isinstance(data, list):
        return []
    return [
        {
            "tag": rel.get("tag_name") or "",
            "name": rel.get("name") or "",
            "body": rel.get("body") or "",
            "published_at": rel.get("published_at") or "",
        }
        for rel in data
    ]


def fetch_open_prs(repo_full, token, limit=10):
    """Open pull requests for a repo, most recently updated first."""
    if not token:
        return []
    url = (
        f"https://api.github.com/repos/{repo_full}/pulls"
        f"?state=open&sort=updated&direction=desc&per_page={limit}"
    )
    data = api_get(url, token)
    if not isinstance(data, list):
        return []
    return [
        {
            "number": pr.get("number"),
            "title": pr.get("title", ""),
            "body": pr.get("body") or "",
            "updated_at": pr.get("updated_at", ""),
            "user": (pr.get("user") or {}).get("login", ""),
            "draft": bool(pr.get("draft")),
        }
        for pr in data
    ]


def within_window(iso_ts, days=WINDOW_DAYS):
    """True when an ISO timestamp falls inside the activity window."""
    if not iso_ts:
        return False
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    return datetime.now(timezone.utc) - dt <= timedelta(days=days)


DEPENDENCY_BOTS = {"dependabot[bot]", "renovate[bot]"}
AUTOMATION_BOTS = {"github-actions[bot]", "app/github-actions"}
NOISE_TITLE_RE = re.compile(
    r"^(?:chore\(deps[^)]*\)|chore:\s*bump|build\(deps[^)]*\))", re.IGNORECASE
)


def is_noise_pr(pr, allow_automation=False):
    """Bot-authored or dependency-bump PRs are not reader-worthy.

    Open PRs allow automation-authored work: a draft release or a catalog
    refresh is meaningful activity, unlike a dependency bump.
    """
    if (pr.get("user") or "") in DEPENDENCY_BOTS:
        return True
    if not allow_automation and (pr.get("user") or "") in AUTOMATION_BOTS:
        return True
    return bool(NOISE_TITLE_RE.match(pr.get("title", "")))


def clean_pr_title(title):
    """Drop the conventional-commit prefix from a PR title."""
    text = re.sub(
        r"^[a-z]+(?:\([^)]*\))?!?:\s*", "", (title or "").strip(), flags=re.IGNORECASE
    )
    text = clean_text(text).strip()
    if text[:1].islower() and not re.match(r"^v\d", text):
        text = text[:1].upper() + text[1:]
    return text


def first_sentence(text, limit=120):
    """First sentence of a description, trimmed at a word boundary."""
    text = re.sub(r"\s+", " ", clean_text(text or "")).strip()
    if not text:
        return ""
    match = re.match(r"(.+?[.!?])(?:\s|$)", text)
    sentence = match.group(1) if match else text
    if len(sentence) > limit:
        sentence = sentence[:limit].rsplit(" ", 1)[0].rstrip(" ,;:-") + "\u2026"
    return sentence


def excerpt(text, limit):
    """Plain-text excerpt for the LLM context."""
    text = re.sub(r"```.*?```", " ", text or "", flags=re.DOTALL)
    text = re.sub(r"\s+", " ", clean_text(text)).strip()
    return text[:limit].rstrip()


def _signal(kind, title, url, date, context, weight):
    return {
        "kind": kind,
        "title": title,
        "url": url,
        "date": date,
        "context": context,
        "weight": weight,
    }


def collect_signals(repo_full, token):
    """Substantive signals for one repo, newest first, with stable ids.

    Releases score highest because they mark a finished milestone; merged
    PRs and open PRs carry the rest of the story. Bot and dependency PRs
    are dropped so a quiet week does not turn into a changelog of bumps.
    """
    signals = []
    base = repo_url(repo_full)

    releases = 0
    for rel in fetch_recent_releases(repo_full, token):
        if releases >= 2:
            break
        if not within_window(rel["published_at"]):
            continue
        title = rel["tag"] or rel["name"] or "release"
        detail = rel["name"] or excerpt(rel["body"], 240)
        signals.append(
            _signal(
                "release",
                title,
                f"{base}/releases/tag/{rel['tag']}" if rel["tag"] else base,
                rel["published_at"],
                f"release {title} published {rel['published_at'][:10]}"
                + (f": {detail}" if detail else ""),
                3,
            )
        )
        releases += 1

    merged = 0
    for pr in fetch_recent_merged_prs(repo_full, token):
        if merged >= 4:
            break
        if not pr.get("merged_at") or not within_window(pr["merged_at"]):
            continue
        if is_noise_pr(pr):
            continue
        signals.append(
            _signal(
                "pr",
                clean_pr_title(pr["title"]) or f"PR #{pr['number']}",
                f"{base}/pull/{pr['number']}",
                pr["merged_at"],
                f"merged pull request #{pr['number']} on {pr['merged_at'][:10]}: "
                f"{pr['title']}"
                + (f" - {excerpt(pr['body'], 400)}" if pr.get("body") else ""),
                2,
            )
        )
        merged += 1

    opened = 0
    for pr in fetch_open_prs(repo_full, token):
        if opened >= 3:
            break
        if not within_window(pr["updated_at"]) or is_noise_pr(
            pr, allow_automation=True
        ):
            continue
        title = clean_pr_title(pr["title"]) or f"PR #{pr['number']}"
        if pr["draft"]:
            title += " (draft)"
        signals.append(
            _signal(
                "open_pr",
                title,
                f"{base}/pull/{pr['number']}",
                pr["updated_at"],
                f"open pull request #{pr['number']} updated {pr['updated_at'][:10]}: "
                f"{pr['title']}"
                + (" (draft)" if pr["draft"] else "")
                + (f" - {excerpt(pr['body'], 400)}" if pr.get("body") else ""),
                2,
            )
        )
        opened += 1

    signals.sort(key=lambda signal: signal["date"], reverse=True)
    for i, signal in enumerate(signals):
        signal["id"] = f"S{i + 1}"
    return signals


def discover_repos(events):
    """Repos named in the public events, most recent first, deduped."""
    repos = []
    seen = set()
    for event in events:
        repo_full = event.get("repo", {}).get("name", "")
        repo_short = repo_full.split("/")[-1]
        if not repo_full.startswith(f"{ORG}/"):
            continue
        if not repo_short or repo_short == ORG or repo_full in seen:
            continue
        seen.add(repo_full)
        repos.append((repo_short, repo_full))
        if len(repos) >= CANDIDATE_N:
            break
    return repos


def build_items(events, token=None):
    """Select the most substantive repos and assemble their LLM items.

    Repos with no signals are dropped; the rest are ranked by signal
    weight and recency, capped at TOP_N, then shown newest first.
    """
    items = []
    for repo_short, repo_full in discover_repos(events):
        signals = collect_signals(repo_full, token)
        if not signals:
            continue
        meta = fetch_repo_meta(repo_full, token)
        items.append(
            {
                "repo": repo_short,
                "full": repo_full,
                "url": repo_url(repo_full),
                "description": meta.get("description", ""),
                "topics": meta.get("topics", []),
                "signals": signals,
                "latest": max(signal["date"] for signal in signals),
                "score": sum(signal["weight"] for signal in signals),
            }
        )
    items.sort(key=lambda item: (item["score"], item["latest"]), reverse=True)
    items = items[:TOP_N]
    items.sort(key=lambda item: item["latest"], reverse=True)
    return items


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


def sanitize_prose(text):
    """Strip markdown and URLs from LLM prose before it reaches the README."""
    text = clean_text(str(text or ""))
    text = re.sub(r"https?://\S+", "", text, flags=re.IGNORECASE)
    text = text.replace("<", "").replace(">", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text.lstrip("-*# ").strip()


def fallback_entry(item):
    """Deterministic entry used when the LLM is unavailable or rejected."""
    headline = first_sentence(item.get("description", "")) or "Recent work"
    signals = [s for s in item["signals"] if s["kind"] in ("pr", "release")]
    if not signals:
        signals = item["signals"]
    return {
        "headline": headline,
        "body": "",
        "links": [s["id"] for s in signals[:2]],
    }


def _links_line(item, entry):
    by_id = {s["id"]: s for s in item["signals"]}
    links = [by_id[link] for link in (entry.get("links") or []) if link in by_id]
    if not links:
        return ""
    return " \u00B7 ".join(f"[{s['title']}]({s['url']})" for s in links)


def render_activity(items, entries):
    """Render the section body from selected items and LLM entries."""
    entries = list(entries or [])
    entries.extend([None] * (len(items) - len(entries)))
    blocks = []
    for item, entry in zip(items, entries):
        entry = entry or fallback_entry(item)
        block = f"- [**{item['repo']}**]({item['url']}) \u2014 {entry['headline']}"
        if entry.get("body"):
            block += f"\n  {entry['body']}"
        links = _links_line(item, entry)
        if links:
            block += f"\n  {links}"
        blocks.append(block)
    return "\n\n".join(blocks) + "\n" if blocks else ""


def llm_completions(payload):
    """POST a chat completion to the LLM gateway via curl.

    Uses curl instead of urllib because the gateway sits behind Cloudflare
    and rejects urllib's TLS fingerprint (HTTP 1010).
    """
    proc = subprocess.run(
        [
            "curl", "-sS", "-m", "120", "-X", "POST",
            f"{API_BASE}/chat/completions",
            "-H", f"Authorization: Bearer {os.environ['OPENCODE_API_KEY']}",
            "-H", "Content-Type: application/json",
            "-H", f"x-opencode-session: {SESSION_ID}",
            "-d", json.dumps(payload),
        ],
        capture_output=True,
        text=True,
        timeout=130,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"curl failed: {proc.stderr.strip()}")
    data = json.loads(proc.stdout)
    if "choices" not in data:
        raise RuntimeError(f"LLM response missing 'choices': {proc.stdout[:300]}")
    return data


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

TECHNICAL_WORDS = [
    "lambda",
    "endpoint",
    "api",
    "daemon",
    "schema",
    "migration",
    "middleware",
    "hook",
    "flag",
    "config",
    "cache",
    "tick",
    "snapshot",
    "refactor",
    "linter",
    "dependency",
    "branch",
    "ci",
    "tests",
    "file",
]

SYSTEM_PROMPT = (
    "You write the Recent Activity section of a solo developer's GitHub "
    "profile README. Readers are visitors: smart people who are not in the "
    "codebase. They want a quick, pleasant sense of what is being built, in "
    "plain language. Translate internals into what the software now does for "
    "its user.\n\n"
    "For every ITEM return:\n"
    "- headline: one sentence, at most 90 characters, on what is happening in "
    "the project now. No PR or issue numbers, no hashes, no conventional "
    "commit prefixes, no file paths, no repo name repetition.\n"
    "- body: 2 short sentences, at most 320 characters, saying what changed "
    "and why a reader would care. Mention an in-progress thread or design "
    "choice when the signals show one. Do not over-explain.\n"
    "- links: 0 to 2 signal ids copied exactly from the ITEM (for example "
    "\"S1\"), in the order referenced. Never invent an id.\n\n"
    "RULES:\n"
    "- Ground every claim in the description or signals. Never infer "
    "motivation, users, metrics, or outcomes.\n"
    "- If the signals are routine maintenance only, say so in one sentence; "
    "never inflate dependency bumps.\n"
    "- When a release has no notes, use the work visible in open or merged "
    "PRs; never mention missing information or apologize for it.\n"
    "- Voice: first person singular, used sparingly. Calm and concrete. No "
    "'we', no marketing adjectives, no exclamation marks, and none of: "
    + ", ".join(FORBIDDEN_WORDS)
    + ".\n"
    "- Do not use technical implementation words: "
    + ", ".join(TECHNICAL_WORDS)
    + ". Product-domain names (MCP, agent, AI) are allowed when they are the "
    "point.\n"
    "- No emoji, markdown links, headings, bullets, dates, or relative times "
    "in the text. Vary headline openings.\n\n"
    "STYLE EXAMPLE (invented project, do not copy facts):\n"
    "technical: 'The worker now batches Redis writes and retries safely.'\n"
    "good body: 'Saved games stop disappearing when the network drops: "
    "progress is written in small batches, so a bad connection costs a few "
    "seconds instead of the session.'\n\n"
    "Reply with JSON only: "
    '{"entries": [{"index": 0, "headline": "...", "body": "...", '
    '"links": ["S1"]}, ...]}, one entry per ITEM. The index is the ITEM '
    "number minus 1."
)

HEADLINE_LIMIT = 120
BODY_LIMIT = 420
ISSUE_RE = re.compile(r"#\s*\d+")
HASH_RE = re.compile(r"\b(?=[a-f0-9]*\d)[a-f0-9]{7,40}\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://", re.IGNORECASE)
WE_RE = re.compile(r"\bwe\b", re.IGNORECASE)


def item_context(item):
    """LLM-facing digest: description, topics and numbered signals."""
    lines = [
        f"PROJECT: {item['repo']}",
        f"what it is: {item.get('description', '')[:300]}",
    ]
    if item.get("topics"):
        lines.append("topics: " + ", ".join(item["topics"][:6]))
    for signal in item["signals"]:
        lines.append(f"[{signal['id']}] {signal['context']}")
    return "\n".join(lines)


def validate_entry(item, entry):
    """Return the reasons an LLM entry cannot be published."""
    if not entry:
        return ["missing entry"]
    headline = entry.get("headline", "")
    body = entry.get("body", "")
    text = f"{headline} {body}"
    reasons = []
    if not headline:
        reasons.append("missing headline")
    if not body:
        reasons.append("missing body")
    if len(headline) > HEADLINE_LIMIT:
        reasons.append(f"headline over {HEADLINE_LIMIT} characters")
    if len(body) > BODY_LIMIT:
        reasons.append(f"body over {BODY_LIMIT} characters")
    lowered = text.lower()
    bad_words = [word for word in FORBIDDEN_WORDS if word in lowered]
    if bad_words:
        reasons.append("marketing filler: " + ", ".join(bad_words))
    if ISSUE_RE.search(text):
        reasons.append("PR/issue numbers are not allowed")
    if HASH_RE.search(text):
        reasons.append("commit hashes are not allowed")
    if URL_RE.search(text):
        reasons.append("URLs are not allowed")
    if any(char in text for char in "`[]"):
        reasons.append("markdown is not allowed")
    if "!" in text:
        reasons.append("exclamation marks are not allowed")
    if WE_RE.search(text):
        reasons.append("use first-person singular or neutral voice")
    return reasons


def _llm_entries(items, feedback=""):
    """One LLM pass over the items, with model fallback.

    Returns one entry dict (or None) per item. The first model that
    answers with parseable JSON wins; an unavailable model falls through
    to the next one instead of silently degrading the whole section.
    """
    numbered = "\n\n".join(
        f"ITEM {i + 1}: {item['repo']}\n{item_context(item)}"
        for i, item in enumerate(items)
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": numbered},
    ]
    if feedback:
        messages.append({"role": "user", "content": feedback})
    last_error = None
    for model in MODELS:
        payload = {
            "model": model,
            "max_tokens": 8000,
            "temperature": 0.5,
            "messages": messages,
            "response_format": {"type": "json_object"},
        }
        try:
            data = llm_completions(payload)
            content = data["choices"][0]["message"].get("content") or ""
            parsed = json.loads(content)
            raw_entries = (
                parsed.get("entries") if isinstance(parsed, dict) else parsed
            )
            if not isinstance(raw_entries, list):
                raise ValueError("entries not a list")
            by_index = {}
            for raw in raw_entries:
                if isinstance(raw, dict) and isinstance(raw.get("index"), int):
                    by_index[raw["index"]] = raw
            results = []
            for i, item in enumerate(items):
                raw = by_index.get(i)
                if not raw:
                    results.append(None)
                    continue
                headline = sanitize_prose(raw.get("headline", ""))
                body = sanitize_prose(raw.get("body", ""))
                known = {signal["id"] for signal in item["signals"]}
                links = []
                for link in raw.get("links") or []:
                    if isinstance(link, str) and link in known and link not in links:
                        links.append(link)
                if headline and body:
                    results.append(
                        {"headline": headline, "body": body, "links": links[:2]}
                    )
                else:
                    results.append(None)
            print(f"LLM model: {model}")
            return results
        except Exception as e:
            last_error = e
            print(f"LLM model {model} failed: {e}")
    raise RuntimeError(f"all LLM models failed: {last_error}")


def _retry_feedback(items, entries, failed):
    """Specific feedback for the entries rejected by validation."""
    reasons = []
    for position, idx in enumerate(failed):
        entry = entries[idx] if idx < len(entries) else None
        problems = validate_entry(items[idx], entry) or ["missing entry"]
        reasons.append(f"Entry {position + 1}: " + "; ".join(problems))
    return (
        "Your previous entries were rejected for:\n- "
        + "\n- ".join(reasons)
        + "\n\nRewrite only these ITEMS, keeping their order. Use only signal "
        "ids from each item. No numbers, links, hashes, exclamation marks, or "
        "marketing filler."
    )


def write_entries(items):
    """Write reader-facing entries for the selected repos.

    A failed validation is retried once with concrete feedback; an entry
    that still fails becomes None and the renderer uses the deterministic
    fallback for that repo.
    """
    if not items:
        return []
    if not os.environ.get("OPENCODE_API_KEY"):
        return [None] * len(items)
    try:
        entries = _llm_entries(items)
    except Exception as e:
        print(f"LLM unavailable, using fallback text: {e}")
        return [None] * len(items)
    failed = [
        i for i, entry in enumerate(entries) if validate_entry(items[i], entry)
    ]
    if not failed:
        return entries
    try:
        retry = _llm_entries(
            [items[i] for i in failed],
            _retry_feedback(items, entries, failed),
        )
    except Exception as e:
        print(f"LLM retry failed: {e}")
        retry = []
    for position, idx in enumerate(failed):
        entry = retry[position] if position < len(retry) else None
        entries[idx] = entry if not validate_entry(items[idx], entry) else None
    return entries


def render_pr_body(repos, blocks, today, project_changes=None):
    """Build the Scribe-style body for the auto-update pull request."""
    project_changes = project_changes or []
    body_lines = ["Auto-generated by update-readme workflow", ""]
    changes = []
    if blocks:
        noun = "entries" if len(repos) != 1 else "entry"
        changes.append(
            f"Updated Recent Activity with {len(repos)} {noun}: {', '.join(repos)}."
        )
    if project_changes:
        changes.append(
            "Refreshed Featured Projects Last Update dates for: "
            + ", ".join(project_changes)
            + "."
        )

    body_lines.append("## What")
    if changes:
        body_lines.append(" ".join(changes))
    else:
        body_lines.append(
            "No substantive public activity or project date changes were found."
        )
    body_lines.append("")
    body_lines.append("## Why")
    body_lines.append(
        "Keeps the profile current so visitors see recent work and the latest "
        "default-branch update date for each featured project."
    )
    body_lines.append("")
    body_lines.append("## How to test")
    body_lines.append(
        "1. Diff this PR and confirm activity claims and links match GitHub."
    )
    body_lines.append(
        "2. Confirm Last Update dates match the latest commit on each default branch."
    )
    body_lines.append("3. Re-run the Update README workflow to refresh both sections.")
    if blocks:
        body_lines.append("")
        body_lines.append("## Recent activity")
        body_lines.extend(blocks.rstrip("\n").split("\n"))
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

    events = fetch_events(token)
    if events is None:
        print("Events unavailable — leaving README unchanged.")
        raise RuntimeError("GitHub Events API unavailable")
    items = build_items(events, token)

    entries = write_entries(items)
    new_rows = render_activity(items, entries)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    m = ACTIVITY_RE.search(content)
    if not m:
        print("Could not find Recent Activity section in README.md")
        set_output(0)
        return

    old_activity = m.group(1).strip()
    activity_changed = bool(new_rows and old_activity != new_rows.strip())
    if not new_rows:
        print("No substantive activity — keeping the current section.")
    elif not activity_changed:
        print("Activity unchanged — checking Featured Projects dates.")

    new_content, project_changes = update_project_dates(content, token)
    if not activity_changed and not project_changes:
        print("README unchanged — no update needed.")
        set_output(0)
        return

    if activity_changed:
        m = ACTIVITY_RE.search(new_content)
        new_content = new_content[: m.start(1)] + new_rows + new_content[m.end(1) :]

    today = format_date(datetime.now(timezone.utc).isoformat())
    new_content = re.sub(
        r"Last updated: .+", f"Last updated: {today}", new_content
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    repos = [item["repo"] for item in items] if activity_changed else []
    body_lines = render_pr_body(
        repos, new_rows if activity_changed else "", today, project_changes
    )
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(body_lines) + "\n")

    changes = []
    if repos:
        changes.append("activity: " + ", ".join(repos))
    if project_changes:
        changes.append("project dates: " + ", ".join(project_changes))
    print("README updated. Changes: " + "; ".join(changes))
    set_output(1)


if __name__ == "__main__":
    main()
