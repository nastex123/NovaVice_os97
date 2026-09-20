# Matriz de Validación: 57 Ideas de Evolución (v2.7.0)

- **Documento:** Verificación de viabilidad de cada idea del anteproyecto contra el código actual
- **Versión:** 2.7.0
- **Fecha:** 2026-09-20 (America/Bogota)
- **Método:** Revisión de módulos existentes (backend FastAPI, frontend Next.js 15, Tauri) mediante inspección de código.

**Leyenda:**
- **N** = idea nueva (no existe equivalente en el código).
- **E** = evolución que reutiliza una capacidad ya implementada (indicada en "Reutiliza").
- La idea **PROP-101** del documento de origen (reranker FlashRank) fue **descartada por duplicada**: `backend/src/rag/reranker.py` ya usa `FlashRank`/ONNX (TODO-1.3). Fue reemplazada por una idea nueva (caché por cluster semántico) para conservar el total de 57.

---

## Bloque 1 — Conocimiento, RAG y Prompts

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 101 | Caché de respuestas por cluster semántico | N | `cache.py` (LRU), embeddings | La caché semántica actual invalida por hash de doc; agrega dedupe a nivel de consulta equivalente (cluster). |
| 102 | Pre-enrutador determinista de tarifas/convenios | E | `query_router.py`, `guided_navigation.py` | Router determinista ya responde <15 ms; se amplía con reglas sintácticas de precios e intenciones de convenios. |
| 103 | Chunking padre-hijo | E | `ingestion.py` (`_extract_blocks` AST) | Chunker AST ya preserva tablas atómicas (TODO-1.2); parent-child agrega retención de contexto de sección. |
| 104 | Memoria episódica comprimida | E | `memory.py`, `vector_store.py` | Perfil episódico de sesión ya existe (extracción de preferencias); agrega compresión vectorial por sesión. |
| 105 | Citas JSON en tuplas Pydantic | E | `structured_output.py`, `faithfulness.py` | Serialización Pydantic y verificación NLI ya existen; agrega esquema de citas {(chunk, score)} en el stream. |
| 106 | Expansión por glosario colombiano | E | `bm25.py` (normalizador fonético/lemas) | Diccionario de lemas ya cubre sedes y convenios; amplía sinónimos coloquiales. |
| 108 | Tablas ASCII de financiación | N | Pipeline stream (síntesis) | Formato de salida nuevo; sin dependencias externas. |
| 109 | Contexto negativo / out-of-scope | E | `intent_router.py`, `engine.py` dispatcher | Clasificador heavy/light ya separa intenciones; agrega sub-prompt explícito de rechazo con límites de dominio. |
| 110 | Autoevaluación NLI pre-stream | E | `faithfulness.py` | NLI post-generación existe; evaluar si el margen de latencia permite gate pre-liberación sin degradar SSE. |

## Bloque 3 — Frontend Next.js

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 121 | Hidratación selectiva RSC | E | Frontera RSC ya aislada (client wrapper) | Agregar `next/dynamic`/`lazy` por componente no crítico. |
| 122 | Subsetting WOFF2 | N | Fuentes retro actuales | Optimización de pesos de fuente; nuevo. |
| 123 | Zustand slices modulares | E | `useSettingsStore.ts`, `useChatStore.ts` (idb-keyval) | Persistencia IndexedDB ya implementada (P-3.4); modulariza en slices. |
| 124 | Cache de AST de remark-gfm | N | `react-markdown` + memoizado de mensajes | Cache cuya clave es el hash del markdown; nuevo. |
| 125 | Gestor de z-index (stack) | N | `DesktopAppWindow.tsx` | Componente de ventana existe; apilador de profundidad es nuevo. |
| 126 | Decodificación offscreen | N | — | `ImageBitmap` / `createImageBitmap`; nuevo. |
| 127 | Modo headless DOM low-end | N | `motion.ts` (base reduced-motion) | `prefers-reduced-motion` ya respeta en `PixiParticleBackground.tsx`; flag crudo de low-end es nuevo. |
| 128 | Prefetch por hover | N | Menú arcade existente | Nuevo. |
| 129 | Error Boundary Blue Screen | N | — | Nuevo. |
| 130 | Snapping 8 px | N | Redimensión de ventanas | Nuevo. |

## Bloque 4 — Arte Visual, CRT y Shaders

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 131 | Fósforo P31 persistente | E | Filtro CRT GPU + slider de fósforo | Shader de threshold ya existe; agrega persistencia temporal acumulativa. |
| 132 | Calibrador curvatura Trinitron | E | OSD (MonitorControlsModal), sliders de curvatura | Slider ya expone curvatura; mejora calibración por hardware. |
| 133 | Línea de retrazado | N | Pipeline CRT | Shader nuevo. |
| 134 | Paleta circadiana | N | Tema CSS actual | Nuevo. |
| 135 | Interferencia EM | N | Pipeline CRT | Shader nuevo, detonado por carga de proceso. |
| 136 | Bisel 3D gradientes | E | `globals.css` (bordes biselados) | Evolución estilística menor. |
| 137 | Sombras sub-pixel 1px | N | — | Nuevo. |
| 138 | Bloom selectivo COP | N | Pipeline CRT | Nuevo. |
| 139 | Dithering 2x2 | N | Texturas retro existentes | Nuevo. |
| 140 | Cristal sucio / reflejos | N | — | Nuevo. |

## Bloque 5 — PixiJS y GSAP

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 142 | Viento Simplex Noise GPU | E | `PixiParticleBackground.tsx` (sway senoidal) | Reemplaza sway con noise por vértice (shader); mismo componente contenedor. |
| 143 | Eases GSAP back/stepped | E | GSAP (`useGsapReveal`, `useGsapHoverGroup`) | Configuración de eases; sin dependencias nuevas. |
| 144 | Fauna reactiva al tipeo | N | — | Nuevo. |
| 145 | Giroscopio móvil | N | — | `DeviceOrientationEvent`; nuevo. |
| 146 | Stagger de tarifas GSAP | N | — | Nuevo. |
| 147 | Glitch al minimizar | N | — | Nuevo. |
| 148 | Partículas magnéticas a CTA | N | Pixi partículas | Fuerza de atracción hacia el CTA; nuevo. |
| 149 | FPS adaptativo | N | Pixi ticker | `maxFPS` dinámico según inactividad; nuevo. |
| 150 | Estela puntero Win95 | N | — | Nuevo (FUTURO). |

## Bloque 9 — DevOps / Kiosco Tauri

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 178 | Kiosco watchdog + bloqueo HW | E | `src-tauri` (tauri.conf.json, TODO-5.11) | Shell Tauri existe; watchdog de proceso y bloqueo de teclas/USB son nuevos. |
| 179 | Delta OTA Tauri | E | Updater nativo de Tauri | Updater existe; instala paquetes diferenciales. |
| 180 | Syncthing P2P | N | — | Nuevo (FUTURO). |
| 181 | Métricas hardware kiosco | E | `metrics.py` (`/metrics/prometheus`) | Exportador Prometheus existe; agrega sensores de HW del dispositivo. |
| 182 | Build ARM64/x86 | N | — | Workflow CI nuevo. |
| 183 | SQLCipher | N | SQLite (`escalations.db`, ChromaDB) | Capa de cifrado local; nuevo. |
| 184 | Sensor de proximidad | N | — | Reanudación/limpieza de kiosco; nuevo. |

## Bloque 10 — Multilingüe

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 185 | Detección de idioma + embeddings multilingües | N | Pipeline de embeddings | Benchmark actual es solo español (80 variantes); nuevo. |
| 186 | Test de nivelación adaptativo | N | — | Nuevo. |
| 187 | Matriz de homologación de exámenes | N | — | Sheet de datos nuevo. |
| 188 | Plan de inmersión ASCII | N | — | Nuevo. |
| 189 | Code-switching Spanglish | N | Glosario (BM25) | Nuevo. |
| 190 | Fichas de pedagogías | N | — | Nuevo. |
| 192 | Diccionario false friends | N | — | Nuevo (FUTURO). |

## Bloque 11 — Negocio y conversión

| ID | Propuesta | Est | Reutiliza | Nota |
| :-- | :-- | :-: | :-- | :-- |
| 194 | Simulador de ROI educativo | N | — | Cálculo nuevo en página/sección de matrícula. |
| 195 | PDF de cotización | N | — | Generación local (librería PDF cliente o server) sin pasarela externa. |
| 196 | Funnels de admisión | E | `metrics.py` (eventos de telemetría) | Eventos de conversión ya trazables; agrega embudos. |
| 198 | Calculadora de subsidios | N | — | Basada en reglas internas de convenios; nuevo. |
| 200 | Causa raíz de abandono | E | `escalations`, telemetría | Vincula clusters de preguntas sin resolución con tickets; nuevo análisis. |

---

## Resumen de validación

| Veredicto | Cantidad |
| :-- | :--: |
| **N** — Nueva, viable local-first | 40 |
| **E** — Evolución de capacidad existente | 17 |
| **Y** — Ya implementada (duplicada, descartada c/ reemplazo) | 1 (PROP-101 original → sustituida) |
| **X** — Fuente externa (descartadas) | 7 (PROP-107, 141, 191, 193, 197, 199) |
| **TOTAL seleccionado** | **57** |