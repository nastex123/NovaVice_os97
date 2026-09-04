import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import settings


class SQLiteTicketRepository:
    """
    Thread-safe, crash-resilient SQLite repository with Write-Ahead Logging (WAL)
    for admission escalation tickets.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (settings.data_dir / "escalations.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS escalation_tickets (
                    ticket_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    query TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    escalation_reason TEXT NOT NULL,
                    assigned_to TEXT,
                    estimated_resolution_window TEXT,
                    status TEXT NOT NULL,
                    conversation_history_json TEXT,
                    candidate_chunks_json TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON escalation_tickets(created_at);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tickets_status ON escalation_tickets(status);")

    def save_ticket(self, ticket: Dict[str, Any]) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO escalation_tickets (
                    ticket_id, created_at, user_id, query,
                    confidence_score, escalation_reason, assigned_to,
                    estimated_resolution_window, status,
                    conversation_history_json, candidate_chunks_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ticket["ticket_id"],
                ticket["created_at"],
                ticket["user_id"],
                ticket["query"],
                float(ticket.get("confidence_score", 0.0)),
                ticket.get("escalation_reason", "unknown"),
                ticket.get("assigned_to", ""),
                ticket.get("estimated_resolution_window", "<2h"),
                ticket.get("status", "pending_human_review"),
                json.dumps(ticket.get("conversation_history_last3", []), ensure_ascii=False),
                json.dumps(ticket.get("top3_candidate_chunks", []), ensure_ascii=False)
            ))

    def get_all_tickets(self, limit: int = 200) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT ticket_id, created_at, user_id, query,
                       confidence_score, escalation_reason, assigned_to,
                       estimated_resolution_window, status,
                       conversation_history_json, candidate_chunks_json
                FROM escalation_tickets
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        tickets = []
        for r in rows:
            tickets.append({
                "ticket_id": r["ticket_id"],
                "created_at": r["created_at"],
                "user_id": r["user_id"],
                "query": r["query"],
                "confidence_score": r["confidence_score"],
                "escalation_reason": r["escalation_reason"],
                "assigned_to": r["assigned_to"],
                "estimated_resolution_window": r["estimated_resolution_window"],
                "status": r["status"],
                "conversation_history_last3": json.loads(r["conversation_history_json"] or "[]"),
                "top3_candidate_chunks": json.loads(r["candidate_chunks_json"] or "[]")
            })
        return tickets

    def migrate_from_json(self, json_path: Path) -> int:
        if not json_path.exists():
            return 0
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                tickets = json.load(f)
            count = 0
            for t in tickets:
                if isinstance(t, dict) and "ticket_id" in t:
                    self.save_ticket(t)
                    count += 1
            return count
        except Exception:
            return 0


sqlite_ticket_repo = SQLiteTicketRepository()
