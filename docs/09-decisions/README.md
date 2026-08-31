# Architecture Decision Records (ADR) - Index

Este directorio almacena el registro formal de todas las decisiones arquitectónicas y técnicas tomadas a lo largo de la evolución del proyecto del Asistente de Admisiones de Nova Tech University.

---

## 📑 Índice General de ADRs

| ID | Título | Estado | Fecha | Área de Decisión |
| :--- | :--- | :---: | :---: | :--- |
| [**ADR-001**](ADR-001-rag-stack-and-pure-python-architecture.md) | Adopción de Stack RAG en Python Puro con FastAPI y ChromaDB | `Accepted` | 2026-08-30 | Core RAG & Backend |
| [**ADR-002**](ADR-002-guided-menu-navigation-state-machine.md) | Máquina de Estados para Navegación Guiada con 9 Opciones y Submenús | `Accepted` | 2026-08-30 | UX Conversacional & Navegación |
| [**ADR-003**](ADR-003-opencode-as-deep-reasoning-human-advisor.md) | Sustitución de Hermes Agent por OpenCode como Servidor de Razonamiento Profundo | `Accepted` | 2026-08-30 | Inteligencia Artificial & Agentes |
| [**ADR-004**](ADR-004-nextjs15-and-pixijs-frontend-architecture.md) | Arquitectura Frontend con Next.js 15, PixiJS WebGL y Renderizado Markdown GFM | `Accepted` | 2026-08-30 | Frontend & Diseño Visual |
| [**ADR-005**](ADR-005-hybrid-retriever-reciprocal-rank-fusion.md) | Recuperación Híbrida Vectorial y Léxica con Fusión RRF y Auto-Ajuste BM25 | `Accepted` | 2026-08-30 | Recuperación de Información & RAG |
| [**ADR-006**](ADR-006-multiplatform-executable-supervision.md) | Lanzador Supervisor Unificado y Suite de Instalación Multiplataforma | `Accepted` | 2026-08-30 | DevOps, Ejecutables & Multiplataforma |
| [**ADR-007**](ADR-007-guardrails-and-structured-escalation-protocol.md) | Protocolo de Guardrails de Entrada y Derivación Estructurada a Consejeros | `Accepted` | 2026-08-30 | Seguridad, Guardrails & Escalamiento |

---

## 🏛️ Estructura Estándar de los ADRs
Cada documento sigue la estructura formal exigida:
- **ID & Título**
- **Fecha** (`America/Bogota`)
- **Estado** (`Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded`)
- **Contexto**
- **Problema**
- **Opciones Consideradas**
- **Decisión**
- **Justificación**
- **Consecuencias (Positivas / Negativas / Riesgos Mitigados)**
