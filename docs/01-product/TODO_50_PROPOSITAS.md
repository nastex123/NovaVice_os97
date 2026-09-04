# 📋 TODO Maestro de Implementación Técnica (50 Propuestas en 5 Fases)
**Proyecto:** *Nova Idiomas Colombia — "Nova OS '97" Admissions Assistant (v2.7.0)*  
**Fecha de Creación:** 2026-09-04 (America/Bogota)  
**Alcance:** Seguimiento granular de tareas de ingeniería (sin tocar temas de seguridad).

---

## 📊 Tablero de Estado General

| Fase | Enfoque Principal | Total Tareas | Completadas | En Progreso | Pendientes | Estado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Fase 1** | Precisión de Datos y Recuperación RAG | 11 | 2 | 0 | 9 | 🚀 En Progreso |
| **Fase 2** | Rendimiento Backend y Resiliencia | 11 | 0 | 0 | 11 | ⏳ Pendiente |
| **Fase 3** | Frontend Moderno, UI Retro & Accesibilidad | 10 | 0 | 0 | 10 | ⏳ Pendiente |
| **Fase 4** | Testing Automatizado, QA & Tooling DX | 8 | 0 | 0 | 8 | ⏳ Pendiente |
| **Fase 5** | Horizontes Futuros y Despliegues Especializados | 11 | 0 | 0 | 11 | ⏳ Pendiente |
| **TOTAL** | **Propuestas de Mejora Técnica** | **51** | **2** | **0** | **49** | **3.9%** |

---

## 🟢 FASE 1: Precisión de Datos y Recuperación RAG (11 Tareas)
> **Objetivo:** Garantizar 0% fragmentación de tablas de precios y cronogramas, ponderación dinámica léxica/densa, re-ranking local de alta fidelidad y aceleración por caché semántico.

- [x] **TODO-1.1 [Prop. 1 - CRÍTICO] Recalibración adaptativa de pesos de fusión RRF:**
  - [x] Implementar detector de entidades en `backend/src/rag/hybrid_retriever.py` (precios COP, códigos de curso, nombres de sedes, horarios).
  - [x] Asignar dinámicamente mayor factor de ponderación a BM25 ($k_{bm25}=40$, $k_{dense}=75$, $w_{bm25}=1.25$) ante consultas de cifras exactas.
  - [x] Validar que la fusión mantenga orden de relevancia en el benchmark de 80 variantes.
- [x] **TODO-1.2 [Prop. 2 - CRÍTICO] Chunking semántico de Markdown consciente de tablas AST:**
  - [x] Implementar parser semántico de bloques Markdown (`_extract_blocks`) en `backend/src/rag/ingestion.py`.
  - [x] Aislar bloques de tablas de precios COP y cronogramas para tratarlos como unidades atómicas indivisibles con preservación de encabezados.
  - [x] Crear tests unitarios en `backend/tests/test_ingestion.py` validando preservación atómica y partición con cabeceras.
- [ ] **TODO-1.3 [Prop. 3 - CRÍTICO] Fase de re-ranking local con Cross-Encoder en CPU:**
  - [ ] Integrar un re-ranker local ultra-liviano (ej. `flashrank` o `bge-reranker-base` con ONNX) en `backend/src/rag/reranker.py`.
  - [ ] Recibir los top-15 candidatos del retriever híbrido y filtrar a los top-5 más relevantes para el LLM.
  - [ ] Medir y garantizar latencia del re-ranker <30ms en CPU estándar.
- [ ] **TODO-1.4 [Prop. 4 - RECOMENDADO] Enrutador semántico de intenciones pre-LLM (Query Router):**
  - [ ] Definir intenciones deterministas de respuesta fija en `backend/src/core/intent_router.py` (ej. ubicación de sedes, agendamiento de test).
  - [ ] Responder consultas exactas en <15ms sin invocar el LLM ni el pipeline de síntesis pesada.
- [ ] **TODO-1.5 [Prop. 5 - RECOMENDADO] Extracción y normalización de metadatos estructurados al indexar:**
  - [ ] Extraer metadatos de documentos (`campus`, `level`, `program_type`, `pricing_cop`) durante el parsing.
  - [ ] Habilitar filtros booleanos estructurados (`where={"campus": "chico"}`) en las llamadas a ChromaDB.
- [ ] **TODO-1.6 [Prop. 6 - RECOMENDADO] Contextual Compression y Sentence Window Retrieval:**
  - [ ] Implementar indexación a nivel de oración individual para matching semántico de alta granularidad.
  - [ ] Reconstituir ventana de contexto (oración anterior y posterior) al armar el contexto final inyectado al LLM.
- [ ] **TODO-1.7 [Prop. 7 - RECOMENDADO] Normalizador fonético y lemático para nombres propios de sedes y convenios:**
  - [ ] Crear normalizador en `backend/src/rag/bm25.py` con manejo de tildes y variantes para términos como "Chicó", "Laureles", "Comfama".
  - [ ] Garantizar matching de BM25 ante consultas con typos comunes de usuarios.
- [ ] **TODO-1.8 [Prop. 19 - CRÍTICO] Caché semántico multicapa en memoria (<5ms):**
  - [ ] Diseñar LRU Cache semántico en `backend/src/core/cache.py` con similitud de coseno >0.96.
  - [ ] Guardar respuestas pre-calculadas para preguntas frecuentes de admisiones.
- [ ] **TODO-1.9 [Prop. 21 - RECOMENDADO] Optimización de parámetros HNSW en ChromaDB:**
  - [ ] Configurar `M=16` y `efConstruction=64` en `backend/src/rag/vector_store.py`.
  - [ ] Verificar reducción del uso de memoria RAM de la base vectorial (~35%).
- [ ] **TODO-1.10 [Prop. 23 - RECOMENDADO] Serialización y persistencia en disco del índice BM25:**
  - [ ] Implementar guardado y carga binaria del vocabulario de BM25 (`bm25_index.pkl`) en `backend/data/`.
  - [ ] Agregar validación por hash SHA-256 de los documentos fuente para invalidar el archivo al haber cambios.
- [ ] **TODO-1.11 [Prop. 43 - RECOMENDADO] Validador sintáctico CI para documentos Markdown:**
  - [ ] Escribir script de test `backend/tests/test_document_integrity.py` que valide sintaxis, columnas y tablas de los 82 documentos.

---

## 🟡 FASE 2: Rendimiento Backend, Resiliencia y Persistencia (11 Tareas)
> **Objetivo:** Desplegar streaming SSE en tiempo real token a token, pooling persistente de conexiones, pipeline en cascada multi-filtro para desambiguación estricta de intenciones, base de datos SQLite transaccional y contenerización lista para producción.

- [ ] **TODO-2.1 [Prop. 11 - CRÍTICO] Streaming SSE token a token en `/api/v1/chat/stream`:**
  - [ ] Implementar generador asíncrono en `backend/src/api/routes.py` utilizando `StreamingResponse(media_type="text/event-stream")`.
  - [ ] Adaptar `advisor_common.py` para emitir chunks parciales de texto en tiempo real.
- [ ] **TODO-2.2 [Prop. 12 - CRÍTICO] Connection pooling HTTP persistente (`httpx.AsyncClient`):**
  - [ ] Refactorizar `OpenCodeAdvisorClient` para utilizar un cliente singleton `httpx.AsyncClient` con keep-alive.
  - [ ] Eliminar la recreación de sesiones TCP por cada mensaje recibido.
- [ ] **TODO-2.3 [Prop. 13 - RECOMENDADO] Circuit Breaker y Backoff Exponencial para proveedores LLM:**
  - [ ] Crear clase `CircuitBreaker` en `backend/src/core/resilience.py` (estados: Closed, Open, Half-Open).
  - [ ] Conmutar automáticamente entre OpenCode y AGY CLI si uno presenta fallos consecutivos o timeouts (>45s).
- [ ] **TODO-2.4 [Prop. 14 - RECOMENDADO] Middleware ASGI con Correlation ID (`X-Request-ID`):**
  - [ ] Agregar middleware en `backend/src/main.py` que genere o capture `X-Request-ID`.
  - [ ] Propagar el ID en cada log emitido y en el header de respuesta HTTP.
- [ ] **TODO-2.5 [Prop. 15 - RECOMENDADO] Migración de `escalations.json` a SQLite transaccional con WAL:**
  - [ ] Crear repositorio `backend/src/data/sqlite_tickets.py` con esquema de tabla `escalation_tickets`.
  - [ ] Habilitar modo `PRAGMA journal_mode=WAL;` para escrituras atómicas concurrentes libres de bloqueos.
  - [ ] Migrar tickets existentes de `escalations.json` a la base de datos `escalations.db`.
- [ ] **TODO-2.6 [Prop. 16 - RECOMENDADO] Validación de esquemas y serializadores nativos Pydantic V2:**
  - [ ] Sustituir conversiones manuales con `json.dumps()` por `model_dump_json()` de Pydantic V2 en todos los modelos API.
- [ ] **TODO-2.7 [Prop. 20 - CRÍTICO] Rutina de compresión y vacuum periódico de ChromaDB:**
  - [ ] Crear tarea programada en background que ejecute `VACUUM` sobre la base subyacente de ChromaDB para desfragmentar espacio en disco.
- [ ] **TODO-2.8 [Prop. 22 - RECOMENDADO] Gestor de snapshots fechados de la base vectorial:**
  - [ ] Implementar utilitario en `backend/src/rag/snapshot_manager.py` para respaldar `chroma_db/` previo a re-indexaciones.
  - [ ] Permitir rollback automático si un proceso de re-indexación es interrumpido.
- [ ] **TODO-2.9 [Prop. 45 - CRÍTICO] Configuración Docker Compose multi-stage:**
  - [ ] Crear `Dockerfile.backend` (Python 3.12 slim multi-stage) y `Dockerfile.frontend` (Node.js 20 alpine standalone).
  - [ ] Crear `docker-compose.yml` que orqueste backend (:8000) y frontend (:3000) en una red interna.
- [ ] **TODO-2.10 [Prop. 46 - CRÍTICO] Validación tipada centralizada con `pydantic-settings`:**
  - [ ] Migrar variables de entorno a una clase `AppSettings` con tipado estricto y valores por defecto en `backend/src/core/config.py`.
- [ ] **TODO-2.11 [CRÍTICO] Pipeline de Enrutamiento de Intenciones en Cascada y Erradicación de Cruces entre Pilares:**
  - [ ] **1. Clasificador de Intención Cerrado & Confidence Gate:**
    - [ ] Definir intents estrictos (`cursos`, `horarios`, `precios`, `sedes`, `becas_descuentos`) con palabras clave exclusivas y umbral de confianza mínimo.
    - [ ] Si la confianza es baja o ambigua, activar pregunta de clarificación o desambiguador Pydantic en lugar de permitir búsqueda global difusa en los 82 documentos.
  - [ ] **2. Hard Domain Mask Obligatorio (Bloqueo Físico en `hybrid_retriever.py`):**
    - [ ] Reemplazar penalizaciones suaves por un bloqueo booleano estricto (`PILLAR_STRICT_CLUSTERS`).
    - [ ] Si la intención es `cursos`, vetar al 100% chunks de sedes (`07_sedes`), horarios (`02_`) y precios (`03_`).
    - [ ] Si la intención es `precios`, vetar al 100% chunks de horarios y sedes.
    - [ ] Si la intención es `sedes`, vetar chunks de precios y cursos.
  - [ ] **3. Score de Compatibilidad Híbrido Consulta-Documento:**
    - [ ] Integrar fórmula compuesta: $\text{Score} = (\text{Dense} \times 0.4) + (\text{BM25} \times 0.3) + (\text{IntentMatch} \times 0.3)$.
    - [ ] Descartar automáticamente documentos con $\text{IntentMatch} == 0$.
  - [ ] **4. Context Validator Pre-LLM (`engine.py`):**
    - [ ] Auditar los chunks recuperados antes de pasarlos al LLM; rechazar y sustituir cualquier fragmento fuera del dominio solicitado.
  - [ ] **5. Output Verification & Prompt con Reglas Estrictas de Dominio (`advisor_common.py`):**
    - [ ] Inyectar regla imperativa en el prompt del asesor: *"La intención es exclusivamente {intent}; solo puedes responder información de {allowed_clusters}; nunca mezcles sedes, horarios ni precios si no fueron solicitados"*.
    - [ ] Validador posterior que detecta términos prohibidos según la intención (ej. si la intención es `cursos`, rechazar respuestas que comiencen con sedes físicas).
  - [ ] **6. Tests de Regresión Automáticos por Intención:**
    - [ ] Batería de pruebas en `backend/tests/test_hybrid_search.py` validando los 5 pilares:
      - *"Cuáles son los cursos disponibles"* $\to$ PASS: cursos/idiomas/MCER \| FAIL: sedes/direcciones.
      - *"Cuánto cuesta inglés B2"* $\to$ PASS: precios/COP/financiación \| FAIL: horarios/sedes.
      - *"Qué sedes tienen"* $\to$ PASS: Bogotá/Medellín/Cali \| FAIL: precios/cursos.

---

## 🔵 FASE 3: Frontend Moderno, UI Retro y Accesibilidad (10 Tareas)
> **Objetivo:** Eliminar prop-drilling con Zustand, decodificar SSE progresivo, acelerar el filtro CRT con WebGL/GPU (60 FPS) y garantizar accesibilidad WCAG AAA.

- [ ] **TODO-3.1 [Prop. 25 - CRÍTICO] Store global centralizado con Zustand:**
  - [ ] Instalar `zustand` en `frontend/`.
  - [ ] Crear stores modulares: `useChatStore` (mensajes, estado de envío), `useDesktopStore` (ventanas, z-index), `useSettingsStore` (CRT, accesibilidad).
  - [ ] Refactorizar componentes para eliminar prop-drilling en `ChatContainer.tsx` y `Desktop.tsx`.
- [ ] **TODO-3.2 [Prop. 26 - CRÍTICO] Consumo de streams SSE con decodificador progresivo UTF-8:**
  - [ ] Crear hook `useChatStream.ts` en el frontend utilizando `ReadableStreamDefaultReader` y `TextDecoder`.
  - [ ] Mostrar el texto entrante progresivamente con cursor parpadeante retro vintage.
- [ ] **TODO-3.3 [Prop. 27 - RECOMENDADO] Virtualización de mensajes del chat (`@tanstack/react-virtual`):**
  - [ ] Implementar lista virtualizada en el contenedor de mensajes para chats con más de 50 intervenciones.
  - [ ] Mantener el auto-scroll hacia el fondo cuando se generen nuevos tokens en streaming.
- [ ] **TODO-3.4 [Prop. 28 - RECOMENDADO] Persistencia de sesiones en `IndexedDB`:**
  - [ ] Implementar almacenamiento asíncrono con `idb-keyval` para historial de chat y preferencias del usuario.
- [ ] **TODO-3.5 [Prop. 29 - RECOMENDADO] Optimización de Server Components (RSC) vs Client Components:**
  - [ ] Separar la cáscara estática del escritorio retro en Server Components de Next.js 15.
  - [ ] Mantener la directiva `'use client'` únicamente en los nodos interactivos.
- [ ] **TODO-3.6 [Prop. 30 - RECOMENDADO] Code splitting dinámico con `next/dynamic`:**
  - [ ] Cargar perezosamente con `ssr: false` el modal de telemetría y el visor de tickets de escalamiento.
- [ ] **TODO-3.7 [Prop. 33 - CRÍTICO] Filtro óptico CRT acelerado por GPU / WebGL:**
  - [ ] Migrar el sombreado de líneas de escaneo y curvatura a clases CSS aceleradas (`transform: translateZ(0)`, `will-change`) o shader WebGL ligero en Canvas.
  - [ ] Verificar tasa estable de 60 FPS sin picos de consumo de CPU en laptops de bajos recursos.
- [ ] **TODO-3.8 [Prop. 34 - RECOMENDADO] Modo accesible "Bypass Retro" (WCAG 2.1 AAA):**
  - [ ] Añadir toggle en la barra de tareas que desactive el filtro CRT y las fuentes pixeladas.
  - [ ] Conmutar a tipografía legible del sistema (Inter / SF Pro) con contraste de color AAA.
- [ ] **TODO-3.9 [Prop. 35 - RECOMENDADO] Navegación por teclado y Focus Trap en ventanas retro:**
  - [ ] Implementar trampa de foco en la ventana del chat (`Tab` / `Shift+Tab`).
  - [ ] Soportar atajos rápidos (`Escape` para cerrar modales, `Alt+Enter` para enviar).
- [ ] **TODO-3.10 [Prop. 36 - RECOMENDADO] Panel de control vintage "Monitor Controls":**
  - [ ] Crear diálogo estilo monitor CRT con sliders para ajustar brillo, curvatura de tubo y grosor de scanlines.

---

## 🟣 FASE 4: Testing Automatizado, QA y Tooling DX (8 Tareas)
> **Objetivo:** Establecer evaluación continua de calidad RAG, simular concurrencia con Locust, tests ultrarrápidos con mocks deterministas y diagnóstico CLI.

- [ ] **TODO-4.1 [Prop. 39 - CRÍTICO] Pipeline de evaluación continua RAG (Ragas / Faithfulness):**
  - [ ] Crear script `scripts/evaluate_rag.py` que calcule métricas de Context Precision, Context Recall y Answer Faithfulness.
  - [ ] Definir dataset dorado de 30 preguntas/respuestas oficiales de admisiones.
- [ ] **TODO-4.2 [Prop. 40 - RECOMENDADO] Pruebas de mutación con `mutmut`:**
  - [ ] Ejecutar `mutmut` sobre los módulos de cálculo financiero (descuentos de contado del 10% y planes 40/30/30).
  - [ ] Corregir cualquier brecha en los tests unitarios donde una mutación sobreviva.
- [ ] **TODO-4.3 [Prop. 41 - RECOMENDADO] Pruebas de carga y concurrencia con Locust:**
  - [ ] Crear archivo `scripts/load_test.py` simulando navegación por menús y preguntas abiertas con 50 usuarios simultáneos.
  - [ ] Validar que el p95 de latencia se mantenga bajo los límites operativos.
- [ ] **TODO-4.4 [Prop. 42 - RECOMENDADO] Proveedor de pruebas `MockDualAdvisor`:**
  - [ ] Implementar clase mock de latencia determinista (<10ms) en la suite de pytest para que los 55 tests corran en <3 segundos.
- [ ] **TODO-4.5 [Prop. 44 - OPCIONAL] Snapshot testing visual con Playwright:**
  - [ ] Configurar Playwright en `frontend/` para capturar snapshots del escritorio retro OS '97 y prevenir regresiones visuales.
- [ ] **TODO-4.6 [Prop. 47 - RECOMENDADO] Hooks de pre-commit con Ruff y ESLint:**
  - [ ] Configurar `.pre-commit-config.yaml` con `ruff check` y `ruff format` para Python, y `prettier` para TypeScript.
- [ ] **TODO-4.7 [Prop. 48 - RECOMENDADO] Comando CLI de diagnóstico `python run.py doctor`:**
  - [ ] Implementar subcomando `doctor` en `run.py` que valide puertos (:8000, :3000, :4096), versiones de Python/Node y salud de ChromaDB.
- [ ] **TODO-4.8 [Prop. 49 - RECOMENDADO] Verificación de diagramas Mermaid en CI:**
  - [ ] Añadir paso de verificación de sintaxis para los bloques Mermaid de `DIAGRAMA.md` y `EXPLICACION_TECNICA.md`.

---

## ⚪ FASE 5: Horizontes Futuros y Despliegues Especializados (11 Tareas)
> **Objetivo:** Graph RAG para itinerarios de certificación, inferencia HyDE, audio procedural retro sintético y empaquetado nativo Tauri para recepciones de sedes.

- [ ] **TODO-5.1 [Prop. 8 - OPCIONAL] Generación Aumentada de Consultas (HyDE):**
  - [ ] Generar respuestas sintéticas de una línea para enriquecer el vector de búsqueda en preguntas extremadamente breves.
- [ ] **TODO-5.2 [Prop. 9 - OPCIONAL] Fallback transparente multi-embeddings:**
  - [ ] Crear conmutador automático si el modelo local `all-MiniLM-L6-v2` presenta errores en entornos sin soporte AVX.
- [ ] **TODO-5.3 [Prop. 10 - FUTURO] Graph RAG liviano para rutas de prerrequisitos:**
  - [ ] Modelar itinerarios de certificación internacional (A1 -> C1) como grafo acíclico dirigido (DAG).
- [ ] **TODO-5.4 [Prop. 17 - OPCIONAL] Exposición formal de métricas OpenMetrics / Prometheus:**
  - [ ] Implementar endpoint `/metrics/prometheus` con percentiles de latencia y tasas de acierto de caché.
- [ ] **TODO-5.5 [Prop. 18 - FUTURO] Worker de re-indexación asíncrono en background:**
  - [ ] Crear observador de archivos (File Watcher) que re-indexe documentos en segundo plano al guardarse cambios en `backend/data/documents/`.
- [ ] **TODO-5.6 [Prop. 24 - OPCIONAL] Exportador de tickets de escalamiento a CSV/XLSX:**
  - [ ] Agregar endpoint `/api/v1/escalations/export` con reporte tabular de aspirantes para el equipo comercial humano.
- [ ] **TODO-5.7 [Prop. 31 - OPCIONAL] Manejo de estado offline con alerta retro vintage:**
  - [ ] Detectar pérdida de conexión en el navegador y mostrar cuadro de diálogo retro ("Error de Comunicación de Red").
- [ ] **TODO-5.8 [Prop. 32 - FUTURO] Arquitectura pluggable de ventanas de escritorio (`DesktopAppWindow`):**
  - [ ] Diseñar interfaz genérica para permitir registrar nuevas aplicaciones en el escritorio OS '97 de forma desacoplada.
- [ ] **TODO-5.9 [Prop. 37 - OPCIONAL] Modo PDA vintage adaptativo para smartphones:**
  - [ ] Diseñar vista optimizada tipo Palm OS / PDA cuando el ancho de pantalla sea inferior a 450px.
- [ ] **TODO-5.10 [Prop. 38 - OPCIONAL] Feedback auditivo procedural con Web Audio API (<2KB):**
  - [ ] Sintetizar clics mecánicos y bleeps vintage al presionar botones o enviar mensajes (desactivado por defecto).
- [ ] **TODO-5.11 [Prop. 50 - FUTURO] Empaquetado nativo de escritorio con Tauri (Modo Kiosco):**
  - [ ] Configurar Tauri (Rust) para generar ejecutable nativo multiplataforma (<15MB) para pantallas táctiles de recepción en sedes físicas.
