# Plan de Evolución: Nova OS '97 "Admissions Assistant" (v2.7.0) — 57 Ideas Priorizadas

- **Documento:** Anteproyecto priorizado de evolución de producto (backlog de 57 ideas)
- **Versión:** 2.7.0
- **Estado:** Planificado (candidato a backlog de sprint)
- **Fecha:** 2026-09-20 (America/Bogota)
- **Origen:** Derivado del documento "Arquitectura de Evolución", filtrado y validado contra el código actual (corpus 83 docs / 245 chunks; v2.7.0).
- **Alcance:** 7 bloques de interés — Conocimiento/RAG, Frontend Next.js, Arte Visual CRT, PixiJS/GSAP, DevOps/Kiosco Tauri, Multilingüe y Negocio.
- **Fuera de alcance (omitido):** Bloques de Backend, Audio, Accesibilidad y Testing, más toda idea que requiera fuentes externas (APIs de clima, pasarelas de pago, calendarios, ERP de cupos, políticas de visa).

---

## 1. Visión General

Este plan organiza **57 ideas de evolución** en 5 fases de entrega, sobre la base funcional ya implementada (57/57 propuestas técnicas previas completadas). Cada idea fue validada contra el código para reutilizar módulos existentes y evitar duplicación (ver `VALIDACION_57_IDEAS.md`).

```text
┌──────────────────────────── FASE 1: NÚCLEO DE CONOCIMIENTO Y NEGOCIO ────────────────────────────┐
│ 102 Router determinista tarifas │ 105 Citas Pydantic │ 149 FPS adaptativo │ 178 Kiosco watchdog  │
│ 183 SQLCipher │ 195 PDF cotización │ 200 Causa raíz abandono                                  │
├──────────────────────────────── FASE 2: EXPERIENCIA, VISUAL Y PERFORMANCE ──────────────────────┤
│ Chunking padre-hijo, memoria episódica, caché cluster, RSC selectiva, font subsetting, z-index, │
│ shaders CRT P31, viento Simplex, GSAP eases, partículas CTA, kiosco metrics, build multilingüe  │
├────────────────────────── FASE 3: CONSOLIDACIÓN Y MULTILINGÜE ───────────────────────────────────┤
│ NLI pre-stream, paleta circadiana, bloom COP, nivelación adaptativa, homologación exámenes,     │
│ inmersión ASCII, code-switching                                                                 │
├────────────────────────────── FASE 4: OPTIMIZACIÓN Y OPCIONALES ────────────────────────────────┤
│ Offscreen, Error Boundary, línea de retrazado, interferencia EM, cristal sucio                  │
├─────────────────────────────────── FASE 5: HORIZONTES FUTUROS ──────────────────────────────────┤
│ Estela puntero Win95, Syncthing P2P, diccionario false friends                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Resumen

| Bloque | Ideas | N | E | CRÍTICO | RECOMENDADO | OPCIONAL | FUTURO |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1. Conocimiento, RAG y Prompts | 9 | 2 | 7 | 2 | 7 | 0 | 0 |
| 3. Frontend Next.js | 10 | 8 | 2 | 0 | 8 | 2 | 0 |
| 4. Arte Visual, CRT y Shaders | 10 | 7 | 3 | 0 | 6 | 4 | 0 |
| 5. PixiJS y GSAP | 9 | 7 | 2 | 1 | 4 | 3 | 1 |
| 9. DevOps / Kiosco Tauri | 7 | 4 | 3 | 2 | 4 | 0 | 1 |
| 10. Multilingüe | 7 | 7 | 0 | 0 | 5 | 1 | 1 |
| 11. Negocio y conversión | 5 | 5 | 0 | 2 | 3 | 0 | 0 |
| **TOTAL** | **57** | **40** | **17** | **7** | **37** | **10** | **3** |

**Leyenda de estado:** **N** = idea nueva (no existe equivalente en el código); **E** = evolución de una capacidad ya implementada (reutiliza módulo existente).

---

## 2. Bloque 1 — Conocimiento, RAG y Prompts

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 101 | Caché de respuestas por cluster semántico (dedupe de consultas equivalentes) | N | Alto | M | 2 | RECOMENDADO |
| 102 | Pre-enrutador determinista de tarifas y convenios (reglas sintácticas de precios) | E | Alto | S | 1 | CRÍTICO |
| 103 | Chunking padre-hijo con metadata de AST Markdown | E | Alto | M | 2 | RECOMENDADO |
| 104 | Memoria episódica comprimida vectorialmente por sesión | E | Medio | M | 2 | RECOMENDADO |
| 105 | Citas JSON en tuplas Pydantic con verificación NLI | E | Alto | S | 1 | CRÍTICO |
| 106 | Expansión de consultas por glosario colombiano | E | Medio | S | 2 | RECOMENDADO |
| 108 | Tablas ASCII de consumo financiero | N | Medio | S | 1 | RECOMENDADO |
| 109 | Sub-prompt de contexto negativo / out-of-scope explícito | E | Medio | S | 1 | RECOMENDADO |
| 110 | Autoevaluación NLI previa a la liberación del stream | E | Alto | L | 3 | RECOMENDADO |

## 3. Bloque 3 — Frontend Next.js

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 121 | Hidratación selectiva RSC por componente | E | Alto | M | 2 | RECOMENDADO |
| 122 | Subsetting WOFF2 de fuentes retro | N | Medio | S | 1 | RECOMENDADO |
| 123 | Zustand en slices modulares con persistencia IndexedDB | E | Medio | S | 2 | RECOMENDADO |
| 124 | Cache de AST de remark-gfm en el render de mensajes | N | Medio | M | 2 | RECOMENDADO |
| 125 | Gestor de z-index (stack de ventanas) | N | Alto | M | 2 | RECOMENDADO |
| 126 | Decodificación offscreen con ImageBitmap | N | Bajo | M | 3 | OPCIONAL |
| 127 | Modo headless DOM low-end | N | Alto | S | 1 | RECOMENDADO |
| 128 | Prefetch por hover en menú arcade | N | Medio | S | 2 | RECOMENDADO |
| 129 | Error Boundary estilo Blue Screen | N | Bajo | S | 3 | OPCIONAL |
| 130 | Snapping de 8 px en redimensión de ventanas | N | Medio | S | 2 | RECOMENDADO |

## 4. Bloque 4 — Arte Visual, CRT y Shaders

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 131 | Fósforo P31 con persistencia temporal (trails) | E | Alto | M | 2 | RECOMENDADO |
| 132 | Calibrador de curvatura Trinitron en OSD | E | Medio | M | 3 | OPCIONAL |
| 133 | Línea de retrazado vertical | N | Bajo | S | 2 | OPCIONAL |
| 134 | Paleta circadiana Colombia (día/noche por hora local) | N | Medio | S | 3 | RECOMENDADO |
| 135 | Interferencia electromagnética en procesos pesados | N | Medio | S | 2 | RECOMENDADO |
| 136 | Bisel 3D por gradientes CSS | E | Bajo | S | 1 | RECOMENDADO |
| 137 | Sombras sub-pixel 1px monócromas | N | Bajo | S | 1 | RECOMENDADO |
| 138 | Bloom selectivo sobre cifras COP | N | Medio | M | 3 | RECOMENDADO |
| 139 | Micro-patrón de dithering 2x2 | N | Bajo | S | 2 | OPCIONAL |
| 140 | Capa de cristal sucio y reflejos | N | Bajo | S | 4 | OPCIONAL |

## 5. Bloque 5 — PixiJS y GSAP

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 142 | Viento por Simplex Noise computado en GPU | E | Medio | M | 2 | RECOMENDADO |
| 143 | Eases GSAP back/stepped en micro-interacciones | E | Medio | S | 1 | RECOMENDADO |
| 144 | Fauna reactiva al tipeo del usuario | N | Bajo | S | 3 | OPCIONAL |
| 145 | Paralaje por giroscopio en móviles | N | Medio | M | 3 | OPCIONAL |
| 146 | Desglose de tarifas secuenciado con GSAP stagger | N | Medio | S | 2 | RECOMENDADO |
| 147 | Glitch al minimizar ventanas | N | Bajo | S | 2 | OPCIONAL |
| 148 | Partículas magnéticas hacia CTA | N | Alto | M | 2 | RECOMENDADO |
| 149 | FPS adaptativo a inactividad (hasta 5 fps) | N | Medio | S | 1 | CRÍTICO |
| 150 | Estela de puntero estilo Win95 | N | Bajo | S | 4 | FUTURO |

## 6. Bloque 9 — DevOps / Kiosco Tauri

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 178 | Kiosco con watchdog y bloqueo de hardware | E | Alto | M | 2 | CRÍTICO |
| 179 | Actualizaciones Delta OTA en Tauri | E | Medio | M | 3 | RECOMENDADO |
| 180 | Sincronización P2P con Syncthing | N | Bajo | L | 4 | FUTURO |
| 181 | Métricas de hardware de kioscos (Prometheus) | E | Medio | S | 2 | RECOMENDADO |
| 182 | Build multi-arquitectura ARM64/x86 | N | Medio | M | 3 | RECOMENDADO |
| 183 | Cifrado SQLCipher de SQLite local | N | Alto | S | 1 | CRÍTICO |
| 184 | Reinicio higiénico por sensor de proximidad | N | Medio | M | 3 | RECOMENDADO |

## 7. Bloque 10 — Multilingüe

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 185 | Detección de idioma + embeddings multilingües | N | Alto | M | 2 | RECOMENDADO |
| 186 | Test de nivelación express adaptativo | N | Alto | L | 2 | RECOMENDADO |
| 187 | Matriz de homologación de exámenes internacionales | N | Medio | S | 1 | RECOMENDADO |
| 188 | Plan de inmersión personalizado ASCII | N | Medio | S | 2 | RECOMENDADO |
| 189 | Code-switching Spanglish | N | Medio | S | 2 | RECOMENDADO |
| 190 | Fichas de enfoques pedagógicos | N | Bajo | S | 3 | OPCIONAL |
| 192 | Diccionario de false friends | N | Bajo | S | 4 | FUTURO |

## 8. Bloque 11 — Negocio y conversión

| ID | Propuesta | Est | Impacto | Esfuerzo | Fase | Prioridad |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| 194 | Simulador de ROI educativo | N | Alto | M | 2 | RECOMENDADO |
| 195 | PDF de cotización oficial (generación local) | N | Alto | M | 1 | CRÍTICO |
| 196 | Funnels de admisión en telemetría | N | Alto | M | 2 | RECOMENDADO |
| 198 | Calculadora de subsidios familiares y de empresa | N | Medio | S | 2 | RECOMENDADO |
| 200 | Registro de causa raíz de abandono | N | Alto | S | 1 | CRÍTICO |

---

## 9. Próximos pasos

1. Priorizar y convertir los 7 CRÍTICO en TODOs accionables (`TODO_SPRINT_PROPUESTAS.md`).
2. Ejecutar cada idea respetando los módulos de reutilización listados en `VALIDACION_57_IDEAS.md`.
3. Sincronizar PRD, Roadmap y CHANGELOG en cada entrega.