from typing import Dict, Any, Optional, Tuple
from src.core.memory import applicant_memory


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

# Semantic Intent Map for Natural Language Normalization
INTENT_SYNONYMS = {
    "horario": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "horarios": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "horarios disponibles": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "horarios existentes": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "que horarios tienen": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "que horarios hay": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "a que hora dan clases": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "jornadas": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "turnos": "Cuales son los horarios, franjas y modalidades de estudio disponibles?",
    "madrugadores": "Que horarios y caracteristicas tiene la franja de madrugadores de 6:00 a 8:00 a.m.?",
    "after work": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
    "sabados": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
    "precio": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "precios": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "precios disponibles": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "precios vigentes": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "costo": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "costos": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "tarifas": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "cuanto vale": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "cuanto cuesta": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
    "planes de pago": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "cuotas": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
    "descuento": "Como funciona el 10% de descuento por pago de contado en modulos y paquetes de idiomas?",
    "descuentos": "Como funciona el 10% de descuento por pago de contado en modulos y paquetes de idiomas?",
    "inscripcion": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "inscripciones": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "matricula": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "matriculas": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "como entrar": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
    "test gratis": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "placement test": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "examen de clasificacion": "Como se realiza el examen de clasificacion (Placement Test) gratuito y como se agendan los resultados?",
    "sedes": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "donde quedan": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "ubicacion": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
    "direcciones": "Donde quedan ubicadas las sedes en Bogota, Medellin y Cali y como contactarlos?",
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
        Universal Omnicanal Navigation Resolver.
        Returns: (response_text, query_to_rag, is_navigation_handled, action_buttons)
        """
        text = raw_input.strip().lower()

        # 1. Global Reset to Root Menu
        if text in ("0", "menu", "inicio", "volver", "back", "home", "menu principal", "principal"):
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

        # 3. Universal Main Pillar Navigation (1, 2, 3, 4) - Works seamlessly from ANY state
        if text in ("1", "cursos", "programas", "idiomas"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_1")
            return SUBMENU_1_TEXT, None, True, self.get_buttons_for_state("submenu_1")
        elif text in ("2", "horario", "horarios", "modalidades"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_2")
            return SUBMENU_2_TEXT, None, True, self.get_buttons_for_state("submenu_2")
        elif text in ("3", "precio", "precios", "costos", "financiacion", "tarifas"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_3")
            return SUBMENU_3_TEXT, None, True, self.get_buttons_for_state("submenu_3")
        elif text in ("4", "admision", "admisiones", "sedes", "test", "matricula", "matriculas"):
            applicant_memory.update_attributes(session_id, "menu_state", "submenu_4")
            return SUBMENU_4_TEXT, None, True, self.get_buttons_for_state("submenu_4")

        # 4. Universal Leaf Shortcuts (1.1, 1.2 ... 4.6) - Works seamlessly from ANY state
        if text in LEAF_QUERY_MAP:
            # Set state corresponding to the pillar prefix
            prefix = text.split(".")[0]
            applicant_memory.update_attributes(session_id, "menu_state", f"submenu_{prefix}")
            return None, LEAF_QUERY_MAP[text], False, get_contextual_buttons(text)

        # 5. Natural Language Intent Normalization (Mapped to targeted queries)
        if text in INTENT_SYNONYMS:
            return None, INTENT_SYNONYMS[text], False, [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Admisiones & Sedes", "value": "4"},
                {"label": "0. Menú Principal", "value": "0"}
            ]

        # 6. Fallback: Any free-form natural language query is passed to RAG seamlessly without state errors
        return None, raw_input, False, [
            {"label": "1. Cursos & Certificaciones", "value": "1"},
            {"label": "2. Horarios & Modalidades", "value": "2"},
            {"label": "3. Precios & Financiación", "value": "3"},
            {"label": "4. Admisiones & Sedes", "value": "4"},
            {"label": "0. Menú Principal", "value": "0"}
        ]


navigation_engine = GuidedNavigationEngine()
