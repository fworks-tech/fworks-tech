# Fábio Borges
**Full-Stack & AI Engineer · Joinville, Brazil** · [flabs.tech](https://flabs.tech)

[![GitHub followers](https://img.shields.io/github/followers/fworks-tech?style=flat-square&logo=github)](https://github.com/fworks-tech)
[![Profile Views](https://komarev.com/ghpvc/?username=fworks-tech&style=flat-square&color=blue)](https://github.com/fworks-tech)
[![Agenthood stars](https://img.shields.io/github/stars/fworks-tech/agenthood?style=flat-square&logo=typescript)](https://github.com/fworks-tech/agenthood)
[![npm](https://img.shields.io/npm/v/agenthood?style=flat-square&logo=npm)](https://www.npmjs.com/package/agenthood)

10+ years across frontend, backend, testing, devops and AI engineering — shipping products for companies in the US, Europe, and Brazil. I balance solid architecture with real-world delivery.

---

## 💝 Support My Work

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor%20Me-%F0%9F%A4%97-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/fworks-tech)
[![LinkedIn](https://img.shields.io/badge/Connect%20on%20LinkedIn-%230077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/fabiorborges)
[![Portfolio](https://img.shields.io/badge/flabs.tech-000000?style=for-the-badge&logo=vercel)](https://flabs.tech)

---

## Featured Projects

| Repository | Description | Last Update |
|---|---|---|
| [flabs.tech](https://github.com/fworks-tech/flabs.tech) | Next.js 16 portfolio and engineering playground — Mantine UI, MDX blog, dynamic OG images, AI assistant, browser quiz, Vitest + Playwright, Storybook 10, axe-core WCAG 2.1 AA checks and Lighthouse CI. Live at [flabs.tech](https://flabs.tech) | 11/15/2026 |
| [agenthood](https://github.com/fworks-tech/agenthood) | Open-source AI engineering team — 20 portable SKILL.md members, an autonomous TypeScript runtime/CLI, MCP tools and tamper-evident decision provenance, with a companion browser Studio. Published on [npm](https://www.npmjs.com/package/agenthood) | 11/24/2026 |
| [agenthood-site](https://github.com/fworks-tech/agenthood-site) | Official Agenthood platform — documentation, Academy and a live browser Studio for chatting with 20 AI members and orchestrating multi-agent workspaces. Live at [agenthood.flabs.tech](https://agenthood.flabs.tech) | 11/24/2026 |
| [atlaslink](https://github.com/fworks-tech/atlaslink) | *(experimental)* Agenthood-powered shared workspace for live human–AI task sessions, with a visual agent DAG, SSE/WebSocket updates, human approval gates and durable SQLite/Postgres storage. Live at [atlas.flabs.tech](https://atlas.flabs.tech) | 11/24/2026 |
| [chaintelescope](https://github.com/fworks-tech/chaintelescope) | *(under refactor)* Crypto intelligence dashboard — live price trends, watchlists, threshold alerts, RSS news, risk panels and a dashboard-grounded AI assistant in the Streamlit app; a Hapi.js/TypeScript API and React 19 + Vite client are replacing it screen by screen. Live at [chaintelescope.flabs.tech/](https://chaintelescope.flabs.tech/) | 11/25/2026 |
| [wormage-demo](https://github.com/fworks-tech/wormage-demo) | *(playable demo)* Turn-based browser artillery with 2–4 teams, three worms per team by default, destructible pixel terrain, wind-aware ballistics and AI opponents that forward-simulate the same physics. Built with React 18, strict TypeScript and PixiJS. Live at [wormage.flabs.tech](https://wormage.flabs.tech) | 11/25/2026 |
| [deeptales](https://github.com/fworks-tech/deeptales) | *(under development)* Godot 4.x horror game generator and authoring Studio — three genre blueprints, five visual styles, branching stories, consequence-driven gameplay and story/art/audio tooling. Live at [deeptales.flabs.tech](https://deeptales.flabs.tech) | 11/06/2026 |
| [kurio-marketplace](https://github.com/fworks-tech/kurio-marketplace) | *(portfolio demo)* NFT marketplace frontend — React 19 + TypeScript, TanStack Router/Query, Tailwind v4 + shadcn/ui and Socket.IO events over browser-only MSW REST/WebSocket mocks, with Vitest and Playwright coverage. Live at [kurio-marketplace-theta.vercel.app](https://kurio-marketplace-theta.vercel.app) | 11/04/2026 |
| [trucksafe](https://github.com/fworks-tech/trucksafe) | *(portfolio demo)* Weather-aware truck route planner — Django API and React/MapLibre UI comparing three routes with deterministic weather/load risk rules, checkpoint ETAs, risk segments and a 0–48h forecast heatmap. Demo weather is simulated. Live at [trucksafe.flabs.tech](https://trucksafe.flabs.tech/) | 10/14/2026 |

---

## Recent Activity

<!-- recent-activity:start -->
- [**chaintelescope**](https://github.com/fworks-tech/chaintelescope) — Live crypto prices now reach the app, with recent results remembered briefly
  The hosted app had been showing placeholder prices because its slim environment lacked the usual exchange connector; it now pulls live quotes directly. Successful market results are also remembered briefly, so repeat views skip the data sources instead of asking again.
  [Fetch live prices over httpx when ccxt is unavailable](https://github.com/fworks-tech/chaintelescope/pull/183) · [Cache successful snapshots and per-provider metrics](https://github.com/fworks-tech/chaintelescope/pull/189)

- [**agenthood**](https://github.com/fworks-tech/agenthood) — Upcoming release adds scoped MCP connections and quicker tool lookups
  The upcoming release adds a way for agents to connect to MCP servers the host declares, with each member limited to its own scope. It also remembers each server's available tools for quicker repeat lookups, and protects the decision record from malformed entries.
  [v4.5.0 (draft)](https://github.com/fworks-tech/agenthood/pull/1145)

- [**wormage-demo**](https://github.com/fworks-tech/wormage-demo) — Dead worms no longer fire, and reporting a bug now captures the match
  A worm that drowns or takes a fatal fall while aiming now ends its turn instead of still firing. The pause menu can capture the current match view and send it with recent game history when you report a bug.
  [End turn when active worm dies during aim](https://github.com/fworks-tech/wormage-demo/pull/257) · [Report bugs with a faithful tab capture](https://github.com/fworks-tech/wormage-demo/pull/252)
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
![Emotion](https://img.shields.io/badge/Emotion-D26AC2?style=flat-square)
![Mantine](https://img.shields.io/badge/Mantine-339AF0?style=flat-square&logo=mantine&logoColor=white)
![Zod](https://img.shields.io/badge/Zod-3068B7?style=flat-square&logo=zod&logoColor=white)
![Storybook](https://img.shields.io/badge/Storybook-FF4785?style=flat-square&logo=storybook&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-22B5BF?style=flat-square)
![TanStack Query](https://img.shields.io/badge/TanStack%20Query-FF4154?style=flat-square&logo=reactquery&logoColor=white)
![TanStack Router](https://img.shields.io/badge/TanStack%20Router-FF4154?style=flat-square&logo=reactrouter&logoColor=white)
![React Hook Form](https://img.shields.io/badge/React%20Hook%20Form-EC5990?style=flat-square&logo=reacthookform&logoColor=white)
![MapLibre GL JS](https://img.shields.io/badge/MapLibre%20GL%20JS-396CB2?style=flat-square&logo=maplibre&logoColor=white)
![React Flow](https://img.shields.io/badge/React%20Flow-FF0072?style=flat-square)
![dagre](https://img.shields.io/badge/dagre-000000?style=flat-square)
![shadcn/ui](https://img.shields.io/badge/shadcn%2Fui-000000?style=flat-square&logo=shadcnui&logoColor=white)
![Radix UI](https://img.shields.io/badge/Radix%20UI-161618?style=flat-square&logo=radixui&logoColor=white)
![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=flat-square&logo=sass&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=flat-square&logo=axios&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.IO-010101?style=flat-square&logo=socketdotio&logoColor=white)

**Game Dev:**
![Godot](https://img.shields.io/badge/Godot-478CBF?style=flat-square&logo=godotengine&logoColor=white)
![PixiJS](https://img.shields.io/badge/PixiJS_8-E72264?style=flat-square)
![Canvas 2D](https://img.shields.io/badge/Canvas_2D-E34F26?style=flat-square&logo=html5&logoColor=white)
![Web Audio API](https://img.shields.io/badge/Web_Audio_API-FF6F00?style=flat-square)

**Backend & APIs:**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-2D4B63?style=flat-square)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Fastify](https://img.shields.io/badge/Fastify-000000?style=flat-square&logo=fastify&logoColor=white)
![Hapi.js](https://img.shields.io/badge/Hapi.js-FF9900?style=flat-square)
![Joi](https://img.shields.io/badge/Joi-4B8BBE?style=flat-square)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![NextAuth](https://img.shields.io/badge/NextAuth-000000?style=flat-square)
![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![GraphQL Codegen](https://img.shields.io/badge/GraphQL%20Codegen-E10098?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Kysely](https://img.shields.io/badge/Kysely-3B82F6?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=flat-square&logo=djangorestframework&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

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
![ImageHash](https://img.shields.io/badge/ImageHash-000000?style=flat-square)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-000000?style=flat-square)
![ccxt](https://img.shields.io/badge/ccxt-1E88E5?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-000000?style=flat-square&logo=ruff)
![mypy](https://img.shields.io/badge/mypy-000000?style=flat-square)

**AI & Agents:**
![Claude AI](https://img.shields.io/badge/Claude_AI-000000?style=flat-square)
![OpenCode](https://img.shields.io/badge/OpenCode-6C5CE7?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![sentence-transformers](https://img.shields.io/badge/sentence--transformers-FF6F00?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-000000?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square)
![OpenRouter](https://img.shields.io/badge/OpenRouter-6467F2?style=flat-square&logo=openrouter&logoColor=white)
![Vercel AI SDK](https://img.shields.io/badge/Vercel%20AI%20SDK-000000?style=flat-square&logo=vercel&logoColor=white)
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
![React Testing Library](https://img.shields.io/badge/React%20Testing%20Library-E33332?style=flat-square&logo=testinglibrary&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Hypothesis](https://img.shields.io/badge/Hypothesis-BD1C2B?style=flat-square)
![MSW](https://img.shields.io/badge/MSW-FF6A33?style=flat-square&logo=mockserviceworker&logoColor=white)
![axe-core](https://img.shields.io/badge/axe--core-FF6F00?style=flat-square)
![Lighthouse CI](https://img.shields.io/badge/Lighthouse%20CI-F44B21?style=flat-square&logo=lighthouse&logoColor=white)
![c8](https://img.shields.io/badge/c8-000000?style=flat-square)

**Cloud & DevOps:**
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Sentry](https://img.shields.io/badge/Sentry-362D59?style=flat-square&logo=sentry&logoColor=white)
![Upstash](https://img.shields.io/badge/Upstash-00E9A3?style=flat-square&logo=upstash&logoColor=white)
![pnpm](https://img.shields.io/badge/pnpm-F69220?style=flat-square&logo=pnpm&logoColor=white)
![tsx](https://img.shields.io/badge/tsx-000000?style=flat-square)
![ESLint](https://img.shields.io/badge/ESLint-4B32C3?style=flat-square&logo=eslint&logoColor=white)
![oxlint](https://img.shields.io/badge/oxlint-000000?style=flat-square)
![commitlint](https://img.shields.io/badge/commitlint-000000?style=flat-square&logo=commitlint&logoColor=white)
![Prettier](https://img.shields.io/badge/Prettier-F7B93E?style=flat-square&logo=prettier&logoColor=black)
![semantic-release](https://img.shields.io/badge/semantic--release-494949?style=flat-square&logo=semanticrelease&logoColor=white)
![Gitleaks](https://img.shields.io/badge/Gitleaks-FF0000?style=flat-square)
![PostHog](https://img.shields.io/badge/PostHog-000000?style=flat-square&logo=posthog&logoColor=white)
![pino](https://img.shields.io/badge/pino-000000?style=flat-square)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-425CC7?style=flat-square&logo=opentelemetry&logoColor=white)

---

## Contact & Writing

- **LinkedIn:** [in/fabiorborges](https://www.linkedin.com/in/fabiorborges) — fastest reply
- **Portfolio:** [flabs.tech](https://flabs.tech) — projects, writing, and contact form
- **npm:** [agenthood](https://www.npmjs.com/package/agenthood) — latest published package

---

*Last updated: Nov 25, 2026
