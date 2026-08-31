from typing import Dict, Any
import httpx


RAG_BACKEND_URL = "http://localhost:8000/api/v1/chat"
DEFAULT_TIMEOUT = 15.0


def query_university_admissions_rag(query: str, user_id: str = "hermes_agent_applicant") -> Dict[str, Any]:
    """
    Queries Nova Tech University admissions RAG system for official information regarding
    tuition fees, payment plans, application deadlines, requirements, modalities, and scholarships.

    Args:
        query (str): The specific question asked by the applicant.
        user_id (str, optional): The applicant identifier. Defaults to 'hermes_agent_applicant'.

    Returns:
        Dict[str, Any]: Dictionary containing status, official response, confidence score,
                       and escalation details if routed to human admissions staff.
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
                    "response": f"Admissions backend returned HTTP status {resp.status_code}.",
                    "escalated_to_human": True
                }
    except Exception as exc:
        return {
            "status": "connection_error",
            "response": f"Could not reach admissions backend at {RAG_BACKEND_URL}. Ensure the server is active. Detail: {str(exc)}",
            "escalated_to_human": True
        }


# Standard tool descriptor for Hermes Agent CLI
tool_definition = {
    "type": "function",
    "function": {
        "name": "query_university_admissions_rag",
        "description": "Queries Nova Tech University admissions knowledge base for tuition, requirements, schedules, and modalities.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The admissions inquiry question."},
                "user_id": {"type": "string", "description": "Optional applicant user ID."}
            },
            "required": ["query"]
        }
    }
}
