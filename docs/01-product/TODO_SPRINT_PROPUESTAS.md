# Sprint de Prioridades CRÍTICO: Nova OS '97 (v2.7.0) — 30 Días

- **Documento:** TODOs accionables de las 7 ideas CRÍTICO del anteproyecto de 57 ideas
- **Versión:** 2.7.0
- **Fecha:** 2026-09-20 (America/Bogota)
- **Horizonte:** 30 días (propuesta de primer sprint de evolución)

---

## Tablero de Estado General

| TODO | Propuesta | Bloque | Área | Esfuerzo | Estado |
| :-- | :-- | :-: | :-: | :-: | :-: |
| TODO-PROP-102 | Pre-enrutador determinista de tarifas/convenios | 1 | Backend | S | Completada |
| TODO-PROP-105 | Citas JSON en tuplas Pydantic | 1 | Backend | S | Completada |
| TODO-PROP-149 | FPS adaptativo por inactividad | 5 | Frontend | S | Completada |
| TODO-PROP-178 | Kiosco watchdog + bloqueo HW | 9 | Tauri | M | Pendiente |
| TODO-PROP-183 | Cifrado en reposo de SQLite/JSON local | 9 | Backend | S | Completada |
| TODO-PROP-195 | PDF de cotización oficial local | 11 | Backend/Frontend | M | Completada |
| TODO-PROP-200 | Registro de causa raíz de abandono | 11 | Backend | S | Completada |

**Total: 7** | Completadas: 6 | Pendientes: 1

---

## 🟢 TODO-PROP-102 [Prop. 102 - CRÍTICO] Pre-enrutador determinista de tarifas y convenios

> **Objetivo:** Responder consultas de precios y convenios con reglas sintácticas deterministas (<15 ms) antes del LLM.

- [x] Ampliar `backend/src/core/query_router.py` con rutas de tarifas, financiación y convenios/descuentos (patrones sintácticos, respuestas canónicas del corpus).
- [x] Responder determinísticamente sin invocar al pipeline denso (equivalente a la derivación a `guided_navigation.py` para entidades de precio).
- [x] Agregar tests unitarios en `backend/tests/test_query_router.py` cubriendo precios, financiación, descuento y convenio por caja.
- **Aceptación:** respuestas deterministas sub-15 ms (rutas nuevas); gate `pytest` en CI (`rag-eval.yml`) verde; benchmark de 80 variantes sin regresión.

## 🟢 TODO-PROP-105 [Prop. 105 - CRÍTICO] Citas JSON en tuplas Pydantic

> **Objetivo:** Rastrear cada afirmación a su chunk fuente con puntaje NLI, emitido en el stream.

- [x] Definir esquema Pydantic `CitationTuple {chunk_id, score, snippet}` en `structured_output.py`.
- [x] Emitir tuplas citadas junto a cada párrafo del SSE.
- [x] Reusar `faithfulness.py` para el scoring de adhesión en tiempo real.
- **Aceptación:** toda aserción de precio/cronograma lleva cita verificable; tests de esquema.
- **Verificación:** run `rag-eval` `35535795484` verde (`82 passed, 1 skipped`) — `backend/tests/test_structured_output.py` (esquema, atribución, grupos por párrafo y stream e2e).

## 🟢 TODO-PROP-149 [Prop. 149 - CRÍTICO] FPS adaptativo por inactividad

> **Objetivo:** Reducir consumo de CPU/GPU del fondo Pixi cuando no hay interacción (hasta 5 fps).

- [x] En `PixiParticleBackground.tsx`, mapear `ticker.maxFPS` según inactividad (reset con pointer/pointerdown/keydown/touchstart): `ACTIVE_FPS=60` / `IDLE_FPS=5` con idle timeout de 3000 ms; listeners con cleanup en el unmount.
- [x] Restaurar FPS nominal al reanudar interacción; respetar `prefers-reduced-motion` (el Pixi ni se crea bajo `reduce`, early return existente).
- **Aceptación:** mínimo 80% de reducción de frames en reposo — se cumple: 60→5 fps = **91.7% menos frames** por ticker de partículas (y >90% en pantallas >60 Hz); al interaccionar vuelve a 60 fps sin reiniciar la escena.
- **Nota de verificación:** sin runtime npm en el equipo de trabajo; el cambio es aislado en el `PixiParticleBackground.tsx` (ticker + listeners + cleanup) y no lo cubre el gate `rag-eval` (backend). Verificar con `npm run build`/lint en un entorno local.

## 🟢 TODO-PROP-178 [Prop. 178 - CRÍTICO] Kiosco con watchdog y bloqueo de hardware

> **Objetivo:** Endurecer el modo kiosco Tauri: reinicio de ventana y bloqueo de HW cuando no hay uso.

- [ ] Watchdog (Rust) que detecte ventana congelada o no recuperable y la recree.
- [ ] Bloqueo de combinaciones del sistema (Alt+F4, Ctrl+W, desktop) y captura de teclado/USB.
- **Aceptación:** sesión ininterrumpida tras 24 h de prueba; log de reinicios.

## 🟢 TODO-PROP-183 [Prop. 183 - CRÍTICO] Cifrado en reposo de SQLite/JSON local (NovVault)

> **Objetivo:** Cifrar la persistencia local (escalations.db + journal JSON) protegiendo datos de visitantes; la DB ilegible sin clave.

- [x] Evaluar SQLCipher para `escalations.db` — **descartado** en runners CI sin `libsqlcipher-dev`; se eligió **NovVault** (Fernet + PBKDF2-HMAC-SHA256 210k iteraciones, clave de env `ESCALATIONS_DB_KEY` sin hardcodear).
- [x] `secure_store.py`: blob `NVVAULT\x00\x01` + salt(16) + token Fernet; escritura atómica y lectura con tolerancia a journals legacy en plano.
- [x] `SQLiteTicketRepository`: artefacto persistente `escalations.db.enc`; copia de trabajo `.work` transitoria (re-creada al abrir, re-cifrada y eliminada al sellar, incluidas `-wal`/`-shm`/`-journal`). Sin clave → modo plano original intacto.
- [x] `EscalationDispatcher`: journal JSON se persiste/lee cifrado cuando hay clave; `read_text_decrypted`/`atomic_write_encrypted`.
- [x] Documentar el modelo de amenaza y backup de clave en `docs/09-decisions/ADR-009-secure-at-rest-encryption-novvault.md`.
- [x] `scripts/decrypt_escalations.py` de recuperación + tests `backend/tests/test_secure_store.py`.
- **Aceptación:** DB ilegible sin clave; backups descifrables con procedimiento documentado; `pytest` y CI verdes.
- **Verificación:** run `rag-eval` `35536635688` verde (`92 passed, 1 skipped`) — `backend/tests/test_secure_store.py` (roundtrip bytes/archivo, clave incorrecta → `InvalidToken`, repo cifrado en reposo descifrable a SQLite válido, repo plano sin cambios, dispatcher JSON cifrado/plano, lectura de env).

## 🟢 TODO-PROP-195 [Prop. 195 - CRÍTICO] PDF de cotización oficial

> **Objetivo:** Generar cotización en PDF localmente (sin pasarela ni servicios externos).

- [x] Endpoint/render local que arma la cotización (programa, valor, descuentos, convenio): `backend/src/core/quote.py` (writer PDF 1.4 propio, sin dependencias nuevas) + `GET /api/v1/quote` (detalle JSON) + `GET /api/v1/quote/pdf` (descarga `application/pdf` con `Content-Disposition: attachment`). Reglas canónicas: Regular/Sabatino $650.000, Intensivo $720.000; contado −10%, caja/universidad/familiar −15%, bono $100.000 por referido; cuotas 40/30/30.
- [x] UI retro consumible desde el chat y desde la sección de matrícula: `QuotePdfCard.tsx` (preview en vivo + descarga) bajo respuestas del pilar precios en `ChatContainer.tsx`, y tile "Cotizar" en el dock del `Footer.tsx` con modal `COTIZACION_OFICIAL.EXE`. Sin cambios al engine (evita regresiones E48).
- **Aceptación:** PDF válido y fiel al formato institucional (banda navy + franja rosa, total, cuotas, notas, fuentes 03_/09_/10_/12_); prueba E2E de descarga en `backend/tests/test_quote_pdf.py` (header `%PDF-1.4`, `%%EOF`, content-type, tokens `$585.000`/`COTIZACION OFICIAL`, 422 en parámetros inválidos).
- **Verificación:** run `rag-eval` `35548867696` verde (`106 passed, 1 skipped`); frontend sin runtime npm en el equipo — revisar con `npm run build` en entorno local.

## 🟢 TODO-PROP-200 [Prop. 200 - CRÍTICO] Registro de causa raíz de abandono

> **Objetivo:** Identificar por qué las conversaciones quedan sin resolver (cluster + tickets).

- [x] Vincular clusters de preguntas sin conversión con los tickets de escalamiento (`escalations`): `backend/src/core/abandonment.py` agrupa cada ticket por pilar (reutilizando clasificación E48/`classify_pillar`), con cuota relativa, causa predominante (`escalation_reason`) y keywords top.
- [x] Reporte de causa raíz en `/metrics/prometheus` o endpoint dedicado: métrica `admissions_abandonment_total_by_cluster{cluster=...}` en `/metrics/prometheus`, `abandonment_by_cluster` en `/api/v1/metrics` y endpoint `/api/v1/escalations/abandonment` (histórico del journal + `live_cluster_abandonment`).
- [x] Telemetría en vivo: `record_escalation(query)` clasifica el cluster al escalar en `engine.py` (ambas ramas de escalamiento).
- [x] CLI para el panel: `scripts/escalation_abandonment_report.py` (extiende feedback_loop D40) y sugerencias de documentación ausente (visas/Australia, niños/edad, mascotas).
- [x] Tests `backend/tests/test_abandonment.py` (clasificación, agrupación, causa, journal plano/vault, métricas y endpoint).
- **Aceptación:** métrica de abandono por cluster/área disponible para el panel de admisiones; `pytest` y CI verdes.
- **Verificación:** run `rag-eval` `35537789393` verde (`98 passed, 1 skipped`) — `backend/tests/test_abandonment.py` (clasificación, agrupación por cluster, causa dominante, suggested docs, journal plano/vault, métricas y endpoint).

---

## Recomendaciones de ejecución

- Ejecutar las preguntas **7 CRÍTICO** en este orden: Backend (102, 105, 183, 200) → Frontend (149, 195) → Tauri (178).
- Reutilizar los módulos listados en `VALIDACION_57_IDEAS.md` para evitar duplicación con el backlog anterior (57/57 completado).
- Sincronizar `PRD.md`, `ROADMAP_50_PROPOSITAS.md` y `CHANGELOG.md` en cada entrega.