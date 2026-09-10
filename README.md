# Fábio Borges
**Full-Stack & AI Engineer · Joinville, Brazil** · [flabs.tech](https://flabs.tech)

[![GitHub followers](https://img.shields.io/github/followers/fworks-tech?style=flat-square&logo=github)](https://github.com/fworks-tech)
[![Profile Views](https://komarev.com/ghpvc/?username=fworks-tech&style=flat-square&color=blue)](https://github.com/fworks-tech)
[![Agenthood stars](https://img.shields.io/github/stars/fworks-tech/agenthood?style=flat-square&logo=typescript)](https://github.com/fworks-tech/agenthood)
[![npm](https://img.shields.io/npm/v/agenthood?style=flat-square&logo=npm)](https://www.npmjs.com/package/agenthood)

10+ years across frontend, backend, testing, devops and AI engineering — shipping products for companies in the US, Europe, and Brazil. I balance solid architecture with real-world delivery.

---

## 📊 GitHub Activity

<div align="center">
  <img src="https://raw.githubusercontent.com/fworks-tech/fworks-tech/output/activity-graph.svg" width="100%" alt="fworks-tech GitHub Activity Graph" />
</div>

---

## 💝 Support My Work

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor%20Me-%F0%9F%A4%97-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/fworks-tech)
[![LinkedIn](https://img.shields.io/badge/Connect%20on%20LinkedIn-%230077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/fabiorborges)
[![Portfolio](https://img.shields.io/badge/flabs.tech-000000?style=for-the-badge&logo=vercel)](https://flabs.tech)

---

## Featured Projects

| Repository | Description |
|---|---|
| [flabs.tech](https://github.com/fworks-tech/flabs.tech) | Next.js 16 portfolio — Once UI design system, MDX blog, dynamic OG images, WCAG 2.1 AA, Vitest + Playwright E2E, Storybook 10, Lighthouse CI. Live at [flabs.tech](https://flabs.tech) |
| [agenthood](https://github.com/fworks-tech/agenthood) | A full AI engineering team that earns every merge. 20 specialized agents across the whole software lifecycle — portable SKILL.md files, an autonomous TypeScript runtime, a browser Studio, and a tamper-evident audit trail for every decision. Published on [npm](https://www.npmjs.com/package/agenthood) |
| [agenthood-site](https://github.com/fworks-tech/agenthood-site) | Agenthood's official platform — docs, Academy, and the browser-based Studio where the AI engineering team runs autonomously with every decision auditable. Live at [agenthood.flabs.tech](https://agenthood.flabs.tech) |
| [atlaslink](https://github.com/fworks-tech/atlaslink) | *(new)* Multi-agent task orchestrator, Agenthood proof-of-concept, and modern UI to customize and integrate agents through gorgeous, easy-to-use, live diagram flows. Preview its development at [atlas.flabs.tech](https://atlas.flabs.tech) |
| [arxiv-manager](https://github.com/fworks-tech/arxiv-manager) | AI-powered visual-reasoning Q&A generator — 7-agent pipeline (draft, self-critique, consensus), CRAG architecture (semantic cache + hybrid retrieve + cross-encoder rerank), 8 MCP tools, hot-swappable prompts, structured observability with token/cost tracking, 220+ tests |

---

## Recent Activity

<!-- recent-activity:start -->
- 🔀 [**agenthood**](https://github.com/fworks-tech/agenthood) — 3 PRs merged into main · just now
  **Brief:** We added `agenthood optimize` (PR #779, commit 4ebc083) — an LLM generate/score loop that maximizes trigger F1 for member descriptions, closing #584.
  Blind A/B eval mode landed in PR #778 (commit 44ecaf8): paired t-test and Cohen d compare two members, per issue #558; also patched js-yaml via npm override.
  PR #774 (commit c6f250e) adds optional `output_format` regex and strict/lenient mode to SKILL.md frontmatter, with MemberRunner validating output after runs.
  **Changes:** [`4ebc083`](https://github.com/fworks-tech/agenthood/commit/4ebc08336fc7a8754b54f9ad420eea0ed04f3ed3) feat(evals): add description optimizatio · [`8cb2a31`](https://github.com/fworks-tech/agenthood/commit/8cb2a3142c535c9246c88463a19720fa30ada5bf) test(commands): add optimize to expected · [`5ffd0ae`](https://github.com/fworks-tech/agenthood/commit/5ffd0ae1ad39ae2942aa7ebdbcb803f017e79e26) test(commands): add tests for optimize c · and 6 more commits

- 🔀 [**agenthood-site**](https://github.com/fworks-tech/agenthood-site) — 3 PRs merged into main · just now
  **Brief:** We bumped dependabot/fetch-metadata from v2 to v3 in PR #216 (commit 14bba69), which now requires Node 24 as the Actions runtime.
  PR #215 (commit 2ea1912) rewrote the README as a visitor-facing landing page and added LICENSE, CONTRIBUTING.md, SECURITY.md, issue/PR templates, package.json metadata, and sitemap routes.
  PR #212 (commit e2cd0d1) added @next/bundle-analyzer via `npm run analyze` to measure the studio bundle, per issue #51.
  **Changes:** [`14bba69`](https://github.com/fworks-tech/agenthood-site/commit/14bba6955399aba7e6039f2caf84afddcfa3e368) chore(deps): bump dependabot/fetch-metad · [`2ea1912`](https://github.com/fworks-tech/agenthood-site/commit/2ea19126c32b07db35e210f78e0c22d1c42dd8fd) docs: rewrite README, add community heal · [`e2cd0d1`](https://github.com/fworks-tech/agenthood-site/commit/e2cd0d1022e7cb5a001f2271edc9ad525a384461) perf: add bundle analyzer for studio bun

- 🔀 [**atlaslink**](https://github.com/fworks-tech/atlaslink) — 3 PRs merged into main · just now
  **Brief:** We moved the database to a local Postgres container on Oracle Free Tier (PR #239, commit 50031f0, issue #54), with Caddy/Let's Encrypt TLS at api.atlas.flabs.tech and deploy.sh generating ATLASLINK_DATABASE_URL.
  PR #238 (commit 1d33f74) rewrote the README into a scannable landing page with CI/Conventional Commits/PRs Welcome badges and a 3-step quick start.
  PR #237 (commit eb72967) makes NodeConfigPanel reject non-integer maxTokens with a 'must be a whole number' error, matching isAgentConfig's Number.isInteger check.
  **Changes:** [`50031f0`](https://github.com/fworks-tech/atlaslink/commit/50031f02de6137e1d2377a937e7882943cc613e7) infra(deploy): add local Postgres + TLS · [`1d33f74`](https://github.com/fworks-tech/atlaslink/commit/1d33f744ab824ec0dae75b2775136de3a8604ef8) docs: rewrite README for clarity, scanab · [`eb72967`](https://github.com/fworks-tech/atlaslink/commit/eb729678922f4834410c98b5671d4f0b0a68d680) fix(config): reject non-integer maxToken
<!-- recent-activity:end -->

---

## Tech Stack

**Frontend:**
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![MUI](https://img.shields.io/badge/MUI-007FFF?style=flat-square&logo=mui&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)
![Storybook](https://img.shields.io/badge/Storybook-FF4785?style=flat-square&logo=storybook&logoColor=white)

**Backend & APIs:**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django)
![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)

**Web & Templating:**
![HTMX](https://img.shields.io/badge/HTMX-3366CC?style=flat-square&logo=htmx&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat-square&logo=jinja&logoColor=white)
![Apollo](https://img.shields.io/badge/Apollo-311C87?style=flat-square&logo=apollographql&logoColor=white)

**Python Ecosystem:**
![Typer](https://img.shields.io/badge/Typer-000000?style=flat-square)
![Rich](https://img.shields.io/badge/Rich-FF6F00?style=flat-square)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-000000?style=flat-square)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-003D7A?style=flat-square)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat-square)

**AI & Agents:**
![Claude AI](https://img.shields.io/badge/Claude_AI-000000?style=flat-square)
![OpenCode](https://img.shields.io/badge/OpenCode-6C5CE7?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![sentence-transformers](https://img.shields.io/badge/sentence--transformers-FF6F00?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-000000?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-191919?style=flat-square)
![LanceDB](https://img.shields.io/badge/LanceDB-44B585?style=flat-square)
![Chroma](https://img.shields.io/badge/Chroma_DB-44B585?style=flat-square)
![Tree-sitter](https://img.shields.io/badge/Tree--sitter-999999?style=flat-square)
![SSE](https://img.shields.io/badge/SSE-009688?style=flat-square)

**Testing:**
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=flat-square&logo=vitest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)

**Cloud & DevOps:**
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)

---

## Contact & Writing

- **LinkedIn:** [in/fabiorborges](https://www.linkedin.com/in/fabiorborges) — fastest reply
- **Portfolio:** [flabs.tech](https://flabs.tech) — projects, writing, and contact form
- **npm:** [agenthood](https://www.npmjs.com/package/agenthood) — latest published package

---

*Last updated: Sep 9, 2026
