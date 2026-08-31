# Technological Enhancement Proposals for Admissions RAG Assistant (Version 2.6.0)

- **Document Version:** 2.6.0
- **Status:** Implemented & Verified
- **Date:** 2026-08-30 (America/Bogota)
- **Scope:** Pure Python RAG Engine, Next.js 15 + PixiJS Frontend, OpenCode Deep Reasoning Engine, Observability & Multiplatform Executables

---

## 1. Implementation Status Overview

| Proposal | Enhancement Area | Status | Implementation Reference |
| :--- | :--- | :---: | :--- |
| **P-01** | Hybrid Search (Dense Cosine + Pure Python BM25 via RRF) | **Implemented** | `src/rag/hybrid_retriever.py` |
| **P-02** | 87 Official Documents & 264 Chunks Knowledge Base | **Implemented** | `data/documents/` (7 Clusters) |
| **P-03** | Interactive Guided State Machine (1-9 & 8 Submenus) | **Implemented** | `src/core/navigation.py` |
| **P-04** | OpenCode Multi-Document Deep Reasoning (45s window) | **Implemented** | `src/core/opencode_client.py` |
| **P-05** | Next.js 15 + PixiJS WebGL Particle Constellation UI | **Implemented** | `frontend/` |
| **P-06** | Native GFM Markdown Renderer (`react-markdown` + `remark-gfm`) | **Implemented** | `frontend/src/components/ChatContainer.tsx` |
| **P-07** | Cross-Platform Installer & Process Launcher (`run.py`) | **Implemented** | `installer.py`, `run.py`, `.bat`, `.sh` |
| **P-08** | Pre-Flight Prompt Injection & Jailbreak Guardrail | **Implemented** | `src/core/guardrails.py` |
| **P-09** | Automated Escalation Logging & Webhook Dispatcher | **Implemented** | `src/core/dispatcher.py` |
| **P-10** | Dual Invalidation-Aware Cache (Exact + Semantic) | **Implemented** | `src/core/cache.py` |
| **P-11** | Prometheus Metrics Exporter & Real-Time JSON Telemetry | **Implemented** | `src/core/metrics.py` |
| **P-12** | Voice Dictation via Browser Web Speech API | **Implemented** | `frontend/src/components/ChatInput.tsx` |

---

## 2. Deep Dive on Core Enhancements

### 2.1 Hybrid Search with Auto-Fitting BM25
- Combines ChromaDB dense vector embeddings with an in-memory pure Python BM25 index that automatically synchronizes with the vector store corpus.
- Aggregates candidate ranks using Reciprocal Rank Fusion (RRF, $k=60$).

### 2.2 OpenCode Intermediary Bridge for Deep Reasoning
- Connects the FastAPI backend to an OpenCode daemon on port 4096.
- Injects the top 5 full candidate chunks into a senior academic advisor reasoning prompt.
- Provides a 45.0-second reasoning window allowing OpenCode to execute full Chain-of-Thought passes (~800+ reasoning tokens) before synthesizing structured answers.

### 2.3 Next.js 15 + PixiJS Web Application
- High-performance WebGL particle background reacting to cursor gravity.
- Dark Glassmorphism sidebar with live server indicators and telemetry cards.
- Native GFM Markdown rendering with custom styled components (neon crimson bullets, callout blockquote cards, clean headers without raw hash marks).
