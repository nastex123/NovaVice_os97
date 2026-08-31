# 🌴 Nova Idiomas Colombia — "Nova OS '97" Admissions Assistant (v2.6.0)

> **Asistente Inteligente de Admisiones con RAG Híbrido (FastAPI + Next.js 15), Switch Dual de Razonamiento (OpenCode / AGY Antigravity) y Experiencia Visual Retro 90s con Filtro CRT Anti-Fatiga.**  
> Diseñado para responder con precisión quirúrgica sobre **cursos de idiomas, franjas horarias, tarifas oficiales en COP, certificaciones internacionales (IELTS, TOEFL, DELF, Goethe) y sedes en Colombia**, garantizando cero alucinaciones y escalamiento estructurado a asesores humanos.

---

## 📚 Documentación Técnica y Exposición

* 📖 **[Guía Maestra de Explicación Técnica y Presentación](EXPLICACION_TECNICA.md):** Documento exhaustivo paso a paso para exponer, enseñar y defender la arquitectura técnica del proyecto ante evaluadores y equipos de desarrollo.
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

## 🏗️ Arquitectura del Sistema (100% en Python + Next.js 15)

```text
┌────────────────────────────────────────────────────────────────────────┐
│               CAPA DE EXPERIENCIA DE USUARIO (FRONTEND)               │
│                                                                        │
│   Next.js 15 (App Router) + TypeScript + Tailwind CSS                  │
│   ├── Ventana Retro Macintosh OS '97 (Barra rayada + Botones retro)   │
│   ├── Filtro Óptico CRT Anti-Glare (Scanlines + Fósforo Ámbar + Switch)│
│   ├── Oasis Tropical Pixel-Art (8 Palmeras con balanceo + Nubes)      │
│   ├── Renderizador Markdown GFM Seguro con Sanitización               │
│   └── Modal de Telemetría en Tiempo Real (Costos, Tokens, Latencia)   │
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
   - **Oasis Pixel-Art Animado:** 8 palmeras multi-capa con balanceo tropical, 8 nubes a la deriva y bandadas de gaviotas a 60 FPS aceleradas por hardware (GPU).

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

El proyecto cuenta con una suite completa de pruebas unitarias y de integración en `pytest`:

```bash
./venv/bin/pytest -v
```

```text
============================= 25 passed in 15.97s ==============================
```

Las 25 pruebas validan:
- Estado del servidor y detección de motor asesor.
- Indexación y chunking con solapamiento de los 82 documentos.
- Búsqueda híbrida (ChromaDB + BM25) y fusión RRF.
- Escalamiento automático a humanos ante consultas fuera de alcance.
- Filtros de seguridad ante inyecciones de prompt.
- Funcionamiento de la máquina de estados de navegación y continuidad de menús.
- Integración E2E tanto con el motor OpenCode como con el motor AGY Antigravity.
