import json
import uuid
import time
from pathlib import Path
from typing import Dict, Any, Optional
import httpx
from src.config import settings


class EscalationDispatcher:
    # Generates persistent escalation tickets and dispatches real-time webhooks.

    def __init__(self, log_path: Optional[Path] = None, webhook_url: Optional[str] = None):
        self.log_path = log_path or settings.escalations_log_path
        self.webhook_url = webhook_url or settings.escalation_webhook_url
        self._ensure_log_exists()

    def _ensure_log_exists(self) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def create_ticket(
        self,
        query: str,
        user_id: str,
        confidence_score: float,
        reason: str = "low_similarity",
        conversation_history: Optional[list] = None,
        top_chunks: Optional[list] = None
    ) -> Dict[str, Any]:
        ticket_id = f"ESC-{time.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        # D36: Extended context for human admissions advisor (last 3 turns + top 3 chunks)
        clean_history = []
        if conversation_history:
            for item in conversation_history[-3:]:
                clean_history.append({
                    "role": item.get("role", "user"),
                    "content": str(item.get("content", item.get("query", "")))[:300]
                })

        clean_chunks = []
        if top_chunks:
            for c in top_chunks[:3]:
                clean_chunks.append({
                    "source": c.get("metadata", {}).get("source", "unknown"),
                    "section": c.get("metadata", {}).get("section", "general"),
                    "preview": str(c.get("text", ""))[:200].replace("\n", " ").strip()
                })

        ticket = {
            "ticket_id": ticket_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "user_id": user_id,
            "query": query,
            "confidence_score": round(confidence_score, 4),
            "escalation_reason": reason,
            "assigned_to": settings.admissions_office_email,
            "estimated_resolution_window": "<2h",
            "status": "pending_human_review",
            "conversation_history_last3": clean_history,
            "top3_candidate_chunks": clean_chunks
        }

        # Persist to SQLite with WAL mode & fallback JSON
        try:
            from src.data.sqlite_tickets import sqlite_ticket_repo
            sqlite_ticket_repo.save_ticket(ticket)
        except Exception:
            pass

        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                tickets = json.load(f)
            tickets.append(ticket)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(tickets, f, indent=2)
        except Exception:
            pass

        return ticket

    def generate_feedback_report(self) -> Dict[str, Any]:
        """
        D40: Weekly feedback loop analyzing unaddressed user queries in escalations.json.
        Returns total tickets, common topics, and suggested new documentation titles.
        """
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                tickets = json.load(f)
        except Exception:
            tickets = []

        if not tickets:
            return {
                "total_escalations": 0,
                "common_topics": {},
                "suggested_documents": []
            }

        # Count common keywords in escalated queries
        word_counts: Dict[str, int] = {}
        for t in tickets:
            q = t.get("query", "").lower()
            import re
            words = set(re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b", q))
            for w in words:
                word_counts[w] = word_counts.get(w, 0) + 1

        # Identify queries with low confidence / out of pillar scope
        low_conf_queries = [t.get("query", "") for t in tickets if t.get("confidence_score", 0.0) < 0.50]

        # Suggest documentation topics
        suggested = []
        if any("visa" in q.lower() or "australia" in q.lower() for q in low_conf_queries):
            suggested.append("21_politica_visas_internacionales_y_alianzas_migratorias.md")
        if any("niño" in q.lower() or "infantil" in q.lower() or "edad" in q.lower() for q in low_conf_queries):
            suggested.append("22_politica_edades_minimas_y_cursos_para_ninos.md")
        if any("mascota" in q.lower() or "pet" in q.lower() for q in low_conf_queries):
            suggested.append("23_politica_acceso_con_mascotas_pet_friendly.md")

        return {
            "total_escalations": len(tickets),
            "low_confidence_count": len(low_conf_queries),
            "frequent_keywords": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "suggested_documents": suggested
        }

    async def dispatch_webhook(self, ticket: Dict[str, Any]) -> bool:
        if not self.webhook_url:
            return False

        payload = {
            "text": f"New University Admissions Escalation Ticket: {ticket['ticket_id']}",
            "ticket": ticket
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(self.webhook_url, json=payload)
                return resp.status_code in (200, 201, 204)
        except Exception:
            return False


escalation_dispatcher = EscalationDispatcher()
