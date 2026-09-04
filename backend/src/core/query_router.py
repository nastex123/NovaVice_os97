import re
import unicodedata
from typing import Dict, Any, Optional

class DeterministicQueryRouter:
    # Sub-15ms deterministic query router for factual admissions intents.
    # Returns verified official canned responses without LLM invocation.

    def __init__(self):
        self._routes = [
            {
                "id": "placement_test_link",
                "patterns": [
                    r"\bplacement\s+test\b",
                    r"\bprueba\s+de\s+(?:nivelaci[oó]n|clasificaci[oó]n)\b",
                    r"\bexamen\s+de\s+(?:nivelaci[oó]n|clasificaci[oó]n)\b",
                    r"\btest\s+gratis\b",
                    r"\bsaber\s+mi\s+nivel\b"
                ],
                "response": (
                    "📝 **Placement Test Oficial 100% Gratis - Nova Idiomas**\n\n"
                    "Puedes presentar la prueba de nivelación diagnóstica en línea sin costo:\n\n"
                    "• **Duración:** 25 a 35 minutos (Gramática, Vocabulario, Listening y Lectura).\n"
                    "• **Resultado:** Inmediato según escala MCER (A1 a C1).\n"
                    "• **Enlace directo:** [Presentar Placement Test Gratis](https://novaidiomas.edu.co/placement-test)\n\n"
                    "🏛️ *Fuente oficial:* Guía de Admisiones y Diagnóstico Académico"
                ),
                "source": "04_02_placement_test_online.md",
                "confidence": 0.98,
                "buttons": [
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            },
            {
                "id": "canales_contacto_admisiones",
                "patterns": [
                    r"\b(?:whatsapp|tel[eé]fono|celular|contacto|correo|email|comunicarme)\b"
                ],
                "response": (
                    "📞 **Canales Oficiales de Atención y Admisiones**\n\n"
                    "Comunícate directamente con nuestros asesores académicos:\n\n"
                    "• **WhatsApp Admisiones:** [+57 300 912 3456](https://wa.me/573009123456)\n"
                    "• **Línea Nacional:** (601) 745-9800\n"
                    "• **Correo Electrónico:** admisiones@novaidiomas.edu.co\n"
                    "• **Horario de atención:** Lunes a Viernes 7:00 a.m. a 8:00 p.m. | Sábados 8:00 a.m. a 2:00 p.m.\n\n"
                    "🏛️ *Fuente oficial:* Directorio de Canales de Atención Nova Idiomas"
                ),
                "source": "15_01_canales_atencion_y_contacto.md",
                "confidence": 0.98,
                "buttons": [
                    {"label": "1. Ver Cursos", "value": "1"},
                    {"label": "3. Ver Precios COP", "value": "3"},
                    {"label": "4. Sedes Físicas", "value": "4"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            }
        ]

    def _normalize(self, text: str) -> str:
        t = unicodedata.normalize("NFD", text.lower())
        t = "".join(c for c in t if unicodedata.category(c) != "Mn")
        return re.sub(r"\s+", " ", t).strip()

    def route(self, query: str) -> Optional[Dict[str, Any]]:
        # Fast pre-filtering
        q_norm = self._normalize(query)
        # Avoid overriding conversational questions like greetings or complex price comparisons
        if len(q_norm) < 4:
            return None

        for route in self._routes:
            for pattern in route["patterns"]:
                if re.search(pattern, q_norm, re.IGNORECASE):
                    return {
                        "status": "success",
                        "response": route["response"],
                        "source_documents": [route["source"]],
                        "confidence_score": route["confidence"],
                        "escalated_to_human": False,
                        "cached": False,
                        "mode": "deterministic_query_router",
                        "action_buttons": route["buttons"]
                    }
        return None

deterministic_query_router = DeterministicQueryRouter()
