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

## Fase A — Normalización & Multi-Intent (1-10) `navigation.py:163,330` `bm25.py:34`

> Objetivo: `horario` 13 sinónimos → replicar a 80 global.

- [ ] **A1** Unicode NFD `navigation.py:330` — `import unicodedata normalize('NFD')` antes de `strip.lower` → `ubicación→ubicacion` `financiación→financiacion`. Test: `ubicación` con tilde hit.
- [ ] **A2** Stemmer ES `bm25.py:34` `vector_store.py:34` — Ya `curso→curs`, verificar `descuento` etc. Test stem.
- [ ] **A3** DICCIONARIO 80 sinónimos global `navigation.py:163` — Añadir 6 `beca→12_04`, 15 `cursos` (`que cursos hay`, `programas`, `ingles`, `frances`, `alemán`, `niveles`, `MCER`), 8 `modalidades` (`virtual`, `presencial`, `hibrida`, `HyFlex`, `grabaciones`), completar `precios` (`financiacion`) y `sedes` (`sede`, `sucursal`, `dirección` con tilde). Ver `explore` del 2026-09-01 para 52 existentes.
- [ ] **A4** Regex tolerante `navigation.py:357` — `r"prec?io|costo|tarifa|cuota"`, `r"bec[as]|ayuda|subsidio"`, `r"modalidad|virtual|hyflex"`.
- [ ] **A5** Typos Levenshtein ≤2 — `horaroi→horario`, `presio→precio` antes de `INTENT_SYNONYMS`.
- [ ] **A6** Intent embedding fallback `vector_store.py:167` — Si `exact` falla, `cosine >0.82` vs centroid 4 leaves canónicos.
- [ ] **A7** Rewriting corta `engine.py:264` — `precio?` (≤4 tokens) → canónica.
- [ ] **A8** Split multi-intent `navigation.py:385` — `horario y precio` split `y/,` → 2 retrievals RRF.
- [ ] **A9** Sinónimos temporales — `en la mañana→2.2`, `cuanto vale→3.1`.
- [ ] **A10** Fecha relativa — `próximo inicio→13_02`.

**Verificación A:** `pytest tests/test_navigation_continuity.py -k becas` + `pytest -k horario` 27/27 + manual `becas disponibles` → `not escalated` (sim >0.35).

---

## Fase B — Recuperación Que Nunca Falla (11-20) `hybrid_retriever.py:62` `ingestion.py:32`

- [ ] **B11** Boost por intent `hybrid_retriever.py:62` — `coverage*1.4` para pilar detectado +0.15 si `source` cluster `03/09/10`, `01`, `08`, `16`, `12_04`.
- [ ] **B12** Fallback BM25 relajado — `b=0.6 candidate 30` si `sim<0.50`.
- [ ] **B13** Re-rank por cluster — Prioriza docs del pillar.
- [ ] **B14** Protección chunk tabla `ingestion.py:32` — `chunk 600/150` para tablas `03_precios`, `02_horarios`.
- [ ] **B15** STOP actualizado `bm25.py:18` — Confirmar `beca` no en STOP.
- [ ] **B16** Centroid por pillar (5) — Pre-compute centroid embedding `precios, cursos, modalidades, sedes, becas→descuentos` → `0.3 * cosine`.
- [ ] **B17** Expansión query — `beca→beca ayuda subsidio descuento`.
- [ ] **B18** Negación — `no virtual` filtra `2.5`.
- [ ] **B19** Spanglish — `schedule→horario` etc.
- [ ] **B20** Cache `0.88` pilar `cache.py:47` — `horario/precio/curso/sede` 0.88, `beca` 0.92.

**Verificación B:** `scripts/test_variants.py` 80 frases reportando `confidence` >0.35 para pilares.

---

## Fase C — Anti-Estancamiento (21-30) `engine.py:130,220` `memory.py:41`

- [ ] **C21** Nunca error duro `navigation.py:384` — `4 botones + Reformulas?`.
- [ ] **C22** Botón Reformular `ChatContainer.tsx:302` — `🔄 Reformular` reintenta `top_k=5 threshold 0.35`.
- [ ] **C23** Memoria fracaso 2x `memory.py:37` — `last_failed` cosine>0.85 → ofrecer menú no ESC.
- [ ] **C24** Clarificación `0.35-0.50` `engine.py:220` — `¿horarios o precios o becas?` 3 botones.
- [ ] **C25** Sugerencias cruzadas `navigation.py:217` — Tras `curso 1.1` → `1.2,3.1,4.1` etc.
- [ ] **C26** Reset suave `navigation.py:333` — `limpiar, reiniciar, volver`.
- [ ] **C27** Breadcrumb clickeable `page.tsx:74`.
- [ ] **C28** Tolerancia `1.1` regex.
- [ ] **C29** Re-engage 60s.
- [ ] **C30** Loop detection 3 mismos `source` → shuffle `RRF`.

**Verificación C:** Manual 3 queries seguidas `precio` no loop, `pytest test_navigation_continuity.py`.

---

## Fase D — Heavy Only (31-40) `config.py:22` `dispatcher.py:24`

- [ ] **D31** Threshold por intent `config.py:22` — `0.35` pilares vs `0.50` heavy (env `THRESHOLD_PILAR=0.35`).
- [ ] **D32** 2 fases `engine.py:220` — `Sim<0.35` → muestra mejor chunk `0.34` + `¿Sí/No asesor?` solo `Sí` → `create_ticket`.
- [ ] **D33** Lista negra very heavy `dispatcher.py:24` — Solo `visa, beca 100%, mascota, Australia...` nunca `horario/precio...`.
- [ ] **D34** Contador `metrics.py` `escalation_rate>0.25` auto-baja.
- [ ] **D35** Asesor silencioso `ChatContainer.tsx:304` — `9. Asesor` botón, no ESC auto.
- [ ] **D36** Contexto ticket — `history 3 + top3 chunks`.
- [ ] **D37** Costo tiempo — `⏱️ <2h ¿prefieres ver 2.3 ahora?`.
- [ ] **D38** Heavy detector — `tokens>15 && sim<0.25 && no intent` → heavy.
- [ ] **D39** Hard rule pilares nunca heavy `engine.py:220` — `if intent in pilares: never escalate`.
- [ ] **D40** Feedback loop `escalations.json` → weekly doc sugerido.

**Verificación D:** `pytest test_rag_pipeline.py -k escalation` → `becas disponibles` ya no `escalated`, `visa Australia` sí `escalated`.

---

## Fase E — Calidad (41-50) `prompt_templates.py:48`

- [ ] **E41** Template por pilar — `horario` tabla 6 filas etc.
- [ ] **E42** Memoria preferencia `memory.py:37` — `modalidad_preferida`.
- [ ] **E43** Resumen 20 tokens.
- [ ] **E44** Validación post-LLM regex `$`/`6:00`.
- [ ] **E45** Citas siempre aunque `cached`.
- [ ] **E46** Idioma ES forzado.
- [ ] **E47** Tono empático.
- [ ] **E48** Métrica por pilar `MetricsModal.tsx`.
- [ ] **E49** Test 80 variantes `test_navigation_continuity.py`.
- [ ] **E50** Playground `scripts/test_variants.py`.

**Verificación E:** `pytest 28/28` + `npm run build` 219kB + manual `E41` tablas.

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

