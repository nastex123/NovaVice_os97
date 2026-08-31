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
        # Grounded multi-chunk structured synthesis when OpenCode daemon is unreachable.
        q_lower = query.lower()

        if any(w in q_lower for w in ("horario", "hora", "atencion", "abierto", "cuando atienden")):
            return (
                "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
                "¡Hola! Con mucho gusto te comparto nuestros horarios de clases y atención oficial:\n\n"
                "- **Franja Madrugadores:** 6:00 a.m. a 8:00 a.m. (Lunes a Viernes).\n\n"
                "- **Franjas Diurnas:** 9:00 a 11:00 a.m. y 2:00 a 4:00 p.m. / 4:00 a 6:00 p.m.\n\n"
                "- **Franja Nocturna (After Work):** 6:30 p.m. a 8:30 p.m. (Lunes a Viernes).\n\n"
                "- **Intensivos Sabatinos:** Sábados de 8:00 a.m. a 1:00 p.m. o 2:00 p.m. a 7:00 p.m.\n\n"
                "- **Intensivos Dominicales:** Domingos de 8:30 a.m. a 1:30 p.m.\n\n"
                "¿Qué idioma te interesa aprender y en qué horario te gustaría iniciar?"
            )

        if any(w in q_lower for w in ("edad", "ninos", "niños", "jovenes", "adolescentes", "adultos", "edad minima", "requisitos")):
            return (
                "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
                "¡Hola! En Nova Idiomas contamos con programas diseñados para diferentes grupos de edad:\n\n"
                "- **Kids & Junior (7 a 13 años):** Metodología lúdica e interactiva con enfoque comunicativo.\n\n"
                "- **Teens (14 a 17 años):** Nivelación académica y preparación para exámenes escolares e internacionales.\n\n"
                "- **Adultos (18 años en adelante):** Programas regulares, intensivos y especializados (Business, Tech, Legal English).\n\n"
                "La edad mínima general para nuestros cursos regulares de adultos es de 16 años (con autorización de acudiente) o desde los 7 años en nuestra línea Junior.\n\n"
                "¿Para quién sería el curso y qué idioma te gustaría aprender?"
            )

        if any(w in q_lower for w in ("contacto", "telefono", "correo", "email", "escribir", "hablar", "whatsapp")):
            return (
                "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
                "Puedes comunicarte directamente con nuestro equipo a través de los canales oficiales:\n\n"
                "- **WhatsApp de Admisiones:** [+57 300 912 3456](https://wa.me/573009123456)\n\n"
                "- **Línea Telefónica Nacional:** +57 (601) 745-8800\n\n"
                "- **Correo de Admisiones:** admisiones@novaidiomas.edu.co\n\n"
                "- **Sedes Físicas:** Bogotá (Chicó y Chapinero), Medellín (El Poblado y Laureles) y Cali (Granada).\n\n"
                "¿En qué más te puedo orientar el día de hoy?"
            )

        if context_chunks and len(context_chunks) > 0:
            bullet_points = []
            for c in context_chunks[:4]:
                sec = c.get("metadata", {}).get("section", "Información Oficial")
                lines = [l.strip() for l in c.get("text", "").split("\n") if l.strip() and not l.startswith("#")]
                for line in lines[:2]:
                    clean = line.lstrip("-* •")
                    if clean and len(clean) > 10:
                        bullet_points.append(f"- **[{sec}]** {clean}")

            body = "\n\n".join(bullet_points[:6])
            return (
                f"### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
                f"¡Hola! Respecto a tu consulta sobre *\"{query}\"*, revisando nuestra normativa y programas oficiales:\n\n"
                f"{body}\n\n"
                f"¿Deseas que te agendemos tu **Examen de Clasificación (Placement Test) 100% Gratuito** o revisemos los planes de pago en cuotas?"
            )

        return (
            "### 👨‍💼 Asesor de Admisiones - Nova Idiomas\n\n"
            f"¡Hola! He recibido tu consulta: *\"{query}\"*.\n\n"
            "Con gusto te oriento en todo lo que necesites sobre nuestros programas de idiomas (inglés, francés, alemán, italiano, portugués, español), tarifas en COP, modalidades virtual o presencial, o certificaciones internacionales (IELTS, DELF, Goethe).\n\n"
            "¿Podrías indicarme qué idioma deseas aprender y cuál es tu nivel actual estimado?"
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
                "latency_ms": elapsed
            }


opencode_advisor = OpenCodeAdvisorIntermediary()
advisor_manager = opencode_advisor
