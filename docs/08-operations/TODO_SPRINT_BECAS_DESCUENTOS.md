# ✅ TODO Sprint — Sistema Respuestas Anti-Estancamiento (Becas=Descuentos) + Retomar en Otra PC

- **Fecha creación:** 2026-09-01 10:30 America/Bogota
- **Branch:** `a7c5a52` + `DIAGRAMA.md` + Fase 2 Pixi/Semántica (27/27 pytest, 219kB build)
- **Decisión clave:** `becas = descuentos` — Nova **no** ofrece becas merit-based. Ver `ADR-008` y doc `12_04_becas_descuentos_aclaratoria.md`.
- **Objetivo:** `horario` en 100 variantes + `precios/becas/cursos/modalidades/sedes` siempre aciertan, **asesor solo very very heavy** (2 fases, threshold pilar 0.35 vs heavy 0.50).
- **Cómo retomar en otra PC:** `git pull` → leer `docs/08-operations/SESSION_HANDOFF_BECAS_DESCUENTOS.md` → seguir este TODO Fase 0 → A→D→B→C→E.

> Marca `[ ]` → `[x] 2026-09-01 HH:MM` al completar. `pytest` y `build` tras cada Fase.

---

## Fase 0 — Documentación (HOY, 0 código, 2h, prioridad HIGH) — ✅ COMPLETADA 2026-09-01 10:55 America/Bogota

- [x] **F0.1** Crear `backend/data/documents/12_04_becas_descuentos_aclaratoria.md` — Doc RAG canónico 180 palabras: `No becas merit, sí descuentos 10% contado (10_01), 15% cajas (12_01), 15% familiar (12_03), bono $100k (09_03)` — **COMPLETADO**: 252 chunks re-indexados, `becas disponibles` ahora `12_04 sim 1.0` (antes 0.25) verificado `hybrid_retriever.retrieve`.
- [x] **F0.2** Actualizar `docs/01-product/PRD.md:32` — §3.4 tabla `Beca (no) vs Descuento (sí)` + link `12_04.md` + `US-07` — **COMPLETADO**.
- [x] **F0.3** Crear `docs/09-decisions/ADR-008-becas-como-descuentos.md` — Context 11 tickets `becas 0.23` + 1 mención `18_03`; Decision `becas=descuentos`; Consequence — **COMPLETADO** `docs/09-decisions/ADR-008*`.
- [x] **F0.4** Actualizar `docs/03-architecture/system-architecture.md:54` — `Threshold 0.50 → 0.35 pilar + 2 fases` + diagrama cache dual — **COMPLETADO**.
- [x] **F0.5** Actualizar `docs/04-engineering/rag-subsystem-deep-dive.md` — § BM25 NFD + 80 synonyms plan + centroid 5 pilares — **COMPLETADO**.
- [x] **F0.6** Actualizar `docs/05-ai/opencode-integration.md` — § heavy 2 fases `Sí/No` + detector — **COMPLETADO**.
- [x] **F0.7** Actualizar `TECHNICAL_EXPLANATION.md` + `EXPLICACION_TECNICA.md` — Demo `becas→descuentos` Q&A — **COMPLETADO** `TECHNICAL_EXPLANATION.md:26` `83 docs`.
- [x] **F0.8** Actualizar `README.md:42` + `README.es.md:42` — Árbol `83 docs` + `12_04` — **COMPLETADO**.
- [x] **F0.9** Actualizar `DIAGRAMA.md:10` — Subgrafo `CACHE 0.35 pilar` + `BECAS→DESCUENTOS` — **COMPLETADO**.
- [x] **F0.10** Actualizar `CHANGELOG.md:8` — Entrada `[2026-09-01 10:46]` lista F0.1-F0.9 — **COMPLETADO**.
- [x] **F0.11** Este TODO + `SESSION_HANDOFF_BECAS_DESCUENTOS.md` — Commit pendiente `docs: Fase 0` — **COMPLETADO**: ambos en `docs/08-operations/` + fix `hybrid_retriever.py:80` tie-break por sim (12_04 ahora top1 para becas).

**Verificación Fase 0:** ✅ `ls 12_04` existe, `grep -r becas docs/ | wc -l >=6` ok, `252 chunks`, `becas disponibles→12_04 sim1.0`, `27/27 pytest` OK, build `219kB`.

---

## Fase A — Normalización & Multi-Intent (1-10) `navigation.py:163,330` `bm25.py:34` — ✅ COMPLETADA 2026-09-01 11:20 America/Bogota (rama feature/becas-descuentos)

- [x] **A1** Unicode NFD `navigation.py:330` — `import unicodedata normalize('NFD')` + `_normalize()` → `ubicación→ubicacion` `financiación→financiacion` — **COMPLETADO**: `Horário` `UBICACIÓN` `FINANCIACIÓN` ahora hit `menu_navigation` verificado.
- [x] **A2** Stemmer ES `bm25.py:34` `vector_store.py:34` — Ya `curso→curs`, `sede→sed` — **COMPLETADO** verificado `vector_store.embed` 1807 dims.
- [x] **A3** DICCIONARIO 80 sinónimos global `navigation.py:163` — 52→**~85** entradas: +12 `beca`→`becas disponibles` (ADR-008), +18 `curso/cursos/programas/idiomas/niveles/mcer/a1/b1/ingles/frances/aleman...`, +18 `modalidad/virtual/presencial/hibrida/hyflex/grabaciones/online/en linea...`, +8 `precio` (`financiacion`, `valor`, `cuanto es`), +8 `sede` (`sede/sucursal/direccion/proximo inicio`) — **COMPLETADO** verificado `85/85` variantes `0 escalados`.
- [x] **A4** Regex tolerante `navigation.py:357` — Pilar sets expandidos: `1: curso/programas/idiomas/niveles/mcer`, `2: horario/modalidad/franja/jornadas/turnos`, `3: precio/costo/tarifa/financiacion/descuento/valor/pago/cuota`, `4: sede/sucursal/inscripcion/ubicacion/direccion/test` — **COMPLETADO**.
- [x] **A5** Typos Levenshtein ≤2 `navigation.py:213` — `_TYPO_MAP` 16 entradas + `_levenshtein` con whitelist `valid_tokens` → `horaroi→horario`, `presio→precio`, `veca→beca`, `orario→horario` — **COMPLETADO** verificado `horaroi/orario/presio` ahora `menu_navigation`.
- [x] **A6** Intent embedding fallback `navigation.py:238` — `_find_intent_by_embedding` dense `384` vs canonicals, threshold `0.82`, cache lazy — **COMPLETADO** (fallback activo, aunque RAG ya cubre 85/85 sin necesitarlo).
- [x] **A7** Rewriting corta `engine.py:264` — Short ≤4 tokens ya via INTENT exact + embedding; `precio?` → `cuanto cuesta` via `precio` intent — **COMPLETADO**.
- [x] **A8** Split multi-intent `navigation.py:385` — `y/and/,` detect → `return raw_input` para RAG hybrid fusión (2 intents) — **COMPLETADO** verificado `horario y precio` → `rag_direct sim 0.62` no escalado.
- [x] **A9** Sinónimos temporales — `en la mañana→2.2`, `cuanto vale→3.1`, `en la noche→2.3`, `fin de semana→2.4` — **COMPLETADO** en INTENT.
- [x] **A10** Fecha relativa — `proximo inicio/cuando empieza/cuando inicia` → `4.2` (13_02 matrícula) — **COMPLETADO**.

**Verificación A:** ✅ `85/85` variantes `0 escalados` (vs heavy `visa Australia` sí escala `0.33`), `27/27 pytest` OK, `27/27` continuidad OK. Hub `vector_store.embed_query` fix `384` vs `1807` aplicado.

---

## Fase B — Recuperación Que Nunca Falla (11-20) `hybrid_retriever.py:62` `ingestion.py:32` — ✅ COMPLETADA 2026-09-02 18:15 America/Bogota

- [x] **B11** Boost por intent `hybrid_retriever.py:62` — `coverage*1.4` para pilar detectado +0.15 si `source` cluster `03/09/10`, `01`, `08`, `16`, `12_04` — **COMPLETADO**: Implementado en `_score_candidates` con boost de cobertura y bonificación de cluster.
- [x] **B12** Fallback BM25 relajado — `b=0.6 candidate 30` si `sim<0.50` — **COMPLETADO**: Activado en `retrieve()` re-evaluando candidatos si el top similarity es menor a 0.50.
- [x] **B13** Re-rank por cluster — Prioriza docs del pillar — **COMPLETADO**: Bonificación suave de +0.015 RRF para chunks del cluster detectado.
- [x] **B14** Protección chunk tabla `ingestion.py:32` — `chunk 600/150` para tablas `03_precios`, `02_horarios` — **COMPLETADO**: Segmentación elástica 600/150 y preservación de líneas de tabla Markdown sin cortes.
- [x] **B15** STOP actualizado `bm25.py:18` — Confirmar `beca` no en STOP — **COMPLETADO**: Lista `DOMAIN_PROTECTED_WORDS` sustraída explícitamente en `PureBM25.__init__`.
- [x] **B16** Centroid por pillar (5) — Pre-compute centroid embedding `precios, cursos, modalidades, sedes, becas→descuentos` → `0.3 * cosine` — **COMPLETADO**: Centroides calculados en `_get_pillar_centroids()` y mezclados $0.7 \cdot \text{sim} + 0.3 \cdot \text{centroid}$.
- [x] **B17** Expansión query — `beca→beca ayuda subsidio descuento` — **COMPLETADO**: `_expand_query()` mapeando intenciones clave de admisiones.
- [x] **B18** Negación — `no virtual` filtra `2.5` — **COMPLETADO**: `_detect_negations()` penalizando modalidades excluidas (virtual / presencial).
- [x] **B19** Spanglish — `schedule→horario` etc. — **COMPLETADO**: `_normalize_spanglish()` con 16 patrones léxicos bilingües.
- [x] **B20** Cache `0.88` pilar `cache.py:47` / `engine.py:228` — `horario/precio/curso/sede` 0.88, `beca` 0.92, 0.95 general — **COMPLETADO**: Umbral adaptativo en `engine.py:230`.

**Verificación B:** ✅ `scripts/test_variants.py` ejecutado: **80/80 variantes aprobadas (100.0%)**, 0 escalamientos indeseados, latencia promedio 48.8ms. Pytest suite: **32/32 tests PASSED**.

---

## Fase C — Anti-Estancamiento (21-30) `engine.py:130,220` `memory.py:41` — ✅ COMPLETADA (2026-09-02 19:14 America/Bogota)

- [x] **C21** Nunca error duro `navigation.py:652` — Retorno suave con 4 botones y prompt conversacional sin pantallas de error duro.
- [x] **C21b** Anti-Respuestas Vacías & Síntesis Multi-Chunk `engine.py:33` `ingestion.py:35` — **COMPLETADO 2026-09-02 19:05 America/Bogota**: Supresión de chunks título huérfanos sin contenido en `ingestion.py` (fusión de encabezados aislados con la subsección siguiente) y síntesis multi-chunk enriquecida en `engine.py` que extrae viñetas y franjas sustantivas de los `top_k` fragmentos, impidiendo que el bot devuelva fichas vacías con solo el título y 'fuente oficial'.
- [x] **C22** Botón Reformular `ChatContainer.tsx:335` — Botón interactivo retro `🔄 Reformular consulta` visible en clarificaciones o baja confianza (<0.55).
- [x] **C23** Memoria fracaso 2x `memory.py:45` `engine.py:351` — `is_failure_loop()` detecta 2 fallos consecutivos y ofrece menú interactivo de opciones guiadas en lugar de escalamiento intempestivo.
- [x] **C24** Clarificación `0.35-0.50` `engine.py:380` — Si la confianza cae en rango ambiguo, ofrece 3 botones de desambiguación (`Cursos`, `Horarios`, `Precios`).
- [x] **C25** Sugerencias cruzadas `engine.py:403` — Sugerencias contextuales automáticas basadas en el documento dominante (`01_` -> horarios/precios, `02_` -> cursos/sedes, `03_` -> cuotas/test).
- [x] **C26** Reset suave `navigation.py:556` — `limpiar, reiniciar, volver, reset, empezar de nuevo, cancelar, borrar, salir`.
- [x] **C27** Breadcrumb clickeable `Header.tsx:72` — Miga de pan interactiva en la cabecera retro para volver al menú con un solo clic.
- [x] **C28** Tolerancia `1.1` regex `navigation.py:593` — Regex `^\s*([1-4])\s*[.,\-\s]\s*([1-6])\s*$` tolerante a puntos, comas, espacios y guiones.
- [x] **C29** Re-engage 60s `page.tsx:73` — Temporizador de 60s de inactividad que sugiere temas clave al aspirante sin bloquear el flujo.
- [x] **C30** Loop detection 3 mismos `source` `memory.py:65` `engine.py:400` — Detección de fuentes repetidas durante 3 turnos seguidos con nota proactiva de desvío.

**Verificación C:** ✅ Pytest `test_navigation_continuity.py` y suite completa: **35/35 tests PASSED** en 3.83s. Benchmark: **80/80 variantes aprobadas (100.0%)**, latencia promedio 38.0ms, 0 fallidos. Build de producción Next.js 15: **Compilación exitosa (0 errores)**.

---

## Fase D — Heavy Only & Restantes (31-40) `config.py:22` `dispatcher.py:24` — ✅ COMPLETADA (10/10 ítems)

- [x] **D31** Threshold por intent `config.py:22` — `0.35` pilares vs `0.50` heavy (env `THRESHOLD_PILAR=0.35`) — **COMPLETADO** (commit 240b5c9).
- [x] **D32** 2 fases `engine.py:220` — `Sim<0.35` → muestra mejor chunk `0.34` + `¿Sí/No asesor?` solo `Sí` → `create_ticket` — **COMPLETADO** (commit 240b5c9).
- [x] **D33** Lista negra very heavy `dispatcher.py:24` — Solo `visa, beca 100%, mascota, Australia...` nunca `horario/precio...` — **COMPLETADO** (commit 240b5c9).
- [x] **D34** Contador `metrics.py` `escalation_rate>0.25` auto-baja — **COMPLETADO** (commit 240b5c9).
- [x] **D35** Asesor silencioso `ChatContainer.tsx:348` — Botón `👤 9. Consultar con un Asesor Académico` con modo asesor sin forzar escalación automática inmediata.
- [x] **D36** Contexto ticket extendido `dispatcher.py:30` `engine.py:201` — Inclusión de `history 3 + top3 candidate chunks` en tickets de `escalations.json`.
- [x] **D37** Costo tiempo en tickets `engine.py:440` — `⏱️ Tiempo estimado de respuesta humana: <2 horas hábiles. ¿Prefieres consultar horarios o tarifas de inmediato?` con botones directos.
- [x] **D38** Heavy detector — `tokens>15 && sim<0.25 && no intent` → heavy — **COMPLETADO** (commit 240b5c9).
- [x] **D39** Hard rule pilares nunca heavy `engine.py:220` — `if intent in pilares: never escalate` — **COMPLETADO** (commit 240b5c9).
- [x] **D40** Feedback loop semanal `scripts/escalation_feedback_loop.py` & `dispatcher.py:65` — Análisis de consultas unhandled en `escalations.json`, clusters temáticos y sugerencia de nuevos documentos de conocimiento.

**Verificación D:** ✅ `53/53 tests PASSED` en Pytest; benchmark `80/80 (100.0%) PASSED` en `test_variants.py` con 31.6ms latencia; feedback loop validado con 126 tickets; Next.js 15 compilación limpia en 5.0s.

---

## Fase E — Calidad & Pulido Final (41-50) `prompt_templates.py:48` — ✅ COMPLETADA (10/10 ítems)

- [x] **E41** Template por pilar `prompt_templates.py:25` — Directivas dinámicas por pilar: Horarios (tabla/franjas con horas exactas), Precios ($ COP, contado 10%, cuotas 40/30/30) y Cursos (MCER).
- [x] **E41b** Enrutador Semántico Vectorial Universal & Clasificación Dual de Intenciones (`intent_router.py`, `navigation.py:642`, `hybrid_retriever.py:195`) — **COMPLETADO 2026-09-02 19:35 America/Bogota**: Creación de `SemanticIntentRouter` con jerarquía de 2 niveles (5 Macro-Pilares y 18 Micro-Intenciones vectorizadas densamente), normalización de anglicismos, warm-up en memoria (<0.5ms), boosting micro-intent (+0.12) y fusión multi-cluster RRF (+0.015). Verificado con 18/18 tests dedicados y 80/80 en benchmark.
- [x] **E42** Memoria preferencia `memory.py:40` `engine.py:168` — Detección y persistencia de `modalidad_preferida`, `ciudad_interes` e `idioma_interes`.
- [x] **E43** Resumen contextual conciso `memory.py:75` `engine.py:489` — `get_conversation_summary()` inyectado dinámicamente en el prompt del LLM.
- [x] **E44** Validación post-LLM regex `$` y `6:00` `engine.py:500` — Aseguramiento de formato monetario ($) en precios y patrones de hora en horarios.
- [x] **E44b** Sanitización de Jargon Técnico & Erradicación de Endpoints en Respuestas (`engine.py:450`, `12_04_becas_descuentos_aclaratoria.md:31`) — **COMPLETADO 2026-09-02 19:18 America/Bogota**: Eliminación de fugas de endpoints REST (como `POST /api/v1/tools/quote`) en el corpus documental y blindaje con filtro regex en la síntesis RAG para garantizar un lenguaje 100% conversacional, natural y amigable para el aspirante.
- [x] **E45** Citas oficiales consistentes siempre incluso en `cached` `engine.py:270` — Garantía de fuente oficial visible y `source_documents` no vacío en respuestas cacheadas.
- [x] **E46** Idioma ES forzado `prompt_templates.py:11` — Regla estricta institucional que prohíbe respuestas en inglés aún con preguntas en Spanglish.
- [x] **E47** Tono empático e institucional `prompt_templates.py:10` — Tono cálido, motivador y estructurado de la marca Nova Idiomas.
- [x] **E48** Métrica por pilar en frontend `MetricsModal.tsx:135` & `metrics.py:25` — Telemetría de distribución de consultas por pilar con barras de porcentaje visuales.
- [x] **E49** Test 80 variantes en pytest `test_navigation_continuity.py:174` — Cobertura representativa de los 5 pilares con 0 escalamientos indeseados.
- [x] **E50** Playground interactivo `scripts/test_variants.py` — Soporte para `--filter`, `--query` individual y benchmark completo con salida UTF-8.

**Verificación E:** ✅ `54/54 tests PASSED` en Pytest en 4.95s; Benchmark `80/80 (100.0%) PASSED` en 27.0ms; Playground interactivo funcional; Compilación Next.js 15 limpia en 4.9s (220kB).

---

## Checklist Retomar en Otra PC

```bash
git pull # trae Fase 0
cat docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md # ver 0/50
cat docs/08-operations/SESSION_HANDOFF_BECAS_DESCUENTOS.md # contexto
ls backend/data/documents/12_04* # doc existe?
./venv/bin/pytest -q # 27/27
# Si Fase 0 incompleta: completar F0.1-F0.11, commit, push
# Luego A→D→B→C→E en orden, marcando [x] y fecha
```

Progreso global: `0/50` → `50/50` | Siguiente acción: Fase 0 Docs.

