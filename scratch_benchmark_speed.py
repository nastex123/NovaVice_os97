import sys
import io
import asyncio
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from src.core.opencode_client import opencode_advisor

async def run_benchmark():
    test_queries = [
        "¿Qué horarios de atención tienen?",
        "¿Tienen residencias o dormitorios en el campus?",
        "¿Cómo funciona la homologación de materias de otra universidad?",
        "¿Cuáles son los requisitos para la Beca Turing del 50%?"
    ]

    print("=" * 60)
    print("🚀 BENCHMARK DE RENDIMIENTO Y VELOCIDAD DE OPENCODE")
    print("=" * 60)

    total_time = 0
    for idx, query in enumerate(test_queries, 1):
        t0 = time.time()
        res = await opencode_advisor.query_advisor(query, f"bench_sess_{idx}")
        elapsed = time.time() - t0
        total_time += elapsed
        snippet = res.get("text", "").replace("\n", " ")[:120]

        print(f"\n[Test {idx}/4] Consulta: {query}")
        print(f"⏱️ Tiempo de respuesta: {elapsed:.2f} segundos ({res.get('latency_ms', 0)} ms)")
        print(f"📦 Origen: {res.get('source', 'unknown')}")
        print(f"💬 Extracto: {snippet}...")

    avg = total_time / len(test_queries)
    print("\n" + "=" * 60)
    print(f"✅ Promedio de latencia por consulta: {avg:.2f} segundos")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
