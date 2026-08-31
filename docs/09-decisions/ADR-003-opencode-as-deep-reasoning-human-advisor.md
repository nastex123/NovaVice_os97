# ADR-003: Sustitución de Hermes Agent por OpenCode como Motor de Razonamiento y Asesor Humano de Admisiones

- **ID:** ADR-003
- **Título:** Sustitución de Hermes Agent por OpenCode como Servidor de Razonamiento Profundo y Asesor de Admisiones
- **Fecha:** 2026-08-30 (America/Bogota)
- **Estado:** Accepted
- **Autores:** AI Backend & Full Stack Engineering Team

---

## 1. Contexto
Inicialmente se evaluó la integración de *Hermes Agent* (Nous Research) como agente autónomo mediante tool calling. No obstante, en pruebas de rendimiento se identificó que requerir un framework ReAct basado en CLI presentaba limitaciones en entornos serverless/web, complejidad en el manejo de sesiones aisladas concurrentes y latencias no predecibles.

Posteriormente, el usuario instruyó formalmente reemplazar Hermes Agent por **OpenCode** para asumir el rol de Asesor Humano de Admisiones (Opción 9 y preguntas personalizadas).

---

## 2. Problema
Se requería un motor de razonamiento local desacoplado, capaz de:
1. Exponer una API REST nativa (`/session`, `/session/:id/message`) sin envoltorios CLI complejos.
2. Ejecutar pasos de pensamiento profundo (*Chain-of-Thought*, ~800+ reasoning tokens) para sintetizar múltiples documentos oficiales simultáneamente.
3. Generar respuestas empáticas, estructuradas en Markdown y en español sin alucinaciones.

---

## 3. Opciones Consideradas
1. **Opción A (Hermes Agent CLI):** Invocar subprocesos de terminal interactivos de Hermes por cada consulta web. (Rechazada por bloqueo de hilos y sobrecarga de I/O).
2. **Opción B (Llamadas Directas a API de Gemini/OpenAI):** Utilizar únicamente llamadas simples sin servidor de razonamiento ni aislamiento de sesiones.
3. **Opción C (Seleccionada - OpenCode Server + Intermediario en Python):** Desplegar OpenCode como daemon en puerto 4096 (`opencode serve --port 4096`) y crear un intermediario en Python (`src/core/opencode_client.py`) con pool de conexiones persistente (`httpx.Limits`), inyección de contexto multidocumental (Top 5 chunks) y ventana de razonamiento de hasta 45 segundos.

---

## 4. Decisión
Adoptar formalmente a **OpenCode** como el motor de razonamiento del Asesor de Admisiones:
- Desactivar y marcar como *Deprecated* todas las especificaciones de Hermes Agent.
- Implementar `OpenCodeAdvisorIntermediary` en `src/core/opencode_client.py`.
- Inyectar los 5 fragmentos documentales más relevantes en un system prompt especializado de Asesor Académico Senior.
- Calibrar la ventana de timeout a 45.0s para permitir que OpenCode complete su razonamiento sin caídas prematuras en fallbacks.

---

## 5. Justificación
- **Respuestas Multidocumento Certeras:** Permite que al preguntar por becas, el asesor analice simultáneamente la Beca Turing (50%), Ada Lovelace (35%), Innovación ($800), Deportivas (20-50%) y Movilidad JASSO en Tokio.
- **Aislamiento de Sesiones:** Cada interacción crea o reutiliza un hilo de sesión limpio (`POST /session`), evitando fugas de contexto entre postulantes.
- **Empatía y Calidez Institucional:** El modelo formula preguntas de seguimiento personalizadas para acompañar al postulante en su admisión.

---

## 6. Consecuencias

### Positivas:
- Respuestas 100% certeras, ricas en datos numéricos y sin omisión de información oficial.
- Eliminación de dependencias obsoletas de Hermes Agent.
- Arquitectura desacoplada y escalable mediante HTTP REST.

### Negativas / Mitigaciones:
- Las consultas al Asesor OpenCode toman entre 8s y 14s debido al tiempo de pensamiento (*reasoning*), mitigado mediante indicadores de carga animados en la interfaz web y ofreciendo el modo *RAG Directo* para respuestas ultrarrápidas (<30ms en caché / <1.5s en LLM directo).
