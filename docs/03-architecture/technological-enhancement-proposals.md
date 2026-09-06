# Technological Enhancement Proposals for Admissions RAG Assistant (Version 2.7.0)

- **Document Version:** 2.7.0
- **Status:** v2.6.0 Implemented & Verified / v2.7.0 Multi-Phase Roadmap Approved
- **Date:** 2026-09-04 (America/Bogota)
- **Scope:** Pure Python RAG Engine, Next.js 15 + Retro OS '97 CRT Frontend, Dual Reasoning Engine (OpenCode + AGY), ChromaDB Persistence, Observability & Multiplatform Tooling (Excluding Security).

---

## 1. Baseline Implementation Status (v2.6.0)

| Proposal | Enhancement Area | Status | Implementation Reference |
| :--- | :--- | :---: | :--- |
| **P-01** | Hybrid Search (Dense Cosine + Pure Python BM25 via RRF) | **Implemented** | `src/rag/hybrid_retriever.py` |
| **P-02** | 82 Official Documents & 245 Chunks Knowledge Base | **Implemented** | `data/documents/` (20 Clusters) |
| **P-03** | Interactive Guided State Machine (1-4 & Submenus + Freeform) | **Implemented** | `src/core/navigation.py` |
| **P-04** | Decoupled Dual Reasoning Engine (OpenCode :4096 & AGY CLI) | **Implemented** | `src/core/opencode_client.py` & `agy_client.py` |
| **P-05** | Next.js 15 + CRT Anti-Glare Optical Filter Retro OS '97 UI | **Implemented** | `frontend/` |
| **P-06** | Native GFM Markdown Renderer (`react-markdown` + `remark-gfm`) | **Implemented** | `frontend/src/components/ChatContainer.tsx` |
| **P-07** | Cross-Platform Installer & Process Launcher (`run.py`) | **Implemented** | `installer.py`, `run.py`, `.bat`, `.sh` |
| **P-08** | Automated Escalation Logging & Tracking Tickets (`ESC-YYYYMMDD-XXXX`) | **Implemented** | `backend/data/escalations.json` |
| **P-09** | Dual Invalidation-Aware Cache (Exact SHA-256 + Semantic Cosine) | **Implemented** | `src/core/cache.py` |
| **P-10** | Prometheus Metrics Exporter & Real-Time JSON Telemetry | **Implemented** | `src/core/metrics.py` |

---

## 2. Multi-Phase Strategic Enhancement Program (50 Proposals)

The comprehensive technical roadmap is organized into 5 phased releases across 7 architectural categories (excluding security guardrails).

### Phase 1: Core Data & RAG Retrieval Quality
*Target: Eliminating table chunk fragmentation, dynamic entity ranking, semantic cache acceleration.*
- **P-1.1 (Prop 1) [CRÍTICO]:** Adaptive RRF rank fusion weights ($k_{bm25}$ vs $k_{dense}$) for exact COP price figures and course codes.
- **P-1.2 (Prop 2) [CRÍTICO]:** Markdown AST semantic chunker preserving financial tables and schedules as atomic units.
- **P-1.3 (Prop 3) [CRÍTICO]:** CPU-optimized lightweight Cross-Encoder re-ranker prior to context injection.
- **P-1.4 (Prop 4) [RECOMENDADO]:** Pre-LLM deterministic semantic query router (<15ms latency).
- **P-1.5 (Prop 5) [RECOMENDADO]:** Extracted structured metadata indexing with ChromaDB boolean filters.
- **P-1.6 (Prop 6) [RECOMENDADO]:** Contextual compression with sentence-window retrieval.
- **P-1.7 (Prop 7) [RECOMENDADO]:** Phonetic & lemmatized normalizer for Colombian campus names (Chapinero, Laureles, Chicó).
- **P-1.8 (Prop 19) [CRÍTICO]:** Multi-tier in-memory semantic cache with cosine similarity >0.96 (<5ms response).
- **P-1.9 (Prop 21) [RECOMENDADO]:** ChromaDB HNSW parameter fine-tuning (`M=16`, `efConstruction=64`, -35% RAM).
- **P-1.10 (Prop 23) [RECOMENDADO]:** Disk-persisted serialized BM25 inverted index with checksum validation.
- **P-1.11 (Prop 43) [RECOMENDADO]:** CI validator for markdown documentation syntax and financial table schemas.

### Phase 2: Backend Architecture, Resilience & Persistence
*Target: Token streaming, persistent connection pools, ACID ticket storage and containerization.*
- **P-2.1 (Prop 11) [CRÍTICO]:** Server-Sent Events (SSE) token-by-token streaming endpoint (`/api/v1/chat/stream`).
- **P-2.2 (Prop 12) [CRÍTICO]:** Singleton `httpx.AsyncClient` connection pool for OpenCode/AGY reasoning communication.
- **P-2.3 (Prop 13) [RECOMENDADO]:** Exponential backoff and circuit breaker for LLM provider failover.
- **P-2.4 (Prop 14) [RECOMENDADO]:** ASGI Correlation ID (`X-Request-ID`) propagation for unified tracing.
- **P-2.5 (Prop 15) [RECOMENDADO]:** SQLite WAL transactional ticket storage replacing flat JSON writes.
- **P-2.6 (Prop 16) [RECOMENDADO]:** Pydantic V2 native serialization (`model_validate` / `model_dump_json`).
- **P-2.7 (Prop 20) [CRÍTICO]:** ChromaDB background vacuum, defragmentation and storage compaction routine.
- **P-2.8 (Prop 22) [RECOMENDADO]:** Dated snapshot and rollback manager for vector database stores.
- **P-2.9 (Prop 45) [CRÍTICO]:** Multi-stage production `docker-compose.yml` for unified local containerization.
- **P-2.10 (Prop 46) [CRÍTICO]:** Strict typed environment variable management with `pydantic-settings`.

### Phase 3: Frontend Modernization, Retro UI Engine & Accessibility
*Target: Global state centralization, progressive token stream rendering, GPU-accelerated CRT filter.*
- **P-3.1 (Prop 25) [CRÍTICO]:** Zustand global state management (chat, desktop windows, telemetry slices).
- **P-3.2 (Prop 26) [CRÍTICO]:** SSE UTF-8 stream reader with progressive typewriter effect.
- **P-3.3 (Prop 27) [RECOMENDADO]:** Message history list virtualization (`@tanstack/react-virtual`).
- **P-3.4 (Prop 28) [RECOMENDADO]:** Asynchronous session persistence using `IndexedDB`.
- **P-3.5 (Prop 29) [RECOMENDADO]:** React Server Components (RSC) boundary isolation in Next.js 15.
- **P-3.6 (Prop 30) [RECOMENDADO]:** Dynamic code splitting (`next/dynamic`) for secondary retro dialogs and modals.
- **P-3.7 (Prop 33) [CRÍTICO]:** WebGL / GPU-accelerated CRT optical filter reducing CPU usage.
- **P-3.8 (Prop 34) [RECOMENDADO]:** WCAG 2.1 AAA accessibility bypass mode with standard typography.
- **P-3.9 (Prop 35) [RECOMENDADO]:** Keyboard navigation and focus trap in retro OS '97 windowing system.
- **P-3.10 (Prop 36) [RECOMENDADO]:** Vintage hardware monitor sliders for phosphor, scanlines and curvature.

### Phase 4: Automated Testing, QA & Developer Experience
*Target: Continuous RAG evaluation, concurrent load testing, deterministic test mocks and diagnostic CLI.*
- **P-4.1 (Prop 39) [CRÍTICO]:** Continuous RAG evaluation pipeline tracking Answer Relevance and Faithfulness.
- **P-4.2 (Prop 40) [RECOMENDADO]:** Mutation testing (`mutmut`) on COP pricing and discount logic.
- **P-4.3 (Prop 41) [RECOMENDADO]:** Locust concurrent load simulation (`scripts/load_test.py`, 50 users).
- **P-4.4 (Prop 42) [RECOMENDADO]:** Deterministic `MockDualAdvisor` provider for sub-3s test execution.
- **P-4.5 (Prop 44) [OPCIONAL]:** Playwright visual snapshot regression tests for the OS '97 desktop.
- **P-4.6 (Prop 47) [RECOMENDADO]:** Automated pre-commit hooks running Ruff and ESLint/Prettier.
- **P-4.7 (Prop 48) [RECOMENDADO]:** Diagnostic CLI command `python run.py doctor`.
- **P-4.8 (Prop 49) [RECOMENDADO]:** Automated Mermaid architecture diagram validation in CI.

### Phase 5: Future Enhancements & Standalone Deployments
*Target: Graph RAG, HyDE, procedural retro audio, commercial export and kiosk mode.*
- **P-5.1 (Prop 8) [OPCIONAL]:** Hypothetical Document Embeddings (HyDE) for sparse questions.
- **P-5.2 (Prop 9) [OPCIONAL]:** Dynamic multi-embedding fallback orchestrator.
- **P-5.3 (Prop 10) [FUTURO]:** Lightweight Graph RAG for course prerequisite DAG traversal.
- **P-5.4 (Prop 17) [OPCIONAL]:** OpenMetrics Prometheus exporter with percentile latency breakdowns.
- **P-5.5 (Prop 18) [FUTURO]:** Background non-blocking document indexing worker with file watchers.
- **P-5.6 (Prop 24) [OPCIONAL]:** Human escalation ticket CSV/XLSX export endpoint.
- **P-5.7 (Prop 31) [OPCIONAL]:** Retro network disconnection dialog with offline reconnection handler.
- **P-5.8 (Prop 32) [FUTURO]:** Pluggable desktop window architecture (`DesktopAppWindow`).
- **P-5.9 (Prop 37) [OPCIONAL]:** Retro PDA / Palm OS responsive layout for mobile screens.
- **P-5.10 (Prop 38) [OPCIONAL]:** Procedural Web Audio mechanical keyboard clicks and retro bleeps (<2KB).
- **P-5.11 (Prop 50) [FUTURO]:** Native Tauri desktop standalone build for physical campus kiosk mode.

---

## 3. Master Reference

For exhaustive rationale, priority definitions, and phased execution schedules, refer to:
- 📖 [Roadmap Maestro de 50 Propuestas (docs/01-product/ROADMAP_50_PROPOSITAS.md)](../01-product/ROADMAP_50_PROPOSITAS.md)
- 📖 [Product Requirements Document (PRD.md)](../01-product/PRD.md)
- 📖 [Architecture Decision Records (docs/09-decisions/)](../09-decisions/)
