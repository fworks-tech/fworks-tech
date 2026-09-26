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
| [deeptales](https://github.com/fworks-tech/deeptales) | *(new)* The horror game factory: a generator framework that stamps complete, playable Godot 4.x horror games from a one-line pitch — Until Dawn-style branching, analog-horror art and audio pipelines, contract-verified output, and a FastAPI/React Studio with visual story editing. Live at [deeptales.flabs.tech](https://deeptales.flabs.tech) |
| [flabs.tech](https://github.com/fworks-tech/flabs.tech) | Next.js 16 portfolio — Once UI design system, MDX blog, dynamic OG images, WCAG 2.1 AA, Vitest + Playwright E2E, Storybook 10, Lighthouse CI. Live at [flabs.tech](https://flabs.tech) |
| [agenthood](https://github.com/fworks-tech/agenthood) | A full AI engineering team that earns every merge. 20 specialized agents across the whole software lifecycle — portable SKILL.md files, an autonomous TypeScript runtime, a browser Studio, and a tamper-evident audit trail for every decision. Published on [npm](https://www.npmjs.com/package/agenthood) |
| [agenthood-site](https://github.com/fworks-tech/agenthood-site) | Agenthood's official platform — docs, Academy, and the browser-based Studio where the AI engineering team runs autonomously with every decision auditable. Live at [agenthood.flabs.tech](https://agenthood.flabs.tech) |
| [atlaslink](https://github.com/fworks-tech/atlaslink) | Multi-agent task orchestrator, Agenthood proof-of-concept, and modern UI to customize and integrate agents through gorgeous, easy-to-use, live diagram flows. Preview its development at [atlas.flabs.tech](https://atlas.flabs.tech) |
| [arxiv-manager](https://github.com/fworks-tech/arxiv-manager) | AI-powered visual-reasoning Q&A generator — 7-agent pipeline (draft, self-critique, consensus), CRAG architecture (semantic cache + hybrid retrieve + cross-encoder rerank), 8 MCP tools, hot-swappable prompts, structured observability with token/cost tracking, 220+ tests |

---

## Recent Activity

<!-- recent-activity:start -->
- 🔀 [**agenthood**](https://github.com/fworks-tech/agenthood) — merged [PR #936](https://github.com/fworks-tech/agenthood/pull/936): fix(skills): adapt the frontmatter parser to js-ya · just now
  **Brief:** We merged #936 (commits 2efb572, 3a351e0) to bump js-yaml 4.3.2→5.4.2 and adapt SkillParser to the v5 API, superseding #930.
  Because the v5 TypeScript rewrite drops the default export, the frontmatter parser's fail-closed YAML path from #515 needed rework; both breakages were verified against 5.4.2.
  **Changes:** [`2efb572`](https://github.com/fworks-tech/agenthood/commit/2efb57286277de3313f6588058b4736a3b4940f7) chore(deps): bump js-yaml from 4.3.2 to · [`3a351e0`](https://github.com/fworks-tech/agenthood/commit/3a351e0d79f2a385b659aee64806ac8557c4c0ad) fix(skills): adapt the frontmatter parse

- 🔀 [**agenthood-site**](https://github.com/fworks-tech/agenthood-site) — 3 PRs merged into main · just now
  **Brief:** From a local agenthood v3.68.1 build, #247 regenerated Studio data and added mediator sections (Scoring Confidence, Parallel Evaluation, Type-Safe Decision Record, Cascade Rules) plus steward sections (Complexity Scoring, Model Tier Routing) to agents.generated.ts.
  The September 2026 AI trends roundup landed in #246 (closes #45), covering frontier model releases, policy shifts, and market signals on the news page.
  Staging gets CI/E2E gates in #234 (closes #47), with the promotion flow documented in README and the branch force-pushed to match main (-d409b9d).
  **Changes:** [`9650a96`](https://github.com/fworks-tech/agenthood-site/commit/9650a9699d998ce66413c9448eac3749a7e38299) feat(studio): add Jev-inspired confidenc · [`b9ae7e7`](https://github.com/fworks-tech/agenthood-site/commit/b9ae7e70878bc5c981ca29a8ed20d9cf5187e042) feat(news): add AI trends September 2026 · [`3d87e28`](https://github.com/fworks-tech/agenthood-site/commit/3d87e286afccd823e5aa44f8736387f264545d00) feat(infra): add staging branch pipeline

- 🔀 [**flabs.tech**](https://github.com/fworks-tech/flabs.tech) — 2 PRs merged into main · just now
  **Brief:** We fixed four analytics defects in #318 (commits bb7d48b, 6dcef33): a shared getConsent() !== 'declined' gate for Vercel/PostHog/self-hosted emitters, CTA label plumbing through PendingEvent → TrackedEvent, IP scrubbing, and engagement dashboards.
  The chat endpoint moved from OpenCode Go to Zen in #316 at src/app/api/chat/route.ts:43, with Playwright mocks updated and a chat-modal-overlay added in AiAssistant.tsx (aria-modal, centralized handleClose).
  **Changes:** [`bb7d48b`](https://github.com/fworks-tech/flabs.tech/commit/bb7d48bd5f806a65ae968903631455d9956d00a9) fix(analytics): consent gate, label plum · [`6dcef33`](https://github.com/fworks-tech/flabs.tech/commit/6dcef33068f9056747c14e26cb31ab9631eeba59) refactor: share BROWSER_KEYS + ScrollDep · [`10e234d`](https://github.com/fworks-tech/flabs.tech/commit/10e234d42039d5e4a594c1752325734f50ddde92) feat(ai): trap focus and separate modal · and 1 more commits
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
![Mantine](https://img.shields.io/badge/Mantine-339AF0?style=flat-square&logo=mantine&logoColor=white)
![Zod](https://img.shields.io/badge/Zod-3068B7?style=flat-square&logo=zod&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)
![Storybook](https://img.shields.io/badge/Storybook-FF4785?style=flat-square&logo=storybook&logoColor=white)

**Game Dev:**
![Godot](https://img.shields.io/badge/Godot-478CBF?style=flat-square&logo=godotengine&logoColor=white)

**Backend & APIs:**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Fastify](https://img.shields.io/badge/Fastify-000000?style=flat-square&logo=fastify&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django)
![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)

**Web & Templating:**
![HTMX](https://img.shields.io/badge/HTMX-3366CC?style=flat-square&logo=htmx&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat-square&logo=jinja&logoColor=white)
![Apollo](https://img.shields.io/badge/Apollo-311C87?style=flat-square&logo=apollographql&logoColor=white)
![MDX](https://img.shields.io/badge/MDX-FCB32C?style=flat-square&logo=mdx&logoColor=black)

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
![Sentry](https://img.shields.io/badge/Sentry-362D59?style=flat-square&logo=sentry&logoColor=white)
![Upstash](https://img.shields.io/badge/Upstash-00E9A3?style=flat-square&logo=upstash&logoColor=white)

---

## Contact & Writing

- **LinkedIn:** [in/fabiorborges](https://www.linkedin.com/in/fabiorborges) — fastest reply
- **Portfolio:** [flabs.tech](https://flabs.tech) — projects, writing, and contact form
- **npm:** [agenthood](https://www.npmjs.com/package/agenthood) — latest published package

---

*Last updated: Sep 26, 2026
