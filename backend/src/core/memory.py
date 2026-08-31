from typing import Dict, Any, List, Optional
import time


class EpisodicApplicantMemory:
    # Stores conversational context and applicant attributes across turns.

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": time.time(),
                "last_active": time.time(),
                "history": [],
                "attributes": {}
            }
        return self.sessions[session_id]

    def add_interaction(
        self,
        session_id: str,
        user_query: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        session = self.get_session(session_id)
        session["last_active"] = time.time()
        session["history"].append({
            "query": user_query,
            "response": assistant_response,
            "metadata": metadata or {},
            "timestamp": time.time()
        })

    def update_attributes(self, session_id: str, key: str, value: Any) -> None:
        session = self.get_session(session_id)
        session["attributes"][key] = value

    def get_recent_history(self, session_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        session = self.get_session(session_id)
        return session["history"][-limit:]


applicant_memory = EpisodicApplicantMemory()
