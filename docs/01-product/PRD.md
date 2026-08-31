# Product Requirements Document (PRD)

## Project Overview
- **Project Name:** University Admissions Intelligent Assistant (RAG) with Next.js 15, PixiJS & OpenCode Reasoning Engine
- **Target Role:** AI Backend & Full Stack Engineer
- **Domain:** Higher Education / Technological University Admissions (Nova Tech University)
- **Document Version:** 2.6.0
- **Status:** Implemented & Verified (100% Test Pass Rate, 19/19 Tests)

---

## 1. Problem Statement
The admissions office of Nova Tech University receives hundreds of repetitive inquiries daily across digital channels regarding academic programs, course syllabi, tuition payment plans, scholarship criteria, admissions calendars, campus housing, credit transfers, career services, specialized labs (such as the NVIDIA H100 GPU cluster), international exchanges, and graduation requirements.

Human admission counselors spent excessive time repeatedly answering standard FAQ inquiries, leading to long wait times, applicant churn, and high operational costs.

---

## 2. Solution Goals & Non-Goals

### Goals
- **Interactive Guided Navigation (9 Options & 8 Thematic Submenus):** Provide a structured numbered menu system (1 to 9 with 40 leaf sub-queries) allowing applicants to navigate official information via single-digit inputs or clickable action buttons.
- **Strict Document Grounding (87 Official Documents & 264 Chunks):** Base all responses strictly on 87 verified university documents across 7 thematic clusters (syllabi, labs, international mobility, banking, student life, career partnerships, regulations), eliminating hallucinations.
- **High-Performance Python Intermediary with OpenCode Deep Reasoning (`Web` ➔ `Python` ➔ `OpenCode`):** Real-time integration routing Option 9 ("Hablar con un Asesor") and open-ended queries to OpenCode acting as the empathetic Human Admissions Advisor, with multi-document high-density context injection.
- **Modern Next.js 15 + PixiJS Web Application:** Goth-Tech visual design with WebGL particle constellation background, collapsible sidebar, Framer Motion transitions, live telemetry polling, and native GFM Markdown rendering (`react-markdown` + `remark-gfm`).
- **Cross-Platform Executables & Supervisor Launcher:** One-click installer (`installer.py`, `install.bat`, `install.sh`) and process supervisor (`run.py`, `start.bat`, `start.sh`) running OpenCode (:4096), FastAPI (:8000), and Next.js (:3000) simultaneously with graceful `SIGINT` termination.
- **Hybrid Retrieval with Auto-Fitting BM25:** Combine dense cosine vector similarity with pure Python BM25 lexical keyword matching and Spanish morphological suffix stemming.
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
