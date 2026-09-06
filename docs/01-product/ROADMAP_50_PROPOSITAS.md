# Roadmap Maestro de Mejoras Técnicas: Nova OS '97 Admissions Assistant (v2.7.0)

- **Documento:** Roadmap Estratégico de Evolución Técnica
- **Versión:** 2.7.0
- **Estado:** Fases 1, 2 y 3 Completadas (100%) | Fases 4 y 5 Planificadas
- **Fecha:** 2026-09-04 (America/Bogota)
- **Alcance:** Arquitectura Backend FastAPI, RAG Híbrido, Base Vectorial ChromaDB, Frontend Next.js 15 / React 19 Retro OS '97, Testing y Developer Experience (Sin tocar temas de seguridad).

---

## 1. Visión General y Estructura por Fases

Este plan maestro organiza las **50 propuestas de mejora técnica** en **5 fases secuenciales de entrega**, asegurando que cada fase incremente la estabilidad, el rendimiento o la experiencia de usuario sin introducir regresiones en la base de código.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ROADMAP DE EVOLUCIÓN TÉCNICA (5 FASES)                          │
├────────────────────┬────────────────────┬────────────────────┬─────────────────────────┤
│ FASE 1: NÚCLEO     │ FASE 2: RENDIM.    │ FASE 3: FRONTEND   │ FASE 4: CALIDAD         │ FASE 5: EVOLUCIÓN │
│ RAG Y DATOS        │ Y ARQUITECTURA     │ Y ACCESIBILIDAD    │ Y TOOLING DX            │ Y HORIZONTES      │
│ (Prop. 1-7, 19, 21,│ (Prop. 11-16, 20,  │ (Prop. 25-30,      │ (Prop. 39-44,           │ (Prop. 8-10, 17,  │
│  23, 43)           │  22, 45, 46)       │  33-36)            │  47-49)                 │  18, 24, 31, 32,  │
│                    │                    │                    │                         │  37, 38, 50)      │
└────────────────────┴────────────────────┴────────────────────┴─────────────────────────┘
```

---

## 2. Mapa Consolidado de las 50 Propuestas por Categoría

### Categoría A: RAG Pipeline & Procesamiento del Conocimiento
- **Propuesta 1 [CRÍTICO]:** Recalibración adaptativa de pesos de fusión RRF ($k_{bm25}$ vs $k_{dense}$) según tipo de entidad (precios COP, códigos de cursos, sedes).
- **Propuesta 2 [CRÍTICO]:** Chunking semántico consciente de AST Markdown para preservar tablas de tarifas y bloques de cronogramas sin cortes artificiales.
- **Propuesta 3 [CRÍTICO]:** Fase de re-ranking local con Cross-Encoder liviano (CPU) previo a la inyección de contexto en el LLM.
- **Propuesta 4 [RECOMENDADO]:** Enrutador semántico de intenciones pre-LLM (Query Router determinista de baja latencia <15ms).
- **Propuesta 5 [RECOMENDADO]:** Extracción y normalización de metadatos estructurados en tiempo de indexación con filtros booleanos en ChromaDB (`where`).
- **Propuesta 6 [RECOMENDADO]:** Contextual Compression y Sentence Window Retrieval para mantener coherencia semántica sin sobrecargar el context window.
- **Propuesta 7 [RECOMENDADO]:** Normalizador fonético y lemático para nombres propios de sedes y convenios colombianos (Chapinero, Laureles, Comfama).
- **Propuesta 8 [OPCIONAL]:** Generación Aumentada de Consultas (HyDE) para preguntas ultra-cortas del usuario.
- **Propuesta 9 [OPCIONAL]:** Fallback transparente multi-embeddings entre modelos locales (bge-small vs ONNX optimizado).
- **Propuesta 10 [FUTURO]:** Graph RAG liviano modelando prerrequisitos y rutas curriculares de certificación internacional en un DAG.

### Categoría B: Backend Architecture & Rendimiento FastAPI
- **Propuesta 11 [CRÍTICO]:** Migración integral a Streaming SSE (Server-Sent Events) en `/api/v1/chat/stream` con emisión progresiva.
- **Propuesta 12 [CRÍTICO]:** Desacoplamiento y pool de conexiones HTTP persistente (`httpx.AsyncClient` singleton) para OpenCode y AGY.
- **Propuesta 13 [RECOMENDADO]:** Mecanismo de Backoff Exponencial y Circuit Breaker para conmutación de proveedores LLM ante degradación.
- **Propuesta 14 [RECOMENDADO]:** Middleware ASGI con inyección y propagación de `X-Request-ID` (Correlation ID) para trazabilidad unificada.
- **Propuesta 15 [RECOMENDADO]:** Migración de `escalations.json` a base transaccional SQLite con modo WAL (Write-Ahead Logging).
- **Propuesta 16 [RECOMENDADO]:** Validación estricta de esquemas con serializadores nativos Pydantic V2 (`model_validate` / `model_dump_json`).
- **Propuesta 17 [OPCIONAL]:** Exposición de métricas nativas OpenMetrics/Prometheus (`/metrics/prometheus`) con latencias p50/p95/p99.
- **Propuesta 18 [FUTURO]:** Worker en background asíncrono para hot-reload y re-indexación no bloqueante al modificar documentos en `backend/data/documents/`.

### Categoría C: Persistencia, Base de Datos & Caché
- **Propuesta 19 [CRÍTICO]:** Caché semántico multicapa en memoria (LRU) con umbral de similitud de coseno >0.96 para respuestas en <5ms.
- **Propuesta 20 [CRÍTICO]:** Rutina automatizada de compresión, vacuum y compactación de archivos de persistencia ChromaDB.
- **Propuesta 21 [RECOMENDADO]:** Calibración de parámetros HNSW (`M=16`, `efConstruction=64`) en ChromaDB para reducir RAM en un 35%.
- **Propuesta 22 [RECOMENDADO]:** Sistema de snapshots fechados de `chroma_db/` con capacidad de rollback inmediato ante re-indexaciones.
- **Propuesta 23 [RECOMENDADO]:** Serialización y persistencia en disco del índice invertido BM25 con hash de invalidación.
- **Propuesta 24 [OPCIONAL]:** Generador y exportador estructurado de tickets de escalamiento a CSV/XLSX (`/api/v1/escalations/export`).

### Categoría D: Frontend Architecture, Next.js 15 & Estado
- **Propuesta 25 [CRÍTICO]:** Centralización de estado global en Zustand (eliminación de prop drilling en chat, desktop y modal de métricas).
- **Propuesta 26 [CRÍTICO]:** Consumo de streams SSE con decodificador UTF-8 (`ReadableStreamDefaultReader`) y efecto progresivo en la UI.
- **Propuesta 27 [RECOMENDADO]:** Virtualización de la lista de mensajes del chat (`@tanstack/react-virtual`) para conversaciones largas.
- **Propuesta 28 [RECOMENDADO]:** Persistencia asíncrona de sesiones y configuración de escritorio en `IndexedDB` (reemplazo de `localStorage`).
- **Propuesta 29 [RECOMENDADO]:** Aislamiento estricto de React Server Components (RSC) vs Client Components en Next.js 15.
- **Propuesta 30 [RECOMENDADO]:** Code Splitting dinámico (`next/dynamic` con `ssr: false`) para componentes secundarios pesados (modales y visor de tickets).
- **Propuesta 31 [OPCIONAL]:** Detección de conectividad offline/online con alerta retro vintage ("Error de Comunicación de Red").
- **Propuesta 32 [FUTURO]:** Arquitectura modular de ventanas desktop extensible (`DesktopAppWindow`) para soportar futuras mini-apps retro.

### Categoría E: UI / Retro CRT Engine & Accesibilidad Web
- **Propuesta 33 [CRÍTICO]:** Aceleración por GPU / WebGL Shader del filtro óptico CRT para eliminar sobrecarga de CPU en equipos limitados.
- **Propuesta 34 [RECOMENDADO]:** Modo accesibilidad "Bypass Retro" con tipografía del sistema y contraste WCAG 2.1 AAA.
- **Propuesta 35 [RECOMENDADO]:** Trampa de foco (Focus Trap) y navegación completa por teclado en la ventana retro (`Tab`, `Escape`, `Enter`).
- **Propuesta 36 [RECOMENDADO]:** Panel de control vintage ("Monitor Controls") con sliders para calibrar brillo, curvatura y scanlines.
- **Propuesta 37 [OPCIONAL]:** Diseño responsivo adaptativo optimizado para smartphones (Modo PDA vintage / Palm OS).
- **Propuesta 38 [OPCIONAL]:** Feedback sonoro procedural retro sintetizado en Web Audio API (<2KB de código) para clicks y envio.

### Categoría F: Testing, Calidad de Software & Benchmarking
- **Propuesta 39 [CRÍTICO]:** Pipeline de evaluación continua de fidelidad RAG con métricas de Answer Relevance y Context Recall.
- **Propuesta 40 [RECOMENDADO]:** Pruebas de mutación (`mutmut`) en el motor de cálculo de precios COP y reglas comerciales.
- **Propuesta 41 [RECOMENDADO]:** Suite de pruebas de carga y concurrencia con Locust (`scripts/load_test.py`) para 50 usuarios simultáneos.
- **Propuesta 42 [RECOMENDADO]:** Proveedor de pruebas `MockDualAdvisor` determinista de latencia controlada para tests instantáneos (<3s).
- **Propuesta 43 [RECOMENDADO]:** Validador CI sintáctico y estructural de documentos Markdown en `backend/data/documents/`.
- **Propuesta 44 [OPCIONAL]:** Snapshot testing visual de la UI retro con Playwright para evitar regresiones de maquetación.

### Categoría G: DevOps, Tooling Local & Developer Experience
- **Propuesta 45 [CRÍTICO]:** Entorno `docker-compose.yml` multi-stage para FastAPI y Next.js con inicio en un solo comando.
- **Propuesta 46 [CRÍTICO]:** Validación tipada centralizada de variables de entorno mediante `pydantic-settings`.
- **Propuesta 47 [RECOMENDADO]:** Hooks de pre-commit automatizados con Ruff (Python) y Prettier/ESLint (TypeScript).
- **Propuesta 48 [RECOMENDADO]:** Comando de diagnóstico CLI `python run.py doctor` para validación instantánea de puertos, dependencias y DB.
- **Propuesta 49 [RECOMENDADO]:** Verificación y renderizado automatizado de diagramas de arquitectura en el pipeline de CI.
- **Propuesta 50 [FUTURO]:** Empaquetado nativo de escritorio standalone con Tauri (Rust) para modo kiosco en recepciones físicas.

---

## 3. Cronograma de Ejecución por Fases

| Fase | Enfoque Principal | Propuestas Asignadas | Estado | Meta Operativa |
| :--- | :--- | :--- | :---: | :--- |
| **Fase 1** | **Precisión de Datos y Recuperación RAG** | 1, 2, 3, 4, 5, 6, 7, 19, 21, 23, 43 | **Completada** | 0% fragmentación de tablas COP, recall semántico exacto, indexación BM25 persistida. |
| **Fase 2** | **Rendimiento Backend y Resiliencia** | 11, 12, 13, 14, 15, 16, 20, 22, 45, 46, TODO-2.11 | **Completada** | Streaming SSE token a token, pooling HTTP, pipeline en cascada multi-filtro (precios vs horarios), SQLite WAL y Docker. |
| **Fase 3** | **Frontend Moderno, UI Retro & Accesibilidad** | 25, 26, 27, 28, 29, 30, 33, 34, 35, 36 | **Completada** | Zustand store, decodificación SSE progresiva, filtro CRT acelerado por GPU (60 FPS), modo WCAG AAA, focus trap y panel OSD de monitor. |
| **Fase 4** | **Testing Automatizado, QA y Tooling DX** | 39, 40, 41, 42, 44, 47, 48, 49 | **Planificada** | Evaluación continua Ragas, Locust carga concurrente, CLI doctor y pre-commits. |
| **Fase 5** | **Ampliación de Experiencia y Nuevos Horizontes** | 8, 9, 10, 17, 18, 24, 31, 32, 37, 38, 50 | **Planificada** | Graph RAG, HyDE, audio web retro, exportador comercial y empaquetado Tauri kiosco. |

---

## 4. Criterios de Aceptación por Fase

1. **Aceptación Fase 1:** Ningún valor de precio o cuota fragmentado en chunks; similitud de búsqueda <10ms en caché; 55 tests de pytest y benchmark 80/80 pasando al 100%.
2. **Aceptación Fase 2:** Time-to-First-Token en streaming <300ms; soporte concurrente multi-hilo de tickets en SQLite sin bloqueos de archivo.
3. **Aceptación Fase 3:** 60 FPS estables en el escritorio retro con CRT activo en laptops de bajos recursos; 0 fugas de re-renderizado mediante Zustand.
4. **Aceptación Fase 4:** Suite completa de tests ejecutándose en <5 segundos con mocks; reporte Locust validando 50 usuarios concurrentes sin caídas.
5. **Aceptación Fase 5:** Todas las características opcionales y futuras documentadas e integradas bajo diseño modular desacoplado.

---

## 5. Tablero de Control y Seguimiento Detallado

Para el seguimiento tarea por tarea con casillas de verificación, responsables y estado operativo:
- 📋 **[Tablero TODO de Implementación (TODO_50_PROPOSITAS.md)](TODO_50_PROPOSITAS.md)**

