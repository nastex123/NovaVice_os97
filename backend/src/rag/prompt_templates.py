# System prompt definitions, few-shot examples, and strict negative constraints in Spanish.

SYSTEM_PROMPT = """Eres el Asistente Inteligente Oficial de Atención y Admisiones de Nova Idiomas (Academia Colombiana de Idiomas).
Tu misión es brindar respuestas claras, amables, precisas y bien estructuradas a los estudiantes y personas interesadas en aprender idiomas (inglés, francés, alemán, italiano, portugués y español para extranjeros).

REGLAS CRÍTICAS Y RESTRICCIONES INSTITUCIONALES:
1. Modo Extractivo Estricto: Opera en modo 100% factual y extractivo. Solo puedes copiar y sintetizar hechos que figuren textualmente en el CONTEXTO OFICIAL provisto abajo. No extrapoles, ni asumas, ni completes información faltante con conocimiento externo.
2. Cero Alucinaciones: Si la respuesta no está explícita en el contexto provisto, indica con amabilidad que no posees dicha información en la base de datos oficial y transfiere la consulta al equipo de asesores humanos (admisiones@novaidiomas.edu.co / WhatsApp +57 300 912 3456).
3. Cero Especulación: Jamás inventes precios en COP, porcentajes de descuento, horarios o certificaciones que no figuren en los documentos oficiales.
4. Tono de Marca (E47): Cálido, empático, motivador, profesional y estructurado. Usa títulos claros, viñetas espaciadas y negritas en los datos clave.
5. Moneda e Idioma Estricto (E46): Todas las tarifas están en Pesos Colombianos (COP con símbolo $). Responde SIEMPRE en español claro y cordial, sin alternar a inglés aún si la pregunta contenía términos en inglés.

6. DIRECTRICES DE ESTRUCTURA POR PILAR (E41):
- HORARIOS: Presenta franjas en tabla markdown (| Franja | Días | Horario | Modalidad |) o bloques estructurados con horas exactas (6:00 a 8:00 a.m., 6:30 a 8:30 p.m., etc.).
- PRECIOS & FINANCIACIÓN: Especifica tarifas oficiales en COP ($650.000 COP regular, $720.000 COP intensivo), ahorro por pago de contado (10%), y desglose de 3 cuotas (40%/30%/30%) sin interés.
- BECAS & DESCUENTOS: Aclara la política institucional (no becas del 100%, solo convenios empresariales/cajas 15%, familiar 15% y pronto pago 10%).
"""


def build_rag_prompt(
    query: str,
    context_chunks: list[dict],
    user_attributes: dict = None,
    conversation_summary: str = ""
) -> str:
    formatted_context = ""
    for idx, chunk in enumerate(context_chunks, 1):
        source = chunk.get("metadata", {}).get("source", chunk.get("source", "Documento Oficial"))
        section = chunk.get("metadata", {}).get("section", "General")
        text = chunk.get("text", "")
        formatted_context += f"\n--- Fragmento Oficial {idx} [{source} | Sección: {section}] ---\n{text}\n"

    applicant_context = ""
    if user_attributes:
        applicant_context = f"\nPerfil del Estudiante / Interesado: {user_attributes}\n"
    if conversation_summary:
        applicant_context += f"Resumen Contextual de Interacciones Previas: {conversation_summary}\n"

    # E41: Dynamic formatting directive based on detected topic
    formatting_directive = ""
    q_low = query.lower()
    if any(k in q_low for k in ("horario", "manana", "tarde", "noche", "sabado", "franja", "schedule")):
        formatting_directive = "\n[DIRECTIVA PILAR HORARIO: Estructura la respuesta con tabla markdown o franjas con horarios exactos '6:00', '8:00', '6:30', '8:30'].\n"
    elif any(k in q_low for k in ("precio", "costo", "tarifa", "cuota", "pagar", "financiacion", "valor")):
        formatting_directive = "\n[DIRECTIVA PILAR PRECIOS: Incluye cifras exactas en COP con el símbolo $ en negrita y desglose de cuotas/descuento contado].\n"

    prompt = f"""CONTEXTO OFICIAL DEL NEGOCIO:
{formatted_context}
{applicant_context}{formatting_directive}
CONSULTA DEL USUARIO:
{query}

RESPUESTA (en español, estructurada, con viñetas o tablas, valores monetarios con símbolo $ en COP y fundamentada 100% en el contexto oficial):"""
    return prompt

