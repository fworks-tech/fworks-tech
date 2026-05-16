# Hi, I am Fábio Ritzel Borges

**GraphQL · React · Next.js · GenAI / RAG**

Senior **full-stack engineer** based in **Joinville, Brazil**, focused on **TypeScript**, **Node.js**, **React**, and **Python** — from product UI to federated APIs, GenAI/RAG demos, tests, and production operations. I care about **clean architecture**, **performance (Core Web Vitals)**, **accessibility-first delivery (WCAG 2.1–oriented)**, and **reliable delivery**.

**Open to senior / staff remote roles** (international teams).  
Portfolios: **[fritzelborges.vercel.app](https://fritzelborges.vercel.app)** · **[fworks-tech.vercel.app](https://fworks-tech.vercel.app/)** (old portfolio)

---

## Featured work

- **[fworks-tech.vercel.app](https://fworks-tech.vercel.app/)** — [repo](https://github.com/fworks-tech/fworks.tech) — old portfolio page and full-stack showcase (Next.js)
- **[fritzelborges](https://fritzelborges.vercel.app)** — [repo](https://github.com/fworks-tech/fritzelborges) — bilingual personal site (EN/PT) on Next.js 16
- **[VeriHire](https://verihire.streamlit.app/)** — [repo](https://github.com/fworks-tech/verihire) — assistive GenAI RAG demo: cross-check candidate documents before human review
- **[Jupyter-Crypto-Wizard](https://jupyter-crypto-wizard.streamlit.app/)** — [repo](https://github.com/fworks-tech/Jupyter-Crypto-Wizard) — Streamlit crypto intelligence workspace (routed dashboard, alerts, news, risk, newsletter, AI assistant)

### fworks.tech (old portfolio)

**[Live site](https://fworks-tech.vercel.app/)** · **[Repository](https://github.com/fworks-tech/fworks.tech)**

Earlier **FWORKS.tech** portfolio and full-stack showcase on **Next.js** (now hosted on Vercel; the `fworks.tech` domain is no longer active): project highlights, skills, experience narrative, and contact. Superseded by [fritzelborges.vercel.app](https://fritzelborges.vercel.app) as the primary portfolio.

### fritzelborges (personal site)

**[Live site](https://fritzelborges.vercel.app)** · **[Repository](https://github.com/fworks-tech/fritzelborges)**

Bilingual portfolio (**English** and **Portuguese**) built with **Next.js 16** (App Router), **React 19**, **TypeScript 6**, and **Tailwind CSS v4**. Resume-backed sections cover about, skills, experience (including pre-2020 roles), education, projects, and contact. **English** is the default locale (`/en`); `/pt` serves Portuguese. Locale routing uses `Accept-Language`, a `NEXT_LOCALE` cookie, and typed dictionaries under `src/i18n/`.

Recent milestones: production deploy on **Vercel** (`fritzelborges.vercel.app`), **Vitest** unit tests and **Playwright** E2E, **GitHub Actions CI** (lint, unit, E2E, build), **Dependabot** for grouped npm updates, sitemap/robots, and **WCAG 2.1–oriented** navigation (desktop anchors, mobile menu, language switcher).

### VeriHire (recent open source)

**[Live demo](https://verihire.streamlit.app/)** · **[Repository](https://github.com/fworks-tech/verihire)** · **[Project board](https://github.com/users/fworks-tech/projects/5)**

VeriHire is an **assistive** GenAI / RAG portfolio project for recruiters and hiring managers: compare a **job pack** (posting + notes), **resume**, and **cover letter**, surface **inconsistencies with citations**, and optionally use **OpenAI** for a structured JSON report. Built with **Python**, **Streamlit**, and **Chroma**; demo heuristics work without an API key.

Recent milestones: **MIT license**, **Python 3.12** deploy on Streamlit Community Cloud, **CI** (pytest + Ruff), **pre-commit**, unit tests, [CONTRIBUTING](https://github.com/fworks-tech/verihire/blob/main/CONTRIBUTING.md) guide, and a public roadmap on the project board.

**Ethics:** assistive only — not for automated hire/reject decisions. Public demos use **synthetic fixtures** only; do not commit real candidate PII.

### Jupyter-Crypto-Wizard

**[Live demo](https://jupyter-crypto-wizard.streamlit.app/)** · **[Repository](https://github.com/fworks-tech/Jupyter-Crypto-Wizard)**

**Jupyter-Crypto-Wizard** (Crypto Market Analyzer) is a **Streamlit** crypto intelligence workspace on **Python 3.11**: routed pages for **Dashboard**, **Alerts**, **News**, **Risk**, and **Newsletter**; a shared sidebar watchlist (up to **100 assets**), market-source and trend filters; KPI rows, price trends, risk panels, alerts feed, RSS news, and local newsletter subscribe. An in-app **AI assistant** answers short, context-grounded questions from the current watchlist snapshot (OpenAI-compatible provider with safe fallbacks). Market and news data use **Binance**, **CoinGecko**, and **Coinbase** adapters with mock/cached fallbacks when APIs are unset.

Recent milestones: **M4** routed navigation and snapshot-driven data pipelines (**v0.2.0**), expanded watchlist and sidebar UX (#41), **GitHub Actions CI** (unittest + Streamlit smoke, compile gates, Ruff lint/format, advisory maintainability), **AI assistant** MVP with grounding tests, launcher scripts, English README, and **MIT license**. Deployed on **Streamlit Community Cloud**.

**Ethics:** informational and assistive only — not financial advice; no autonomous trading or exchange execution. Public demos use provider fallbacks when keys are not configured.

---

## What I build

- **GraphQL & integration:** federated subgraphs, OpenAPI/WSDL analysis, resolvers, schema validation, CI and production readiness for telecom-scale integrations
- **React platforms:** reusable components, Storybook, Redux Toolkit, performance tuning (lazy loading, memoization, code splitting), Jest + Playwright
- **GenAI & data apps:** RAG pipelines, assistive document cross-check workflows (e.g. recruiting), Streamlit dashboards, LLM-assisted tooling
- **E‑commerce & data-heavy UIs:** performance, SEO, accessibility, and multi-region UX (Farfetch ecosystem experience)
- **Quality & observability:** New Relic instrumentation, Lighthouse-driven improvements, Cypress/Jest/Puppeteer, Sonar/Jenkins/GitLab pipelines

---

## Experience (short)

| Period | Role | Company | Focus |
|--------|------|---------|--------|
| 12/2025 – Present | Full-Stack TypeScript & Node Engineer | BairesDev | GraphQL subgraphs, telecom partners (AT&T, Cox, T‑Mobile, Windstream), observability, production ops |
| 01/2025 – 09/2025 | Full-Stack React & Node Engineer | BairesDev | React, Storybook, Redux Toolkit, Jest, Playwright, CWV, a11y, Tailwind / MUI / Styled Components |
| 01/2023 – 04/2024 | Full Stack Engineer | Present Technologies | Farfetch front-end performance & UX; Liminal Link rebuild; LinkGPT-style AI assistant |
| 08/2021 – 09/2022 | Senior Frontend Developer (lead 8 months) | DBC Company | Architecture, dashboards (Chart.js), WCAG, A/B testing |
| 07/2020 – 08/2021 | Senior Frontend Developer | Gofind | Dual apps, GitLab CI, REST, i18n, Node/AWS when needed |
| 06/2019 – 07/2020 | Senior Frontend Developer | SoftExpert | Enterprise React / Redux / MUI, Formik, Cypress |
| 06/2018 – 06/2019 | R&D Engineer I | TOTVS | Full lifecycle, Protractor training, quality |
| 06/2017 – 06/2018 | QA Technician | TOTVS | Protractor training, Jenkins CI, SonarQube |
| 06/2016 – 06/2017 | Intern | TOTVS | Internal web frameworks, e2e automation |

*May 2024 – Dec 2024: PUCPR postgraduate studies and portfolio / open-source work (old portfolio at [fworks-tech.vercel.app](https://fworks-tech.vercel.app/), VeriHire, and related projects). Oct – Nov 2025: gap between two separate BairesDev contracts.*

---

## Education

- **PUCPR** — Postgraduate, *Software Architecture, Data Science & Cybersecurity* (2025 – 2027)
- **UNINTER** — Associate's degree, *Systems Analysis and Development* (2018 – 2021)

---

## Stack (high level)

**Frontend:** TypeScript · React · Next.js · Tailwind CSS · Storybook  
**Backend & APIs:** Node.js · GraphQL · REST · Python · Streamlit  
**Data & AI:** SQL · MongoDB · Chroma · RAG / LLM  
**Cloud & ops:** AWS · Terraform · Docker · Git · New Relic · CloudWatch  

---

## Languages

- **English** — fluent (professional)
- **Portuguese** — native
- **Spanish / French** — elementary

---

## Interests

AI · machine learning · software architecture · full-stack development · automation · agents (portfolio tooling, e.g. VeriHire) · DevOps

---

## Contact

- **[fritzelborges.vercel.app](https://fritzelborges.vercel.app)**
- **[fworks-tech.vercel.app](https://fworks-tech.vercel.app/)** (old portfolio)
- **[LinkedIn](https://www.linkedin.com/in/fabiorborges)**

For email or phone, use LinkedIn messages or the contact form on fritzelborges.vercel.app.

---

*Last updated from GitHub profile & repos — May 16, 2026.*
