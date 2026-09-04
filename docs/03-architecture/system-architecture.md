# System Architecture (Version 2.7.0 - Resilience & Performance)

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
                  HTTP /api/v1/chat/stream (SSE)
                           │                                  │
                           +─────────────────┬────────────────+
                                             │
                                             v
┌────────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Application Core (:8000)                   │
│               (ASGI Middleware with X-Request-ID Correlation)              │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Block C: Pre-Flight Guardrails & Prompt Injection Sanitizer          │  │
│  │ (Detects jailbreaks, prompt extraction, malicious payloads)          │  │
│  └──────────────────────────────────┬───────────────────────────────────┘  │
│                                     │ Clean Inbound Query                  │
│                                     v                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Guided Navigation State Machine (src/core/navigation.py:163,330)     │  │
│  │ Root 1-4 (24 leaves) + 80 intent synonyms (horario/precio/beca→      │  │
│  │ descuento/curso/modalidad/sede) + Unicode NFD + typo Levenshtein     │  │
│  │ '0' Return, Heavy Only advisor (9)                                   │  │
│  └───────┬──────────────────────────────────────────────────────┬───────┘  │
│          │ Option 9 / Advisor Mode                              │          │
│          v                                                      │ RAG Flow │
│  ┌──────────────────────────────────────────────┐               │          │
│  │ Python Intermediary (opencode_client.py)    │               │          │
│  │ - Persistent httpx.AsyncClient Pooling       │               │          │
│  │ - CircuitBreaker with Exponential Backoff    │               │          │
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
│          │      │ Block E: Adaptive Dual-Layer Cache                    │  │
│          │      │ 1. Exact SHA-256 ──► Hit (<30ms)                     ─┐│  │
│          │      │ 2. Semantic 0.95 (0.88 pilar: horario/precio/curso/   ─┤│  │
│          │      │    modalidad/sede/beca→descuento) via embed_query     ││  │
│          │      └───────────────────┬───────────────────────────────────┼┘  │
│          │                          │ Cache Miss                        │   │
│          │                          v                                   │   │
│          │      ┌──────────────────────────────────────────────────┐    │   │
│          │      │ Block A: Hybrid Retrieval, Hard Mask & Reranker  │    │   │
│          │      │ - Hard Domain Masking (100% cross-pillar veto)   │    │   │
│          │      │ - 83 Docs + Dense ChromaDB + Okapi BM25 index    │    │   │
│          │      │ - Candidate expansion to top-20 + FlashRank ONNX │    │   │
│          │      │ - Pre-LLM Context Domain Validator               │    │   │
│          │      └───────────────────┬──────────────────────────────┘    │   │
│          │                          │ Top 5 Reranked Chunks             │   │
│          │                          v                                   │   │
│          │      ┌──────────────────────────────────────────────────┐    │   │
│          │      │ Relevance & Post-LLM Faithfulness NLI Gate       │    │   │
│          │      │ - Faithfulness threshold >= 0.80 (NLI entailment)│    │   │
│          │      │ - Self-consistency N=3 in medium confidence      │    │   │
│          │      │ - PostLLM Guardrails ($ COP, time formats, PII)  │    │   │
│          │      └───────────┬──────────────────────────┬───────────┘    │   │
│          │                  │ Pass                     │ Fail (<0.50)   │   │
│          │                  v                          v                │   │
│          │      ┌───────────────────────┐  ┌───────────────────────┐    │   │
│          │      │ Block B: Synthesis    │  │ Block D: Escalation   │    │   │
│          │      │ Prompt (Temp=0.0) &   │  │ Dispatcher & SQLite   │    │   │
│          │      │ Structured Citations  │  │ WAL Ticket Store      │    │   │
│          │      └───────────┬───────────┘  └───────────┬───────────┘    │   │
│          │                  │                          │                │   │
│          +──────────────────┼──────────────────────────┼────────────────┘   │
│                             │                          │                    │
│                             v                          v                    │
│                  ┌──────────────────────┐   ┌───────────────────────┐       │
│                  │ JSON Response & Meta │   │ SQLite Ticket (WAL)   │       │
│                  │ (Citations, Latency) │   │ (escalations.db)      │       │
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

### 2.2 Ingestion & Indexing Pipeline (`src/rag/ingestion.py:32`)
- **Source Directory:** `data/documents/` (83 docs, 245 chunks, 20 clusters + `12_04_becas_descuentos_aclaratoria.md` canónico).
- **Chunking Engine:** Markdown section splitter (`##`, `###`) 500/100 (600/150 para tablas precios/horarios protegido Fase B14).
- **Vector Store:** ChromaDB `all-MiniLM-L6-v2` / `BAAI/bge` + fallback TF-IDF `embed_query()` para cache semántica; centroid por pilar (5) Fase B16. Rutina `vacuum()` y SnapshotManager para rollback seguro.
- **Lexical Index:** Pure Python BM25 `k1 1.5 b 0.75` + Unicode NFD + STOP 62 + expansión query + lemas canónicos de sedes colombianas.

### 2.3 Guided Navigation State Machine (`src/core/navigation.py:163,330`)
- **Root Menu:** 4 pilares (1 Cursos 1.1-1.6, 2 Horarios 2.1-2.6, 3 Precios 3.1-3.5, 4 Sedes 4.1-4.6) + 80 synonyms (horario/precio/beca→descuento/curso/modalidad/sede) + typo + intent embedding cosine 0.82 + multi-intent split.
- **Becas→Descuentos:** `beca/becas/ayudas/subsidio/scholarship/becas disponibles` → `12_04` (ADR-008). Sin merit becas.
- **Heavy Only:** `0` return, `9` asesor solo very heavy (lista negra `visa/beca 100%/Australia`).

### 2.4 OpenCode Advisor Intermediary (`src/core/opencode_client.py`)
- **REST Client:** High-performance `httpx.AsyncClient` con persistent connection pooling.
- **Resilience Layer:** Circuit Breaker pattern con backoff exponencial (`src/core/resilience.py`).
- **Context Injection:** Inyecta top 5 fragmentos enriquecidos recuperados.
- **Reasoning Timeout:** Ventana de 45.0 segundos permitiendo ejecución completa de Chain-of-Thought.

### 2.5 Persistencia Relacional y Registro de Escalaciones (`src/data/sqlite_tickets.py`)
- **Motor de Base de Datos:** SQLite 3 con Write-Ahead Logging (`PRAGMA journal_mode=WAL;`).
- **Integridad Transaccional:** Cumplimiento ACID completo, lecturas y escrituras no bloqueantes concurrentes y migración histórica desde `escalations.json`.
