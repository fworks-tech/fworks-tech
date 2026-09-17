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
- Docs cleanup across agenthood: changelog, skills licensing, and Discussions routing
  **Brief:** Consolidated all shipped vscode-extension/CHANGELOG.md content under one dated 0.1.0 - 2026-09-16 section (#841, e48fd6f), closing #149 so the marketplace listing stops rendering a placeholder.
  Added `license: MIT` frontmatter to 16 skills/*/SKILL.md files and a SkillsMP badge in README (#840, 490565b) for schema compliance, and moved usage questions and member pitches to Discussions (#839, ca1a1a2) with a bilingual welcome post #835.
  **Changes:** [`e48fd6f`](https://github.com/fworks-tech/agenthood/commit/e48fd6f8b0a6ee0282be0dbcefe7561053697147) docs(vscode): consolidate 0.1.0 changelo · [`490565b`](https://github.com/fworks-tech/agenthood/commit/490565bc1df959122a3d39845eba1e09444a53d3) chore(skills): add MIT license frontmatt · [`4784b9c`](https://github.com/fworks-tech/agenthood/commit/4784b9c5158e81c5fb09badb4e37f99eff88cbc1) docs: add SkillsMP registry badge to REA · and 1 more commits

- Dependency bumps land across the site and the extension
  **Brief:** Bumped next, @next/bundle-analyzer and eslint-config-next to 16.3.5 (#233, f4c6118), the last patch flagged by `npm run check:deps` so local and CI installs stay lockfile-consistent.
  Dependabot groups moved alongside: six minor updates (#230, 67f76de) led by @sentry/nextjs 10.74.0 and react/react-dom 19.3.0, plus eight patch updates (#229, c4bb6ac) carrying the @mantine packages from 9.6.0 to 9.6.1.
  **Changes:** [`f4c6118`](https://github.com/fworks-tech/agenthood-site/commit/f4c6118ae282834cae26b4b41424f5561d573aeb) chore(deps): bump next family to 16.3.5 · [`67f76de`](https://github.com/fworks-tech/agenthood-site/commit/67f76de0d1ffeef95023891a2e9b8fd529601b30) chore(deps): bump the minor-dependencies · [`b43c271`](https://github.com/fworks-tech/agenthood-site/commit/b43c271bab484d26709af8e44d76055de7591f45) Merge remote-tracking branch 'origin/mai · and 1 more commits

- Delta-encoded checkpoints arrive, then get hardened and tested
  **Brief:** Delta channels for runner checkpoints shipped in src/session/deltaChannel.ts (#270, c7e3c62) with planWrite, reconstructRows and migration 7 for Postgres and SQLite, re-anchoring a full snapshot every 10 writes via ATLASLINK_CHECKPOINT_SNAPSHOT_EVERY.
  Review hardening in #271 (f43959b) adds baseCount to delta rows and returns null from loadCheckpoint on failed replay in all three backends; #269 (9f4a8f0) pins SessionThread to its 50-turn TURN_WINDOW for a 1000-turn session, closing #117.
  **Changes:** [`f43959b`](https://github.com/fworks-tech/atlaslink/commit/f43959bee9575a4bf2ad3115fa9d858bf1841141) fix(session): harden delta channels per · [`c7e3c62`](https://github.com/fworks-tech/atlaslink/commit/c7e3c6271b6faa8ae2fa554c435f4bb80de48eef) feat(session): delta channels for checkp · [`9f4a8f0`](https://github.com/fworks-tech/atlaslink/commit/9f4a8f042325e86c1f64ee116e0436a83454ff42) test(dashboard): prove thread render cap
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

*Last updated: Sep 17, 2026
