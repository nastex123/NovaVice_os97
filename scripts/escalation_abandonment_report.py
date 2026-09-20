#!/usr/bin/env python3
"""
Escalation Abandonment Report (PROP-200, extensión de D40).
Analiza los tickets de escalamiento registrados (journal JSON, plano o vault
NovVault) y desglosa la causa raíz de abandono por cluster/área de admisiones
para el panel del equipo comercial.

Uso:
    python scripts/escalation_abandonment_report.py
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from src.config import settings
from src.core.abandonment import load_tickets, build_abandonment_report
from src.core.secure_store import get_vault_password


def run(verbose: bool = True) -> dict:
    try:
        tickets = load_tickets(settings.escalations_log_path, get_vault_password())
    except Exception:
        tickets = []
    report = build_abandonment_report(tickets)

    if verbose:
        print("=" * 70)
        print("REPORTE DE CAUSA RAÍZ DE ABANDONO POR CLUSTER (PROP-200)")
        print("=" * 70)
        print(f"Total de tickets (preguntas sin conversión): {report['total_escalations']}")
        for cluster, data in report["by_cluster"].items():
            if data["total"] == 0:
                continue
            print(f"\n[{cluster}] {data['total']} tickets ({data['share'] * 100:.1f}%)")
            print(f"  Causa predominante: {data['dominant_reason']}")
            print(f"  Keywords: {', '.join(data['top_keywords']) or '-'}")
        print("\nDocumentación sugerida (gaps de conocimiento, criterio D40):")
        if report["suggested_documents"]:
            for doc in report["suggested_documents"]:
                print(f"  📝 [NUEVO] backend/data/documents/{doc}")
        else:
            print("  - No se detectan temas críticos ausentes en el corpus.")
        print("=" * 70)

    return report


if __name__ == "__main__":
    run()