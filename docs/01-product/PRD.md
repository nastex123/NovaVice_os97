# Product Requirements Document (PRD)

## Project Overview
- **Project Name:** Nova Idiomas Colombia Admissions Intelligent Assistant (RAG) with "Nova OS '97" Retro UI, Next.js 15 & Dual Reasoning Engine (OpenCode + AGY Antigravity)
- **Target Role:** AI Backend & Full Stack Engineer
- **Domain:** Language Academy & Higher Education Admissions (Nova Idiomas Colombia)
- **Document Version:** 2.6.0
- **Status:** Implemented & Verified (100% Test Pass Rate, 25/25 Tests)

---

## 1. Problem Statement
The admissions department of Nova Idiomas Colombia receives hundreds of repetitive inquiries daily across digital channels regarding language programs (English, French, German, Italian, Portuguese, Spanish for foreigners), class schedules (morning, afternoon, after-work evening, Saturdays, Sundays), COP tuition pricing, installment payment plans (0% interest), level placement tests, international certifications (IELTS, TOEFL, Cambridge, DELF/DALF, Goethe), and campus locations (Bogota Chicó/Chapinero, Medellin Poblado/Laureles, Cali Granada, and 100% Virtual Sync).

Human admission counselors spent excessive time repeatedly answering standard FAQ inquiries, leading to long wait times, applicant churn, and high operational costs.

---

## 2. Solution Goals & Non-Goals

### Goals
- **Interactive Guided Navigation (Root Menu & Pillar Submenus):** Provide a structured numbered menu system (Options 1 to 4 with sub-options and root menu 0) allowing applicants to navigate official information via single-digit inputs or clickable action buttons.
- **Strict Document Grounding (82 Official Documents & 245 Chunks):** Base all responses strictly on 82 verified institutional documents across all language courses, schedules, COP pricing, refund policies, international certifications, and campus venues, eliminating hallucinations.
- **Dual AI Advisor Engine (OpenCode Daemon vs AGY Antigravity CLI):** Pre-launch supervisor switch (`run.py -a [opencode|agy]`) allowing dynamic selection between local OpenCode reasoning daemon (:4096) and Google Antigravity (AGY) reasoning engine with multi-document high-density context injection.
- **"Nova OS '97" Poolsuite / GTA Vice City Retro Web Application:** Macintosh '97 retro desktop experience with live vintage 1997 clock, striped titlebars, CRT optical anti-glare filter with ON/OFF switch, warm anti-fatigue color palette, and high-density animated pixel-art tropical palms, clouds and seagulls (GPU 60 FPS).
- **Cross-Platform Executables & Supervisor Launcher:** One-click installer (`installer.py`, `install.bat`, `install.sh`) and process supervisor (`run.py`, `start.bat`, `start.sh`) running FastAPI (:8000), Next.js (:3000), and OpenCode (:4096 when active) simultaneously with graceful `SIGINT` termination.
- **Hybrid Retrieval with Auto-Fitting BM25:** Combine dense cosine vector similarity (ChromaDB) with pure Python BM25 lexical keyword matching and Spanish morphological suffix stemming.
- **Graceful Multi-Channel Escalation:** Reliably detect out-of-scope inquiries (threshold < 0.50), log structured tracking tickets (`ESC-YYYYMMDD-XXXX`), and dispatch webhook notifications.
- **Dual-Layer Caching & Observability:** Sub-30ms cache hits, automated document-invalidation triggers, JSON telemetry (`/api/v1/metrics`), and Prometheus metrics (`/metrics/prometheus`).

### Non-Goals
- Automated final degree certification without human committee approval.
- Direct credit card billing inside the chat interface.
- Open-ended arbitrary chit-chat unrelated to the university's academic offerings and admissions.
- **Merit-based scholarships (becas):** Nova does not offer `beca` scholarships; only discounts (10% contado, 15% cajas/familiar, $100k bono) per `12_04_becas_descuentos_aclaratoria.md` and `ADR-008`. Queries about `becas` map to discounts to avoid hallucination.

---

## 3. User Personas & User Stories

### User Personas
1. **Prospective Student (Applicant):** Seeks clear, instant details on programs, syllabi, labs, tuition, housing, international exchanges, scholarships, and transfers.
2. **Admissions Counselor (Human Staff):** Reviews structured escalation tickets and collaborates with OpenCode advisor sessions.
3. **University AI/IT Administrator:** Monitors system health, Prometheus telemetry, and knowledge base indexing.

### User Stories
- **US-01 (Guided Exploration):** *As an applicant, I want to type numbers (1 to 4) or click buttons to explore programs, schedules, COP pricing, and campuses step-by-step, with 80+ natural language variants (horario/precio/beca→descuento/curso/modalidad/sede).*
- **US-02 (Human Advisor via OpenCode Deep Reasoning — Heavy Only):** *As an applicant seeking personalized guidance for very heavy cases (visa, legal, beca 100%), I want escalation only after 2-phase confirmation (show best chunk + “¿Sí/No?”), not for routine pilar queries.*
- **US-07 (Becas→Descuentos):** *As an applicant asking about scholarships, I want a clear answer that Nova has no merit becas but offers 10%/15% descuentos, grounded in `12_04_becas_descuentos_aclaratoria.md`.*
- **US-03 (Clean Markdown Typography):** *As an applicant, I want to read structured responses with custom glowing bullet points, callout quote boxes, and clear headers without raw markdown symbols.*
- **US-04 (Curriculums & Labs):** *As an engineer applicant, I want to inspect specific course syllabi (e.g. CS-201 Algorithms) or GPU research cluster specs (NVIDIA H100).*
- **US-05 (International Mobility):** *As a foreign student, I want to verify I-20 visa procedures and exchange programs with TU Munich or Tokyo Tech (JASSO scholarship).*
- **US-06 (One-Click Launch):** *As a user or evaluator, I want to run `start.bat` or `start.sh` to boot the entire system (backend, OpenCode, and frontend) simultaneously.*

---

## 4. Functional Requirements Matrix

| ID | Requirement | Priority | Implementation Component | Status |
| :--- | :--- | :---: | :--- | :---: |
| **FR-01** | Pure Python RAG Engine (No LangChain/n8n) | P0 | `src/rag/engine.py` | Complete |
| **FR-02** | Hybrid Search (Dense Cosine + Auto-Fitting BM25) | P0 | `src/rag/hybrid_retriever.py` | Complete |
| **FR-03** | 83 Official Documents & 245 Chunks Corpus (+ `12_04` becas→descuentos) | P0 | `data/documents/` (20 Clusters, 83 docs) | Complete (Fase 0) |
| **FR-04** | Guided Menu State Machine (1-4 pillars, 24 leaves, `0` return) + 80 intent synonyms + threshold pilar 0.35 vs heavy 0.50 | P0 | `src/core/navigation.py:163,330` | Planned (Fase A/D) |
| **FR-05** | Python Intermediary Bridge to OpenCode (Port 4096) | P0 | `src/core/opencode_client.py` | Complete |
| **FR-06** | OpenCode Multi-Document Deep Reasoning (45s window) | P0 | `src/core/opencode_client.py` | Complete |
| **FR-07** | Next.js 15 + PixiJS Web Frontend (App Router, Tailwind) | P0 | `frontend/` | Complete |
| **FR-08** | GFM Markdown Renderer (`react-markdown` + `remark-gfm`) | P0 | `frontend/src/components/ChatContainer.tsx` | Complete |
| **FR-09** | Cross-Platform Installer & Process Launcher (`run.py`) | P0 | `installer.py`, `run.py`, `.bat`, `.sh` | Complete |
| **FR-10** | Pre-Flight Prompt Injection Guardrail | P0 | `src/core/guardrails.py` | Complete |
| **FR-11** | Automated Human Escalation Logging (`escalations.json`) — Heavy Only (2-phase Sí/No, lista negra very heavy) | P1 | `src/core/dispatcher.py:24`, `engine.py:220` | Planned (Fase D31-40) |
| **FR-12** | Dual Cache with File-Hash Invalidation + Semantic 0.88 pilar (vs 0.95) | P1 | `src/core/cache.py:47` `vector_store.py:167` | Implemented (Fase 2) + Planned (B20) |
| **FR-13** | SSE Real-Time Streaming (`/api/v1/chat/stream`) | P1 | `src/api/routes.py` | Complete |
| **FR-14** | JSON & Prometheus Telemetry (`/metrics/prometheus`) | P1 | `src/core/metrics.py` | Complete |
| **FR-15** | Automated Pytest Test Suite (55/55 Tests Passed) | P0 | `tests/` | Complete |

---

## 5. Strategic Roadmap & Phased Implementation (50 Proposals)

The long-term technical evolution of Nova OS '97 is organized into **5 sequential phases** covering 50 architectural proposals without touching security guardrails.

For full technical specifications, acceptance criteria, and category breakdowns, refer to:
- 📖 **[Roadmap Maestro de 50 Propuestas Técnicas (docs/01-product/ROADMAP_50_PROPOSITAS.md)](ROADMAP_50_PROPOSITAS.md)**
- 📖 **[Propuestas de Mejora Tecnológica (docs/03-architecture/technological-enhancement-proposals.md)](../03-architecture/technological-enhancement-proposals.md)**

| Phase | Core Objective | Key Deliverables | Status |
| :--- | :--- | :--- | :---: |
| **Phase 1** | **Data Precision & RAG Retrieval Quality** | Proposals 1-7, 19, 21, 23, 43 (Adaptive RRF, AST Table Chunker, Cross-Encoder, Semantic Cache) | **Completed** |
| **Phase 2** | **Backend Resilience & Persistence** | Proposals 11-16, 20, 22, 45, 46 (SSE Stream, HTTP Pool, Circuit Breaker, SQLite WAL, Docker) | **Completed** |
| **Phase 3** | **Modern Frontend & Accessible Retro UI** | Proposals 25-30, 33-36 (Zustand, SSE Reader, Virtualization, WebGL CRT, WCAG AAA Mode) | **Completed** |
| **Phase 4** | **Automated Testing & Developer Experience** | Proposals 39-44, 47-49 (RAG Evaluation Pipeline, Mutation Testing, Locust, CLI Doctor) | **Planned** |
| **Phase 5** | **Future Horizons & Specialized Deployments** | Proposals 8-10, 17, 18, 24, 31, 32, 37, 38, 50 (Graph RAG, Web Audio, Tauri Kiosk Mode) | **Planned** |

