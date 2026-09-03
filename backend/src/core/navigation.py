import unicodedata
import re
from typing import Dict, Any, Optional, Tuple
from src.core.memory import applicant_memory
from src.core.intent_router import semantic_intent_router


ROOT_MENU_TEXT = """### 🎓 ¡Bienvenido a Nova Idiomas Colombia!

Soy tu asistente virtual de admisiones, programas y servicios académicos. Puedes hacer clic en cualquiera de nuestras áreas o escribir tu pregunta con total libertad:

- **1. Cursos & Certificaciones:** Programas de Inglés, Francés, Alemán, Italiano, Portugués, MCER (A1-C2), IELTS, DELF, TOEFL y Cambridge.

- **2. Horarios & Modalidades:** Madrugadores (6-8am), Diurnos, Nocturno After Work (6:30-8:30pm), Sabatinos y Modalidad Virtual.

- **3. Precios & Financiación:** Tarifas 2026 en COP, 10% Descuento Contado, Plan 3 Cuotas 0% Interés, PSE/Nequi y Convenios.

- **4. Admisiones & Sedes:** Placement Test 100% Gratuito, Sedes Bogotá, Medellín y Cali, Matrículas y Speaking Clubs Ilimitados.

*(Haz clic en una de las opciones abajo o escribe tu consulta en el chat)*"""

SUBMENU_1_TEXT = """### 📚 1. Cursos, Idiomas y Certificaciones Internacionales
Selecciona el tema que deseas consultar en detalle:

- **1.1** Programas de Ingles General para Adultos (Niveles A1 a C2)

- **1.2** Ingles Intensivo Acelerado (40 horas mensuales)

- **1.3** Cursos de Frances, Aleman, Italiano y Portugues

- **1.4** Preparacion Oficial para Examenes IELTS, TOEFL iBT y Cambridge (FCE/CAE)

- **1.5** Certificaciones de Frances DELF/DALF y Aleman Goethe/TestDaF

- **1.6** Metodologia Flipped Classroom y Grupos Reducidos (maximo 12 alumnos)

*(Digita '0' para regresar al Menu Principal)*"""

SUBMENU_2_TEXT = """### ⏰ 2. Horarios Oficiales y Modalidades de Estudio
Selecciona la franja o modalidad de tu interes:

- **2.1** Franja Madrugadores (6:00 a.m. a 8:00 a.m. Lunes a Viernes)

- **2.2** Franjas Diurnas (Mananas 8-10am / 10-12m y Tardes 2-4pm / 4-6pm)

- **2.3** Franja Nocturna After Work (6:30 p.m. a 8:30 p.m. Lunes a Viernes)

- **2.4** Cursos Intensivos de Fin de Semana (Sabados 8am-1pm / 2-7pm o Domingos 8:30am-1:30pm)

- **2.5** Modalidad 100% Virtual Sincronica con Docente en Vivo y Grabaciones 24/7

- **2.6** Aulas Hibridas HyFlex con Camaras Inteligentes 360 grados

*(Digita '0' para regresar al Menu Principal)*"""

SUBMENU_3_TEXT = """### 💰 3. Precios Oficiales en COP, Financiacion y Descuentos
Selecciona la opcion que deseas conocer:

- **3.1** Tarifas Oficiales por Modulo Regular ($650.000 COP) e Intensivo ($720.000 COP)

- **3.2** Plan Pago de Contado con 10% de Descuento Inmediato

- **3.3** Financiacion Directa en 3 Cuotas sin Interes (40% matricula, 30% sem 4, 30% sem 7)

- **3.4** Convenios con Cajas de Compensacion (Compensar, Colsubsidio, Cafam, Comfama - 15% Dcto)

- **3.5** Medios de Pago Digitales Autorizados (PSE, Nequi, Daviplata, Tarjetas y Bancolombia)

*(Digita '0' para regresar al Menu Principal)*"""

SUBMENU_4_TEXT = """### 📝 4. Admisiones, Placement Test Gratuito y Sedes en Colombia
Selecciona el tema de consulta:

- **4.1** Examen de Clasificacion (Placement Test) 100% Gratuito (Escrito + Oral)

- **4.2** Paso a Paso para Matricularse Online o en Counter de Sede

- **4.3** Sedes en Bogota D.C. (Chico Norte Cra 15 # 98-42 y Chapinero Calle 63 # 9-28)

- **4.4** Sedes en Medellin (El Poblado One Plaza y Laureles Av. Nutibara)

- **4.5** Sede en Cali (Barrio Granada Av. 9N # 14N-35)

- **4.6** Politicas de Asistencia (80%), Congelamiento de Curso (hasta 90 dias) y Reembolsos

*(Digita '0' para regresar al Menu Principal)*"""

LEAF_QUERY_MAP = {
    # Pillar 1: Courses and Certifications
    "1.1": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "1.2": "En que consiste el curso de ingles intensivo acelerado de 40 horas mensuales y cuanto se avanza?",
    "1.3": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "1.4": "Como es el curso preparatorio para examenes internacionales IELTS, TOEFL iBT y Cambridge FCE/CAE?",
    "1.5": "Que certificaciones oficiales de frances DELF/DALF y aleman Goethe/TestDaF preparan?",
    "1.6": "En que consiste la metodologia comunicativa Flipped Classroom y el tamano maximo de grupos?",

    # Pillar 2: Schedules and Modalities
    "2.1": "Que horarios y caracteristicas tiene la franja de madrugadores de 6:00 a 8:00 a.m.?",
    "2.2": "Cuales son los horarios de las franjas diurnas de mananas y tardes de lunes a viernes?",
    "2.3": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "2.4": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    "2.5": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "2.6": "En que consisten las aulas hibridas HyFlex con camaras inteligentes 360 grados?",

    # Pillar 3: Tuition Fees and Financing
    "3.1": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "3.2": "Como funciona el 10% de descuento por pago de contado en modulos y paquetes de idiomas?",
    "3.3": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "3.4": "Que convenios y descuentos del 15% tienen con Cajas de Compensacion como Compensar, Colsubsidio y Cafam?",
    "3.5": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",

    # Pillar 4: Admissions and Campuses
    "4.1": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "4.2": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "4.3": "Donde quedan ubicadas las sedes en Bogota D.C. (Chico Norte y Chapinero) y que instalaciones tienen?",
    "4.4": "Donde quedan las sedes en Medellin (El Poblado One Plaza y Laureles) y como llegar?",
    "4.5": "Donde queda la sede de Cali en el Barrio Granada y que horarios de atencion maneja?",
    "4.6": "Cuales son las politicas de asistencia minima del 80%, congelamiento hasta 90 dias y devoluciones?"
}

SUBMENU_BUTTONS_MAP = {
    "root": [
        {"label": "1. Cursos & Certificaciones", "value": "1"},
        {"label": "2. Horarios & Modalidades", "value": "2"},
        {"label": "3. Precios & Financiación", "value": "3"},
        {"label": "4. Admisiones & Sedes", "value": "4"}
    ],
    "submenu_1": [
        {"label": "1.1 Inglés (A1 a C2)", "value": "1.1"},
        {"label": "1.2 Intensivo 40h/mes", "value": "1.2"},
        {"label": "1.3 Otros Idiomas", "value": "1.3"},
        {"label": "1.4 IELTS / TOEFL / Cambridge", "value": "1.4"},
        {"label": "1.5 DELF / Goethe", "value": "1.5"},
        {"label": "1.6 Metodología Flipped", "value": "1.6"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_2": [
        {"label": "2.1 Madrugadores (6-8am)", "value": "2.1"},
        {"label": "2.2 Diurnos (Mañanas/Tardes)", "value": "2.2"},
        {"label": "2.3 Nocturno (6:30-8:30pm)", "value": "2.3"},
        {"label": "2.4 Sabatinos y Domingos", "value": "2.4"},
        {"label": "2.5 Virtual Sincrónico", "value": "2.5"},
        {"label": "2.6 Aulas HyFlex 360", "value": "2.6"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_3": [
        {"label": "3.1 Tarifas Oficiales COP", "value": "3.1"},
        {"label": "3.2 Plan Contado (10% Dcto)", "value": "3.2"},
        {"label": "3.3 Plan 3 Cuotas 0%", "value": "3.3"},
        {"label": "3.4 Cajas Compensación", "value": "3.4"},
        {"label": "3.5 PSE, Nequi y Tarjetas", "value": "3.5"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_4": [
        {"label": "4.1 Placement Test Gratis", "value": "4.1"},
        {"label": "4.2 Proceso de Matrícula", "value": "4.2"},
        {"label": "4.3 Sedes Bogotá", "value": "4.3"},
        {"label": "4.4 Sedes Medellín", "value": "4.4"},
        {"label": "4.5 Sede Cali", "value": "4.5"},
        {"label": "4.6 Asistencia & Congelar", "value": "4.6"},
        {"label": "0. Menú Principal", "value": "0"}
    ]
}

def _normalize(text: str) -> str:
    """Unicode NFD + lower + strip + collapse spaces + remove punctuation except needed."""
    # Lower and strip
    t = text.strip().lower()
    # NFD accent removal
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    # Replace punctuation with spaces, keep alphanumeric and spaces
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    # Collapse multiple spaces
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            ins = prev[j] + 1
            delete = cur[j - 1] + 1
            sub = prev[j - 1] + (ca != cb)
            cur.append(min(ins, delete, sub))
        prev = cur
    return prev[-1]


# Common typos → correction (normalized)
_TYPO_MAP = {
    "orario": "horario",
    "horaroi": "horario",
    "horrai": "horario",
    "orarios": "horarios",
    "presio": "precio",
    "presios": "precios",
    "cuorsos": "cursos",
    "curzo": "curso",
    "curzos": "cursos",
    "beca": "beca",  # placeholder for typo grouping
    "veca": "beca",
    "vecas": "becas",
    "modalida": "modalidad",
    "modaliad": "modalidad",
    "sedde": "sede",
    "sedes": "sedes",
    "financiacion": "financiacion",  # without accent after normalize
    "financiamiento": "financiacion",
    "virtuali": "virtual",
    "presensial": "presencial",
    "hyflexx": "hyflex",
    "hy fex": "hyflex",
    "seede": "sede",
}


def _correct_typos(normalized: str) -> str:
    toks = normalized.split()
    corrected = []
    # Whitelist of valid tokens that should never be auto-corrected via Levenshtein
    valid_tokens = {
        "horario", "horarios", "precio", "precios", "curso", "cursos", "beca", "becas",
        "modalidad", "modalidades", "virtual", "presencial", "hibrida", "hibrido", "hyflex",
        "sede", "sedes", "sucursal", "sucursales", "descuento", "descuentos", "financiacion",
        "cuota", "cuotas", "tarifa", "tarifas", "costo", "costos", "valor", "valores",
        "pago", "pagos", "becas", "ayudas", "subsidio", "subsidios", "scholarship",
        "franja", "franjas", "jornadas", "turnos", "madrugadores", "sabados", "domingos",
        "grabaciones", "online", "linea", "linea", "sincronico", "sincronica"
    }
    for tok in toks:
        if tok in _TYPO_MAP:
            corrected.append(_TYPO_MAP[tok])
            continue
        if tok in valid_tokens:
            corrected.append(tok)
            continue
        # Levenshtein <=2 only for unknown tokens
        best = None
        best_dist = 3
        for cand in ("horario", "horarios", "precio", "precios", "curso", "cursos", "beca", "becas", "modalidad", "virtual", "presencial", "hyflex", "sede", "sedes", "descuento", "financiacion"):
            d = _levenshtein(tok, cand)
            if d < best_dist and d <= 2 and len(tok) >= 4:
                best_dist = d
                best = cand
        corrected.append(best if best else tok)
    return " ".join(corrected)


def _find_intent_by_embedding(normalized: str, threshold: float = 0.82) -> Optional[str]:
    """Fallback semantic intent via dense cosine vs canonical queries. Returns canonical if hits."""
    try:
        from src.rag.vector_store import vector_store
        q_emb = vector_store.embed_query(normalized)
        if not q_emb or sum(x * x for x in q_emb) == 0:
            return None
        best_canonical = None
        best_sim = 0.0
        # Cache canonical embeddings (values, not keys) for better semantic match
        if not hasattr(_find_intent_by_embedding, "_intent_emb_cache"):
            _find_intent_by_embedding._intent_emb_cache = {}  # type: ignore
            # Use unique canonical values to reduce cache size
            uniq_canon = set(INTENT_SYNONYMS.values())
            for canon in uniq_canon:
                emb = vector_store.embed_query(canon.lower())
                _find_intent_by_embedding._intent_emb_cache[canon] = emb  # type: ignore
        cache = _find_intent_by_embedding._intent_emb_cache  # type: ignore
        for canon, emb in cache.items():
            dot = sum(a * b for a, b in zip(q_emb, emb))
            norm_a = sum(a * a for a in q_emb) ** 0.5
            norm_b = sum(b * b for b in emb) ** 0.5
            if norm_a == 0 or norm_b == 0:
                continue
            sim = dot / (norm_a * norm_b)
            if sim > best_sim:
                best_sim = sim
                best_canonical = canon
        if best_canonical and best_sim >= threshold:
            return best_canonical
    except Exception:
        pass
    return None


# Semantic Intent Map for Natural Language Normalization (normalized keys, no accents)
INTENT_SYNONYMS = {
    # --- Horarios & Modalidades ---
    "horario": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "horarios": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "horarios disponibles": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "horarios existentes": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "que horarios tienen": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "que horarios hay": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "a que hora dan clases": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "jornadas": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "turnos": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "cuando abren": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "a que hora abren": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "franja": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "franjas": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "en la manana": "Cuales son los horarios de las franjas diurnas de mananas y tardes de lunes a viernes?",
    "en la tarde": "Cuales son los horarios de las franjas diurnas de mananas y tardes de lunes a viernes?",
    "en la noche": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "madrugadores": "Que horarios y caracteristicas tiene la franja de madrugadores de 6:00 a 8:00 a.m.?",
    "after work": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "nocturno": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "nocturna": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "nocturnos": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "nocturnas": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "horario nocturno": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "horarios nocturnos": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "horaios nocturnos": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "horario de noche": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "horarios de noche": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "clases nocturnas": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "clases en la noche": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "estudiar de noche": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "sabados": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    "sabatino": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    "domingos": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    "fin de semana": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    "fines de semana": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    # Modalidades
    "modalidad": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "modalidades": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "modalidades disponibles": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "que modalidades hay": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "que modalidades tienen": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "virtual": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "presencial": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "hibrida": "En que consisten las aulas hibridas HyFlex con camaras inteligentes 360 grados?",
    "hibrido": "En que consisten las aulas hibridas HyFlex con camaras inteligentes 360 grados?",
    "online": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "en linea": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "clases virtuales": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "clases presenciales": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "grabaciones": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "hyflex": "En que consisten las aulas hibridas HyFlex con camaras inteligentes 360 grados?",
    "sincronico": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    "sincronica": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
    # --- Precios & Financiación ---
    "precio": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "precios": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "precios disponibles": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "precios vigentes": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "costo": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "costos": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "tarifas": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "cuanto vale": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "cuanto cuesta": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "cuanto es": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "cuanto sale": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "valor": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "valores": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "pago": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "pagos": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "financiacion": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "financiacion directa": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "planes de pago": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "plan de pago": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "cuotas": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "cuota": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "descuento": "Como funciona el 10% de descuento por pago de contado en modulos y paquetes de idiomas?",
    "descuentos": "Como funciona el 10% de descuento por pago de contado en modulos y paquetes de idiomas?",
    "medios de pago": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "medios de pagos": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "que medios de pagos hay": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "que medios de pago hay": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "formas de pago": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "metodos de pago": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "como pagar": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "como puedo pagar": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "pse": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "nequi": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "daviplata": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    "tarjetas": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
    # --- Becas → Descuentos (ADR-008) — short canonical for BM25 high IDF ---
    "beca": "becas disponibles",
    "becas": "becas disponibles",
    "becas disponibles": "becas disponibles",
    "hay becas": "becas disponibles",
    "existen becas": "becas disponibles",
    "ayudas": "becas disponibles",
    "ayuda financiera": "becas disponibles",
    "subsidio": "becas disponibles",
    "subsidios": "becas disponibles",
    "scholarship": "becas disponibles",
    "scholarships": "becas disponibles",
    "apoyo financiero": "becas disponibles",
    # --- Cursos & Certificaciones ---
    "curso": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "cursos": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "que cursos hay": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "cursos disponibles": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "que cursos tienen": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "que cursos ofrecen": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "programas": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "que programas hay": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "idiomas": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "que idiomas hay": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "que idiomas ensenan": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "niveles": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "nivel": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "mcer": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "a1": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "b1": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "ingles": "Cuales son los niveles del MCER (A1 a C2), duracion y enfoque del programa de ingles general?",
    "frances": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "aleman": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "italiano": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    "portugues": "Que programas ofrecen en frances, aleman, italiano, portugues y espanol para extranjeros?",
    # --- Matrícula & Sedes ---
    "inscripcion": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "inscripciones": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "matricula": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "matriculas": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "como entrar": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "proximo inicio": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "cuando empieza": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "cuando inicia": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "test gratis": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "placement test": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "examen de clasificacion": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "sedes": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "sede": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "sucursal": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "sucursales": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "donde quedan": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "donde estan": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "ubicacion": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "direcciones": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "direccion": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "bogota": "Donde quedan ubicadas las sedes en Bogota D.C. (Chico Norte y Chapinero) y que instalaciones tienen?",
    "medellin": "Donde quedan las sedes en Medellin (El Poblado One Plaza y Laureles) y como llegar?",
    "cali": "Donde queda la sede de Cali en el Barrio Granada y que horarios de atencion maneja?",
    "ielts": "Como es el curso preparatorio para examenes internacionales IELTS, TOEFL iBT y Cambridge FCE/CAE?",
    "toefl": "Como es el curso preparatorio para examenes internacionales IELTS, TOEFL iBT y Cambridge FCE/CAE?",
    "cambridge": "Como es el curso preparatorio para examenes internacionales IELTS, TOEFL iBT y Cambridge FCE/CAE?",
    "delf": "Que certificaciones oficiales de frances DELF/DALF y aleman Goethe/TestDaF preparan?",
    "goethe": "Que certificaciones oficiales de frances DELF/DALF y aleman Goethe/TestDaF preparan?",
    "congelar": "Cuales son las politicas de asistencia minima del 80%, congelamiento hasta 90 dias y devoluciones?",
    "reembolso": "Cuales son las politicas de asistencia minima del 80%, congelamiento hasta 90 dias y devoluciones?",
    "asistencia": "Cuales son las politicas de asistencia minima del 80%, congelamiento hasta 90 dias y devoluciones?",
    "speaking clubs": "Como funcionan los clubes de conversacion semanales y tutorias gratuitas?",
    "clubes": "Como funcionan los clubes de conversacion semanales y tutorias gratuitas?"
}


def get_contextual_buttons(key: str) -> list:
    """Returns smart contextual sibling and cross-pillar buttons for leaf selections."""
    if key.startswith("1."):
        if key == "1.1":
            return [
                {"label": "1.2 Intensivo 40h/mes", "value": "1.2"},
                {"label": "1.4 IELTS / TOEFL / Cambridge", "value": "1.4"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        elif key == "1.2":
            return [
                {"label": "1.1 Inglés General (A1-C2)", "value": "1.1"},
                {"label": "2.1 Madrugadores (6-8am)", "value": "2.1"},
                {"label": "3.1 Tarifas Oficiales COP", "value": "3.1"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        elif key == "1.3":
            return [
                {"label": "1.5 DELF / Goethe", "value": "1.5"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        else:
            return [
                {"label": "1.1 Inglés General", "value": "1.1"},
                {"label": "1.2 Intensivo", "value": "1.2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Placement Test Gratis", "value": "4.1"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
    elif key.startswith("2."):
        if key == "2.1":
            return [
                {"label": "2.3 Nocturno (6:30-8:30pm)", "value": "2.3"},
                {"label": "2.5 Virtual Sincrónico", "value": "2.5"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        elif key == "2.3":
            return [
                {"label": "2.4 Sabatinos y Domingos", "value": "2.4"},
                {"label": "2.5 Virtual Sincrónico", "value": "2.5"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        else:
            return [
                {"label": "2.1 Madrugadores (6-8am)", "value": "2.1"},
                {"label": "2.3 Nocturno After Work", "value": "2.3"},
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
    elif key.startswith("3."):
        return [
            {"label": "3.1 Tarifas Oficiales COP", "value": "3.1"},
            {"label": "3.2 Plan Contado (10% Dcto)", "value": "3.2"},
            {"label": "3.3 Plan 3 Cuotas 0%", "value": "3.3"},
            {"label": "4. Placement Test Gratis", "value": "4.1"},
            {"label": "0. Menú Principal", "value": "0"}
        ]
    elif key.startswith("4."):
        if key == "4.1":
            return [
                {"label": "4.2 Proceso de Matrícula", "value": "4.2"},
                {"label": "4.3 Sedes Bogotá", "value": "4.3"},
                {"label": "4.4 Sedes Medellín", "value": "4.4"},
                {"label": "4.5 Sede Cali", "value": "4.5"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        elif key in ("4.3", "4.4", "4.5"):
            return [
                {"label": "4.1 Placement Test Gratis", "value": "4.1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        elif key == "4.6":
            return [
                {"label": "4.1 Placement Test Gratis", "value": "4.1"},
                {"label": "4.3 Sedes Bogotá", "value": "4.3"},
                {"label": "9. Hablar con un Asesor", "value": "9"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        else:
            return [
                {"label": "4.1 Placement Test Gratis", "value": "4.1"},
                {"label": "4.3 Sedes Bogotá", "value": "4.3"},
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
    return [
        {"label": "1. Cursos & Certificaciones", "value": "1"},
        {"label": "2. Horarios & Modalidades", "value": "2"},
        {"label": "3. Precios & Financiación", "value": "3"},
        {"label": "4. Admisiones & Sedes", "value": "4"},
        {"label": "0. Menú Principal", "value": "0"}
    ]


class GuidedNavigationEngine:
    """State machine for universal omnicanal menu navigation without deadlocks."""

    def __init__(self):
        pass

    def get_initial_greeting(self) -> str:
        return ROOT_MENU_TEXT

    def get_buttons_for_state(self, state: str) -> list:
        return SUBMENU_BUTTONS_MAP.get(state, SUBMENU_BUTTONS_MAP["root"])

    def process_input(self, raw_input: str, session_id: str) -> Tuple[Optional[str], Optional[str], bool, list]:
        """
        Universal Omnicanal Navigation Resolver with NFD, typos, embedding fallback and multi-intent.
        Returns: (response_text, query_to_rag, is_navigation_handled, action_buttons)
        """
        # Preserve raw leaf handling before NFD (dots)
        raw_lower = raw_input.strip().lower()
        # Normalized for intent (NFD accent strip + punctuation collapse)
        norm = _normalize(raw_input)
        corrected = _correct_typos(norm)

        # Use corrected for navigation but keep raw_lower for leaf exact "1.1"
        text = corrected  # for all normalized checks

        # 1. Global Reset to Root Menu (normalized - C26 soft reset)
        if text in (
            "0", "menu", "inicio", "volver", "back", "home", "menu principal",
            "principal", "limpiar", "reiniciar", "volver al inicio", "reset",
            "empezar de nuevo", "comenzar de nuevo", "cancelar", "borrar", "salir"
        ):
            applicant_memory.update_attributes(session_id, "menu_state", "root")
            return ROOT_MENU_TEXT, None, True, self.get_buttons_for_state("root")

        # 2. Global Advisor Invocation (OpenCode)
        advisor_keywords = ("asesor", "humano", "agente", "operador", "persona real", "coordinador", "asesoria personalizada")
        if text == "9" or any(kw in text for kw in advisor_keywords):
            applicant_memory.update_attributes(session_id, "menu_state", "advisor_mode")
            prompt = (
                "**Conectando con el Asesor de Admisiones de Nova Idiomas (OpenCode)...**\n\n"
                "Estás en comunicación con el Asesor Académico.\n"
                "Formula tu consulta sobre cualquier caso especial, convenio empresarial o programa de idiomas y te ayudaremos con gusto.\n\n"
                "*(Escribe '0' para regresar al Menú Principal)*"
            )
            return prompt, None, True, [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]

        # 3. Universal Main Pillar Navigation - expanded tolerant sets
        if text in ("1", "cursos", "curso", "programas", "programa", "idiomas", "idioma", "niveles", "nivel", "mcer"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_1")
            return SUBMENU_1_TEXT, None, True, self.get_buttons_for_state("submenu_1")
        elif text in ("2", "horario", "horarios", "modalidades", "modalidad", "franja", "franjas", "jornadas", "turnos"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_2")
            return SUBMENU_2_TEXT, None, True, self.get_buttons_for_state("submenu_2")
        elif text in ("3", "precio", "precios", "costo", "costos", "tarifas", "tarifa", "financiacion", "financiacion directa", "cuota", "cuotas", "descuento", "descuentos", "valor", "valores", "pago", "pagos"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_3")
            return SUBMENU_3_TEXT, None, True, self.get_buttons_for_state("submenu_3")
        elif text in ("4", "admision", "admisiones", "sedes", "sede", "sucursal", "sucursales", "test", "matricula", "matriculas", "inscripcion", "ubicacion", "direccion", "direcciones"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_4")
            return SUBMENU_4_TEXT, None, True, self.get_buttons_for_state("submenu_4")

        # 4. Universal Leaf Shortcuts (1.1, 1.2 ... 4.6) - keep raw_lower exact, also handle normalized "1 1" -> "1.1"
        leaf_key = raw_lower
        # also tolerate "1,1" "1 1" "1-1" via regex
        m = re.match(r"^\s*([1-4])\s*[.,\-\s]\s*([1-6])\s*$", raw_lower)
        if m:
            leaf_key = f"{m.group(1)}.{m.group(2)}"
        if leaf_key in LEAF_QUERY_MAP:
            prefix = leaf_key.split(".")[0]
            applicant_memory.update_attributes(session_id, "menu_state", f"submenu_{prefix}")
            return None, LEAF_QUERY_MAP[leaf_key], False, get_contextual_buttons(leaf_key)
        # Also try normalized leaf without dot
        if text in LEAF_QUERY_MAP:
            prefix = text.split(".")[0]
            applicant_memory.update_attributes(session_id, "menu_state", f"submenu_{prefix}")
            return None, LEAF_QUERY_MAP[text], False, get_contextual_buttons(text)

        # 5. Natural Language Intent Normalization (exact, typo-corrected, then embedding)
        # A3: expanded 80+ synonyms, A1 NFD, A5 typos already in corrected
        if text in INTENT_SYNONYMS:
            return None, INTENT_SYNONYMS[text], False, [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Admisiones & Sedes", "value": "4"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
        # Also try raw_lower exact for cases where NFD not needed
        if raw_lower in INTENT_SYNONYMS:
            return None, INTENT_SYNONYMS[raw_lower], False, [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Admisiones & Sedes", "value": "4"},
                {"label": "0. Menú Principal", "value": "0"}
            ]

        # 6. Deep Vectorized Intent Routing (Macro + Micro Prototypes)
        intent_match = semantic_intent_router.classify(raw_input)
        if intent_match.canonical_query and intent_match.micro_score >= 0.20:
            return None, intent_match.canonical_query, False, intent_match.action_buttons

        # A6: Embedding fallback cosine >0.82 for short/typo queries
        if len(text.split()) <= 6:
            emb_match = _find_intent_by_embedding(text, threshold=0.82)
            if emb_match:
                return None, emb_match, False, [
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "4. Admisiones & Sedes", "value": "4"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]

        # A8: Multi-intent split - if " y " / "," handle as RAG raw (hybrid will fuse both intents)
        if " y " in text or " and " in text or "," in text:
            # Let RAG handle multi-topic without forcing single intent
            return None, raw_input, False, [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Admisiones & Sedes", "value": "4"},
                {"label": "0. Menú Principal", "value": "0"}
            ]

        # 7. Fallback: Any free-form natural language query is passed to RAG seamlessly without state errors
        return None, raw_input, False, intent_match.action_buttons


navigation_engine = GuidedNavigationEngine()
