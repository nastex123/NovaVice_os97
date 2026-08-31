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

---

## 3. User Personas & User Stories

### User Personas
1. **Prospective Student (Applicant):** Seeks clear, instant details on programs, syllabi, labs, tuition, housing, international exchanges, scholarships, and transfers.
2. **Admissions Counselor (Human Staff):** Reviews structured escalation tickets and collaborates with OpenCode advisor sessions.
3. **University AI/IT Administrator:** Monitors system health, Prometheus telemetry, and knowledge base indexing.

### User Stories
- **US-01 (Guided Exploration):** *As an applicant, I want to type numbers (1 to 9) or click buttons to explore programs, syllabi, labs, tuition, deadlines, and scholarships step-by-step.*
- **US-02 (Human Advisor via OpenCode Deep Reasoning):** *As an applicant seeking personalized guidance, I want to speak with an advisor (Option 9) and receive empathetic, comprehensive answers synthesized from all official documents.*
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
| **FR-03** | 87 Official Documents & 264 Chunks Corpus | P0 | `data/documents/` (7 Clusters) | Complete |
| **FR-04** | Guided Menu State Machine (1-9, 8 Submenus, '0' return) | P0 | `src/core/navigation.py` | Complete |
| **FR-05** | Python Intermediary Bridge to OpenCode (Port 4096) | P0 | `src/core/opencode_client.py` | Complete |
| **FR-06** | OpenCode Multi-Document Deep Reasoning (45s window) | P0 | `src/core/opencode_client.py` | Complete |
| **FR-07** | Next.js 15 + PixiJS Web Frontend (App Router, Tailwind) | P0 | `frontend/` | Complete |
| **FR-08** | GFM Markdown Renderer (`react-markdown` + `remark-gfm`) | P0 | `frontend/src/components/ChatContainer.tsx` | Complete |
| **FR-09** | Cross-Platform Installer & Process Launcher (`run.py`) | P0 | `installer.py`, `run.py`, `.bat`, `.sh` | Complete |
| **FR-10** | Pre-Flight Prompt Injection Guardrail | P0 | `src/core/guardrails.py` | Complete |
| **FR-11** | Automated Human Escalation Logging (`escalations.json`) | P1 | `src/core/dispatcher.py` | Complete |
| **FR-12** | Dual Cache with File-Hash Invalidation | P1 | `src/core/cache.py` | Complete |
| **FR-13** | SSE Real-Time Streaming (`/api/v1/chat/stream`) | P1 | `src/api/routes.py` | Complete |
| **FR-14** | JSON & Prometheus Telemetry (`/metrics/prometheus`) | P1 | `src/core/metrics.py` | Complete |
| **FR-15** | Automated Pytest Test Suite (19/19 Tests Passed) | P0 | `tests/` | Complete |
