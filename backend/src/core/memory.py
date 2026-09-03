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

    def record_failure(self, session_id: str) -> int:
        """C23: Tracks consecutive failure turns (low confidence or clarifications)."""
        session = self.get_session(session_id)
        fails = session.get("consecutive_failures", 0) + 1
        session["consecutive_failures"] = fails
        return fails

    def reset_failures(self, session_id: str) -> None:
        """Resets the consecutive failures counter upon an informative answer."""
        session = self.get_session(session_id)
        session["consecutive_failures"] = 0

    def is_failure_loop(self, session_id: str) -> bool:
        """Returns True if the applicant has experienced 2 or more consecutive failures."""
        session = self.get_session(session_id)
        return session.get("consecutive_failures", 0) >= 2

    def record_sources(self, session_id: str, sources: List[str]) -> None:
        """C30: Stores source document signatures to detect repetitive retrieval loops."""
        session = self.get_session(session_id)
        if "source_history" not in session:
            session["source_history"] = []
        sig = ",".join(sorted(sources[:2])) if sources else ""
        session["source_history"].append(sig)
        if len(session["source_history"]) > 6:
            session["source_history"] = session["source_history"][-6:]

    def is_source_loop(self, session_id: str) -> bool:
        """Returns True if the last 3 turns yielded the exact same document sources."""
        session = self.get_session(session_id)
        hist = session.get("source_history", [])
        if len(hist) < 3:
            return False
        last3 = hist[-3:]
        return len(set(last3)) == 1 and bool(last3[0])


applicant_memory = EpisodicApplicantMemory()
