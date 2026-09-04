# 🔄 Session Handoff — Becas=Descuentos + 50 Anti-Estancamiento

- **Fecha:** 2026-09-01 10:40 America/Bogota
- **Repo:** `https://github.com/nastex123/NovaVice_os97.git` (local `synapse-admissions-ai`, branch actual `a7c5a52` + Fase 2 Pixi/Semántica)
- **Estado actual al cerrar PC anterior:**
  - `27/27 pytest` PASSED (33s), `219kB` build Next.js (PIXI híbrido real 36 partículas)
  - `becas` gap: 0 synonyms, 0 leaves, 1 mención incidental `18_03`, 11 tickets escalados `0.23` (`becas disponibles` siempre `knowledge_gap`)
  - `horario` baseline 13 synonyms +6 leaves +10 docs (100%), `precios` 11 synonyms (90%), `cursos` 5/6 (60%), `modalidades` 0/2 (35%), `sedes` 7/3 (85%)
  - Fase 2 completada: semántica implementada, `n8n`/`hermes_skills` borrados, Pixi híbrido, radio placebo eliminado
  - `DIAGRAMA.md` + `run.py` Ctrl+C fix ya aplicados (10:15)

- **Decisiones clave para continuar:**
  - `becas = descuentos` — Nova **no** ofrece becas merit-based. Solo `10% contado (10_01)`, `15% cajas (12_01)`, `15% familiar (12_03)`, `bono $100k (09_03)`. Ver `ADR-008` a crear.
  - `asesor solo very very heavy` → threshold pilar `0.35` vs heavy `0.50`, 2 fases `¿Sí/No?` (D32), hard rule `D39` pilares nunca heavy.
  - Plan Mode → Build Mode: este handoff + `TODO_SPRINT_BECAS_DESCUENTOS.md` son únicos puntos de entrada.

- **Qué se va a hacer (resumen 50 + Fase 0):**
  - **Fase 0 Docs (10 archivos, hoy):** `12_04_becas_descuentos_aclaratoria.md` + `ADR-008` + actualizar `PRD`, `system-architecture`, `rag-deep-dive`, `opencode-integration`, `TECHNICAL_EXPLANATION`, `README`, `DIAGRAMA`, `CHANGELOG` + este handoff + TODO.
  - **Fase Código A→D→B→C→E (5-6 días):** A Normalización 1-10, D Heavy Only 31-40 (prioritario para dejar de escalar `becas`), B RAG 11-20, C Anti-Stuck 21-30, E Calidad 41-50. Ver TODO para `file:line`.

- **Cómo retomar en otra PC (3 comandos):**
  ```bash
  git pull  # o git fetch + checkout rama trabajo
  cat docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md  # ver 0/50 y Fase 0 0/11
  cat docs/08-operations/SESSION_HANDOFF_BECAS_DESCUENTOS.md  # este archivo
  ls backend/data/documents/12_04*  # verifica doc existe tras Fase 0
  ./venv/bin/pytest -q  # debe 27/27
  ```
  Si `TODO` Fase 0 incompleta → completar `F0.1-F0.11`, commit `docs: Fase 0 becas=descuentos`, push. Luego seguir `A→D→B→C→E` marcando `[x] HH:MM`.

- **Archivos clave para leer primero:**
  - `docs/08-operations/TODO_SPRINT_BECAS_DESCUENTOS.md` (checklist vivo)
  - `docs/09-decisions/ADR-008-becas-como-descuentos.md` (a crear, contexto becas)
  - `backend/src/core/navigation.py:163` (INTENT_SYNONYMS actuales 52)
  - `backend/src/rag/bm25.py:18` (STOP 62 + stemming)
  - `backend/src/rag/engine.py:220` (threshold 0.50 hoy → 0.35 pilar)
  - `backend/data/documents/` (82 docs, añadir `12_04`)

- **Bloqueo actual:**
  - Plan Mode activo al crear handoff — salir con `Build Mode` (o `/exit` en CLI) para escribir docs Fase 0.
  - Siguiente acción tras salir: crear `12_04_becas_descuentos_aclaratoria.md` y `ADR-008`.

- **Contacto/Notas:**
  - Todo en `docs/` por petición usuario (“en docs”).
  - No tocar seguridad/arquitectura más allá de thresholds documentados.
  - Pregunta pendiente: ¿ threshold `D39` hard rule vs `.env` configurable? Recomendado hard rule para otra PC (más simple).
