# 🧠 Synapse Admissions AI (`synapse-admissions-ai`) — v2.6.0

An enterprise-grade, cost-efficient Retrieval-Augmented Generation (RAG) platform engineered in pure Python and FastAPI for Nova Tech University admissions, accompanied by a **Next.js 15 + PixiJS Modern Goth-Tech Web Application** and a **Deep Reasoning OpenCode Human Advisor Intermediary**.

It automates repetitive applicant inquiries (syllabi, NVIDIA H100 GPU labs, international visas, exchange programs, payment methods, housing, transfer credits, career hub, and graduation rules), grounds answers strictly on institutional business documents, incorporates hybrid search (dense + BM25) with Spanish stemming, features an interactive guided menu navigation system (1 to 9 with 8 thematic submenus), and connects through a high-performance Python intermediary to **OpenCode** as the live Human Admissions Advisor with multi-document deep reasoning.

---

## Architecture Overview

```text
[Student / Next.js 15 Web App (:3000)]          [Telegram Bot Worker]
(PixiJS WebGL + ReactMarkdown GFM)                       │
                 │ (Reverse Proxy)                       ▼
                 ▼                             [Webhook Gateway]
       [FastAPI REST Gateway (:8000)] ──► [Prompt Injection Defense]
                 │
                 ▼
       [Guided Menu State Machine (Options 1-9, 8 Submenus, '0' Return)]
                 │
                 ├── (Option 9 / Advisor Mode) ──► [Python Intermediary: src/core/opencode_client.py]
                 │                                         │ (Top 5 Chunks + 45s Reasoning Window)
                 │                                         ▼
                 │                               [OpenCode Deep Reasoning Server (:4096)]
                 │                                         │
                 │                                         ▼
                 │                               [Empathetic Multi-Beca Markdown Output]
                 │
                 └── (Standard RAG Query)
                           │
                           ▼
       [Dual Cache (Exact SHA-256 + Semantic)] ──► (Instant Cache Hit Return <30ms)
                           │ (Cache Miss)
                           ▼
       [Hybrid Search Engine: ChromaDB (Local) + Auto-Fitting Pure BM25]
                           │
                           ▼
       [Reciprocal Rank Fusion (RRF) & Relevance Guardrail (Threshold: 0.50)]
                           │
                           ▼
       [System Prompt + 3 Few-Shot Context Engine / Structured Synthesis]
                           │
                           ▼
       [Prometheus Telemetry & Live Web UI with Interactive Action Buttons]
```

---

## Key Features

- **Strict Document Grounding (87 Official Documents & 264 Chunks):** Enterprise corpus covering 20 course syllabi, 10 specialized research labs (including NVIDIA H100 GPU cluster), 10 international mobility programs (TU Munich, Tokyo Tech, UC Berkeley), 10 banking and financial aid policies, 10 student life and health services, 10 employability and startup programs, and 10 academic regulations and master's degrees.
- **Interactive Guided Navigation Engine:** Numbered root menu (1 to 9) with 8 thematic submenus (1.1..8.5), return controls (`0`), and dynamic interactive action buttons.
- **Python Intermediary with OpenCode (`Web` ➔ `Python` ➔ `OpenCode`):** Real-time integration connecting Option 9 ("Hablar con un Asesor") directly to a local OpenCode server instance acting as the Human Admissions Advisor with multi-document context injection and deep Chain-of-Thought reasoning.
- **Modern Next.js 15 + PixiJS Web Application (`frontend/`):** WebGL particle background with mouse magnetism, collapsible dark glassmorphism sidebar, live server status badges, telemetry counters, and native GFM Markdown rendering (`react-markdown` + `remark-gfm`).
- **Cross-Platform Executables & Launcher:** Single-click installers (`installer.py`, `install.bat`, `install.sh`) and unified supervisor runner (`run.py`, `start.bat`, `start.sh`) running OpenCode (:4096), FastAPI (:8000), and Next.js (:3000) simultaneously with graceful `Ctrl+C` shutdown.
- **Hybrid Retrieval & Auto-Fitting BM25:** Combines dense cosine similarity with BM25 lexical keyword matching, Reciprocal Rank Fusion (RRF), and bilingual morphological suffix stemming.
- **Automated Pytest Suite (19/19 Tests - 100% Pass):** Comprehensive unit, integration, executable, guardrail, and RAG tests.

---

## Quick Start Guide

### 1. Installation
#### Windows:
```cmd
install.bat
```
#### Linux / macOS:
```bash
chmod +x install.sh
./install.sh
```

### 2. Execution (All Services)
#### Windows:
```cmd
start.bat
```
#### Linux / macOS:
```bash
chmod +x start.sh
./start.sh
```

### 3. Access Live Endpoints
- **Next.js 15 Web Application:** [http://localhost:3000/](http://localhost:3000/)
- **FastAPI Core Service:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **OpenCode Advisor Daemon:** [http://127.0.0.1:4096/](http://127.0.0.1:4096/)
- **Swagger Documentation:** [http://localhost:3000/docs](http://localhost:3000/docs)
- **Prometheus Metrics:** [http://localhost:3000/metrics/prometheus](http://localhost:3000/metrics/prometheus)

---

## Knowledge Base Corpus (`data/documents/`)

| Cluster | Document Count | Key Topics Covered | Indexed Chunks |
| :--- | :---: | :--- | :---: |
| **1. Syllabi & Academic Curriculums** | 20 docs | Algorithms (CS-201), Microservices (SE-302), Deep Learning (AI-401), SOC Defense (SEC-305), Cloud & DevOps, Quantum Computing, Vector DBs, React/Next.js Full Stack. | 60 |
| **2. Specialized Research Labs** | 10 docs | NVIDIA H100 Supercomputing (64 GPUs, Slurm), MakerSpace 3D, Cyber Range Red Team, XR Lab (Apple Vision Pro/Quest 3), Cisco Networking, Autonomous Robotics. | 32 |
| **3. International Mobility & Visas** | 10 docs | I-20 student visa, exchange programs with TU Munich (Germany), Tokyo Tech (JASSO scholarship), UC Berkeley Silicon Valley Immersion, UPM Double Degree. | 32 |
| **4. Banking, Tuition & Financial Aid** | 10 docs | Payment gateways (Chase, Santander, Davivienda, Stripe, USDC), Plan B 4-installment financing, Alan Turing Scholarship (50%), Ada Lovelace Women in Tech (35%). | 32 |
| **5. Student Life, Health & Athletics** | 10 docs | Free urgent medical care, CrossFit and sports gym, meal plans ($90/mo), Nova eSports gaming arena (RTX 4080), Nova Shuttle electric bus transit, EV chargers. | 32 |
| **6. Employability & Partnerships** | 10 docs | Nova Ventures Startup Incubator ($100k seed fund), Microsoft Learn, AWS Academy, Google Cloud, Tech Career Expo (60+ companies), paid internships ($600-$1400/mo). | 32 |
| **7. Academic Regulations & Master's** | 10 docs | Code of Honor anti-plagiarism, Capstone thesis rubric, M.Sc. in Generative AI and Offensive Cyber, 100% student IP ownership, RPL work experience validation. | 32 |
| **Foundation Core Documents** | 7 docs | Programs, tuition, admissions guide, housing, credit transfers, career hub, and graduation rules. | 12 |
| **Total Global Knowledge Base** | **87 Documents** | *Fully indexed in ChromaDB and Pure Python BM25* | **264 Chunks** |

---

## Running Automated Tests

```bash
pytest -v
```

```text
============================= 19 passed in 1.80s ==============================
```
