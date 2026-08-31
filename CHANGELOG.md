# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### [2026-08-30 23:23] [Changed]
- **Adopción de Nombre Oficial del Proyecto y Repositorio: `synapse-admissions-ai`:**
  - Definido formalmente el nombre de marca **Synapse Admissions AI** (`synapse-admissions-ai`) para el repositorio de GitHub y el ecosistema del proyecto.
  - Actualizado `frontend/package.json` con `"name": "synapse-admissions-ai"` y versión `2.6.0`.
  - Configurado el archivo maestro `.gitignore` excluyendo entornos virtuales (`venv/`), dependencias de Node (`node_modules/`), artefactos de build (`.next/`), archivos `.env` y temporales de testing (`.pytest_cache/`).
  - Sincronizado el título principal de [`README.md`](README.md).
- Motivo: Establecer una identidad de proyecto moderna, técnica y unificada lista para su publicación en GitHub.

### [2026-08-30 23:20] [Docs]
- **Creación de Guías Técnicas Profundas de Ingeniería y Optimización en `docs/`:**
  - **`docs/04-engineering/backend-core-guide.md`**: Desglose técnico de cada módulo del backend (`config.py`, `guardrails.py`, `navigation.py`, `opencode_client.py`, `cache.py`, `dispatcher.py`, `memory.py`, `metrics.py`), bloques de código comentados, propósito operativo y justificación técnica.
  - **`docs/04-engineering/rag-subsystem-deep-dive.md`**: Guía profunda del motor RAG, fórmulas matemáticas (Okapi BM25 TF/IDF y Reciprocal Rank Fusion $k=60$), lematización en español y segmentación con solapamiento (*overlap*).
  - **`docs/04-engineering/frontend-nextjs-pixijs-guide.md`**: Arquitectura del frontend moderno Next.js 15, aceleración WebGL con PixiJS, componentes estilizados de `react-markdown` y captura de voz.
  - **`docs/04-engineering/executables-and-operations-guide.md`**: Especificación de la suite de ejecutables multiplataforma (`run.py`, `installer.py`, scripts `.bat` y `.sh`), gestión de subprocesos y captura de señales `SIGINT`.
  - **`docs/08-operations/optimization-and-performance-guide.md`**: Análisis exhaustivo de las 7 optimizaciones técnicas implementadas (timeout de razonamiento de 45s, auto-poblado BM25, pool HTTPX, caché con invalidación por hash, renderizado WebGL por GPU y Markdown GFM).
- Motivo: Proveer una documentación técnica de nivel enterprise que explique detalladamente para qué sirve cada componente, las tecnologías utilizadas, los bloques de código y las razones de cada optimización.

### [2026-08-30 23:15] [Docs]
- **Creación de Suite Completa de Architecture Decision Records (ADR-001 a ADR-007):**
  - **`ADR-001`**: *Adopción de Stack RAG en Python Puro con FastAPI y ChromaDB frente a Plataformas No-Code y Frameworks Pesados.*
  - **`ADR-002`**: *Diseño de Máquina de Estados para Navegación Guiada Interactiva con 9 Opciones y 8 Submenús Temáticos.*
  - **`ADR-003`**: *Sustitución de Hermes Agent por OpenCode como Servidor de Razonamiento Profundo y Asesor Humano de Admisiones.*
  - **`ADR-004`**: *Adopción de Next.js 15, PixiJS WebGL y Renderizador Markdown GFM para la Experiencia de Usuario.*
  - **`ADR-005`**: *Implementación de Recuperación Híbrida combinando Similitud Coseno Densa y BM25 en Python Puro con Reciprocal Rank Fusion.*
  - **`ADR-006`**: *Arquitectura de Supervisión de Procesos y Suite de Instalación Multiplataforma para Windows y Linux (`run.py`, `installer.py`).*
  - **`ADR-007`**: *Diseño de Guardrails de Seguridad de Entrada y Protocolo de Escalamiento Humano con Tickets Estructurados.*
  - **`docs/09-decisions/README.md`**: Índice general de decisiones arquitectónicas con tabla de estados, fechas y áreas.
- Motivo: Formalizar exhaustivamente las justificaciones, alternativas evaluadas y consecuencias de todas las decisiones técnicas tomadas en la evolución del proyecto bajo los estándares de la skill de documentación.

### [2026-08-30 23:08] [Added]
- **Renderizador Markdown Completo GFM con Estética Dark Glassmorphism en Frontend:**
  - Integradas las librerías `react-markdown` y `remark-gfm` en `frontend/src/components/ChatContainer.tsx` eliminando por completo el renderizado de signos residuales de sintaxis (como `#### - `, `* `, `> ` o `---`).
  - **Viñetas con Brillo Neón Carmesí:** Cada elemento de lista desordenada (`* `, `- `, `•`) se procesa como un ítem con viñeta luminosa personalizada (`bg-crimson shadow-glow`).
  - **Cajas de Notas y Citas Estilizadas (`blockquote`):** Las líneas de advertencia o aclaración que inician con `>` se transforman en tarjetas translúcidas Dark Glassmorphism con borde lateral carmesí e ícono de información (`Info`).
  - **Encabezados Limpios y Tipografía:** Títulos (`H1-H4`) renderizados con tipografía de exhibición (`font-display`), resaltados en color rose/cyber-blue y sin mostrar signos `#`.
  - **Sanitizador Previo:** Función `sanitizeMarkdown` que corrige patrones mixtos (ej. encabezados combinados con guiones) antes de la renderización.
- Motivo: Proporcionar una lectura impecable, visual y profesional de las respuestas enriquecidas del Asesor OpenCode sin caracteres de sintaxis visibles.
