import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.core.metrics import classify_pillar
from src.core.secure_store import read_text_decrypted

PILLAR_LABELS = ("cursos", "horarios", "precios", "sedes", "becas", "unknown")

_DOC_GAP_HEURISTICS = [
    ("visa", "australia", "21_politica_visas_internacionales_y_alianzas_migratorias.md"),
    ("niño", "infantil", "edad", "22_politica_edades_minimas_y_cursos_para_ninos.md"),
    ("mascota", "pet", "23_politica_acceso_con_mascotas_pet_friendly.md"),
]


def load_tickets(log_path: Path, vault_password: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lee tickets de escalamiento desde el journal JSON (plano o vault NovVault)."""
    payload = read_text_decrypted(log_path, vault_password)
    if not payload:
        return []
    data = json.loads(payload)
    return data if isinstance(data, list) else []


def _dominant_reason(tickets: List[Dict[str, Any]]) -> str:
    reasons: Dict[str, int] = {}
    for t in tickets:
        r = t.get("escalation_reason", "unknown") or "unknown"
        reasons[r] = reasons.get(r, 0) + 1
    if not reasons:
        return "none"
    return max(reasons.items(), key=lambda kv: kv[1])[0]


def _top_keywords(tickets: List[Dict[str, Any]], limit: int = 5) -> List[str]:
    counts: Dict[str, int] = {}
    for t in tickets:
        for w in set(re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b", (t.get("query", "") or "").lower())):
            counts[w] = counts.get(w, 0) + 1
    return [w for w, _ in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:limit]]


def suggest_documents(tickets: List[Dict[str, Any]]) -> List[str]:
    """Mismo criterio D40: propone documentos de conocimiento ausentes."""
    low_conf = [t.get("query", "").lower() for t in tickets if float(t.get("confidence_score", 1.0)) < 0.50]
    suggested = []
    for haystack_needle, doc in _DOC_GAP_HEURISTICS:
        if any(h in " ".join(low_conf) for h in haystack_needle):
            suggested.append(doc)
    return suggested


def build_abandonment_report(tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Causa raíz de abandono por cluster/área (PROP-200).

    Agrupa los tickets de escalamiento (preguntas sin conversión) por pilar de
    admisiones y desglosa la causa predominante, keywords y cuota relativa.
    """
    grouped: Dict[str, List[Dict[str, Any]]] = {p: [] for p in PILLAR_LABELS}
    for t in tickets:
        grouped[classify_pillar(t.get("query", ""))].append(t)

    total = len(tickets)
    by_cluster: Dict[str, Dict[str, Any]] = {}
    for p in PILLAR_LABELS:
        group = grouped[p]
        by_cluster[p] = {
            "total": len(group),
            "share": round(len(group) / max(1, total), 4),
            "dominant_reason": _dominant_reason(group),
            "top_keywords": _top_keywords(group, limit=5)
        }

    return {
        "report_type": "escalation_abandonment",
        "total_escalations": total,
        "by_cluster": by_cluster,
        "suggested_documents": suggest_documents(tickets)
    }