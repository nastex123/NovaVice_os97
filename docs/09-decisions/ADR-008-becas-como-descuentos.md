# ADR-008 — Becas como Descuentos (No Merit-Based)

- **ID:** ADR-008
- **Fecha:** 2026-09-01 (America/Bogota)
- **Estado:** `Accepted`
- **Área:** Producto / RAG Knowledge
- **Relacionado:** `12_04_becas_descuentos_aclaratoria.md`, `TODO_SPRINT_BECAS_DESCUENTOS.md`, `PRD.md:US-07`

---

## Contexto

Auditoría 2026-09-01 detectó gap crítico: `becas` tiene **0 synonyms en `navigation.py:163`**, **0 leaves**, **1 mención incidental** en `18_03_talleres_redaccion_y_ensayos.md` (Chevening externa) vs `horario` 13 synonyms +6 leaves +10 docs. Resultado: 11 tickets `escalations.json` con `becas` sim `0.23-0.49` siempre `knowledge_gap` escalado, mientras `precios` 11 synonyms casi 0 escalamientos. `guardrails.py:20` solo bloquea `beca 100%` como injection, no como consulta legítima `becas disponibles`.

Nova Idiomas Colombia no opera programa de becas merit/deportivas; el modelo comercial son **descuentos**: `10% contado (10_01)`, `15% cajas (12_01)`, `15% familiar (12_03)`, `bono $100k (09_03)`.

## Problema

- RAG alucinaría si inventa becas sin doc canónico (violación `SYSTEM_PROMPT` regla 1).
- Sin doc, `becas disponibles` → `MaxSim 0.25` < `threshold 0.50` → ticket humano innecesario que podría responder con descuentos.
- Usuario esperaba “becas” como sinónimo coloquial de “ayuda financiera”.

## Opciones Consideradas

| Opción | Descripción | Pros | Contras |
| :--- | :--- | :--- | :--- |
| **A** | Crear 3 docs becas merit (Turing 50% etc.) | Cubre beca real | Requiere negocio/presupuesto, alucinar sin aprobación |
| **B (Elegida)** | `becas = descuentos` — 1 doc `12_04` aclaratoria + 6 synonyms `beca/becas/ayudas/subsidio/scholarship/becas disponibles` → `12_04` | 0 alucinación, 0 escalamiento, reutiliza descuentos existentes | Si futuro hay becas merit, necesita ADR-009 |
| **C** | Mantener escalamiento | Simple | Churn alto, 11 tickets/mes por tema frecuente |

## Decisión

**Opción B.** Crear `backend/data/documents/12_04_becas_descuentos_aclaratoria.md` canónico que indica `No becas merit, sí descuentos 10%/15%/bono` con citas `10_01,12_01,12_03,09_03`. Añadir `INTENT_SYNONYMS` 6 entradas `beca` → query canónica `¿Qué becas y ayudas financieras ofrecen y requisitos?` resuelta por `12_04`. Threshold pilar `0.35` (Fase D31) aplica a `beca→descuento` como a `horario/precio/curso/modalidad/sede`. Lista negra very heavy solo `beca 100%` (injection) mantiene bloqueo `guardrails.py:20`.

## Justificación

- **Grounding 100%:** Respuesta `No becas, sí descuentos` citando `12_04` cumple `SYSTEM_PROMPT` sin inventar.
- **Anti-estancamiento:** `becas disponibles` ya no es `0.25` heavy sino `0.85` hit a `12_04` (STOP + centroid pilar).
- **Negocio:** Alinea producto con realidad financiera de academia de idiomas (no universidad con becas).

## Consecuencias

- **Positiva:** `becas` deja 0 escalamientos (vs 11/mes), `pytest` `test_cache_semantic` con `becas disponibles` → `not escalated`.
- **Negativa:** Si futuro hay programa Turing/Ada Lovelace, requiere crear docs `becas_*.md` y revertir 6 synonyms a leaves 3.6.
- **Riesgo mitigado:** Escalamiento heavy solo si `beca 100%` injection o `tokens>15 && sim<0.25` (D38), no por `becas`.

## Validación

- `grep -r "becas" backend/data/documents/12_04` → hit
- `pytest backend/tests/test_navigation_continuity.py -k becas` → `not escalated` tras Fase A3/D31
- `scripts/test_variants.py` incluye 10 `becas` variantes reporte `confidence >0.35`
