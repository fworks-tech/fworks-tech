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
- Agenthood v3.65.2 wraps tools for OpenAI-compatible providers; v3.65.1 polls npm in release verify.
  **Brief:** We shipped v3.65.2 (#861, bde8acc) wrapping ToolSchema as {type:'function', function:{...}} in validateTools, fixing Groq 400s on tools.0.type missing (#860, e034c1d).
  v3.65.1 (#858, b4a30bd) swaps the fixed sleep in release verify for an npm registry poll (#857, closes #856).
  **Changes:** [`b20fdb4`](https://github.com/fworks-tech/agenthood/commit/b20fdb4481797befdd828917361e6faadc88c763) chore(release): v3.65.2 · [`e034c1d`](https://github.com/fworks-tech/agenthood/commit/e034c1d0d91614fc559abea54ec44d2c3c836cdf) fix(llm): wrap tools in OpenAI function · [`a187e89`](https://github.com/fworks-tech/agenthood/commit/a187e89bc0ff4b71a08299a5d6098ef56fa60203) chore(release): v3.65.1

- Atlaslink fixes provider key env mapping, swaps Groq fallback model, bumps agenthood, and adds room follow-ups.
  **Brief:** Provider key resolution got fixed in #284 (ffb884b) by reading agenthood's canonical PROVIDER_KEYS registry, so opencode-go no longer reports unconfigured despite OPENCODE_API_KEY being set.
  The same PR replaces the dead Groq fallback mixtral-8x7b-32768 with openai/gpt-oss-120b (be8047b), and #283 (a23cb84) bumps agenthood to 3.65.2 for the tool-wrapping fix.
  Room work in #282 (661a632) adds lifecycle SSE status patching via useSessions.patchSessionStatus and a POST /tasks/:id/followup route for terminal-session questions.
  **Changes:** [`ffb884b`](https://github.com/fworks-tech/atlaslink/commit/ffb884be56cdad46a8b028c523102e31ba5211a3) fix(dashboard): resolve provider key env · [`be8047b`](https://github.com/fworks-tech/atlaslink/commit/be8047b6d66a558f08df6376f81a0a6ab1bac0cc) chore(config): point groq fallback at op · [`a23cb84`](https://github.com/fworks-tech/atlaslink/commit/a23cb84bf82cd1af8ad3854a1b25697a8661ff0d) chore(deps): bump agenthood to 3.65.2 fo · and 1 more commits

- Flabs.tech brings blog drafts into compliance, syncs repo docs, and fixes MDX SSG with a client component.
  **Brief:** Four blog drafts came into pattern compliance in #315 (e678c8a), adding subtitle/shareText, extending the mantine summary to 200 chars, fixing the mailman 6-to-4 platform count, and rewriting the firehose Tailwind premise to the Mantine migration.
  Our repo-wide spec audit in #314 (e593d3a) syncs README, AGENTS.md, env example and specs, fixing stale model ids/test counts and documenting admin area, cross-posting, OTLP logging, TBT/FCP budgets, mobile-chrome, gitleaks job, and missing env vars.
  CustomLink moved into its own 'use client' component in #313 (f083839) to fix SSG prerendering for blog posts with internal markdown links.
  **Changes:** [`e678c8a`](https://github.com/fworks-tech/flabs.tech/commit/e678c8a0eda7bdc748411e067c00574199b66323) docs(blog): bring 4 drafts into pattern · [`e593d3a`](https://github.com/fworks-tech/flabs.tech/commit/e593d3a24d47bbf1ea9a5d78c99ade539dc13417) docs: sync README, AGENTS.md, env exampl · [`f083839`](https://github.com/fworks-tech/flabs.tech/commit/f083839427b123d7d2c00d7ce9c953d1e4639a93) fix(mdx): extract CustomLink to 'use cli
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

*Last updated: Sep 18, 2026
