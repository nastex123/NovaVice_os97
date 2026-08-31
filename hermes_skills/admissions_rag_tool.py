from typing import Dict, Any
import httpx


RAG_BACKEND_URL = "http://localhost:8000/api/v1/chat"
DEFAULT_TIMEOUT = 15.0


def query_language_academy_rag(query: str, user_id: str = "hermes_agent_applicant") -> Dict[str, Any]:
    """
    Consulta la base de conocimiento oficial de Nova Idiomas Colombia sobre
    horarios, precios en COP, niveles MCER, inscripciones, certificaciones y modalidades.

    Args:
        query (str): La pregunta específica del postulante o estudiante.
        user_id (str, optional): Identificador del usuario.

    Returns:
        Dict[str, Any]: Diccionario con respuesta oficial fundamentada, puntaje de confianza y citaciones.
    """
    payload = {
        "user_id": user_id,
        "query": query,
        "use_hermes_mode": True
    }

    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.post(RAG_BACKEND_URL, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "status": data.get("status", "success"),
                    "response": data.get("response", ""),
                    "confidence_score": data.get("confidence_score", 1.0),
                    "escalated_to_human": data.get("escalated_to_human", False),
                    "escalation_ticket_id": data.get("escalation_ticket_id", None),
                    "source_documents": data.get("source_documents", [])
                }
            else:
                return {
                    "status": "error",
                    "response": f"El backend de Nova Idiomas retornó estado HTTP {resp.status_code}.",
                    "escalated_to_human": True
                }
    except Exception as exc:
        return {
            "status": "connection_error",
            "response": f"No se pudo conectar al backend de Nova Idiomas en {RAG_BACKEND_URL}. Detalle: {str(exc)}",
            "escalated_to_human": True
        }


# Descriptor estándar para integración de herramientas con agentes LLM
tool_definition = {
    "type": "function",
    "function": {
        "name": "query_language_academy_rag",
        "description": "Consulta la base de conocimiento oficial de Nova Idiomas (precios COP, horarios, niveles MCER, sedes, certificaciones).",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Pregunta del usuario sobre cursos de idiomas."},
                "user_id": {"type": "string", "description": "ID de usuario opcional."}
            },
            "required": ["query"]
        }
    }
}

