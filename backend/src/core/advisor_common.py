import re
import asyncio
from typing import Dict, Any, Optional, List, AsyncGenerator


def format_context_chunks(context_chunks: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Formats retrieved document chunks into an organized multi-document string for LLM reasoning.
    """
    if not context_chunks:
        return "No se encontraron documentos específicos."

    formatted_chunks = []
    for i, c in enumerate(context_chunks[:5]):
        src = c.get("metadata", {}).get("source", f"Documento_{i+1}")
        sec = c.get("metadata", {}).get("section", "General")
        text_snippet = c.get("text", "").strip()
        formatted_chunks.append(f"--- Documento [{src}] - Sección: [{sec}] ---\n{text_snippet}")

    return "\n\n".join(formatted_chunks)


def build_advisor_reasoning_prompt(query: str, context_chunks: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Constructs the high-depth Admissions Advisor reasoning prompt.
    Both OpenCode and AGY use this exact prompt to ensure identical analytical and structural depth.
    """
    context_str = format_context_chunks(context_chunks)

    return (
        "Eres el Asesor Académico Senior de Admisiones en Nova Idiomas (Academia Colombiana de Idiomas).\n"
        "Tu objetivo es brindar respuestas exhaustivas, certeras, cálidas, empáticas y fundamentadas exclusivamente en la documentación oficial del negocio.\n\n"
        "DIRECTRICES DE RAZONAMIENTO, SÍNTESIS Y FORMATO:\n"
        "1. Analiza cuidadosamente todo el contexto oficial proporcionado y responde de manera completa a lo que el estudiante o interesado pregunta.\n"
        "2. Si el usuario solicita tablas, comparativas o resúmenes estructurados, genera tablas Markdown limpias y completas.\n"
        "3. Si la pregunta abarca precios, detalla los valores en pesos colombianos ($ COP), el 10% de descuento por pronto pago y la financiación directa a 3 cuotas sin interés (40%/30%/30%).\n"
        "4. Si la pregunta abarca horarios, incluye las franjas exactas (Madrugadores 6-8am, Diurnas, Nocturna After Work 6:30-8:30pm, Sabatinos y Dominicales) y modalidades (Virtual en vivo, Presencial, HyFlex 360°).\n"
        "5. Utiliza formato Markdown profesional con títulos claros (###), tablas cuando aporten valor o se soliciten, viñetas (•) y negritas.\n"
        "6. Mantén siempre un tono humano, cercano, motivador e institucionalmente riguroso en español.\n"
        "7. Cierra tu mensaje haciendo una pregunta de seguimiento orientada a su perfil o invitándolo a agendar su Placement Test 100% gratuito.\n\n"
        f"CONTEXTO OFICIAL VERIFICADO:\n{context_str}\n\n"
        f"CONSULTA DEL USUARIO:\n{query}"
    )


def generate_advisor_fallback(query: str, context_chunks: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    High-depth grounded fallback synthesis covering all 5 pillars when LLM engines are unreachable.
    Shared identically across OpenCode and AGY clients.
    """
    q_lower = query.lower()

    # 1. Precios / Tarifas / Cuotas / Financiación
    if any(w in q_lower for w in ("precio", "precios", "tarifa", "tarifas", "costo", "costos", "cuanto", "vale", "valen", "cuota", "cuotas", "financiacion", "financiar", "pago", "pagos")):
        return (
            "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
            "¡Hola! Con gusto te detallo nuestra estructura oficial de tarifas y planes de pago en pesos colombianos (COP):\n\n"
            "• **Curso Regular Bimestral (40 horas lectivas):** $650.000 COP por módulo.\n"
            "• **Curso Intensivo Mensual (40 horas aceleradas):** $720.000 COP por módulo.\n"
            "• **Curso Sabatino o Dominical (40 horas):** $650.000 COP por ciclo.\n"
            "• **Clases Privadas Personalizadas 1 a 1:** Paquete de 10 horas por $650.000 COP ($65.000 COP/hora) o paquete de 20 horas por $1.200.000 COP.\n\n"
            "**Planes de Pago y Facilidades:**\n"
            "• **Pago de Contado:** 10% de descuento directo sobre el valor total del módulo antes del inicio de clases.\n"
            "• **Financiación Directa a 3 Cuotas sin Interés:** Sin fiador ni centrales de riesgo (Cuota 1: 40% al matricularte, Cuota 2: 30% en semana 4, Cuota 3: 30% en semana 7).\n"
            "• **Medios de Pago Habilitados:** PSE, tarjetas débito y crédito (Visa/Mastercard/Amex), transferencias Bancolombia / Davivienda y botón digital Nequi/Daviplata.\n\n"
            "¿Qué programa o idioma te gustaría iniciar para verificar los cupos disponibles?"
        )

    # 2. Horarios / Franjas / Noche / Madrugadores / Modalidades
    if any(w in q_lower for w in ("horario", "horarios", "franja", "franjas", "noche", "nocturno", "nocturna", "manana", "tarde", "sabatino", "sabado", "domingo", "modalidad", "virtual", "presencial", "hyflex")):
        return (
            "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
            "¡Hola! Te presento nuestras franjas horarias y modalidades de estudio disponibles:\n\n"
            "• **Franja Madrugadores (Early Birds):** 6:00 a.m. a 8:00 a.m. (Lunes a Viernes) — Ideal antes de iniciar la jornada laboral.\n"
            "• **Franjas Diurnas:** 9:00 a 11:00 a.m. y 2:00 a 4:00 p.m. / 4:00 a 6:00 p.m. (Lunes a Viernes).\n"
            "• **Franja Nocturna (After Work):** 6:30 p.m. a 8:30 p.m. (Lunes a Viernes) — Nuestra franja más solicitada para profesionales y universitarios.\n"
            "• **Cursos de Fin de Semana:** Sábados de 8:00 a.m. a 1:00 p.m. o 2:00 p.m. a 7:00 p.m., y Domingos de 8:30 a.m. a 1:30 p.m.\n\n"
            "**Modalidades de Estudio:**\n"
            "• **100% Virtual Sincrónico:** Clases en vivo con docente interactivo y grabaciones de respaldo 24/7 en el Campus Virtual.\n"
            "• **Presencial:** Sedes físicas equipadas con salones inteligentes, aire acondicionado y cafetería.\n"
            "• **Aulas Híbridas HyFlex 360°:** Libertad de alternar entre asistir presencialmente o conectarte en vivo desde cualquier lugar.\n\n"
            "¿En qué franja horaria te resultaría más cómodo tomar tus clases?"
        )

    # 3. Cursos / Programas / Exámenes / Idiomas / Certificaciones
    if any(w in q_lower for w in ("curso", "cursos", "programa", "programas", "idioma", "idiomas", "ingles", "frances", "aleman", "italiano", "portugues", "mcer", "nivel", "niveles", "ielts", "toefl", "cambridge", "delf", "goethe")):
        return (
            "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
            "¡Hola! En Nova Idiomas impartimos 6 idiomas bajo los estándares internacionales del Marco Común Europeo de Referencia (MCER):\n\n"
            "• **Inglés General & Intensivo:** Niveles A1 (Principiante), A2 (Elemental), B1 (Intermedio), B2 (Independiente), C1 (Avanzado) y C2 (Maestría).\n"
            "• **Otros Idiomas:** Francés, Alemán, Italiano, Portugués brasileño y Español para extranjeros.\n"
            "• **Preparación Oficial para Exámenes:** Cursos especializados para IELTS, TOEFL iBT, Cambridge (B2 First / C1 Advanced), DELF / DALF y Goethe-Zertifikat.\n"
            "• **Metodología Flipped Classroom:** Enfoque 100% comunicativo y práctico con clubes de conversación semanales incluidos sin costo adicional.\n\n"
            "¿Cuál es el idioma que deseas dominar y cuál es tu meta (estudios, trabajo o migración)?"
        )

    # 4. Sedes / Direcciones / Ciudades / Ubicación
    if any(w in q_lower for w in ("sede", "sedes", "donde", "ubicacion", "direccion", "direcciones", "bogota", "medellin", "cali", "chico", "chapinero", "poblado", "laureles", "granada")):
        return (
            "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
            "¡Hola! Con gusto te comparto la ubicación de nuestras sedes principales en Colombia:\n\n"
            "• **Bogotá D.C.:**\n"
            "  - *Sede Chicó Norte:* Calle 93B # 13-45 (cerca del Parque de la 93).\n"
            "  - *Sede Chapinero Central:* Carrera 7 # 54-20 (zona universitaria).\n"
            "• **Medellín:**\n"
            "  - *Sede El Poblado:* Carrera 43A # 5A-113, Edificio One Plaza Business Center.\n"
            "  - *Sede Laureles:* Circular 4 # 73-28 (a 2 cuadras del Primer Parque de Laureles).\n"
            "• **Cali:**\n"
            "  - *Sede Barrio Granada:* Avenida 9N # 14N-35 (Zona Rosa de Granada).\n\n"
            "Todas nuestras sedes cuentan con salones climatizados, laboratorios multimedia y biblioteca. ¿Te gustaría agendar una visita presencial o presentar el examen de nivelación virtual?"
        )

    # 5. Becas / Descuentos / Convenios
    if any(w in q_lower for w in ("beca", "becas", "descuento", "descuentos", "convenio", "convenios", "subsidio", "subsidios", "caja", "compensacion", "comfama", "compensar", "colsubsidio")):
        return (
            "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
            "¡Hola! Te comparto la política oficial sobre ayudas económicas y beneficios vigentes:\n\n"
            "• **Política Oficial Institucional:** Nova Idiomas no cuenta con becas del 100% ni de cobertura total ni de manutención.\n"
            "• **Convenios con Cajas de Compensación:** 15% de descuento en la matrícula para afiliados a Compensar, Colsubsidio, Cafam y Comfama.\n"
            "• **Descuento Familiar:** 15% de descuento para el segundo miembro de un mismo núcleo familiar matriculado simultáneamente.\n"
            "• **Plan Referidos:** Bono de $100.000 COP aplicable al siguiente módulo por cada amigo o conocido que se matricule.\n"
            "• **Pronto Pago:** 10% de descuento directo pagando de contado el módulo completo.\n\n"
            "¿Estás afiliado a alguna caja de compensación para validar tu descuento corporativo?"
        )

    # 6. Fallback estructurado y deduplicado con Chunks de Contexto
    if context_chunks and len(context_chunks) > 0:
        content_bullets = []
        seen_texts = set()

        for c in context_chunks[:4]:
            c_text = c.get("text", "")
            lines = [l.strip() for l in c_text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("---")]
            for l in lines:
                clean = re.sub(r"^[\-*•\d.]+\s*", "", l).strip()
                clean_norm = clean.lower().replace(" ", "")
                if clean and len(clean) > 15 and clean_norm not in seen_texts:
                    seen_texts.add(clean_norm)
                    content_bullets.append(f"• {clean}")
                if len(content_bullets) >= 6:
                    break
            if len(content_bullets) >= 6:
                break

        if content_bullets:
            body = "\n".join(content_bullets)
            return (
                "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
                "¡Hola! Revisando nuestra documentación oficial institucional, te comparto la información correspondiente a tu consulta:\n\n"
                f"{body}\n\n"
                "¿Deseas que te agendemos tu **Examen de Clasificación (Placement Test) 100% Gratuito** o revisemos opciones de horario o matrícula?"
            )

    return (
        "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
        "¡Hola! Con gusto te oriento en todo lo que necesites sobre nuestros programas de idiomas (inglés, francés, alemán, italiano, portugués, español), tarifas oficiales en COP, modalidades virtual y presencial, o certificaciones internacionales (IELTS, DELF, Goethe).\n\n"
        "¿Podrías indicarme qué idioma deseas aprender o qué aspecto te gustaría consultar en detalle?"
    )


async def stream_advisor_tokens(
    text: str,
    chunk_delay: float = 0.015
):
    """
    Asynchronous token-by-token streamer for admissions advisor answers.
    Emits natural word and punctuation tokens with realistic cadence.
    """
    tokens = re.findall(r"\S+|\s+", text)
    for token in tokens:
        yield token
        if chunk_delay > 0:
            await asyncio.sleep(chunk_delay)
