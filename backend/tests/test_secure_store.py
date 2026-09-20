import json
import sqlite3

import pytest
from cryptography.fernet import InvalidToken

from src.core.secure_store import (
    encrypt_bytes,
    decrypt_bytes,
    encrypt_file,
    decrypt_file,
    atomic_write_encrypted,
    read_text_decrypted,
    get_vault_password,
)
from src.data.sqlite_tickets import SQLiteTicketRepository
from src.core.dispatcher import EscalationDispatcher

PASSWORD = "clave_de_prueba_unicamente_local"


def _ticket(ticket_id="ESC-20260920-ABC123"):
    return {
        "ticket_id": ticket_id,
        "created_at": "2026-09-20T22:00:00-0500",
        "user_id": "visitor_01",
        "query": "¿tienen pasantías con empresas tecnológicas?",
        "confidence_score": 0.31,
        "escalation_reason": "low_similarity",
        "assigned_to": "admisiones@novaidiomas.edu.co",
        "estimated_resolution_window": "<2h",
        "status": "pending_human_review",
        "conversation_history_last3": [{"role": "user", "content": "hola"}],
        "top3_candidate_chunks": [{"source": "05_visas.md", "section": "general", "preview": "sin pasantías"}],
    }


def test_encrypt_decrypt_roundtrip():
    payload = b"Nova Idiomas - datos sensibles del visitante"
    cipher = encrypt_bytes(payload, PASSWORD)
    assert cipher.startswith(b"NVVAULT\x00\x01")
    assert payload not in cipher
    assert decrypt_bytes(cipher, PASSWORD) == payload


def test_decrypt_wrong_password_raises():
    cipher = encrypt_bytes(b"secreto", PASSWORD)
    with pytest.raises(InvalidToken):
        decrypt_bytes(cipher, "clave_incorrecta")


def test_encrypt_file_decrypt_file(tmp_path):
    src = tmp_path / "db.bin"
    tgt = tmp_path / "db.bin.enc"
    src.write_bytes(b"sqlite-content")
    encrypt_file(src, tgt, PASSWORD)
    assert tgt.exists()
    assert b"sqlite-content" not in tgt.read_bytes()
    assert decrypt_file(tgt, PASSWORD) == b"sqlite-content"


def test_atomic_json_encryption_via_helpers(tmp_path):
    log = tmp_path / "journal.json"
    atomic_write_encrypted(log, json.dumps([{"q": "precio"}]), PASSWORD)
    assert b"precio" not in log.read_bytes()
    assert json.loads(read_text_decrypted(log, PASSWORD))[0]["q"] == "precio"
    atomic_write_encrypted(log, "[]", None)
    assert log.read_text(encoding="utf-8") == "[]"


def test_repo_encrypted_mode_decrypts_to_working_sqlite(tmp_path):
    db = tmp_path / "esc.db"
    repo = SQLiteTicketRepository(db_path=db, vault_password=PASSWORD)
    repo.save_ticket(_ticket())

    enc = db.with_name(db.name + ".enc")
    assert enc.exists()
    assert not db.exists()
    assert not list(tmp_path.glob("*.work"))
    assert not list(tmp_path.glob("*-wal"))

    raw = decrypt_file(enc, PASSWORD)
    assert raw.startswith(b"SQLite format 3\x00")

    recovered = tmp_path / "recovered.db"
    recovered.write_bytes(raw)
    conn = sqlite3.connect(str(recovered))
    count = conn.execute("SELECT COUNT(*) FROM escalation_tickets").fetchone()[0]
    conn.close()
    assert count == 1

    with pytest.raises(InvalidToken):
        decrypt_file(enc, "otra_clave")


def test_repo_encrypted_mode_reopens_across_instances(tmp_path):
    db = tmp_path / "esc.db"
    repo = SQLiteTicketRepository(db_path=db, vault_password=PASSWORD)
    repo.save_ticket(_ticket("ESC-20260920-AAA111"))
    repo.save_ticket(_ticket("ESC-20260920-BBB222"))

    repo2 = SQLiteTicketRepository(db_path=db, vault_password=PASSWORD)
    tickets = repo2.get_all_tickets()
    assert sorted(t["ticket_id"] for t in tickets) == ["ESC-20260920-AAA111", "ESC-20260920-BBB222"]
    assert db.with_name(db.name + ".enc").exists()
    assert not db.exists()


def test_repo_plaintext_mode_unchanged(tmp_path):
    db = tmp_path / "esc.db"
    repo = SQLiteTicketRepository(db_path=db)
    repo.save_ticket(_ticket())
    assert db.exists()
    assert not db.with_name(db.name + ".enc").exists()
    assert len(repo.get_all_tickets()) == 1


def test_dispatcher_json_encrypted_at_rest(tmp_path):
    log = tmp_path / "escalations.json"
    dispatcher = EscalationDispatcher(log_path=log, vault_password=PASSWORD)
    t = _ticket()
    dispatcher.create_ticket(
        query=t["query"],
        user_id=t["user_id"],
        confidence_score=t["confidence_score"],
        conversation_history=t["conversation_history_last3"],
        top_chunks=t["top3_candidate_chunks"],
    )

    raw = log.read_bytes()
    assert b"pasant" not in raw
    assert b"visitor" not in raw

    payload = read_text_decrypted(log, PASSWORD)
    tickets = json.loads(payload)
    assert len(tickets) == 1
    assert tickets[0]["ticket_id"].startswith("ESC-")


def test_dispatcher_json_plaintext_when_no_key(tmp_path):
    log = tmp_path / "escalations.json"
    dispatcher = EscalationDispatcher(log_path=log)
    t = _ticket()
    dispatcher.create_ticket(
        query=t["query"],
        user_id=t["user_id"],
        confidence_score=t["confidence_score"],
        conversation_history=t["conversation_history_last3"],
        top_chunks=t["top3_candidate_chunks"],
    )
    data = json.loads(log.read_text(encoding="utf-8"))
    assert "pasant" in data[0]["query"]


def test_get_vault_password_reads_env(monkeypatch):
    monkeypatch.setenv("ESCALATIONS_DB_KEY", "  supersecreta  ")
    assert get_vault_password() == "supersecreta"
    monkeypatch.delenv("ESCALATIONS_DB_KEY", raising=False)
    assert get_vault_password() is None