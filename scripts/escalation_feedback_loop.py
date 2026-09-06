#!/usr/bin/env python3
"""
Escalation Feedback Loop & Knowledge Gap Analyzer (Item D40)
Analyzes unaddressed applicant inquiries from backend/data/escalations.json,
identifies recurring themes, and suggests documentation updates.
"""
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from src.core.dispatcher import escalation_dispatcher


def run_feedback_loop(verbose: bool = True) -> dict:
    report = escalation_dispatcher.generate_feedback_report()
    
    if verbose:
        print("=" * 70)
        print("📊 REPORTE SEMANAL DE ESCALAMIENTOS & GAPS DE CONOCIMIENTO (D40)")
        print("=" * 70)
        print(f"Total de tickets registrados: {report['total_escalations']}")
        print(f"Consultas con baja confianza (<0.35): {report['low_confidence_count']}")
        print("\nPalabras clave más frecuentes en consultas no resueltas:")
        for kw, cnt in report["frequent_keywords"].items():
            print(f"  • {kw:<15} ({cnt} menciones)")
        
        print("\nDocumentación sugerida para incorporar a la base de conocimiento:")
        if report["suggested_documents"]:
            for doc in report["suggested_documents"]:
                print(f"  📝 [NUEVO] backend/data/documents/{doc}")
        else:
            print("  ✅ No se detectan temas críticos ausentes en el corpus actual.")
        print("=" * 70)

    return report


if __name__ == "__main__":
    run_feedback_loop()
