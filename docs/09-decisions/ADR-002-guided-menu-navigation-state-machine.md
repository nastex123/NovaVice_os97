# ADR-002: Máquina de Estados para Navegación Guiada Interactiva por Menús

- **ID:** ADR-002
- **Título:** Diseño de Máquina de Estados para Navegación Guiada Interactiva con Opciones Numéricas y Botones de Acción
- **Fecha:** 2026-08-30 (America/Bogota)
- **Estado:** Accepted
- **Autores:** AI Backend & Full Stack Engineering Team

---

## 1. Contexto
En un portal de admisiones universitarias, muchos postulantes no saben con exactitud qué preguntar inicialmente o desconocen la amplitud de la oferta académica, becas y servicios disponibles. Los chatbots conversacionales de texto libre puro a menudo generan fricción o respuestas genéricas cuando el usuario formula preguntas vagas (ej. "información", "ayuda").

---

## 2. Problema
¿Cómo guiar al postulante de forma interactiva y estructurada para que descubra la totalidad de los 87 documentos oficiales de Nova Tech University, manteniendo al mismo tiempo la capacidad de procesar consultas abiertas de lenguaje natural?

---

## 3. Opciones Consideradas
1. **Opción A (Texto Libre Exclusivo):** Forzar al usuario a formular preguntas completas en lenguaje natural sin ningún menú ni botones de orientación.
2. **Opción B (Árbol Rígido Hardcodeado):** Limitar el sistema exclusivamente a un IVR textual donde solo se acepten números y no se permita lenguaje natural.
3. **Opción C (Seleccionada - Arquitectura Híbrida Guiada):** Implementar una máquina de estados conversacional (`src/core/navigation.py`) con:
   - Menú principal de 9 opciones estructuradas.
   - 8 submenús temáticos (ej. `1.1` a `1.7` para sílabos, `5.1` a `5.5` para laboratorios).
   - Comandos de retorno global (`0`, `menu`).
   - Botones de acción rápida interactivos en la interfaz web.
   - Procesamiento transparente de lenguaje natural en cualquier nivel del árbol.

---

## 4. Decisión
Implementar la clase `GuidedNavigationEngine` en `src/core/navigation.py` conectada con la memoria del postulante (`src/core/memory.py`). La máquina de estados:
- Procesa dígitos directos (`1` a `9`).
- Mapea códigos de submenú (`1.1`, `5.1`) a consultas de alta precisión (`LEAF_QUERY_MAP`).
- Inyecta metadatos `action_buttons` en la respuesta JSON para que el frontend renderice botones clicables interactivos.
- Si el usuario introduce una consulta en lenguaje natural, la máquina delega la consulta directamente al motor RAG o al Asesor OpenCode sin romper el flujo.

---

## 5. Justificación
- **Reducción de Fricción:** El usuario puede postularse o revisar aranceles haciendo clics rápidos o digitando números del 1 al 9.
- **Descubrimiento del Corpus:** Expone los 7 clusters temáticos (laboratorios GPU H100, intercambios internacionales, becas, startups) desde el primer mensaje de bienvenida.
- **Flexibilidad Total:** Combina la certidumbre de los árboles de decisión con la potencia semántica de los LLMs.

---

## 6. Consecuencias

### Positivas:
- Menor tasa de rebote y mayor tasa de conversión de postulantes.
- Soporte en múltiples canales (web con botones y terminal/CLI con dígitos numéricos).
- Respuestas instantáneas y sin ambigüedad en opciones predefinidas.

### Negativas / Mitigaciones:
- Necesidad de sincronizar los textos de submenús cuando se agreguen nuevos documentos, mitigada mediante el catálogo centralizado `LEAF_QUERY_MAP`.
