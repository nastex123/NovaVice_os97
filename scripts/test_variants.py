import sys
import asyncio
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'backend'))

from src.rag.engine import rag_engine
from src.rag.ingestion import ingestion_pipeline
from src.core.cache import query_cache

TEST_VARIANTS = [
    ('becas_descuentos', 'tienen becas para estudiar?'),
    ('becas_descuentos', 'como postular a una beca'),
    ('becas_descuentos', 'que becas ofrecen para ingles'),
    ('becas_descuentos', 'becas del 50 por ciento'),
    ('becas_descuentos', 'hay alguna ayuda economica o beca'),
    ('becas_descuentos', 'convenios con cajas de compensacion'),
    ('becas_descuentos', 'descuento por pago de contado'),
    ('becas_descuentos', 'descuento para familiares'),
    ('becas_descuentos', 'bono de matricula de 100 mil'),
    ('becas_descuentos', 'descuentos en matricula vigentes'),
    ('becas_descuentos', 'subsidio comfama o compensar'),
    ('becas_descuentos', 'scholarship options'),
    ('becas_descuentos', 'financial discounts'),
    ('becas_descuentos', 'rebajas en las cuotas'),
    ('becas_descuentos', 'plan referidos amigos'),
    ('becas_descuentos', 'aclaratoria de becas y convenios'),

    ('precios', 'cuanto cuesta el curso de ingles'),
    ('precios', 'cuales son las tarifas de los programas'),
    ('precios', 'precio por modulo en pesos colombianos'),
    ('precios', 'inversion total para el intensivo'),
    ('precios', 'cuanto vale el examen de clasificacion'),
    ('precios', 'planes de pago y financiacion a cuotas'),
    ('precios', 'cuotas mensuales sin intereses'),
    ('precios', 'metodos de pago tarjeta debito credito'),
    ('precios', 'cuanto cuesta frances para principiantes'),
    ('precios', 'costo de aleman b1'),
    ('precios', 'precios del curso semi-intensivo'),
    ('precios', 'valor de la matricula'),
    ('precios', 'que precio tienen los cursos sabatinos'),
    ('precios', 'fees and prices'),
    ('precios', 'cuanto es la cuota inicial'),
    ('precios', 'financiacion directa con la academia'),

    ('horarios', 'que horarios tienen disponibles'),
    ('horarios', 'horario de clases por la manana'),
    ('horarios', 'tienen clases en la noche para trabajadores'),
    ('horarios', 'cursos los fines de semana sabados'),
    ('horarios', 'clases los domingos intensivas'),
    ('horarios', 'modalidad 100% virtual sincronica'),
    ('horarios', 'tienen clases presenciales'),
    ('horarios', 'modalidad hibrida o hyflex'),
    ('horarios', 'que pasa si falto a una clase grabaciones'),
    ('horarios', 'politica de asistencia minima 80 por ciento'),
    ('horarios', 'horario de ingles intensivo diario'),
    ('horarios', 'clases 2 veces por semana'),
    ('horarios', 'schedules available'),
    ('horarios', 'clases en la manana presencial'),
    ('horarios', 'horario nocturno de 6:30 a 8:30'),
    ('horarios', 'franjas horarias de aleman'),

    ('cursos', 'que cursos de idiomas ofrecen'),
    ('cursos', 'curso de ingles general desde cero'),
    ('cursos', 'preparacion para examen ielts'),
    ('cursos', 'curso de toefl y cambridge'),
    ('cursos', 'cursos de frances alianza delf dalf'),
    ('cursos', 'aleman para visas de trabajo goethe'),
    ('cursos', 'curso de italiano intensivo'),
    ('cursos', 'portugues de brasil para negocios'),
    ('cursos', 'espanol para extranjeros dele'),
    ('cursos', 'clubes de conversacion y speaking'),
    ('cursos', 'niveles marco comun europeo a1 a c2'),
    ('cursos', 'ingles para ninos o solo adultos'),
    ('cursos', 'que idiomas dictan'),
    ('cursos', 'curso semi intensivo de ingles'),
    ('cursos', 'certificaciones internacionales homologables'),
    ('cursos', 'programas academicos ofertados'),

    ('sedes', 'donde estan ubicadas las sedes'),
    ('sedes', 'direccion de la sede bogota chico'),
    ('sedes', 'sede bogota chapinero telefono'),
    ('sedes', 'sede medellin el poblado direccion'),
    ('sedes', 'sede medellin laureles como llegar'),
    ('sedes', 'sede cali barrio granada'),
    ('sedes', 'como agendar el examen de clasificacion'),
    ('sedes', 'examen de nivelacion presencial o virtual'),
    ('sedes', 'como inscribirme a un curso'),
    ('sedes', 'requisitos de matricula para extranjeros'),
    ('sedes', 'proximo inicio de clases cuando empieza'),
    ('sedes', 'calendario academico de admisiones'),
    ('sedes', 'sucursales en colombia'),
    ('sedes', 'campus locations'),
    ('sedes', 'atencion en sede presencial'),
    ('sedes', 'congelacion de matricula por viaje o salud')
]

async def run_benchmark(filter_pillar: str = None, single_query: str = None):
    query_cache.invalidate()
    ingestion_pipeline.run()

    if single_query:
        print('=' * 75)
        print(f"PLAYGROUND CONSULTA INDIVIDUAL: '{single_query}'")
        print('=' * 75)
        t0 = time.time()
        res = await rag_engine.answer_query(single_query, session_id='playground_single')
        dt = (time.time() - t0) * 1000
        print(f"Estado: {res.get('status')}")
        print(f"Confianza: {res.get('confidence_score', 0.0):.3f}")
        print(f"Latencia: {dt:.1f} ms")
        print(f"Modo: {res.get('mode')}")
        print(f"Escalado: {res.get('escalated_to_human')}")
        print(f"Fuentes: {res.get('source_documents', [])}")
        print("\n--- RESPUESTA GENERADA ---")
        print(res.get('response', ''))
        print('=' * 75)
        return True

    variants = TEST_VARIANTS
    if filter_pillar:
        variants = [v for v in TEST_VARIANTS if filter_pillar.lower() in v[0].lower()]
        print(f"Filtrando {len(variants)} variantes para el pilar: '{filter_pillar}'")

    print('=' * 75)
    print(f'INICIANDO PLAYGROUND DE EVALUACIÓN: {len(variants)} VARIANTES (FASE E VERIFICACIÓN)')
    print('=' * 75)
    
    passed = 0
    failed = 0
    latencies = []
    
    for idx, (pillar, query) in enumerate(variants, 1):
        t0 = time.time()
        res = await rag_engine.answer_query(query, session_id=f'bench_{idx}')
        dt = (time.time() - t0) * 1000
        latencies.append(dt)
        
        status = res.get('status')
        conf = res.get('confidence_score', 0.0)
        escalated = res.get('escalated_to_human', False)
        sources = res.get('source_documents', [])
        top_src = sources[0] if sources else 'None'
        
        is_ok = (status == 'success') and (not escalated) and (conf >= 0.35)
        if is_ok:
            passed += 1
            mark = 'OK'
        else:
            failed += 1
            mark = 'FAIL'
            
        print(f'[{idx:02d}/{len(variants):02d}] {mark:^4} [{pillar:^16}] conf={conf:.3f} | {dt:5.1f}ms | {query[:36]:<36} -> {top_src[:25]}')
        
    avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
    print('=' * 75)
    print(f'RESULTADOS: {passed}/{len(variants)} APROBADOS ({passed/len(variants)*100:.1f}%) | {failed} FALLIDOS')
    print(f'LATENCIA PROMEDIO: {avg_lat:.1f}ms | ESCALAMIENTOS NO DESEADOS: {failed}')
    print('=' * 75)
    return failed == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Playground de Variantes y Evaluación RAG (E50)")
    parser.add_argument("--filter", "-f", type=str, help="Filtrar por pilar (cursos, horarios, precios, sedes, becas)")
    parser.add_argument("--query", "-q", type=str, help="Ejecutar una consulta libre individual en el playground")
    args = parser.parse_args()

    success = asyncio.run(run_benchmark(filter_pillar=args.filter, single_query=args.query))
    sys.exit(0 if success else 1)