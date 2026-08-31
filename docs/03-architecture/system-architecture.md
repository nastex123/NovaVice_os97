# System Architecture (Version 2.6.0)

## 1. End-to-End Multi-Tier Architectural Diagram

```text
                               INBOUND CLIENT TIERS
        +──────────────────────────────────────+──────────────────────────────+
        |       Next.js 15 Web App (:3000)     |         Telegram Bot         |
        |   (PixiJS WebGL + ReactMarkdown)     |     (Async Webhook/Poll)     |
        +──────────────────┬───────────────────+──────────────┬───────────────+
                           │ (Next.js Reverse Proxy)          │
                           v                                  v
                  HTTP /api/v1/chat                   Webhook Handler
                  HTTP /api/v1/chat/stream
                           │                                  │
                           +─────────────────┬────────────────+
                                             │
                                             v
┌────────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Application Core (:8000)                   │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Block C: Pre-Flight Guardrails & Prompt Injection Sanitizer          │  │
│  │ (Detects jailbreaks, prompt extraction, malicious payloads)          │  │
│  └──────────────────────────────────┬───────────────────────────────────┘  │
│                                     │ Clean Inbound Query                  │
│                                     v                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Guided Navigation State Machine (src/core/navigation.py)             │  │
│  │ Root Menu (1-9), 8 Submenus (1.1..8.5), '0' Return Command           │  │
│  └───────┬──────────────────────────────────────────────────────┬───────┘  │
│          │ Option 9 / Advisor Mode                              │          │
│          v                                                      │ RAG Flow │
│  ┌──────────────────────────────────────────────┐               │          │
│  │ Python Intermediary (opencode_client.py)    │               │          │
│  │ - Multi-Document High-Density Context Feed   │               │          │
│  │ - 45s Deep Reasoning Window (Chain-of-Thgt)  │               │          │
│  │ - Empathetic Markdown Synthesis & Persona    │               │          │
│  └───────┬──────────────────────────────────────┘               │          │
│          │                                                      │          │
│          v                                                      │          │
│  [OpenCode Deep Reasoning Server (:4096)]                       │          │
│          │                                                      │          │
│          │                                                      v          │
│          │      ┌───────────────────────────────────────────────────────┐  │
│          │      │ Block E: Adaptive Invalidation-Aware Query Cache      │  │
│          │      │ 1. Exact Match (SHA-256 Hash Table) ──► Hit (<30ms) ─┐│  │
│          │      │ 2. Semantic Cache (Similarity > 0.95) ──► Hit (<30ms)┤│  │
│          │      └───────────────────┬───────────────────────────────────┼┘  │
│          │                          │ Cache Miss                        │   │
│          │                          v                                   │   │
│          │      ┌──────────────────────────────────────────────────┐    │   │
│          │      │ Block A: Hybrid Retrieval & Ranking Subsystem    │    │   │
│          │      │ - 87 Official Documents (264 Indexed Chunks)     │    │   │
│          │      │ - Dense Cosine Search (ChromaDB + Local Engine)  │    │   │
│          │      │ - Pure Python BM25 with Auto-Corpus Fitting      │    │   │
│          │      │ - Reciprocal Rank Fusion (RRF, k=60)             │    │   │
│          │      └───────────────────┬──────────────────────────────┘    │   │
│          │                          │ Top 5 Ranked Chunks               │   │
│          │                          v                                   │   │
│          │      ┌──────────────────────────────────────────────────┐    │   │
│          │      │ Relevance Threshold Filter (Score >= 0.50)       │    │   │
│          │      └───────────┬──────────────────────────┬───────────┘    │   │
│          │                  │ Pass                     │ Fail (<0.50)   │   │
│          │                  v                          v                │   │
│          │      ┌───────────────────────┐  ┌───────────────────────┐    │   │
│          │      │ Block B: Synthesis    │  │ Block D: Escalation   │    │   │
│          │      │ Prompt & Gemini / RAG │  │ Dispatcher & Ticket   │    │   │
│          │      └───────────┬───────────┘  └───────────┬───────────┘    │   │
│          │                  │                          │                │   │
│          +──────────────────┼──────────────────────────┼────────────────┘   │
│                             │                          │                    │
│                             v                          v                    │
│                  ┌──────────────────────┐   ┌───────────────────────┐       │
│                  │ JSON Response & Meta │   │ Human Handoff Ticket  │       │
│                  │ (Citations, Latency) │   │ (escalations.json)    │       │
│                  └──────────────────────┘   └───────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Taxonomy & Responsibilities

### 2.1 Web Frontend Architecture (`frontend/`)
- **Next.js 15 (App Router):** Server-rendered framework with client-side interactivity, proxying `/api/*` to the FastAPI backend.
- **PixiJS Canvas (`PixiParticleBackground.tsx`):** WebGL particle constellation engine with mouse magnetism.
- **ReactMarkdown Engine (`ChatContainer.tsx`):** Native GFM markdown renderer with Dark Glassmorphism callouts, glowing neon bullets, and clear typography.
- **Process Supervisor (`run.py`):** Multi-process launcher managing OpenCode (:4096), FastAPI (:8000), and Next.js (:3000).

### 2.2 Ingestion & Indexing Pipeline (`src/rag/ingestion.py`)
- **Source Directory:** `data/documents/` (87 verified university documents across 7 thematic clusters).
- **Chunking Engine:** Markdown section splitter (`##`, `###`) with character chunking (500 chars) and 100-character overlap.
- **Vector Store:** ChromaDB with Pure Python vector persistence and cosine similarity.
- **Lexical Index:** Pure Python BM25 with automatic corpus fitting on startup.

### 2.3 Guided Navigation State Machine (`src/core/navigation.py`)
- **Root Menu:** 9 official options with single-digit routing.
- **Submenus (1 to 8):** Detailed thematic trees (e.g. 1.1 to 1.7 for syllabi, 5.1 to 5.5 for NVIDIA H100 GPU cluster).
- **Option 9:** Direct routing to OpenCode Advisor mode.

### 2.4 OpenCode Advisor Intermediary (`src/core/opencode_client.py`)
- **REST Client:** High-performance `httpx.AsyncClient` with connection pooling.
- **Context Injection:** Injects top 5 complete retrieved chunks.
- **Reasoning Timeout:** 45.0-second window allowing complete Chain-of-Thought execution.
