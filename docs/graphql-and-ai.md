# GraphQL & API Engineering

![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![Apollo](https://img.shields.io/badge/Apollo-311C87?style=flat-square&logo=apollographql&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![WunderGraph](https://img.shields.io/badge/WunderGraph-FF4785?style=flat-square)
![New Relic](https://img.shields.io/badge/New_Relic-008C99?style=flat-square&logo=newrelic&logoColor=white)

GraphQL and Apollo are at the core of how I design and ship backend APIs. I work schema-first, treat the SDL as a contract, and enforce type safety end-to-end via TypeScript code generation.

**Recent Experience — BairesDev (Dec 2025 – present)**

- Engineered automated AI checkout systems using **GraphQL federation** for major US telecom partners, processing **1,000+ daily transactions**
- Architected **federated subgraph solutions** end-to-end: API analysis → subgraph design → CI/infrastructure setup → production rollout
- Used **WunderGraph** as the federation gateway layer — routing, composition, and type-safe client generation across subgraphs
- Implemented **New Relic flow-tracking instrumentation** for real-time observability across the federated graph
- Stack: GraphQL · Apollo Federation · WunderGraph · TypeScript · Node.js · AWS · Clean Architecture · OpenAPI · New Relic

**Apollo Server & Federation**

- Apollo Server with TypeScript — typed resolvers, context setup, plugin authoring
- Apollo Federation: distributed subgraph schemas unified behind a single gateway; each domain owns its slice of the graph
- Federated entities, `@key` directives, reference resolvers, and cross-subgraph extends patterns
- Gateway-level query planning, subgraph health checks, and graceful degradation

**Schema Design**

- Schema-first: SDL defines the contract before implementation starts — shared between frontend, backend, and QA
- Nullable vs non-null discipline: every field decided intentionally, not defaulted
- Input types, custom scalars, enums, and union/interface patterns for polymorphic domains
- Versioning strategy: additive evolution, deprecation workflow, breaking-change detection in CI

**Resolvers & Data Layer**

- N+1 elimination via DataLoader — batching and per-request caching as a standard practice, not an afterthought
- Query complexity analysis and depth limits to protect backend services from abusive queries
- Resolver middleware chains for auth (JWT / API key), rate limiting, and audit logging
- Cursor-based pagination (`first`/`after`) and offset pagination depending on data access patterns

**Mutations & Subscriptions**

- Input validation at the GraphQL layer (before business logic) — schema-enforced constraints + custom validation
- Subscription resolvers with `PubSub` / Redis channels for real-time data delivery
- Error handling: typed error unions vs generic `GraphQLError`, client-readable codes

**Performance & Observability**

- Response caching: `@cacheControl` directives, CDN-compatible GET caching for persisted queries
- Persisted queries (APQ) to reduce payload size and enable CDN caching
- New Relic flow-tracking + resolver-level tracing for production federated graphs
- Schema change alerting and performance regression detection integrated into CI

**AI-Assisted Development**

- Daily use of [Claude Code](https://claude.ai/code) for schema review, resolver implementation, test generation, and refactoring
- Built [Agenthood](https://github.com/fworks-tech/agenthood) — an open-source AI agent framework that enforces code quality, commit standards, and PR review discipline through 14 specialized agent skills

---

# Agentic AI Knowledge

Working at the intersection of production AI systems and software engineering. Key domains:

**Reasoning & Planning**

- ReAct loops (Reason + Act cycles), Chain-of-Thought, Tree-of-Thought
- Multi-step agentic workflows with human-in-the-loop approval gates
- Goal chaining across sessions, rollback on rejection

**Memory Architecture**

- 5-tier memory: Short-Term (working context) → Long-Term (persistent facts) → Episodic (past executions) → Project (per-project adaptation) → Residual (decay-weighted trace signals)
- Context compression before LLM calls (token budget management)
- Memory governance: TTL, retention policies, per-project namespacing

**Retrieval-Augmented Generation**

- Agentic RAG: agent decides _whether, what, and when_ to retrieve — not a mandatory pipeline step
- Hierarchical Parent→Child chunking: child embeds for precision, parent retrieved for context
- Knowledge Graph DB (`IGraphStore`): structural/relationship queries alongside vector similarity
- Tree-sitter: deterministic AST parsing for TypeScript/Python/Go — real code entity extraction

**Multi-Agent Orchestration**

- Orchestrator pattern: user → validator → queue → orchestrator → member → safety guard → response
- 14 specialized members over one general-purpose agent
- Society self-awareness: `SocietyIndexer` + `OracleAgent` — any member can query the collective institutional memory
- Dynamic model routing: `ComplexityScorer` → cheap model (Groq/local) or capable model (Anthropic) by query budget

**Production Hardening**

- RiskManager: per-tool constraint validation, process sandboxing (filesystem/network allowlists)
- `IProtocol`: typed failure modes and retry policies for agent-to-user, agent-to-agent, and agent-to-tool surfaces
- EvalRunner: automated quality metrics (hallucination rate, relevance, groundedness, latency)
- EpisodeLearner: self-improving feedback loop — eval scores → long-term memory → better future responses

**Agent-Agnostic Design**

- Skills as Markdown files — portable across Claude Code, GitHub Copilot, Gemini CLI, OpenAI Codex CLI, CodeBuddy
- `ILLMProvider` abstraction with automatic failover across providers
- Groq as default free provider; Ollama for fully offline execution
