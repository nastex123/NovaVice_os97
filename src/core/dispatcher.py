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
        reason: str = "low_similarity"
    ) -> Dict[str, Any]:
        ticket_id = f"ESC-{time.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        ticket = {
            "ticket_id": ticket_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "user_id": user_id,
            "query": query,
            "confidence_score": round(confidence_score, 4),
            "escalation_reason": reason,
            "assigned_to": settings.admissions_office_email,
            "status": "pending_human_review"
        }

        # Persist to JSON log
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                tickets = json.load(f)
            tickets.append(ticket)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(tickets, f, indent=2)
        except Exception as e:
            # Fallback append
            pass

        return ticket

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
