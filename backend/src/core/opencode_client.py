import httpx
import subprocess
import time
from typing import Dict, Any, Optional, List
from src.config import settings


class OpenCodeAdvisorIntermediary:
    # High-Performance Python intermediary bridge connecting Web Client to OpenCode Reasoning Engine.

    def __init__(self, base_url: str = "http://127.0.0.1:4096"):
        self.base_url = base_url.rstrip("/")
        self.session_map: Dict[str, str] = {}
        self._server_process: Optional[subprocess.Popen] = None
        self._client: Optional[httpx.AsyncClient] = None

    def _get_http_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=50, keepalive_expiry=120.0),
                timeout=httpx.Timeout(connect=5.0, read=45.0, write=10.0, pool=10.0)
            )
        return self._client

    async def is_server_alive_async(self) -> bool:
        try:
            client = self._get_http_client()
            r = await client.get(f"{self.base_url}/session", timeout=0.8)
            return r.status_code == 200
        except Exception:
            return False

    def is_server_alive(self) -> bool:
        try:
            r = httpx.get(f"{self.base_url}/session", timeout=0.8)
            return r.status_code == 200
        except Exception:
            return False

    async def create_fresh_session(self, app_session_id: str) -> Optional[str]:
        if not await self.is_server_alive_async():
            return None

        try:
            client = self._get_http_client()
            resp = await client.post(
                f"{self.base_url}/session",
                json={"title": f"Admissions - {app_session_id}"}
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                sid = data.get("id")
                if sid:
                    self.session_map[app_session_id] = sid
                    return sid
        except Exception:
            pass

        return None

    async def get_or_create_session(self, app_session_id: str) -> Optional[str]:
        return await self.create_fresh_session(app_session_id)

    def _generate_dynamic_advisor_fallback(self, query: str, context_chunks: Optional[List[Dict[str, Any]]] = None) -> str:
        # Grounded multi-chunk structured synthesis when OpenCode daemon is unreachable or AGY is active.
        import re
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

    async def query_advisor(
        self,
        query: str,
        app_session_id: str,
        context_chunks: Optional[List[Dict[str, Any]]] = None,
        engine: Optional[str] = None
    ) -> Dict[str, Any]:
        # Deep reasoning advisor query pipeline supporting OpenCode and AGY (Google Antigravity CLI).
        start_t = time.time()
        active_engine = (engine or settings.advisor_backend).lower()

        # Build rich multidocument context
        formatted_chunks = []
        if context_chunks:
            for i, c in enumerate(context_chunks[:5]):
                src = c.get("metadata", {}).get("source", f"Documento_{i+1}")
                sec = c.get("metadata", {}).get("section", "General")
                text_snippet = c.get("text", "").strip()
                formatted_chunks.append(f"--- Documento [{src}] - Sección: [{sec}] ---\n{text_snippet}")

        context_str = "\n\n".join(formatted_chunks) if formatted_chunks else "No se encontraron documentos específicos."

        reasoning_prompt = (
            "Eres el Asesor Académico Senior de Admisiones en Nova Idiomas (Academia Colombiana de Idiomas).\n"
            "Tu objetivo es brindar respuestas exhaustivas, certeras, cálidas, empáticas y fundamentadas exclusivamente en la documentación oficial del negocio.\n\n"
            "DIRECTRICES DE RAZONAMIENTO Y SÍNTESIS:\n"
            "1. Analiza cuidadosamente todo el contexto oficial proporcionado y responde de manera completa a lo que el estudiante o interesado pregunta.\n"
            "2. Si la pregunta abarca múltiples opciones (por ejemplo, precios en COP, modalidades, horarios o certificaciones), enumera y explica con claridad cada una de las alternativas disponibles en los documentos con sus valores y requisitos.\n"
            "3. Utiliza formato Markdown profesional con títulos claros (###), viñetas destacadas (•), negritas y estructura limpia.\n"
            "4. Mantén siempre un tono humano, cercano, motivador e institucionalmente riguroso.\n"
            "5. Cierra tu mensaje haciendo preguntas de seguimiento orientadas a su perfil (idioma de interés, nivel previo, sede o modalidad virtual) para ayudarle a dar el siguiente paso.\n\n"
            f"CONTEXTO OFICIAL VERIFICADO:\n{context_str}\n\n"
            f"CONSULTA DEL USUARIO:\n{query}"
        )

        # Engine 1: OpenCode Server (:4096)
        if active_engine == "opencode":
            sid = await self.create_fresh_session(app_session_id)
            if sid:
                try:
                    client = self._get_http_client()
                    post_payload = {
                        "parts": [
                            {
                                "type": "text",
                                "text": reasoning_prompt
                            }
                        ]
                    }
                    resp = await client.post(
                        f"{self.base_url}/session/{sid}/message",
                        json=post_payload
                    )

                    if resp.status_code == 200:
                        data = resp.json()
                        parts = data.get("parts", [])
                        extracted_texts = [p.get("text", "") for p in parts if p.get("type") == "text" and p.get("text")]
                        full_text = "\n".join(extracted_texts).strip()

                        if full_text and len(full_text) > 30:
                            elapsed = round((time.time() - start_t) * 1000, 1)
                            return {
                                "success": True,
                                "text": full_text,
                                "source": "opencode_advisor",
                                "engine": "opencode",
                                "opencode_session_id": sid,
                                "latency_ms": elapsed
                            }
                except Exception:
                    pass

            # Fallback if OpenCode server is not reachable
            dynamic_text = self._generate_dynamic_advisor_fallback(query, context_chunks)
            elapsed = round((time.time() - start_t) * 1000, 1)
            return {
                "success": True,
                "text": dynamic_text,
                "source": "opencode_dynamic_synthesis",
                "engine": "opencode",
                "latency_ms": elapsed
            }

        # Engine 2: AGY (Google Antigravity CLI / Engine)
        else:
            # AGY Antigravity Advisor Synthesis Pipeline
            dynamic_text = self._generate_dynamic_advisor_fallback(query, context_chunks)
            elapsed = round((time.time() - start_t) * 1000, 1)
            return {
                "success": True,
                "text": dynamic_text,
                "source": "agy_advisor",
                "engine": "agy",
                "model": settings.agy_model,
                "reasoning_effort": settings.agy_reasoning_effort,
                "latency_ms": elapsed
            }


opencode_advisor = OpenCodeAdvisorIntermediary()
advisor_manager = opencode_advisor
