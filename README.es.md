# 🌴 Nova Idiomas Colombia — Asistente de Admisiones "Nova OS '97" (v2.7.0)

<div align="center">

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Language: Español](https://img.shields.io/badge/Idioma-Español-green.svg)](README.es.md)
[![Tests: 72/72 Pasados](https://img.shields.io/badge/Tests-72%2F72%20Pasados-brightgreen.svg)](backend/tests/)
[![Fidelidad Factual: 50/50 (100%)](https://img.shields.io/badge/Fidelidad-50%2F50%20(100%25)-brightgreen.svg)](scripts/evaluate_rag.py)
[![Next.js 15](https://img.shields.io/badge/Frontend-Next.js%2015-black.svg)](frontend/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.115-009688.svg)](backend/)
[![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-orange.svg)](backend/data/chroma_db/)
[![Docker Compose](https://img.shields.io/badge/Docker-Multi--stage%20Listo-blue.svg)](docker-compose.yml)

</div>

> **Asistente Inteligente de Admisiones con RAG Híbrido (FastAPI + Next.js 15), Switch Dual de Razonamiento (OpenCode / AGY Antigravity) y Experiencia Visual Retro 90s con Filtro CRT Anti-Fatiga.**  
> Diseñado para responder con precisión quirúrgica sobre **cursos de idiomas, franjas horarias, tarifas oficiales en COP, certificaciones internacionales (IELTS, TOEFL, DELF, Goethe) y sedes en Colombia**, garantizando cero alucinaciones y escalamiento estructurado a asesores humanos.

---

## 📚 Documentación Técnica y Exposición

* 📖 **[Guía Maestra de Explicación Técnica y Presentación](EXPLICACION_TECNICA.md):** Documento exhaustivo paso a paso para exponer, enseñar y defender la arquitectura técnica del proyecto ante evaluadores y equipos de desarrollo (*[Versión en Inglés](TECHNICAL_EXPLANATION.md)*).
* 🚀 **[Roadmap Estratégico de 50 Propuestas Técnicas](docs/01-product/ROADMAP_50_PROPOSITAS.md):** Plan maestro de evolución técnica en 5 fases secuenciales (RAG, Backend, Frontend, Testing y DevOps) sin tocar seguridad.
* 📜 **[Registro de Cambios (Changelog)](CHANGELOG.md):** Historial cronológico estricto de todas las modificaciones y versiones bajo zona horaria `America/Bogota`.
* 🏛️ **[Directorio de Arquitectura y Decisiones (docs/)](docs/):** Documentación técnica organizada por PRD, Arquitectura, Ingeniería, IA y ADRs.

---

## 📌 Caso de Uso y Objetivos de Negocio

La academia de idiomas **Nova Idiomas Colombia** cuenta con sedes en **Bogotá (Chicó y Chapinero)**, **Medellín (Poblado y Laureles)**, **Cali (Granada)** y una división **100% Virtual Sincrónica**. Recibe cientos de consultas diarias:
- **Cursos y Metodología:** Inglés General, Intensivo, Business English, Francés DELF/DALF, Alemán Goethe, Portugués, Español para extranjeros. Metodología *Flipped Classroom* comunicativa.
- **Horarios y Franjas:** Madrugadores (6:00-8:00 AM), Diurnos, Nocturnos (After Work 6:30-8:30 PM), Sabatinos y Dominicales.
- **Precios y Financiación en COP:** Tarifas oficiales en Pesos Colombianos, 10% de descuento por pago de contado, 3 cuotas sin interés con Nequi/PSE/Bancolombia y convenios con cajas de compensación (Compensar, Colsubsidio, Comfama).
- **Examen de Clasificación:** Placement Test 100% gratuito con agendamiento inmediato.
- **Certificaciones Oficiales:** Preparación y registro para IELTS Academic/General, TOEFL iBT, Cambridge B2/C1, DELF/DALF y Goethe.

---

## 📂 Estructura del Repositorio (Monorepo Limpio)

```text
synapse-admissions-ai/ (NovaVice_os97)
├── backend/                               # 🐍 Backend FastAPI & Inteligencia Artificial
│   ├── data/                              # Base de conocimiento (83 docs, incl. 12_04 becas→descuentos) y tickets
│   │   ├── documents/                     # Archivos Markdown con programas y reglamentos
│   │   └── escalations.json               # Registro de tickets humanos
│   ├── src/                               # Código fuente backend (API, bot, core, rag)
│   ├── tests/                             # Suite completa de 27 pruebas en Pytest (incl. caché semántica)
│   └── requirements.txt                   # Dependencias Python
│
├── frontend/                              # 🌐 Aplicación Web Retro Next.js 15
│   ├── src/                               # Componentes, App Router y Estilos CRT
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/                                  # 📚 Documentación Técnica y Arquitectónica
│   ├── assets/                            # Recursos y PDFs (Enunciado original)
│   ├── 01-product/                        # PRD (becas=descuentos)
│   ├── 03-architecture/                   # Arquitectura y propuestas (threshold 0.35 pilar)
│   ├── 04-engineering/                    # Guías de ingeniería y diseño técnico (centroid, NFD)
│   ├── 05-ai/                             # Integraciones de IA y OpenCode/AGY (heavy only)
│   ├── 08-operations/                     # Optimización, SESSION_HANDOFF y TODO becas
│   └── 09-decisions/                      # Architecture Decision Records (ADR-001 a ADR-008)
│
├── scripts/                               # 🛠️ Scripts auxiliares e instaladores
│   ├── installer.py                       # Lógica de instalación multiplataforma
│   ├── install.sh                         # Instalador para Linux / macOS
│   └── install.bat                        # Instalador para Windows
│
├── .agents/                               # Reglas y configuraciones de agentes
├── .env.example                           # Plantilla de variables de entorno
├── AGENTS.md                              # Definición de agentes y comandos
├── CHANGELOG.md                           # Historial cronológico estricto
├── TECHNICAL_EXPLANATION.md               # Guía técnica maestra en inglés
├── EXPLICACION_TECNICA.md                 # Guía técnica maestra en español
├── README.md                              # Documentación principal en inglés
├── README.es.md                           # Documentación en español
├── pytest.ini                             # Configuración centralizada de Pytest
├── run.py                                 # Supervisor raíz multi-proceso con selector
├── start.sh                               # Lanzador rápido Linux/macOS
└── start.bat                              # Lanzador rápido Windows
```

---

## 🏗️ Arquitectura del Sistema (100% en Python + Next.js 15)

```text
┌────────────────────────────────────────────────────────────────────────┐
│               CAPA DE EXPERIENCIA DE USUARIO (FRONTEND)               │
│                                                                        │
│   Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS       │
│   ├── Shell RSC (app/page.tsx) y Frontera de Cliente (RetroDesktop.tsx)│
│   ├── Stores Centralizados Zustand (useChatStore, useSettingsStore...) │
│   ├── Code Splitting Dinámico (next/dynamic, -54.3% bundle inicial)    │
│   ├── Lista Virtualizada (@tanstack/react-virtual en >30 mensajes)     │
│   ├── Filtro Óptico CRT Acelerado por GPU (transform: translateZ, 60fps│
│   ├── Modo Accesible "Bypass Retro" WCAG 2.1 AAA (.a11y-mode >=7:1)    │
│   ├── Trampa de Foco Accesible (useFocusTrap.ts) y Atajos de Teclado   │
│   ├── Panel OSD Vintage "Monitor Controls" (Calibración en tiempo real)│
│   ├── Oasis Pixel-Art (8 Palmeras + 18 Nubes + Gaviotas + Hierba Pixel)│
│   └── Modal de Telemetría en Tiempo Real (Costos, Tokens, Latencia)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON (:3000 -> :8000)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 CAPA DE ENTRADA Y API GATEWAY (FASTAPI)                │
│                                                                        │
│   FastAPI Core Engine (:8000) + Pydantic v2 Schemas                    │
│   ├── POST /api/v1/chat       (Consulta conversacional y navegación)  │
│   ├── GET  /api/v1/health     (Estado, docs indexados, motor asesor)  │
│   ├── GET  /api/v1/metrics    (Telemetría de tokens, latencia y cache)│
│   └── POST /api/v1/escalate   (Generación de tickets humanos)         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│         CAPA DE ENRUTAMIENTO DETERMINISTA Y CACHÉ SEMÁNTICO            │
│                                                                        │
│   ├── Máquina de Estados de Navegación (Opciones 1..4, Submenús y 0)   │
│   │     └─► Retorno Determinista Inmediato (<5ms, 0 tokens gastados)   │
│   │                                                                    │
│   └── Caché Semántico Dual (Hash SHA-256 + Vectorial)                  │
│         └─► Cache Hit: Retorno Sub-30ms                                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Cache Miss / Consulta Abierta)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 PIPELINE RAG HÍBRIDO (DENSE + SPARSE)                  │
│                                                                        │
│   1. Recuperación Densa (ChromaDB Persistent + Embeddings ONNX Local)  │
│   2. Recuperación Léxica (BM25 Okapi + Stemming en Español)            │
│   3. Fusión de Ranking (Reciprocal Rank Fusion RRF, k = 60)            │
│   4. Guardrail de Relevancia (Umbral 0.50 -> Escalamiento a Humano)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│          CAPA DE RAZONAMIENTO DUAL: ASESOR DE ADMISIONES               │
│                                                                        │
│   Switch Pre-Lanzamiento (`run.py --advisor [opencode|agy]`):          │
│   [Opción 1: OpenCode Daemon :4096]   [Opción 2: AGY Antigravity CLI]  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Características Principales

1. **RAG Híbrido con 82 Documentos Oficiales (245 Chunks):**
   - Indexación en ChromaDB y BM25 de todos los programas, niveles MCER, precios, sedes y reglamentos.
   - Respuestas fundamentadas al 100% en información institucional verificada.

2. **Switch Pre-Lanzamiento de Motor de Asesoría (OpenCode vs AGY):**
   - Permite seleccionar interactivamente o por CLI el motor de inferencia:
     - `[1] 🤖 OpenCode Reasoning Engine (:4096)`
     - `[2] 🚀 AGY (Google Antigravity CLI / Engine)`

3. **Frontend Retro "Nova OS '97" & Filtro CRT Anti-Fatiga:**
   - Estética inspirada en Poolsuite.net y GTA Vice City de los 80s/90s.
   - **Filtro Óptico CRT:** Scanlines horizontales sutiles y fósforo ámbar que inhiben activamente la fatiga ocular, con interruptor `[ 📺 CRT: ON/OFF ]`.
   - **Oasis Pixel-Art Animado:** 8 palmeras multi-capa con balanceo, **18 nubes volumétricas bidireccionales (9 L2R + 9 R2L)** y 6 bandadas de gaviotas con aleteo 2 estados, más **alfombra densa de hierba verde seco retro (#8A9A6A) con 28 mechones con sway** a 60 FPS GPU (base estática + tufts `grassSway`).

4. **Navegación Guiada Determinista y Cero Alucinaciones:**
   - Menú interactivo estructurado (1. Cursos, 2. Horarios, 3. Precios COP, 4. Sedes/Admisiones y retorno 0).
   - Umbral de confianza semántica de 0.50: si la consulta está fuera del alcance oficial, genera un ticket `ESC-YYYYMMDD-XXXX` y deriva a secretaría académica.

5. **Telemetría y Control de Costos en Vivo:**
   - Panel de métricas con seguimiento de consultas, tasa de aciertos en caché, tasa de escalamiento a humano, consumo de tokens y costo estimado en USD.

---

## ⚡ Instalación y Puesta en Marcha

### Prerrequisitos
- **Python 3.10 o superior** (Recomendado 3.12)
- **Node.js (v18+) y npm**

### 1. Instalación Automática
```bash
# En Linux / macOS:
./install.sh

# En Windows:
install.bat
```
*(Crea el entorno virtual `venv`, instala las dependencias de Python y Node.js, e indexa automáticamente los 82 documentos en ChromaDB).*

### 2. Ejecución con Selector de Motor
```bash
# Modo interactivo (te preguntará si deseas OpenCode o AGY):
./start.sh
# o en Windows: start.bat
# o con Python: python3 run.py

# Iniciar directamente con AGY (Google Antigravity CLI):
./start.sh -a agy

# Iniciar directamente con OpenCode:
./start.sh -a opencode
```

Al iniciar, se levantarán automáticamente:
- 🌐 **Frontend Retro Nova OS '97:** [http://localhost:3000](http://localhost:3000)
- 🐍 **Backend FastAPI Core:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📖 **Documentación Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📊 **Métricas Prometheus:** [http://127.0.0.1:8000/metrics/prometheus](http://127.0.0.1:8000/metrics/prometheus)

---

## 🔌 Endpoints de la API REST

- `POST /api/v1/chat`: Consulta interactiva con respuesta RAG estructurada y botones de acción.
- `POST /api/v1/chat/stream`: Streaming de respuestas token por token (SSE).
- `POST /api/v1/webhook`: Webhook universal para integración con formularios web y canales externos.
- `POST /api/v1/tools/quote`: Cálculo dinámico de cotizaciones en COP con descuentos.
- `POST /api/v1/tools/placement-test`: Registro para examen de nivelación gratuito.
- `GET /api/v1/metrics`: Telemetría operativa en formato JSON.
- `GET /api/v1/escalations`: Registro de tickets de escalamiento humano.
- `GET /api/v1/health`: Estado de salud, documentos indexados y motor de asesor configurado.

---

## 🧪 Pruebas Automatizadas

El proyecto cuenta con una suite completa de 72 pruebas unitarias, de integración y E2E en `pytest`:

```bash
pytest backend/tests -v
```

```text
======================== 72 passed, 1 warning in ~88s ========================
```

Las 72 pruebas validan:
- Estado del servidor y detección del motor de asesor (OpenCode / AGY).
- Indexación, chunking y preservación semántica de tablas AST de los 83 documentos.
- Búsqueda híbrida (ChromaDB + BM25) y fusión RRF adaptativa.
- Clasificador y enrutador semántico de micro-intenciones sin secuestro de consultas abiertas.
- Escalamiento automático a humanos ante consultas complejas o fuera de dominio.
- Filtros de seguridad ante inyecciones de prompt y sanitización Unicode NFD.
- Streaming SSE continuo, serialización Pydantic v2 y persistencia transaccional SQLite WAL.
- Coexistencia fluida de aciertos de caché exacta y similitud coseno semántica.

## URL del Repositorio: https://github.com/nastex123/NovaVice_os97.git
