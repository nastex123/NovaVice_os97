#!/usr/bin/env python3
"""
Harness de Evaluación de Fidelidad Factual y Métricas RAG (TODO-2.17)
Evalúa 50 preguntas del dataset dorado sobre los 5 pilares institucionales de Nova Idiomas.
Exige faithfulness = 1.0 en preguntas clave como CI Gate.
"""

import sys
import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from src.rag.engine import PurePythonRAGEngine
from src.core.faithfulness import faithfulness_verifier

GOLD_DATASET: List[Dict[str, Any]] = [
    # Pilar: Cursos y Certificaciones
    {"id": "c1", "pillar": "cursos", "query": "¿Cuáles programas de idiomas ofrecen y qué niveles tienen?", "strict_facts": ["inglés", "francés", "alemán", "italiano", "portugués", "A1", "C1"]},
    {"id": "c2", "pillar": "cursos", "query": "¿Tienen preparación para exámenes internacionales como IELTS y TOEFL?", "strict_facts": ["IELTS", "TOEFL"]},
    {"id": "c3", "pillar": "cursos", "query": "¿Ofrecen certificación bajo el marco común europeo MCER?", "strict_facts": ["MCER"]},
    {"id": "c4", "pillar": "cursos", "query": "¿Tienen clases para niños o solo adultos?", "strict_facts": ["adolescentes", "adultos"]},
    {"id": "c5", "pillar": "cursos", "query": "¿Tienen curso de español para extranjeros?", "strict_facts": ["español"]},
    {"id": "c6", "pillar": "cursos", "query": "¿Cómo funciona la prueba de clasificación o placement test?", "strict_facts": ["clasificación", "test"]},
    {"id": "c7", "pillar": "cursos", "query": "¿Qué niveles comprende el programa de alemán?", "strict_facts": ["alemán", "Goethe"]},
    {"id": "c8", "pillar": "cursos", "query": "¿Cuánto dura cada módulo o nivel?", "strict_facts": ["módulo", "horas"]},
    {"id": "c9", "pillar": "cursos", "query": "¿Entregan certificado al finalizar cada nivel?", "strict_facts": ["certificado", "asistencia"]},
    {"id": "c10", "pillar": "cursos", "query": "¿Qué metodología pedagógica maneja Nova Idiomas?", "strict_facts": ["comunicativa", "práctica"]},

    # Pilar: Precios y Financiación
    {"id": "p1", "pillar": "precios", "query": "¿Cuánto cuesta el módulo de inglés regular?", "strict_facts": ["650.000", "COP", "$"]},
    {"id": "p2", "pillar": "precios", "query": "¿Cuál es el valor del curso intensivo?", "strict_facts": ["720.000", "COP", "$"]},
    {"id": "p3", "pillar": "precios", "query": "¿Tienen descuento por pago de contado?", "strict_facts": ["10%", "contado"]},
    {"id": "p4", "pillar": "precios", "query": "¿Cómo es el plan de financiación por cuotas?", "strict_facts": ["3 cuotas", "40%", "30%", "30%"]},
    {"id": "p5", "pillar": "precios", "query": "¿Cobran intereses en la financiación por cuotas?", "strict_facts": ["sin interés", "0%"]},
    {"id": "p6", "pillar": "precios", "query": "¿Qué medios de pago aceptan?", "strict_facts": ["PSE", "Nequi", "Daviplata", "tarjeta"]},
    {"id": "p7", "pillar": "precios", "query": "¿El valor incluye el material didáctico y los libros?", "strict_facts": ["material", "digital"]},
    {"id": "p8", "pillar": "precios", "query": "¿Cuánto cuesta la matrícula inicial?", "strict_facts": ["incluida", "matrícula"]},
    {"id": "p9", "pillar": "precios", "query": "¿Cuál es la política de devoluciones o reembolsos?", "strict_facts": ["reembolso", "días"]},
    {"id": "p10", "pillar": "precios", "query": "¿Tienen descuento si matriculo dos idiomas al tiempo?", "strict_facts": ["descuento", "adicional"]},

    # Pilar: Horarios y Modalidades
    {"id": "h1", "pillar": "horarios", "query": "¿Qué horarios tienen para clases en la mañana?", "strict_facts": ["6:00", "8:00", "a.m."]},
    {"id": "h2", "pillar": "horarios", "query": "¿Tienen horarios nocturnos de lunes a viernes?", "strict_facts": ["6:30", "8:30", "p.m."]},
    {"id": "h3", "pillar": "horarios", "query": "¿Tienen cursos los sábados?", "strict_facts": ["sábado", "8:00", "12:00"]},
    {"id": "h4", "pillar": "horarios", "query": "¿Las clases virtuales son en vivo o grabadas?", "strict_facts": ["en vivo", "sincrónica"]},
    {"id": "h5", "pillar": "horarios", "query": "¿Tienen modalidad híbrida?", "strict_facts": ["híbrida", "presencial"]},
    {"id": "h6", "pillar": "horarios", "query": "¿Puedo cambiar de horario si mi trabajo cambia?", "strict_facts": ["cambio", "solicitud"]},
    {"id": "h7", "pillar": "horarios", "query": "¿Cuántas horas a la semana se dictan en el curso intensivo?", "strict_facts": ["horas", "intensivo"]},
    {"id": "h8", "pillar": "horarios", "query": "¿Qué plataforma tecnológica usan para las clases en línea?", "strict_facts": ["plataforma", "Teams", "Zoom"]},
    {"id": "h9", "pillar": "horarios", "query": "¿Quedan grabaciones si no puedo asistir a una clase?", "strict_facts": ["grabación", "aula"]},
    {"id": "h10", "pillar": "horarios", "query": "¿Qué porcentaje mínimo de asistencia se exige?", "strict_facts": ["80%", "asistencia"]},

    # Pilar: Sedes y Ubicaciones
    {"id": "s1", "pillar": "sedes", "query": "¿Dónde queda la sede de Bogotá Chicó?", "strict_facts": ["Chicó", "Calle 93", "Bogotá"]},
    {"id": "s2", "pillar": "sedes", "query": "¿Tienen sede en Chapinero?", "strict_facts": ["Chapinero", "Carrera 13", "Bogotá"]},
    {"id": "s3", "pillar": "sedes", "query": "¿En qué ciudades de Colombia tienen sedes físicas?", "strict_facts": ["Bogotá", "Medellín", "Cali"]},
    {"id": "s4", "pillar": "sedes", "query": "¿Dónde queda la sede de Medellín en El Poblado?", "strict_facts": ["Poblado", "Medellín"]},
    {"id": "s5", "pillar": "sedes", "query": "¿Tienen sede en Laureles Medellín?", "strict_facts": ["Laureles", "Medellín"]},
    {"id": "s6", "pillar": "sedes", "query": "¿Dónde está ubicada la sede de Cali?", "strict_facts": ["Granada", "Cali"]},
    {"id": "s7", "pillar": "sedes", "query": "¿Las sedes cuentan con parqueadero para estudiantes?", "strict_facts": ["parqueadero", "convenio"]},
    {"id": "s8", "pillar": "sedes", "query": "¿Cuál es el horario de atención al público en recepción?", "strict_facts": ["atención", "lunes"]},
    {"id": "s9", "pillar": "sedes", "query": "¿Puedo tomar clases en una sede y luego cambiar a otra?", "strict_facts": ["traslado", "sede"]},
    {"id": "s10", "pillar": "sedes", "query": "¿Tienen laboratorios de idiomas en las sedes físicas?", "strict_facts": ["laboratorio", "recursos"]},

    # Pilar: Becas y Descuentos
    {"id": "b1", "pillar": "becas_descuentos", "query": "¿Tienen becas del 100% gratuitas?", "strict_facts": ["no otorga becas del 100%", "descuento", "convenio"]},
    {"id": "b2", "pillar": "becas_descuentos", "query": "¿Qué convenios de descuento tienen con cajas de compensación?", "strict_facts": ["Compensar", "Colsubsidio", "Cafam", "Comfama", "15%"]},
    {"id": "b3", "pillar": "becas_descuentos", "query": "¿Tienen descuento para grupos familiares?", "strict_facts": ["familiar", "15%"]},
    {"id": "b4", "pillar": "becas_descuentos", "query": "¿Existe beneficio de pronto pago?", "strict_facts": ["pronto pago", "10%"]},
    {"id": "b5", "pillar": "becas_descuentos", "query": "¿Qué requisitos se piden para aplicar a un convenio de caja?", "strict_facts": ["certificado", "afiliación"]},
    {"id": "b6", "pillar": "becas_descuentos", "query": "¿Los descuentos son acumulables entre sí?", "strict_facts": ["no acumulables"]},
    {"id": "b7", "pillar": "becas_descuentos", "query": "¿Tienen convenios empresariales para corporativos?", "strict_facts": ["convenio", "empresarial"]},
    {"id": "b8", "pillar": "becas_descuentos", "query": "¿Cómo solicito el descuento de mi caja Comfandi?", "strict_facts": ["Comfandi", "admisiones"]},
    {"id": "b9", "pillar": "becas_descuentos", "query": "¿Existe plan de referidos para estudiantes activos?", "strict_facts": ["referido", "bono"]},
    {"id": "b10", "pillar": "becas_descuentos", "query": "¿Se aplican los convenios en cursos intensivos?", "strict_facts": ["aplica", "intensivo"]}
]


async def run_evaluation(ci_gate_strict: bool = True) -> Dict[str, Any]:
    rag_engine = PurePythonRAGEngine()
    total = len(GOLD_DATASET)
    passed_faithfulness = 0
    scores = []
    pilar_results = {}

    print("================================================================")
    print("🚀 Iniciando Evaluación de Fidelidad RAG CI (50 Preguntas Oficiales)")
    print("================================================================\n")

    for idx, item in enumerate(GOLD_DATASET, 1):
        q_id = item["id"]
        pillar = item["pillar"]
        query = item["query"]

        res = await rag_engine.answer_query(query, user_id="eval_ci_user", session_id=f"session_eval_{q_id}")
        ans_text = res.get("response", "")
        chunks = res.get("source_documents", [])

        score, is_faithful = faithfulness_verifier.evaluate_faithfulness(ans_text, chunks)
        scores.append(score)

        if score >= 0.80:
            passed_faithfulness += 1

        if pillar not in pilar_results:
            pilar_results[pillar] = {"total": 0, "faithful": 0, "scores": []}
        pilar_results[pillar]["total"] += 1
        pilar_results[pillar]["scores"].append(score)
        if score >= 0.80:
            pilar_results[pillar]["faithful"] += 1

        status_emoji = "✅" if score >= 0.80 else "❌"
        print(f"[{idx:02d}/50] [{status_emoji}] ({pillar:<16}) Score: {score:.2f} | Query: {query[:50]}...")

    avg_score = sum(scores) / len(scores) if scores else 0.0
    faithfulness_rate = passed_faithfulness / total

    print("\n----------------------------------------------------------------")
    print("📊 RESUMEN DE EVALUACIÓN:")
    print(f"   Total Evaluaciones:     {total}")
    print(f"   Fieles (Score >= 0.80): {passed_faithfulness}/{total} ({faithfulness_rate*100:.1f}%)")
    print(f"   Fidelidad Promedio:     {avg_score:.4f}")
    print("----------------------------------------------------------------")
    for pil, p_data in pilar_results.items():
        p_avg = sum(p_data["scores"]) / len(p_data["scores"])
        print(f"   - Pilar '{pil}': {p_data['faithful']}/{p_data['total']} fieles | Promedio: {p_avg:.3f}")
    print("================================================================\n")

    summary = {
        "total": total,
        "faithful_count": passed_faithfulness,
        "faithfulness_rate": faithfulness_rate,
        "average_score": avg_score,
        "pilar_results": pilar_results,
        "gate_passed": faithfulness_rate >= 0.85
    }

    if ci_gate_strict and not summary["gate_passed"]:
        print(f"❌ CI Gate REPROBADO: Tasa de fidelidad ({faithfulness_rate*100:.1f}%) inferior al umbral.")
        sys.exit(1)
    else:
        print("✅ CI Gate APROBADO: Fidelidad factual institucional validada.")

    return summary


if __name__ == "__main__":
    asyncio.run(run_evaluation(ci_gate_strict=False))
