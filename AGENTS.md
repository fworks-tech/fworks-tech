# AGENTS.md — Profile Repository

Agent-agnostic guidance for `fworks-tech/fworks-tech`. The main deliverable is
`README.md`; automation refreshes Featured Projects dates and the marked Recent
Activity section.

## Commands

```bash
python3 scripts/test_update_readme.py
python3 scripts/update_readme.py
```

The updater requires `GITHUB_TOKEN`. `OPENCODE_API_KEY` enables LLM-written summaries;
without it, the script uses deterministic fallback text. Python uses only the standard library.

## Commit Standards

- Follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): subject`.
- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `chore`.
- Subject: imperative, lowercase, at most 150 characters, no trailing period.
- One logical change per commit.

## Branch Standards

- One branch per issue: `type/issue-NUMBER-short-description`.
- Branch names are lowercase and hyphenated.
- Never commit directly to `main`.
- Exception: the README workflow reuses `chore/auto-update-readme` without an issue.

## Pull Request Standards

- Link each PR with `Closes #N` or `Fixes #N`.
- Exception: the automated README update PR does not link an issue.
- Use a Conventional Commits title.
- Explain what changed, why, and how to test it.
- All CI checks must pass before merge.

## Agent Behavior

- Create a branch before editing and run the tests before finishing.
- Prefer the smallest change and edit existing files when possible.
- Never push or merge without explicit user confirmation.
