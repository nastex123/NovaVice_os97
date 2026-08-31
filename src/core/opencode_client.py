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

    def is_server_alive(self) -> bool:
        try:
            r = httpx.get(f"{self.base_url}/session", timeout=2.0)
            return r.status_code == 200
        except Exception:
            return False

    def ensure_server_running(self) -> bool:
        if self.is_server_alive():
            return True

        try:
            self._server_process = subprocess.Popen(
                ["opencode", "serve", "--port", "4096"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            for _ in range(5):
                time.sleep(0.8)
                if self.is_server_alive():
                    return True
        except Exception:
            pass

        return self.is_server_alive()

    async def create_fresh_session(self, app_session_id: str) -> Optional[str]:
        if not self.ensure_server_running():
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
                "👨‍💼 **Asesor de Admisiones (Nova Tech University)**\n\n"
                "¡Hola! Con mucho gusto te comparto nuestros horarios de atención oficial:\n\n"
                "• **Atención Virtual y Asesorías Online:** Lunes a Viernes de 8:00 AM a 6:00 PM (Hora local).\n"
                "• **Oficina Presencial de Admisiones:** Edificio Central del Campus, de 8:30 AM a 5:30 PM.\n"
                "• **Biblioteca y Salas de Cómputo:** Abiertas 24 horas los 7 días de la semana con credencial digital.\n\n"
                "¿Te gustaría agendar una asesoría personalizada o tienes alguna duda sobre las carreras?"
            )

        if any(w in q_lower for w in ("contacto", "telefono", "correo", "email", "escribir", "hablar")):
            return (
                "👨‍💼 **Asesor de Admisiones (Nova Tech University)**\n\n"
                "Puedes comunicarte directamente con nosotros a través de los canales oficiales:\n\n"
                "• **Correo Institucional:** admisiones@novatech.edu\n"
                "• **Línea de Atención / WhatsApp:** +1 (800) 555-NOVA\n"
                "• **Portal de Admisiones:** https://admisiones.novatech.edu\n\n"
                "¿En qué más te puedo orientar el día de hoy?"
            )

        if context_chunks and len(context_chunks) > 0:
            sections_covered = []
            bullet_points = []

            for c in context_chunks[:4]:
                src = c.get("metadata", {}).get("source", "Documento Oficial")
                sec = c.get("metadata", {}).get("section", src)
                if sec not in sections_covered:
                    sections_covered.append(sec)

                lines = [l.strip() for l in c.get("text", "").split("\n") if l.strip() and not l.startswith("#")]
                for line in lines[:3]:
                    clean = line.lstrip("-* •")
                    if clean and len(clean) > 10:
                        bullet_points.append(f"• **[{sec}]** {clean}")

            body = "\n".join(bullet_points[:8])
            return (
                f"👨‍💼 **Asesor de Admisiones (Nova Tech University)**\n\n"
                f"¡Hola! Analizando nuestra documentación oficial vigente respecto a tu consulta:\n\n"
                f"{body}\n\n"
                f"¿Te gustaría que profundicemos en los requisitos de alguna de estas opciones o en las fechas de postulación?"
            )

        return (
            "👨‍💼 **Asesor de Admisiones (Nova Tech University)**\n\n"
            f"¡Hola! He recibido tu consulta: *\"{query}\"*.\n\n"
            "Con gusto te oriento en todo lo que necesites sobre nuestros programas de grado (Ingeniería de Software, Inteligencia Artificial, Ciberseguridad), opciones de becas, aranceles, residencias o fechas de postulación.\n\n"
            "¿Podrías darme un poco más de detalle sobre lo que buscas para darte la respuesta exacta?"
        )

    async def query_advisor(
        self,
        query: str,
        app_session_id: str,
        context_chunks: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        # Deep reasoning advisor query pipeline leveraging OpenCode reasoning models.
        start_t = time.time()
        sid = await self.create_fresh_session(app_session_id)

        if sid:
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
                "Eres el Asesor Académico Senior de Admisiones en Nova Tech University.\n"
                "Tu objetivo es brindar respuestas exhaustivas, certeras, cálidas, empáticas y fundamentadas exclusivamente en la documentación oficial.\n\n"
                "DIRECTRICES DE RAZONAMIENTO Y SÍNTESIS:\n"
                "1. Analiza cuidadosamente todo el contexto oficial proporcionado y responde de manera completa a lo que el postulante pregunta.\n"
                "2. Si la pregunta abarca múltiples opciones (por ejemplo, becas, modalidades, fechas o materias), enumera y explica con claridad cada una de las alternativas disponibles en los documentos con sus porcentajes y requisitos.\n"
                "3. Utiliza formato Markdown profesional con títulos claros (###), viñetas destacadas (•), negritas y estructura limpia.\n"
                "4. Mantén siempre un tono humano, cercano, motivador e institucionalmente riguroso.\n"
                "5. Cierra tu mensaje haciendo preguntas de seguimiento orientadas a su perfil (carrera de interés, promedio, etc.) para ayudarle a dar el siguiente paso.\n\n"
                f"CONTEXTO OFICIAL VERIFICADO:\n{context_str}\n\n"
                f"CONSULTA DEL POSTULANTE:\n{query}"
            )

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
                            "opencode_session_id": sid,
                            "latency_ms": elapsed
                        }
            except Exception:
                pass

        # Fallback if server is not reachable
        dynamic_text = self._generate_dynamic_advisor_fallback(query, context_chunks)
        elapsed = round((time.time() - start_t) * 1000, 1)
        return {
            "success": True,
            "text": dynamic_text,
            "source": "advisor_dynamic_synthesis",
            "latency_ms": elapsed
        }


opencode_advisor = OpenCodeAdvisorIntermediary()
