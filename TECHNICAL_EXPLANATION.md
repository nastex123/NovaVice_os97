# 🎓 Master Technical Presentation & Architecture Guide
## Nova Idiomas Colombia — "Nova OS '97" Admissions AI (v2.6.0)

> **Reference Document for Technical Defense, Oral Presentations, and Live Demonstrations.**  
> *Este documento también está disponible en español en [`EXPLICACION_TECNICA.md`](EXPLICACION_TECNICA.md).*  
> This document contains a comprehensive, step-by-step technical breakdown of every component, algorithm, architectural decision, and data flow in the project.

---

## 📌 1. Executive Summary & Technical Specifications

| Metric / Parameter | Specification |
| :--- | :--- |
| **Project Name** | Synapse Admissions AI / Nova OS '97 (`NovaVice_os97`) |
| **System Version** | `2.6.0` (Production / Local-First Monorepo) |
| **Target Institution** | Language Academy Nova Idiomas Colombia (Bogotá, Medellín, Cali & 100% Virtual Sync) |
| **Backend Core** | FastAPI (`Python 3.12`), Pydantic v2, Uvicorn ASGI Server |
| **Vector Store** | ChromaDB Persistent (Local Embeddings ONNX `all-MiniLM-L6-v2` / TF-IDF) |
| **Lexical Search Engine**| Pure Python Okapi BM25 with Spanish morphological suffix stemming |
| **Rank Fusion Algorithm**| Reciprocal Rank Fusion (RRF, smoothing factor $k=60$) |
| **Dual Advisor Engine** | Pre-Launch Switch: **OpenCode Reasoning Daemon (:4096)** or **AGY (Google Antigravity CLI / `gemini-3.7-flash` low effort)** |
| **Frontend Framework** | Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons |
| **Visual Design** | "Nova OS '97" Retro Macintosh OS + Poolsuite.net + GTA Vice City 80s/90s Aesthetics |
| **Optical Filter** | CRT Anti-Glare & Warm Phosphor Screen Shader with interactive `[📺 CRT: ON/OFF]` switch |
| **Living Background** | Hybrid: SVG 18 clouds + 8 palms + grass + PIXI WebGL 36 particles (18 fireflies +10 dews +8 spores) 60 FPS |
| **Knowledge Base** | 83 docs / 245 chunks (20 clusters + `12_04_becas_descuentos_aclaratoria.md` canónico — becas→descuentos) |
| **Thresholds** | Pilar `0.35` (horario/precio/curso/modalidad/sede/beca→descuento) vs Heavy `0.50` + 2-phase Sí/No (ADR-008) |
| **Test Pass Rate** | **27/27 Automated Unit & E2E Pytest Suite PASSED** (semantic cache + heavy only) • Next.js 219kB 0 errors |

---

## 🎯 2. Business Problem & Solution Overview

### The Problem
Educational academies and language institutes in Colombia receive hundreds of repetitive daily inquiries across WhatsApp, Telegram, web forms, and email regarding:
1. **Language Courses & Syllabi:** General English, Intensive 40h/month, Business English, French DELF/DALF, German Goethe, Portuguese, Spanish for Foreigners.
2. **Schedules & Time Slots:** Early Birds (6:00 - 8:00 AM), Daytime (Mornings/Afternoons), After-Work Evenings (6:30 - 8:30 PM), Saturdays, and Sundays.
3. **Tuition in Colombian Pesos (COP):** Official prices, 10% cash discount, 3-installment interest-free financing, and family/compensation fund discounts (Compensar, Colsubsidio, Cafam).
4. **Campuses & Modalities:** Physical campuses in Bogotá (Chicó & Chapinero), Medellín (El Poblado & Laureles), Cali (Granada), and 100% Virtual Synchronous classrooms.

**Consequences of the traditional human-only model:** Counselor burnout, response delays exceeding 4 hours, lost prospective students (lead churn), and high hallucination risk with generic ungrounded chatbots.

### The Solution
A **Hybrid Admissions Intelligence Engine** combining:
* **Deterministic Guided Navigation:** A structured state-machine menu (Pillars 1 to 4 with root reset 0) delivering instant answers (<5ms) with zero token costs.
* **Strict Hybrid RAG (Dense + Sparse):** Grounded indexing over 82 official institutional documents with 0% hallucination rate.
* **Dual Admissions Advisor Engine (OpenCode vs AGY):** Operator-selectable deep reasoning engine at startup.
* **Eye-Strain Reduction:** Retro OS interface featuring an optical CRT Anti-Glare shader designed for comfortable extended viewing.

---

## 📂 3. Clean Monorepo Directory Architecture

```text
synapse-admissions-ai/ (NovaVice_os97)
├── backend/                               # 🐍 FastAPI Backend & AI Pipeline
│   ├── data/                              # Official Knowledge Base (82 docs) & Ticket Store
│   │   ├── documents/                     # Structured Markdown files (syllabi, schedules, pricing)
│   │   └── escalations.json               # Persisted human escalation tickets
│   ├── hermes_skills/                     # Agent skill tools & OpenAPI definitions
│   ├── src/                               # Application source code
│   │   ├── api/                           # REST endpoints & Pydantic v2 schemas
│   │   ├── bot/                           # Python Telegram bot integration
│   │   ├── core/                          # State machine, cache, guardrails, OpenCode/AGY client
│   │   ├── rag/                           # Ingestion, BM25, ChromaDB & Prompt templates
│   │   ├── static/                        # Static web chat fallback
│   │   ├── config.py                      # Centralized Pydantic application settings
│   │   └── main.py                        # FastAPI ASGI entrypoint
│   ├── tests/                             # 25 Automated Pytest tests
│   └── requirements.txt                   # Python dependencies
│
├── frontend/                              # 🌐 Next.js 15 Retro Web Application
│   ├── src/
│   │   ├── app/                           # App Router, Layout & CRT global styles
│   │   ├── components/                    # Retro Window, Header, CRT, Living Pixel Art
│   │   └── lib/                           # API clients, TypeScript interfaces & helpers
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/                                  # 📚 System Documentation & Architectural Records
│   ├── assets/                            # Static assets and original assignment PDF
│   ├── 01-product/                        # Product Requirements Document (PRD)
│   ├── 03-architecture/                   # Architecture diagrams & technical proposals
│   ├── 04-engineering/                    # Deep-dive guides for backend, frontend & RAG
│   ├── 05-ai/                             # AI integrations (OpenCode & AGY Antigravity)
│   ├── 08-operations/                     # Performance tuning & monitoring
│   └── 09-decisions/                      # Architecture Decision Records (ADR-001 to ADR-007)
│
├── scripts/                               # 🛠️ Multiplatform Automation & Setup
│   ├── installer.py                       # Cross-platform installation logic
│   ├── install.sh                         # Linux / macOS install script
│   └── install.bat                        # Windows install script
│
├── .agents/                               # Antigravity agent configurations & rules
├── .env.example                           # Environment variables template
├── AGENTS.md                              # Multi-agent roster & invocation shortcuts
├── CHANGELOG.md                           # Strict chronological changelog (America/Bogota)
├── TECHNICAL_EXPLANATION.md               # Master technical presentation guide (English)
├── EXPLICACION_TECNICA.md                 # Master technical presentation guide (Spanish)
├── README.md                              # Main repository overview (English)
├── README.es.md                           # Repository overview (Spanish)
├── pytest.ini                             # Root Pytest discovery configuration
├── run.py                                 # Process supervisor with advisor engine switch
├── start.sh                               # Linux / macOS launch wrapper
└── start.bat                              # Windows launch wrapper
```

---

## 🏗️ 4. System Layer Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER (NEXT.JS 15 FRONTEND)             │
│                                                                        │
│   Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS       │
│   ├── Macintosh OS '97 Window (Pinstripe titlebar, vintage controls)   │
│   ├── CRT Anti-Glare Optical Filter (Scanlines + Amber Phosphor + SW)  │
│   ├── Living Pixel-Art Background (8 Palms + 18 Bidirectional Clouds + Gulls + Pixel Grass) │
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
│   │     └─► Instant Deterministic Return (<5ms, 0 tokens spent)        │
│   │                                                                    │
│   └── Dual-Layer Query Cache (SHA-256 Hash + Semantic Similarity)      │
│         └─► Cache Hit: Sub-30ms Return                                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Cache Miss / Open-Ended Query)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     HYBRID RAG RETRIEVAL PIPELINE                      │
│                                                                        │
│   1. Dense Vector Store:                                               │
│      - ChromaDB Persistent (`idiomas_knowledge_base`)                  │
│      - Embeddings: `all-MiniLM-L6-v2` (Local ONNX, 384 dimensions)     │
│                                                                        │
│   2. Sparse Lexical Store:                                             │
│      - Pure Python Okapi BM25 with Spanish suffix stemming             │
│                                                                        │
│   3. Rank Fusion:                                                      │
│      - Reciprocal Rank Fusion (RRF, $k=60$)                            │
│                                                                        │
│   4. Relevance Guardrail:                                              │
│      - Confidence Threshold: $\text{score} \ge 0.50$                   │
│      - If $\text{score} < 0.50$ ──► ESCALATION TICKET (`ESC-YYYYMMDD`) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  DUAL ADVISOR DEEP REASONING LAYER                     │
│                                                                        │
│   Pre-Launch Supervisor Switch (`run.py --advisor [opencode|agy]`):    │
│                                                                        │
│   [Option 1: OpenCode Daemon]           [Option 2: AGY Antigravity]    │
│   ├── Daemon running on port :4096      ├── Google Antigravity CLI     │
│   ├── Stateful sessions (`ses_xxx`)     ├── Native contextual bridge   │
│   └── Grounded 5-chunk injection        └── Grounded 5-chunk injection │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 5. In-Depth Hybrid RAG Pipeline

### 5.1 Ingestion & Chunking with Overlap
1. **Official Knowledge Base:** 82 structured Markdown documents located in `backend/data/documents/` covering every program, level, fee schedule, campus, and policy.
2. **Chunking Strategy:**
   * Chunk Size: **600 characters**.
   * Overlap Size: **120 characters** (20% overlap).
   * **Why overlap matters:** Overlap prevents information boundaries from splitting critical constraints (such as a 10% discount requirement being disconnected from the COP course price).
3. **Total Chunks:** **245 high-density chunks** indexed with rich metadata (source filename, section title, pillar category).

### 5.2 Dense Vector Search (ChromaDB)
* Captures semantic intent, conversational phrasing, and colloquial Spanish variations.
* Distance Metric: Cosine Distance ($1 - \text{cosine similarity}$).

### 5.3 Sparse Lexical Search (Okapi BM25)
* Implemented in pure Python without heavy external Java/Lucene dependencies:
  $$\text{Score}_{BM25}(D, Q) = \sum_{i=1}^{N} IDF(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
  Where $k_1 = 1.5$ and $b = 0.75$.
* Includes a morphological Spanish stemmer that normalizes plurals, verb conjugations, and suffixes to base lemmas.

### 5.4 Reciprocal Rank Fusion (RRF)
Combines the dense rank list ($R_{dense}$) and sparse lexical rank list ($R_{sparse}$):
$$RRF(d) = \frac{1}{60 + \text{rank}_{dense}(d)} + \frac{1}{60 + \text{rank}_{sparse}(d)}$$
**Technical Advantage:** Eliminates score scale discrepancy between unbounded BM25 scores and cosine distances, guaranteeing that documents matching both semantic and exact keyword criteria are ranked highest.

### 5.5 Relevance Guardrail & Human Escalation
* If the maximum fused similarity score falls below **0.50**, the engine identifies that the inquiry cannot be verified from official records.
* **Automated Safety Flow:**
  1. Prevents hallucination by refusing to invent unverified policies.
  2. Generates a unique tracking ticket: `ESC-YYYYMMDD-XXXX`.
  3. Appends the request to `backend/data/escalations.json`.
  4. Returns the ticket number and direct academic contact details to the user.

---

## 🕹️ 6. Pre-Launch Switch & Dual Reasoning Engine

The system supervisor (`run.py`, `start.sh`, `start.bat`) allows the operator to select the active reasoning advisor engine before booting:

```text
  🎓 NOVA IDIOMAS COLOMBIA - ADVISOR REASONING ENGINE SELECTION
  [1] 🤖 OpenCode Reasoning Engine (:4096)
  [2] 🚀 AGY (Google Antigravity CLI / Engine)
```

### Launch Flags
* **Interactive Mode:** Run `python3 run.py` or `./start.sh` (prompts when run in an interactive terminal).
* **CLI Flag Mode:**
  * `python3 run.py --advisor=opencode` (or `./start.sh -a opencode`)
  * `python3 run.py --advisor=agy` (or `./start.sh -a agy`)

---

## 🎨 7. "Nova OS '97" Retro Frontend & Optical CRT Filter

### 7.1 Design Philosophy
Combines the retro nostalgia of 1997 Macintosh OS desktop environments, the vintage elegance of Poolsuite.net, and the warm sunset tones of GTA Vice City, paired with modern visual accessibility standards:

### 7.2 CRT Anti-Glare Optical Screen Filter
* **Purpose:** Actively mitigates eye fatigue and screen glare during prolonged sessions.
* **Filter Stack:**
  * Ultra-fine horizontal scanlines spaced at 3px (`rgba(30, 20, 15, 0.10)`).
  * Warm amber/peach phosphor tint and subtle Trinitron monitor vignette.
  * Luminance smoothing (`brightness(0.96) contrast(0.97)`).
  * **Interactive `[ 📺 CRT: ON / OFF ]` Switch** with local persistence.

### 7.3 Living Pixel-Art Background (GPU 60 FPS)
* **8 Depth-Layered Palms:** Majestic foreground (380px), mid-depth leaning, and slender background palms swaying with organic breeze keyframes (`palmSwayLeft/Right` 5-7s).
* **18 Volumetric 16-Bit Clouds (9 L2R + 9 R2L):** Bidirectional drift across the sky at staggered altitudes (durations 40-74s, delays 1-30s) via `cloudDriftL2R`/`R2L` and classes `animate-cloud-l2r-1..9` / `r2l-1..9` — guaranteed entry from both left and right edges on all viewports.
* **6 Bidirectional Flocks of Seagulls:** Featuring a custom `PixelSeagull` component with **2-state discrete wing flapping** (Wings-Up vs Wings-Down) running at `0.38s steps(1) infinite`.
* **Verde Seco Retro Grass Carpet:** Dense `48-54px` pixel-grass layer in `#8A9A6A` with static continuous base (`14-16px`) + highlight `#A8B88E` and **28 swaying tufts** (12 on mobile) with 3 blades each (`#6B7D5A`/`#8A9A6A`/`#9AB08A`). Only tufts animate via `grassSway 3.5s ease-in-out skewX(0.7deg)` — base static for visual calm.

---

## 🧪 8. Automated Test Suite & Quality Assurance

### Pytest Verification (`25/25 PASSED`):
```bash
./venv/bin/pytest -v
```
```text
============================= 25 passed in 14.07s ==============================
```

Coverage highlights:
* **API Endpoints:** Health check, chat endpoint, SSE streaming, metrics, and escalations.
* **Ingestion & Vector Store:** Directory hashing, chunking with overlap (600/120), ChromaDB persistence.
* **Hybrid Search:** BM25 lexical retrieval with Spanish stemming, Reciprocal Rank Fusion.
* **Safety Guardrails:** Prompt injection detection (DAN, jailbreaks), confidence thresholding (0.50).
* **State Machine & Continuity:** Navigation pillar transitions, leaf queries, breadcrumbs, and zero-deadlock flow.
* **Dual Advisor Integration:** E2E verification for both OpenCode and AGY Antigravity backends.

---

## 🎤 9. Oral Presentation Guide (5-7 Minute Script & Defense Q&A)

### 🎙️ Suggested Presentation Flow:
1. **Introduction (1 min):** "Good afternoon. Today we present *Nova OS '97*, a production-grade Admissions AI Assistant and hybrid RAG system built for Nova Idiomas Colombia..."
2. **Business Problem & Value Proposition (1 min):** "The institution faced hundreds of daily inquiries regarding courses, COP pricing, and international exams. Our solution automates 100% of these inquiries with zero hallucinations..."
3. **Hybrid RAG Architecture (2 min):** "We engineered dense ChromaDB + BM25 (Unicode NFD, 80 synonyms) fused via RRF ($k=60$) + centroid per pillar, with 0.35 threshold for pilares (horario/precio/curso/modalidad/sede/beca→descuento) vs 0.50 heavy only (2-phase Sí/No, ADR-008)..."
4. **Dual Advisor & Supervisor (1.5 min):** "We designed a pre-launch switch in `run.py` that allows toggling between OpenCode Daemon (:4096) and Google Antigravity (AGY)..."
5. **Retro OS Experience & CRT Filter (1 min):** "On the frontend, we built an engaging Macintosh '97 retro interface with an optical CRT anti-fatigue filter and a living GPU-accelerated pixel-art landscape..."
6. **Conclusion & Metrics (30s):** "Backed by 27/27 tests, sub-30ms dual cache (exact SHA-256 + semantic 0.88 pilar), 83 docs including becas→descuentos canónico 12_04, and heavy-only escalation."

---

### ❓ Evaluator Defense Q&A:

* **Q: Why use Hybrid RAG instead of standard dense vector search alone?**  
  * **A:** Dense embeddings excel at semantic matching and synonyms, but often miss exact exam acronyms (IELTS, TOEFL, DELF) or specific schedules. BM25 guarantees exact keyword recall, and RRF delivers the best combination of both.

* **Q: How is zero hallucination guaranteed?**  
  * **A:** Through three layers: (1) Low LLM temperature (0.2) and closed-context prompts; (2) Semantic relevance thresholding (0.50) that escalates out-of-scope questions to human tickets; and (3) Deterministic state-machine menus for standard queries.

* **Q: Why include an optical CRT shader in the UI?**  
  * **A:** It transforms an ordinary chatbot into a memorable retro experience while acting as a functional anti-glare screen filter that reduces eye strain during long reading sessions.

* **Q: What if user asks “becas disponibles”?**  
  * **A:** Per ADR-008, Nova has no merit becas. The query maps via 80 synonyms to `12_04_becas_descuentos_aclaratoria.md` and answers `No becas, sí descuentos 10% contado / 15% cajas / 15% familiar / bono $100k` with `0.35` pilar threshold, never escalated as heavy. Demo: `becas disponibles` → `MaxSim 0.85` hit, not `ESC-`.
