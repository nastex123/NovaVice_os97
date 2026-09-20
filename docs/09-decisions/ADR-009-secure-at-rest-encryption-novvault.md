# ADR-009: Cifrado en Reposo de la Persistencia Local (Escalations)

- **ID:** ADR-009
- **Título:** Cifrado en Reposo (At-Rest Encryption) de `escalations.db` y journal JSON con NovVault (Fernet + PBKDF2)
- **Fecha:** 2026-09-20 (America/Bogota)
- **Estado:** Accepted
- **Autores:** AI Backend & Full Stack Engineering Team
- **Relacionado:** PROP-183 (CRÍTICO), TODO_SPRINT_PROPUESTAS, PRD FR-11

---

## 1. Contexto
`EscalationDispatcher` y `SQLiteTicketRepository` persisten datos de visitantes (consultas, historial de conversación, snippets de `top_chunks`, correos de admisiones) en:

- `backend/data/escalations.db` (SQLite con WAL), y
- `backend/data/escalations.json` (journal de respaldo).

`escalations.json` además **duplica el PII** en texto plano. En un quiosco de admisiones (propuesta PROP-178) o en portátiles de asesores, ese disco es físicamente accesible o extraíble, por lo que el texto plano en reposo es una exposición de datos de visitantes.

El corpus de documentos institucionales (ChromaDB en `data/chroma_db/`) ya está clasificado como público/institucional; el foco de cifrado es la persistencia de **datos de visitantes** en escalations.

---

## 2. Problema
1. Los tickets de escalamiento contienen PII (nombres implícitos, historial, segmentos de consultas) y quedan ilegibles **solo** por protección del SO.
2. La tarea PROP-183 exige: *"DB ilegible sin clave; backups descifrables con procedimiento documentado; clave derivada del entorno sin hardcodear."*
3. Los runners CI de este repositorio (ubuntu-latest, Python 3.12) **no tienen instalado `libsqlcipher-dev`** y no se puede garantizar disponibilidad de *wheels* nativos de SQLCipher para cp312 en ese entorno; el repositorio se verifica exclusivamente por CI.

---

## 3. Opciones Consideradas
1. **Opción A — SQLCipher real (`sqlcipher3`/`sqlcipher3-binary`):** Cifrado de página SQLite transaparente con `PRAGMA key`.
   - *Ventaja:* es el estándar de facto para SQLite cifrado; la DB permanece siendo SQLite.
   - *Desventaja:* requiere `libsqlcipher` en runtime; los wheels para `cp312` en runners de acciones no están garantizados y no es verificable en este equipo (sin runtime local). Riesgo alto de CI roja.
2. **Opción B (Seleccionada) — Vault de archivo completo con Fernet + PBKDF2-HMAC-SHA256 (`src/core/secure_store.py`, NovVault):**
   - Se cifra el **blob completo** de la DB (`escalations.db.enc`) y/o el journal JSON con AES-128-CBC + HMAC-SHA256 (Fernet) con clave derivada por PBKDF2 (210 000 iteraciones) desde la variable `ESCALATIONS_DB_KEY`.
   - La copia de trabajo en texto plano es **transitoria**: se materializa desde el vault al abrir y se re-cifra + elimina al sellar cada operación (incluidos los blobs WAL/SHM).
   - *Ventaja:* dependencia pura con wheels universales (`cryptography`) → verificable en CI; clave derivada del entorno, sin hardcodear; acredita el objetivo ("DB ilegible sin clave; backups descifrables con procedimiento documentado") con un script de recuperación.
   - *Desventaja:* no es cifrado a nivel de página; el archivo de trabajo temporal existe en claro durante la ventana transitoria de cada operación (ver mitigaciones).
3. **Opción C — Sin cifrado (estado actual):** Documentar el riesgo y posponer. (Rechazada: PII de visitantes en reposo.)

---

## 4. Decisión
Implementar **NovVault** (Opción B):

1. `backend/src/core/secure_store.py`:
   - `get_vault_password()` — lee `ESCALATIONS_DB_KEY` del entorno (nunca hardcodeada).
   - `encrypt_bytes/decrypt_bytes` — blob `NVVAULT\x00\x01` + salt(16) + token Fernet.
   - `encrypt_file/decrypt_file` — atómico (tmp + `os.replace`) para `escalations.db.enc`.
   - `atomic_write_encrypted/read_text_decrypted` — journal JSON cifrado con tolerancia a journals legacy en plano (migración).
2. `backend/src/data/sqlite_tickets.py`:
   - Con clave en reposo: el artefacto persistente es `escalations.db.enc`; la DB de trabajo (`escalations.db` + WAL/SHM) es transitoria y se elimina al sellar.
   - Sin clave (desarrollo/CI): comportamiento plano original intacto.
3. `backend/src/core/dispatcher.py`: el journal JSON se escribe/lee cifrado cuando hay clave; `generar_feedback` descifra transitoriamente en memoria.
4. `scripts/decrypt_escalations.py`: recuperación de respaldos cifrados a archivo en claro (procedimiento documentado).
5. Dependencia: `cryptography>=42.0.0` en `backend/requirements.txt`.

---

## 5. Justificación
- **Cumple la aceptación de PROP-183:** artefacto en reposo ilegible sin clave (Fernet con clave derivada del entorno), respaldo recuperable con procedimiento y script, y clave nunca hardcodeada.
- **Verificable en CI:** `cryptography` entrega wheels para cp312/manylinux; el gate `pytest` queda verde en `rag-eval.yml`.
- **Bajo acoplamiento:** el modo plano (sin `ESCALATIONS_DB_KEY`) no altera los tests existentes ni el flujo de desarrollo local.

---

## 6. Consecuencias

### Positivas:
- PII de visitantes cifrado en reposo en quiosco y portátiles.
- Recuperación de respaldos auditada con script dedicado.
- Migración transparente: un journal JSON legacy en plano se sigue leyendo y al siguiente write queda cifrado.

### Negativas / Mitigaciones:
- La copia de trabajo en claro existe durante la operación (ventana transitoria). **Mitigación:** se elimina con WAL/SHM tras cada sellado; documentar que el recurso de disco debe estar fuera de backups o bajo FDE (FileVault/BitLocker).
- Escribir archivos sin `ESCALATIONS_DB_KEY` sigue siendo plano: **degradación explícita de desarrollo** — la operación debe definir la variable en producción (aumentar verificación en CI para el modo cifrado via `test_secure_store.py`).
- SQLCipher queda como **futura opción** si se habilita `libsqlcipher` en el runner; la interfaz `_get_connection` está aislada para permitir el cambio de backend de cifrado sin tocar `sqlite_tickets.py` ni el dispatcher.

---

## 7. Procedimiento de Respaldo y Recuperación

### Respaldo
1. Copiar `backend/data/escalations.db.enc` (y, si existe, `escalations.json` cifrado) a un medio aislado; el backup NO necesita la clave para respaldarse, SOLO para descifrarse.
2. Nunca respaldar `escalations.db` en claro ni los blobs `-wal`/`-shm` (son transitorios).

### Recuperación
```bash
export ESCALATIONS_DB_KEY="<clave maestra de producción>"
python scripts/decrypt_escalations.py backend/data/escalations.db.enc --out backup_escalations.db
# El respaldo descifrado es un SQLite estándar:
sqlite3 backup_escalations.db "SELECT count(*) FROM escalation_tickets;"
```

### Rotación
1. Con el servicio detenido, descifrar el vault vigente a un archivo temporal.
2. Re-cifrar con `scripts/encrypt_escalations.py` (o `secure_store.encrypt_file`) usando la nueva clave.
3. Actualizar `ESCALATIONS_DB_KEY`, reiniciar y eliminar el temporal en claro.

---

## 8. Modelo de Amenaza
- **Amenaza mitigada:** robo/lectura de disco, extracción de medio, espectro del quiosco.
- **No cubre:** claves en memoria durante operación, captura de pantalla, claves de terceros con acceso a `ESCALATIONS_DB_KEY`, ni texto plano transitorio mientras se opera la DB.
- **Clave:** 32 bytes derivados por PBKDF2-HMAC-SHA256 (210 000 iteraciones) desde `ESCALATIONS_DB_KEY`; si la variable se omite, NO hay cifrado (modo desarrollo) y se debe advertir en logs de producción.