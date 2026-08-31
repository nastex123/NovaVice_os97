# Technical Design Document (TDD) - Version 2.6.0

## 1. Comprehensive Project Directory Structure

```text
.
├── CHANGELOG.md
├── README.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── installer.py                    # Cross-platform interactive installer (OS detector & dependencies)
├── install.bat                     # Windows one-click installer
├── install.sh                      # Linux/macOS one-click installer
├── run.py                          # Multi-process supervisor launcher (OpenCode + FastAPI + Next.js)
├── start.bat                       # Windows one-click runner
├── start.sh                        # Linux/macOS one-click runner
├── frontend/                       # Modern Next.js 15 + PixiJS Web Application
│   ├── package.json                # Next.js, PixiJS, Framer Motion, ReactMarkdown, Tailwind
│   ├── tsconfig.json
│   ├── next.config.mjs             # Reverse proxy routing /api/* to FastAPI :8000
│   ├── tailwind.config.ts          # Dark Glassmorphism obsidian theme with crimson glow
│   └── src/
│       ├── app/
│       │   ├── layout.tsx          # Root HTML with PixiJS WebGL background
│       │   ├── page.tsx            # Main chat interface with 9 options & live telemetry
│       │   └── globals.css
│       ├── components/
│       │   ├── PixiParticleBackground.tsx  # Interactive WebGL particle constellation
│       │   ├── Sidebar.tsx         # Collapsible sidebar with telemetry & mode toggle
│       │   ├── Header.tsx          # Institutional branding & breadcrumbs
│       │   ├── ChatContainer.tsx   # ReactMarkdown GFM renderer with custom styled components
│       │   ├── ChatInput.tsx       # Voice dictation (Web Speech API) & suggestion chips
│       │   └── Footer.tsx
│       └── lib/
│           ├── types.ts            # TypeScript interfaces
│           └── api.ts              # Fetch client for chat, metrics, and health
├── docs/
│   ├── 01-product/
│   │   └── PRD.md
│   ├── 03-architecture/
│   │   ├── system-architecture.md
│   │   └── technological-enhancement-proposals.md
│   ├── 04-engineering/
│   │   └── technical-design.md
│   ├── 05-ai/
│   │   ├── opencode-integration.md
│   │   └── hermes-agent-integration.md (Deprecated)
│   └── 09-decisions/
│       └── ADR-001-rag-stack-and-architecture.md
├── data/
│   ├── chroma_db/                  # Persistent local vector store (87 documents, 264 chunks)
│   ├── escalations.json            # Human escalation tickets log
│   └── documents/                  # 87 Official university knowledge documents across 7 clusters
├── src/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application entrypoint (REST + Static fallback)
│   ├── config.py                   # Pydantic v2 settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py               # REST endpoints (/api/v1/chat, /metrics, /health)
│   │   └── schemas.py              # Pydantic schemas (use_opencode_mode, action_buttons)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── guardrails.py           # Pre-flight prompt injection filter
│   │   ├── navigation.py           # Guided state machine (1-9, 8 submenus, '0' return)
│   │   ├── opencode_client.py      # Deep reasoning OpenCode intermediary bridge (45s window)
│   │   ├── cache.py                # Dual-layer exact & semantic cache
│   │   ├── dispatcher.py           # Escalation logger & webhook dispatcher
│   │   ├── memory.py               # In-memory applicant state tracking
│   │   └── metrics.py              # Metrics collector & Prometheus exporter
│   └── rag/
│       ├── __init__.py
│       ├── bm25.py                 # Pure Python BM25 index with auto-fitting
│       ├── engine.py               # Master pure Python RAG orchestrator
│       ├── hybrid_retriever.py     # Hybrid search with Reciprocal Rank Fusion
│       ├── ingestion.py            # Document ingestion & vectorization pipeline
│       ├── prompt_templates.py     # Grounded system prompt builders
│       └── vector_store.py         # Vector store manager
└── tests/                          # Automated Pytest test suite (19 tests - 100% pass)
    ├── test_api_routes.py
    ├── test_executables.py         # Tests for installer and launcher scripts
    ├── test_guardrails.py
    ├── test_hybrid_search.py
    ├── test_ingestion.py
    ├── test_navigation.py          # Tests for 9 options and 8 submenus
    ├── test_opencode_intermediary.py
    └── test_rag_pipeline.py
```

---

## 2. API Contract Specifications

### `POST /api/v1/chat`
**Request Payload:**
```json
{
  "query": "hay becas disponibles?",
  "user_id": "postulante_nextjs",
  "session_id": "sess_nextjs_abc123",
  "use_opencode_mode": true
}
```

**Response Payload (200 OK):**
```json
{
  "status": "success",
  "response": "¡Hola! ... ### 1. Beca Turing ... ### 2. Beca Ada Lovelace ...",
  "source_documents": [
    "aranceles_y_becas.md (Sección: Becas y Ayudas)",
    "beca_women_in_tech_ada_lovelace.md (Sección: Requisitos)"
  ],
  "confidence_score": 1.0,
  "escalated_to_human": false,
  "cached": false,
  "mode": "opencode_advisor",
  "latency_ms": 11259.2,
  "action_buttons": [
    { "label": "0. Menú Principal", "value": "0" },
    { "label": "9. Otra Consulta al Asesor", "value": "9" }
  ]
}
```

---

## 3. Automated Test Verification (19/19 Tests)
- `tests/test_api_routes.py`: Health, chat, metrics, and escalations API routes.
- `tests/test_executables.py`: Existence, executable structure, and OS selector in installer/launcher.
- `tests/test_guardrails.py`: Prompt injection detection and relevance threshold.
- `tests/test_hybrid_search.py`: Lexical BM25 and Reciprocal Rank Fusion.
- `tests/test_ingestion.py`: Chunking with overlap and hash calculation.
- `tests/test_navigation.py`: 9-option root menu, 8 submenus, and '0' reset.
- `tests/test_opencode_intermediary.py`: OpenCode client connection and advisor mode.
- `tests/test_rag_pipeline.py`: End-to-end RAG question answering.
