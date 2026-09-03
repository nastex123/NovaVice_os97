# 🌴 Nova Idiomas Colombia — "Nova OS '97" Admissions Assistant (v2.6.0)

<div align="center">

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Language: Español](https://img.shields.io/badge/Language-Español-green.svg)](EXPLICACION_TECNICA.md)
[![Tests: 55/55 Passed](https://img.shields.io/badge/Tests-55%2F55%20Passed-brightgreen.svg)](backend/tests/)
[![Benchmark: 80/80 Passed](https://img.shields.io/badge/Benchmark-80%2F80%20(100%25)-brightgreen.svg)](scripts/test_variants.py)
[![Next.js 15](https://img.shields.io/badge/Frontend-Next.js%2015-black.svg)](frontend/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.115-009688.svg)](backend/)
[![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-orange.svg)](backend/data/chroma_db/)

</div>

> **Intelligent Admissions & Student Support Assistant with Hybrid RAG (FastAPI + Next.js 15), Decoupled Dual Deep Reasoning Engine Switch (OpenCode / AGY Antigravity), and a 90s Retro Desktop Experience with an Optical CRT Anti-Glare Filter.**  
> Designed to provide verified, zero-hallucination answers regarding **language courses, official schedules, tuition in Colombian Pesos (COP), international certifications (IELTS, TOEFL, Cambridge, DELF, Goethe), and campus locations**, with seamless automated escalation to human counselors.

---

## 📚 Technical Documentation & Master Guides

* 📖 **[Master Technical Presentation & Architecture Guide (English)](TECHNICAL_EXPLANATION.md):** Exhaustive 12-section technical manual, Mermaid UML diagrams, code snippets with file paths, and step-by-step request traces.
* 📖 **[Guía Maestra de Explicación Técnica (Español)](EXPLICACION_TECNICA.md):** Manual técnico exhaustivo en Español con paridad espejo 1:1, arquitectura de código, diagramas y trazas didácticas.
* 📜 **[Changelog](CHANGELOG.md):** Chronological log of all additions, refactors, and releases tracked under `America/Bogota` timezone.
* 🏛️ **[Architecture & Decision Records (docs/)](docs/):** System PRD, engineering deep-dives, AI integrations, and ADRs (ADR-001 through ADR-008).

---

## 📌 Business Use Case & Solution Overview

**Nova Idiomas Colombia** operates physical campuses across **Bogotá (Chicó & Chapinero)**, **Medellín (El Poblado & Laureles)**, **Cali (Granada)**, and an active **100% Virtual Synchronous** division. It handles hundreds of daily inquiries:
- **Language Programs:** General English, Intensive 40h/month, Business English, French DELF/DALF, German Goethe, Italian, Portuguese, Spanish for foreigners. Communicative *Flipped Classroom* methodology.
- **Schedules & Shifts:** Early Birds (6:00-8:00 AM), Daytime (Mornings/Afternoons), After-Work Evenings (6:30-8:30 PM), Saturdays, and Sundays.
- **Tuition & Financing (COP):** Official rates in Colombian Pesos, 10% lump-sum cash discount, 3-installment interest-free plans (40% initial, 30% month 1, 30% month 2), and compensation fund partnerships (Compensar, Colsubsidio, Cafam, Comfama).
- **Placement Testing:** 100% free Diagnostic Placement Test with automated scheduling.
- **Official Certifications:** Complete preparation for IELTS Academic/General, TOEFL iBT, Cambridge B2/C1, DELF/DALF, and Goethe.

---

## 📂 Repository Architecture (Clean Monorepo)

```text
synapse-admissions-ai/ (NovaVice_os97)
├── backend/                               # 🐍 FastAPI Backend & AI Pipelines
│   ├── data/                              # Official Knowledge Base (82 docs) & Ticket Store
│   │   ├── documents/                     # Structured Markdown files (courses, prices, campuses)
│   │   ├── chroma_db/                     # Persistent ChromaDB vector storage
│   │   └── escalations.json               # Persisted human escalation tickets
│   ├── src/                               # Application source code
│   │   ├── api/                           # REST endpoints (/chat, /health, /metrics, /escalate)
│   │   ├── core/                          # Core logic (advisor_common, opencode_client, agy_client, navigation)
│   │   └── rag/                           # Retrieval-Augmented Generation (engine, hybrid_retriever, bm25)
│   ├── tests/                             # 55 Automated Pytest tests (unit, integration & e2e)
│   └── requirements.txt                   # Python dependencies
│
├── frontend/                              # 🌐 Next.js 15 Retro Web Application
│   ├── src/                               # Components, App Router & CRT global styles
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/                                  # 📚 System Documentation & Architectural Records
│   ├── 01-product/                        # Product Requirements Document (PRD)
│   ├── 03-architecture/                   # Architecture diagrams & technical proposals
│   ├── 04-engineering/                    # Deep-dive guides for backend, frontend & RAG
│   ├── 05-ai/                             # AI integrations (OpenCode & AGY Antigravity specification)
│   └── 09-decisions/                      # Architecture Decision Records (ADR-001 to ADR-008)
│
├── scripts/                               # 🛠️ Multiplatform Automation & Benchmarks
│   ├── test_variants.py                   # 80-variant linguistic benchmark runner (100% passed)
│   ├── installer.py                       # Cross-platform installation logic
│   ├── install.bat / install.sh           # Native Windows and Linux/macOS install scripts
│   └── start.bat / start.sh               # Native Windows and Linux/macOS launcher scripts
│
├── CHANGELOG.md                           # Chronological changelog (America/Bogota)
├── TECHNICAL_EXPLANATION.md               # Master technical presentation guide (English)
├── EXPLICACION_TECNICA.md                 # Master technical presentation guide (Spanish)
├── README.md                              # Main repository overview (English)
├── pytest.ini                             # Root Pytest discovery configuration
└── run.py                                 # Supervised launcher with interactive advisor selector
```

---

## 🏗️ System Layer Architecture (100% Python + Next.js 15)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER (NEXT.JS 15 FRONTEND)             │
│                                                                        │
│   Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS       │
│   ├── Macintosh OS '97 Window (Pinstripe titlebar, vintage controls)   │
│   ├── CRT Anti-Glare Optical Filter (Scanlines + Amber Phosphor + SW)  │
│   ├── Living Pixel-Art Background (8 Palms + 18 Clouds + Gulls + Grass)│
│   ├── Safe GFM Markdown Renderer with HTML Sanitization                │
│   └── Real-time Telemetry Modal (Latency, Tokens, Cost, Cache Ratio)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (:3000 -> :8000)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   API GATEWAY & ROUTING (FASTAPI BACKEND)              │
│                                                                        │
│   FastAPI Core Engine (:8000) + Pydantic v2 Models                     │
│   ├── POST /api/v1/chat       (Conversational query & menu navigation) │
│   ├── GET  /api/v1/health     (Health status, indexed docs, advisor)   │
│   ├── GET  /api/v1/metrics    (Live telemetry, cache rates & tokens)   │
│   └── POST /api/v1/escalate   (Human escalation ticket creation)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               SECURITY GUARDRAILS LAYER (ZERO-TRUST PIPELINE)          │
│                                                                        │
│   Pre-Flight Safety Checks                                             │
│   ├── Prompt Injection Detection (DAN, jailbreaks, instruction bypass) │
│   └── Input Sanitization, Unicode Normalization & Length Bounds        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              DETERMINISTIC ROUTING & DUAL-LAYER CACHE                  │
│                                                                        │
│   ├── Guided State Machine Navigation (Options 1..4, Submenus & 0)     │
│   │     └─► Instant Deterministic Return (<4ms, 0 tokens spent)        │
│   │                                                                    │
│   └── Dual-Layer Query Cache (SHA-256 Hash + Semantic Cosine Match)    │
│         └─► Cache Hit: Sub-30ms Return                                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Cache Miss / Open-Ended Query)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     HYBRID RAG RETRIEVAL PIPELINE                      │
│                                                                        │
│   1. Dense Vector Store (ChromaDB + Local ONNX `all-MiniLM-L6-v2`)     │
│   2. Sparse Lexical Store (Pure Python Okapi BM25 + Spanish Stemmer)   │
│   3. Rank Fusion (Reciprocal Rank Fusion RRF, k = 60)                  │
│   4. Relevance Guardrail (Threshold 0.50 -> Human Ticket Escalation)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               DECOUPLED DUAL ADVISOR REASONING LAYER                   │
│                                                                        │
│   [Core Prompting & Fallback: advisor_common.py]                       │
│   ├── [Option 1: OpenCode Server (:4096)] via opencode_client.py       │
│   └── [Option 2: AGY Antigravity CLI] via agy_client.py                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Hybrid RAG over 82 Official Institutional Documents (245 Chunks):**
   - Grounded ChromaDB vector indexing and BM25 lexical keyword recall over all language courses, schedules, COP pricing, campuses, and regulations.
   - 100% grounded responses eliminating hallucinations.

2. **Decoupled Dual Advisor Engine Selector (OpenCode vs AGY):**
   - Choose interactively or via CLI flags at boot time:
     - `[1] 🤖 OpenCode Reasoning Engine (:4096)`
     - `[2] 🚀 AGY (Google Antigravity CLI / Engine)`
   - **Reasoning Parity:** Both engines generate rich, complete Markdown tables and structured payment schedules backed by `advisor_common.py`.

3. **Retro "Nova OS '97" Frontend with Anti-Glare CRT Filter:**
   - Nostalgic design inspired by Poolsuite.net and GTA Vice City 80s/90s aesthetics.
   - **Optical CRT Screen Filter:** Subtle horizontal scanlines and warm amber phosphor actively reducing eye fatigue, with an interactive `[ 📺 CRT: ON/OFF ]` switch.
   - **Living Tropical Pixel-Art Landscape:** 8 depth-layered swaying palm trees, 18 bidirectional volumetric drifting clouds, 6 flocks of seagulls with authentic 2-state wing flapping, and a retro pixel-grass carpet with 28 swaying tufts running at 60 FPS GPU hardware acceleration.

4. **Deterministic Guided Navigation & Zero Hallucination Guardrails:**
   - Structured 4-pillar menu navigation (1. Courses, 2. Schedules, 3. COP Pricing, 4. Admissions/Campuses, with 0 root reset).
   - Strict confidence evaluation: automatically generates a tracking ticket `ESC-YYYYMMDD-XXXX` and escalates out-of-scope queries to human admissions staff.

5. **Real-Time Telemetry & Token Cost Tracking:**
   - Collapsible retro telemetry modal tracking total queries, cache hit ratios, human escalation rates, token consumption, and pillar distribution.

---

## ⚡ Quickstart & Installation

### Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- **Node.js (v18+) & npm**

### 1. Automatic Installation
```bash
# On Linux / macOS:
./install.sh

# On Windows:
install.bat
```
*(Automatically initializes the virtual environment, installs Python and Node.js dependencies, and indexes the 82 knowledge base documents in ChromaDB).*

### 2. Launch with Advisor Engine Selector
```bash
# Interactive mode (prompts to choose between OpenCode and AGY):
./start.sh
# or on Windows: start.bat
# or with Python: python run.py

# Launch directly with AGY (Google Antigravity CLI):
python run.py --advisor=agy

# Launch directly with OpenCode:
python run.py --advisor=opencode
```

When started, all services boot concurrently:
- 🌐 **Retro Nova OS '97 Frontend:** [http://localhost:3000](http://localhost:3000)
- 🐍 **FastAPI Core Backend:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📖 **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📊 **Prometheus Metrics:** [http://127.0.0.1:8000/metrics/prometheus](http://127.0.0.1:8000/metrics/prometheus)

---

## 🔌 REST API Endpoints

- `POST /api/v1/chat`: Interactive conversational query with structured RAG response and quick action buttons.
- `POST /api/v1/chat/stream`: Token-by-token streaming responses (Server-Sent Events / SSE).
- `POST /api/v1/webhook`: Universal webhook endpoint for CRM, form, and external channel integrations.
- `POST /api/v1/tools/quote`: Dynamic COP course quote calculator with cash and installment discounts.
- `POST /api/v1/tools/placement-test`: Free diagnostic placement test registration.
- `GET /api/v1/metrics`: Live JSON telemetry and runtime statistics.
- `GET /api/v1/escalations`: Persisted log of human escalation tickets.
- `GET /api/v1/health`: System health status, indexed document count, and active advisor engine.

---

## 🧪 Automated Testing & Benchmarks

The project includes an exhaustive suite of unit, integration, and E2E tests in Pytest:

```bash
pytest backend/tests -v
```

```text
============================= 55 passed in ~27s ==============================
```

And a linguistic benchmark validating 80 real-world user variants:
```bash
python scripts/test_variants.py
```

```text
===========================================================================
RESULTS: 80/80 PASSED (100.0%) | 0 FAILED | AVERAGE LATENCY: 26.5ms
===========================================================================
```

---

## URL: https://github.com/nastex123/NovaVice_os97.git
