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
- agenthood 3.63.3: #830 narrows the verify placeholder scan to marker form, and #829 aligns the ESLint dev tree.
  **Brief:** We merged #830 (aa42b57), restricting verify's placeholder patterns to marker form (TODO/FIXME/TBD plus a structural character) and skipping fenced/inline code, with regression tests in 1b2d24e.
  That clears the false failures in the-doorman, the-warden, code-smell-detection and validation-and-enforcement (closes #816, #753); the release commit is ec580b8.
  #829 (0620117, 359b7a9) chains six swallowed errors through Error(msg, { cause }) and moves @eslint/js to 10.0.1 to match eslint 10.10.0, noted in CONTRIBUTING.
  **Changes:** [`ec580b8`](https://github.com/fworks-tech/agenthood/commit/ec580b85ba91891f6b14f6301b90e9ae3ee9c1f2) chore(release): v3.63.3 · [`1bf3b55`](https://github.com/fworks-tech/agenthood/commit/1bf3b55ba6a7cc76c726c581739e5b4b66bf5bd2) fix(verify): narrow placeholder scan to · [`1b2d24e`](https://github.com/fworks-tech/agenthood/commit/1b2d24ee270f6e7c2de7079319e18f4d7ea5b0c7) test(verify): regression tests for place · and 4 more commits

- atlaslink's phone pass: #260 reworks the session room, #259 drops a dead mobile header and reworks the cost chart, #258 polls costs every 5s.
  **Brief:** Session room on mobile landed in #260 (5e44aca): reply and steer forms stack, inputs render at 16px, Send/Steer/Interrupt/Resume/Ask Atlas hit 44px targets, and palette agents become tappable buttons feeding drafts the same way as drag-and-drop.
  #259 removes the duplicate header bar on the home route (6205413), makes the cost badge live and mobile-visible (aeff2fd), and caps the cost legend at the top 7 agents with daily, weekly and monthly views (6492b47).
  Polling every 5s while the tab is visible arrives in #258 (47559b0) through useCost and useCostHistory, holding the last good data when a poll fails.
  **Changes:** [`5e44aca`](https://github.com/fworks-tech/atlaslink/commit/5e44aca25d7d11f31035c777d33d60133f703fc7) feat(room): make the session room usable · [`6205413`](https://github.com/fworks-tech/atlaslink/commit/6205413e04e8fc01f1f517b64cdaca25a6002b94) fix(mobile): remove the dead second head · [`aeff2fd`](https://github.com/fworks-tech/atlaslink/commit/aeff2fd0ed1214fe31ea3b5ebe35f9f4f6f45cea) feat(header): poll the cost badge from t · and 2 more commits

- agenthood-site: #228 reworks playground chat, #227 cycles 12 terminal examples, #226 adds the 2026-09-13 digest.
  **Brief:** Playground chat now renders three conversational starters per member for all 20 members from agentStarters.ts, replacing the SKILL.md "When to Use" bullets users never would have typed (#228, c43be24).
  The same PR composes member system prompts with style, roster and orchestration (c53dc0e, 2b258cd), while #227 loops 12 examples across 11 members plus agenthood list in TypingTerminal.tsx with a GITHUB_TOKEN build fix (69f9db6, 1093f31).
  #226 (6f9666b) publishes the automated 2026-09-13 news digest.
  **Changes:** [`c43be24`](https://github.com/fworks-tech/agenthood-site/commit/c43be24fecab0a25521c93be67597c6c6ca45068) feat(studio): show curated conversationa · [`c53dc0e`](https://github.com/fworks-tech/agenthood-site/commit/c53dc0e8d7e079a8c08af94b46e10fbae245495d) feat(studio): compose member system prom · [`2b258cd`](https://github.com/fworks-tech/agenthood-site/commit/2b258cdb36b33fd4ff10b0ebf23e7df1c6f80ccb) refactor(studio): address review finding · and 3 more commits
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

*Last updated: Sep 14, 2026
