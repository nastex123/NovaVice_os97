from typing import Dict, Any, Optional, Tuple
from src.core.memory import applicant_memory


ROOT_MENU_TEXT = """🎓 **¡Bienvenido a la Oficina de Admisiones de Nova Tech University!**
¿Qué área de información deseas consultar hoy? Digita el número de la opción o haz clic en los botones:

1️⃣ **Carreras, Mallas y Sílabos de Asignaturas** (Software, IA, Cyber, Sílabos CS-201, SE-302, AI-401...)
2️⃣ **Aranceles, Cuotas y Convenios Bancarios** (Precios, Plan A 10%, Plan B cuotas sin interés, tarjetas, USDC)
3️⃣ **Calendario, Requisitos y Movilidad Internacional** (Otoño 2026, Visas I-20, TU Munich, Tokyo Tech, Berkeley)
4️⃣ **Becas, Ayudas Financieras y Trabajo-Estudio** (Beca Turing 50%, Ada Lovelace 35%, empleo en campus $12/hr)
5️⃣ **Laboratorios Especializados e Investigación** (Clúster GPU NVIDIA H100, MakerSpace 3D, Cyber Range, XR Lab)
6️⃣ **Vida Estudiantil, Salud, Deportes y Campus** (Residencias $400-$650, Centro Médico gratis, Gym, Arena e-Sports)
7️⃣ **Empleabilidad, Startups y Alianzas Tech** (Incubadora Nova Ventures $100k, Microsoft, AWS, Google, Pasantías)
8️⃣ **Reglamentos, Titulación y Posgrados** (Maestrías M.Sc. IA/Cyber, Capstone, 100% Propiedad Intelectual)
9️⃣ **Hablar con un Asesor de Admisiones (Vía OpenCode)**

💡 *(Puedes escribir **0** en cualquier momento para regresar a este Menú Principal)*"""

SUBMENU_1_TEXT = """📚 **1. Carreras de Grado, Mallas Curriculares y Sílabos**
Digita el número de la opción que deseas consultar en detalle:

1.1 💻 Lic. en Ingeniería de Software & Sílabo Algoritmos (CS-201)
1.2 🤖 Lic. en Inteligencia Artificial Aplicada & Sílabo Deep Learning (AI-401)
1.3 🛡️ Lic. en Ciberseguridad & Sílabo Operaciones SOC (SEC-305)
1.4 ☁️ Cloud Computing, DevOps (CC-303) & Bases de Datos NoSQL / Vectoriales (DB-204)
1.5 🌐 Desarrollo Web Full Stack Moderno (WD-205: React, Next.js, TypeScript)
1.6 ⚛️ Introducción a la Computación Cuántica (QC-405: Qubits y Algoritmo de Shor)
1.7 🏛️ Modalidades de Estudio (100% Online Asíncrono, Híbrido y Presencial)
0. ↩️ Volver al Menú Principal"""

SUBMENU_2_TEXT = """💰 **2. Aranceles, Métodos de Pago y Financiación**
Digita el número de la opción que deseas revisar:

2.1 📊 Tabla Oficial de Aranceles por Semestre de cada Carrera ($3,000 - $3,200 USD)
2.2 💵 Plan A: Pago Contado por Semestre (10% de Descuento Inmediato)
2.3 💳 Plan B: Financiación Directa en 4 Cuotas Mensuales con 0% de Interés
2.4 🏦 Convenios Bancarios Oficiales (Chase, Santander, Davivienda, Stripe, Crypto USDC)
2.5 🔄 Política Oficial de Cancelación, Reembolsos y Devoluciones de Matrícula
0. ↩️ Volver al Menú Principal"""

SUBMENU_3_TEXT = """📅 **3. Calendario Académico, Admisión y Trámites Internacionales**
Digita el número de la opción que deseas revisar:

3.1 🍂 Convocatoria Principal Otoño 2026 (Cierre de postulaciones: 15 de julio de 2026)
3.2 🌸 Convocatoria de Primavera 2027 y Términos Intensivos
3.3 🛂 Guía de Trámite de Visa de Estudiante Formulario I-20 y Seguro Médico
3.4 🌍 Programas de Intercambio Internacional (TU Munich en Alemania, Tokyo Tech en Japón, UC Berkeley)
3.5 🔄 Transferencias Externas y Convalidación de Materias (Homologación hasta 50%)
0. ↩️ Volver al Menú Principal"""

SUBMENU_4_TEXT = """🏆 **4. Becas de Excelencia, Ayudas Económicas y Empleo en Campus**
Digita el número de la opción que deseas explorar:

4.1 🌟 Beca Alan Turing a la Excelencia Académica (50% de Cobertura en toda la carrera)
4.2 👩‍💻 Beca Ada Lovelace para Mujeres en Tecnología (35% de Descuento + Mentoría)
4.3 💼 Programa Trabajo-Estudio en Campus (Hasta 15 hrs/semana con pago de $12 USD/hora)
4.4 ⚽ Beca para Deportistas Destacados, e-Sports y Descuentos por Hermanos (15% - 20%)
0. ↩️ Volver al Menú Principal"""

SUBMENU_5_TEXT = """🔬 **5. Laboratorios Especializados e Investigación Científica**
Digita el número de la infraestructura que deseas conocer:

5.1 ⚡ Clúster de Supercómputo GPU NVIDIA H100 (64 GPUs Tensor Core, Slurm y Cuotas de Grado)
5.2 🖨️ MakerSpace, Impresión 3D de Resina / Carbono y Corte Láser CNC
5.3 🛡️ Cyber Range y Laboratorio de Red Team Aislado para Simulaciones de Ciberataque
5.4 🥽 XR Lab: Tecnologías Inmersivas, Apple Vision Pro, Meta Quest 3 y Manus Prime
5.5 🤖 Laboratorio de Robótica Móvil, Drones Autónomos y Bioinformática con AlphaFold 3
0. ↩️ Volver al Menú Principal"""

SUBMENU_6_TEXT = """🌿 **6. Vida Universitaria, Salud, Deportes y Residencias**
Digita el número del servicio de bienestar que deseas consultar:

6.1 🏠 Residencias Universitarias en Campus (Studio Tech $650/mes, Doble $400/mes y política de mascotas)
6.2 🏥 Centro Médico de Urgencias y Atención Psicológica Gratuita (8 sesiones/semestre)
6.3 🏋️ Gimnasio Universitario, CrossFit, Nutrición y Cafeterías Saludables ($90/mes)
6.4 🎮 Arena Gamer Oficial y Club de Deportes Electrónicos Nova eSports (Monitores 240Hz, RTX 4080)
6.5 🚌 Transporte Universitario Gratuito Nova Shuttle y Estaciones de Carga para Autos Eléctricos
0. ↩️ Volver al Menú Principal"""

SUBMENU_7_TEXT = """💼 **7. Empleabilidad, Startups y Alianzas Empresariales**
Digita el número de la iniciativa laboral que deseas consultar:

7.1 🚀 Incubadora Nova Ventures ($100,000 USD anuales en capital semilla para proyectos estudiantiles)
7.2 🤝 Alianzas Oficiales con Microsoft Learn, AWS Academy y Google Cloud (Vouchers gratis)
7.3 📈 Nova Career Hub (94% de inserción laboral), Tech Career Expo y Pasantías Remuneradas ($600-$1400/mes)
7.4 🌐 Red de Graduados Alumni Network con presencia en más de 25 países
0. ↩️ Volver al Menú Principal"""

SUBMENU_8_TEXT = """📜 **8. Reglamentos Académicos, Titulación y Posgrados**
Digita el número del tema normativo o posgrado que deseas explorar:

8.1 ⚖️ Código de Honor, Integridad Académica y Normativa Disciplinaria Anti-Plagio
8.2 🎓 Guía de Titulación Capstone y 100% de Propiedad Intelectual del Software para el Alumno
8.3 🤖 Maestría M.Sc. en Inteligencia Artificial Generativa y LLMs (18 meses, 100% Online)
8.4 🛡️ Maestría M.Sc. en Ciberseguridad Ofensiva y Cloud (Preparación OSCP / CISSP)
8.5 💼 Convalidación de Asignaturas por Trayectoria Laboral Demostrada (RPL)
0. ↩️ Volver al Menú Principal"""

LEAF_QUERY_MAP = {
    # Cluster 1: Programas y Sílabos
    "1.1": "¿Cuál es la duración, malla curricular y sílabo del curso de Algoritmos CS-201 en Ingeniería de Software?",
    "1.2": "¿Qué materias, laboratorios GPU y sílabo de Deep Learning AI-401 tiene la carrera de Inteligencia Artificial?",
    "1.3": "¿Cuáles son los pilares, certificaciones y sílabo del curso de Ciberseguridad Defensiva y SOC SEC-305?",
    "1.4": "¿Qué temas se estudian en Cloud Computing CC-303 y Bases de Datos NoSQL y Vectoriales DB-204?",
    "1.5": "¿En qué consiste el curso de Desarrollo Web Full Stack Moderno WD-205 con React y Next.js?",
    "1.6": "¿Cuáles son los contenidos del curso electivo de Introducción a la Computación Cuántica QC-405?",
    "1.7": "¿Qué modalidades de estudio existen, incluyendo 100% online asíncrona, híbrida y presencial?",

    # Cluster 2: Aranceles y Pagos
    "2.1": "¿Cuánto cuesta el semestre de cada carrera universitaria y cuál es el costo total estimado?",
    "2.2": "¿Cómo funciona el Plan A de pago único con 10% de descuento y cuál es el ahorro?",
    "2.3": "¿Cómo funciona el Plan B de financiamiento en 4 cuotas mensuales sin intereses?",
    "2.4": "¿Cuáles son los convenios bancarios autorizados y canales de pago como Chase, Santander, Stripe y USDC?",
    "2.5": "¿Cuál es la política oficial de reembolsos y devoluciones por semanas de retiro?",

    # Cluster 3: Calendario y Movilidad
    "3.1": "¿Cuáles son las fechas límite de postulación e inicio de clases para la convocatoria de Otoño 2026?",
    "3.2": "¿Cuáles son las fechas para Primavera 2027 y términos intensivos de verano?",
    "3.3": "¿Cuáles son los requisitos para la visa de estudiante I-20 y el seguro médico internacional obligatorio?",
    "3.4": "¿Cómo funcionan los programas de intercambio con TU Munich, Tokyo Tech con beca JASSO y Berkeley?",
    "3.5": "¿Cuáles son los requisitos para transferencias externas y convalidación de hasta el 50% de materias?",

    # Cluster 4: Becas
    "4.1": "¿Cuáles son los requisitos y porcentaje de cobertura de la Beca Alan Turing del 50%?",
    "4.2": "¿En qué consiste la Beca Ada Lovelace para Mujeres en Tecnología del 35% y mentorías?",
    "4.3": "¿Cómo funciona el Programa Trabajo-Estudio on-campus de $12 dólares por hora?",
    "4.4": "¿Qué becas deportivas existen y cómo aplican los descuentos familiares por hermanos?",

    # Cluster 5: Laboratorios
    "5.1": "¿Qué infraestructura tiene el Clúster de Supercómputo GPU NVIDIA H100 y cómo se asignan las horas de uso?",
    "5.2": "¿Qué maquinarias y normas de seguridad tiene el MakerSpace y laboratorio de impresión 3D?",
    "5.3": "¿Qué características tiene el Cyber Range y laboratorio de Red Team aislado para pruebas de ataque?",
    "5.4": "¿Qué equipamiento tiene el Laboratorio de Tecnologías Inmersivas y Realidad Mixta XR Lab?",
    "5.5": "¿Qué investigaciones se realizan en robótica autónoma, drones y bioinformática con AlphaFold 3?",

    # Cluster 6: Vida Estudiantil
    "6.1": "¿Cuáles son las tarifas de residencias universitarias, tipos de habitación y políticas sobre mascotas?",
    "6.2": "¿Qué servicios médicos gratuitos y sesiones de atención psicológica ofrece el centro de salud?",
    "6.3": "¿Qué equipamiento tiene el gimnasio universitario y cuánto cuesta el plan de comidas en las cafeterías?",
    "6.4": "¿Qué equipamiento tiene la Arena Gamer y el club de e-Sports de Nova Tech?",
    "6.5": "¿Cuáles son las rutas del transporte universitario gratuito Nova Shuttle y cargadores eléctricos?",

    # Cluster 7: Empleabilidad
    "7.1": "¿Cómo apoya la incubadora Nova Ventures con capital semilla de 100 mil dólares a startups estudiantiles?",
    "7.2": "¿Qué certificaciones gratuitas ofrecen las alianzas con Microsoft Learn, AWS Academy y Google Cloud?",
    "7.3": "¿Cómo funciona la bolsa de empleo Nova Career Hub y cuánto pagan las pasantías remuneradas?",
    "7.4": "¿Cómo está conformada la red de egresados Alumni Network y qué beneficios ofrece?",

    # Cluster 8: Reglamentos y Posgrados
    "8.1": "¿Qué establece el código de honor respecto a la integridad académica y sanciones por plagio?",
    "8.2": "¿Cómo es la rúbrica de defensa de tesis Capstone y de quién es la propiedad intelectual del software?",
    "8.3": "¿Cuáles son los requisitos y aranceles de la Maestría en IA Generativa y LLMs?",
    "8.4": "¿Qué duración y certificaciones tiene la Maestría en Ciberseguridad Ofensiva?",
    "8.5": "¿Cómo funciona la convalidación de materias por experiencia laboral demostrada RPL?"
}

SUBMENU_BUTTONS_MAP = {
    "root": [
        {"label": "1. Carreras y Sílabos", "value": "1"},
        {"label": "2. Aranceles y Pagos", "value": "2"},
        {"label": "3. Fechas y Visas", "value": "3"},
        {"label": "4. Becas y Empleo", "value": "4"},
        {"label": "5. Labs GPU H100", "value": "5"},
        {"label": "6. Residencias y Campus", "value": "6"},
        {"label": "7. Startups y Alianzas", "value": "7"},
        {"label": "8. Titulación y Posgrados", "value": "8"},
        {"label": "9. Asesor OpenCode", "value": "9"}
    ],
    "submenu_1": [
        {"label": "1.1 Ing. de Software (CS-201)", "value": "1.1"},
        {"label": "1.2 IA & Deep Learning (AI-401)", "value": "1.2"},
        {"label": "1.3 Ciberseguridad (SEC-305)", "value": "1.3"},
        {"label": "1.4 Cloud & DevOps (CC-303)", "value": "1.4"},
        {"label": "1.5 Full Stack (WD-205)", "value": "1.5"},
        {"label": "1.6 Cuántica (QC-405)", "value": "1.6"},
        {"label": "1.7 Modalidades de Estudio", "value": "1.7"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_2": [
        {"label": "2.1 Tabla de Aranceles", "value": "2.1"},
        {"label": "2.2 Plan A (10% Dcto)", "value": "2.2"},
        {"label": "2.3 Plan B (4 Cuotas)", "value": "2.3"},
        {"label": "2.4 Convenios Bancarios", "value": "2.4"},
        {"label": "2.5 Reembolsos", "value": "2.5"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_3": [
        {"label": "3.1 Convocatoria Otoño 2026", "value": "3.1"},
        {"label": "3.2 Primavera & Verano 2027", "value": "3.2"},
        {"label": "3.3 Visa I-20 & Seguro", "value": "3.3"},
        {"label": "3.4 Intercambios (TUM/Japón/Berkeley)", "value": "3.4"},
        {"label": "3.5 Transferencias & Convalidación", "value": "3.5"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_4": [
        {"label": "4.1 Beca Turing (50%)", "value": "4.1"},
        {"label": "4.2 Beca Ada Lovelace (35%)", "value": "4.2"},
        {"label": "4.3 Trabajo-Estudio ($12/hr)", "value": "4.3"},
        {"label": "4.4 Becas Atletas & Familia", "value": "4.4"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_5": [
        {"label": "5.1 Clúster GPU NVIDIA H100", "value": "5.1"},
        {"label": "5.2 MakerSpace & 3D", "value": "5.2"},
        {"label": "5.3 Cyber Range Red Team", "value": "5.3"},
        {"label": "5.4 XR Lab (Vision Pro)", "value": "5.4"},
        {"label": "5.5 Robótica & AlphaFold 3", "value": "5.5"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_6": [
        {"label": "6.1 Residencias & Mascotas", "value": "6.1"},
        {"label": "6.2 Centro Médico & Psicología", "value": "6.2"},
        {"label": "6.3 Gym, CrossFit & Cafeterías", "value": "6.3"},
        {"label": "6.4 Arena Gamer e-Sports", "value": "6.4"},
        {"label": "6.5 Nova Shuttle & Autos EV", "value": "6.5"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_7": [
        {"label": "7.1 Nova Ventures ($100k Seed)", "value": "7.1"},
        {"label": "7.2 Microsoft / AWS / Google", "value": "7.2"},
        {"label": "7.3 Career Hub & Pasantías", "value": "7.3"},
        {"label": "7.4 Alumni Network Global", "value": "7.4"},
        {"label": "0. Menú Principal", "value": "0"}
    ],
    "submenu_8": [
        {"label": "8.1 Código de Honor & Ética", "value": "8.1"},
        {"label": "8.2 Tesis & 100% Propiedad Intelectual", "value": "8.2"},
        {"label": "8.3 Maestría M.Sc. en IA Generativa", "value": "8.3"},
        {"label": "8.4 Maestría M.Sc. en Ciberseguridad", "value": "8.4"},
        {"label": "8.5 Convalidación Laboral RPL", "value": "8.5"},
        {"label": "0. Menú Principal", "value": "0"}
    ]
}


class GuidedNavigationEngine:
    # State machine for guided menu navigation in Spanish with clickable button actions.

    def __init__(self):
        pass

    def get_initial_greeting(self) -> str:
        return ROOT_MENU_TEXT

    def get_buttons_for_state(self, state: str) -> list:
        return SUBMENU_BUTTONS_MAP.get(state, SUBMENU_BUTTONS_MAP["root"])

    def process_input(self, raw_input: str, session_id: str) -> Tuple[Optional[str], Optional[str], bool, list]:
        # Returns (response_text, query_to_rag, is_navigation_handled, action_buttons)
        text = raw_input.strip().lower()
        session = applicant_memory.get_session(session_id)
        current_state = session.get("attributes", {}).get("menu_state", "root")

        # Global return to root menu
        if text in ("0", "menu", "inicio", "volver", "back", "home", "menu principal", "principal"):
            applicant_memory.update_attributes(session_id, "menu_state", "root")
            return ROOT_MENU_TEXT, None, True, self.get_buttons_for_state("root")

        # Switch to advisor mode (OpenCode powered)
        if text in ("9", "asesor", "hablar con asesor", "humano", "contacto", "asesoria"):
            applicant_memory.update_attributes(session_id, "menu_state", "advisor_mode")
            prompt = (
                "👨‍💼 **Conectando con el Asesor de Admisiones (Vía OpenCode)...**\n\n"
                "¡Hola! Estás en contacto directo con nuestro Asesor de Admisiones de Nova Tech University.\n"
                "Escribe cualquier consulta sobre tu perfil, carreras, laboratorios GPU H100, intercambios internacionales, convalidaciones, residencias o becas, "
                "y te responderé con atención personalizada.\n\n"
                "💡 *(Escribe **0** en cualquier momento para regresar al Menú Principal)*"
            )
            return prompt, None, True, [{"label": "0. Volver al Menú", "value": "0"}]

        # Direct shortcut for leaf options from any state
        if text in LEAF_QUERY_MAP:
            return None, LEAF_QUERY_MAP[text], False, [{"label": "0. Menú Principal", "value": "0"}, {"label": "9. Asesor OpenCode", "value": "9"}]

        # Handle Root Menu
        if current_state == "root":
            if text == "1":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_1")
                return SUBMENU_1_TEXT, None, True, self.get_buttons_for_state("submenu_1")
            elif text == "2":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_2")
                return SUBMENU_2_TEXT, None, True, self.get_buttons_for_state("submenu_2")
            elif text == "3":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_3")
                return SUBMENU_3_TEXT, None, True, self.get_buttons_for_state("submenu_3")
            elif text == "4":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_4")
                return SUBMENU_4_TEXT, None, True, self.get_buttons_for_state("submenu_4")
            elif text == "5":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_5")
                return SUBMENU_5_TEXT, None, True, self.get_buttons_for_state("submenu_5")
            elif text == "6":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_6")
                return SUBMENU_6_TEXT, None, True, self.get_buttons_for_state("submenu_6")
            elif text == "7":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_7")
                return SUBMENU_7_TEXT, None, True, self.get_buttons_for_state("submenu_7")
            elif text == "8":
                applicant_memory.update_attributes(session_id, "menu_state", "submenu_8")
                return SUBMENU_8_TEXT, None, True, self.get_buttons_for_state("submenu_8")
            else:
                # Direct natural language query at root level
                return None, raw_input, False, self.get_buttons_for_state("root")

        # Handle Submenu States
        if current_state.startswith("submenu_"):
            # Check for invalid single digit or unrecognized code
            sub_id = current_state.replace("submenu_", "")
            err_msg = (
                f"⚠️ La opción *\"{raw_input}\"* no forma parte de este submenú.\n\n"
                f"Por favor selecciona una de las opciones válidas (ej. {sub_id}.1, {sub_id}.2...) o digita **0** para regresar al Menú Principal."
            )
            return err_msg, None, True, self.get_buttons_for_state(current_state)

        return None, raw_input, False, self.get_buttons_for_state("root")


navigation_engine = GuidedNavigationEngine()
