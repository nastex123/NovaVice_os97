import re
import unicodedata
from typing import Dict, Any, Optional

_MENU_BUTTONS = [
    {"label": "1. Cursos & Certificaciones", "value": "1"},
    {"label": "2. Horarios & Modalidades", "value": "2"},
    {"label": "3. Precios & Financiación", "value": "3"},
    {"label": "0. Menú Principal", "value": "0"}
]

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
            },
            {
                "id": "convenios_descuentos",
                "patterns": [
                    r"\bcaja\s+de\s+compensacion\b",
                    r"\bcompensar\b",
                    r"\bcolsubsidio\b",
                    r"\bcafam\b",
                    r"\bcomfama\b",
                    r"\bcomfenalco\b",
                    r"\bcomfandi\b",
                    r"\bhermanos?\b",
                    r"\bconyuges?\b",
                    r"\bparejas?\b",
                    r"\bsegundo\s+miembro\b",
                    r"\breferidos?\b",
                    r"\bbono\b",
                    r"\bdescuento\s+(?:por|para|familiar|empresarial|universitario|en)\b",
                    r"\bdescuentos?\s+por\b",
                    r"\bsubsidio\s+monetario\b",
                    r"\bempleados?\s+de\s+empresas?\b",
                    r"\bconvenio\s+(?:con|cajas?|colsubsidio|cafam|comfama|comfenalco|comfandi)\b"
                ],
                "response": (
                    "🤝 **Convenios y Descuentos - Nova Idiomas**\n\n"
                    "**Cajas de Compensación Familiar (15% de matrícula, Categorías A y B, con certificado afiliación vigente):**\n"
                    "• Bogotá y Cundinamarca: Compensar, Colsubsidio y Cafam.\n"
                    "• Antioquia: Comfama y Comfenalco Antioquia.\n"
                    "• Valle del Cauca: Comfandi y Comfenalco Valle.\n"
                    "• Posibilidad de redimir el subsidio monetario educativo en cursos regulares e intensivos.\n\n"
                    "**Universitarios:** 15% de descuento permanente (pregrado y posgrado) presentando carné estudiantil vigente.\n"
                    "**Familiar o Parejas:** 15% para el segundo miembro de la familia inscrito simultáneamente.\n"
                    "**Convenios Empresariales:** 20% para empleados y familiares de empresas aliadas registradas.\n"
                    "**Referidos:** bono de $100.000 COP por cada amigo que se matricule referido por ti.\n\n"
                    "🏛️ *Fuente oficial:* 12_01_convenios_cajas_de_compensacion.md"
                ),
                "source": "12_01_convenios_cajas_de_compensacion.md",
                "confidence": 0.98,
                "buttons": _MENU_BUTTONS
            },
            {
                "id": "financiacion_medios_pago",
                "patterns": [
                    r"\bmedios?\s+de\s+pago\b",
                    r"\bformas?\s+de\s+pago\b",
                    r"\bplan\s+de\s+(?:3|tres)\s+cuotas?\b",
                    r"\bplan\s+de\s+contado\b",
                    r"\bcuantas?\s+cuotas?\b",
                    r"\bcuotas?\s+sin\s+(?:bancos?|intereses?)\b",
                    r"\bpago\s+en\s+cuotas\b",
                    r"\bcontado\b",
                    r"\bnequi\b",
                    r"\bdaviplata\b",
                    r"\bpse\b",
                    r"\btarjetas?\b",
                    r"\btransferencias?\b",
                    r"\beffecty\b",
                    r"\bsured\b",
                    r"\bcorresponsales?\b",
                    r"\bcomo\s+puedo\s+pagar\b"
                ],
                "response": (
                    "💳 **Financiación y Medios de Pago - Nova Idiomas**\n\n"
                    "**Plan de Contado:** 10% de descuento directo pagando el valor total antes del inicio de clases.\n\n"
                    "**Plan 3 Cuotas sin Interés (financiación directa, sin bancos, 0% de interés y sin consulta a Datacrédito):**\n"
                    "• 1ª Cuota (40%): al momento de la matrícula.\n"
                    "• 2ª Cuota (30%): semana 4 de clases.\n"
                    "• 3ª Cuota (30%): semana 7 de clases.\n"
                    "*Ejemplo Módulo Intensivo $720.000: $288.000 → $216.000 → $216.000.*\n\n"
                    "**Medios de Pago Habilitados:**\n"
                    "• PSE, Nequi, Daviplata, Tarjetas de Crédito y Débito (Visa, Mastercard, American Express, Diners Club).\n"
                    "• Transferencias: Bancolombia, Banco de Bogotá y Davivienda.\n"
                    "• Efectivo y corresponsales: sedes físicas, Efecty, SuRed y corresponsales Bancolombia.\n\n"
                    "🏛️ *Fuente oficial:* 03_precios_tarifas_y_financiacion.md"
                ),
                "source": "03_precios_tarifas_y_financiacion.md",
                "confidence": 0.98,
                "buttons": _MENU_BUTTONS
            },
            {
                "id": "precios_tarifas",
                "patterns": [
                    r"\bcuanto\s+cuest(?:a|an|e)\b",
                    r"\bcuanto\s+vale\b",
                    r"\bcual\s+es\s+el\s+precio\b",
                    r"\bcosto\s+del\s+curso\b",
                    r"\bvalor\s+del\s+curso\b",
                    r"\bvalor\s+del\s+modulo\b",
                    r"\bcuanto\s+es\s+el\s+valor\b",
                    r"\bprecio\s+de(?:l| la)\b",
                    r"\bpagar\s+por\b"
                ],
                "response": (
                    "💰 **Precios y Tarifas Oficiales (COP) - Nova Idiomas**\n\n"
                    "Todos los valores incluyen acceso a la plataforma digital y clubes de conversación. Sin cobros ocultos.\n\n"
                    "**Módulos y Ciclos (40 horas académicas):**\n"
                    "• Curso Regular Bimestral: $650.000 COP por módulo.\n"
                    "• Curso Intensivo Mensual: $720.000 COP por módulo.\n"
                    "• Curso Sabatino / Dominical: $650.000 COP por ciclo.\n\n"
                    "**Clases Privadas Personalizadas 1 a 1:**\n"
                    "• 10 horas: $650.000 COP ($65.000 COP/hora).\n"
                    "• 20 horas: $1.200.000 COP ($60.000 COP/hora).\n"
                    "• 40 horas: $2.200.000 COP ($55.000 COP/hora).\n\n"
                    "**Paquetes por Nivel Completo:**\n"
                    "• Elemental A1 (2 módulos): $1.200.000 COP (ahorras $100.000).\n"
                    "• Básico A2 (2 módulos): $1.200.000 COP (ahorras $100.000).\n"
                    "• Intermedio B1 (3 módulos): $1.750.000 COP (ahorras $200.000).\n"
                    "• Avanzado B2 (3 módulos): $1.750.000 COP (ahorras $200.000).\n"
                    "• Bilingüismo Total (A1+A2+B1+B2, 10 módulos): $5.500.000 COP (ahorro de $1.500.000).\n\n"
                    "🏛️ *Fuente oficial:* 03_precios_tarifas_y_financiacion.md"
                ),
                "source": "03_precios_tarifas_y_financiacion.md",
                "confidence": 0.98,
                "buttons": _MENU_BUTTONS
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

        # Deterministic canned responses only for concise, direct queries (<=10 words).
        # Longer composite queries (e.g. "precio + horarios") flow to RAG for full context.
        if len(q_norm.split()) > 10:
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
