# CLAUDE.md

This file provides guidance to Claude Code (and other AI coding agents) when working with code in this repository.

This is the **GitHub profile README repository** for the `fworks-tech` organization.
It controls the public profile page at `github.com/fworks-tech`. The main deliverable is
`README.md` — the profile README.

---

## Commands

```bash
python3 scripts/update_readme.py    # Manually regenerate the project table
```

No npm/yarn/build step needed — this is not a Node.js project.

### If you are an AI coding agent

Read `AGENTS.md` and `oath.md` first to understand behavior and standards.
Then use this file as your primary reference for commands and project structure.

---

## Project Structure

```
/
├── README.md                         # GitHub profile README (main deliverable)
├── AGENTS.md                         # Convention registry for AI agents
├── CLAUDE.md                         # This file
├── oath.md                           # The Society oath
├── .github/
│   └── workflows/
│       └── update-readme.yml         # Daily scheduled: auto-updates README project table
├── scripts/
│   ├── update_readme.py              # Python: fetches repos, regenerates table
│   └── update_summary.txt            # Output log from last auto-update
├── docs/
│   └── graphql-and-ai.md             # Knowledge doc: GraphQL + AI engineering
└── .gitignore                        # Empty — all files tracked
```

## Key files

| File | Purpose |
|------|---------|
| `README.md` | The profile README — badges, featured projects, tech stack, contact |
| `scripts/update_readme.py` | Python script that auto-generates the featured projects table from the GitHub API |
| `.github/workflows/update-readme.yml` | CI workflow — runs daily at 08:00 UTC, creates PR if table changed |

## Conventions

- **Conventional Commits** required (`type(scope): subject`)
- **No direct pushes to `main`** — always use a branch + PR
- Python scripts use standard library only (no pip dependencies)
- The auto-update workflow creates branches named `chore/auto-update-readme-YYYY-MM-DD`
