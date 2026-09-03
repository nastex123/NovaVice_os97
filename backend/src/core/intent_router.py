import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

from src.rag.vector_store import vector_store


@dataclass
class IntentMatch:
    top_macro_pillar: str
    macro_score: float
    top_micro_intent: Optional[str] = None
    micro_score: float = 0.0
    canonical_query: Optional[str] = None
    target_cluster: Optional[str] = None
    is_multi_intent: bool = False
    secondary_micro_intent: Optional[str] = None
    secondary_score: float = 0.0
    action_buttons: List[Dict[str, str]] = field(default_factory=list)


# 1. Macro-Pillars Semantic Prototypes (Top-level domains)
MACRO_PILLARS_PROTOTYPES: Dict[str, str] = {
    "cursos_idiomas_niveles": (
        "programas de ingles frances aleman italiano portugues espanol niveles mcer a1 a2 b1 b2 c1 c2 "
        "cursos intensivos regulares preparacion examenes internacionales ielts toefl cambridge delf dalf goethe "
        "certificaciones homologables clubes de conversacion speaking clubs"
    ),
    "horarios_modalidades_franjas": (
        "horarios de clases franjas turnos jornadas manana tarde noche madrugadores 6 a 8 am after work 6:30 a 8:30 pm "
        "cursos intensivos de fin de semana sabatinos dominicales sabados y domingos modalidades 100% virtual sincronico "
        "en vivo clases remotas grabaciones 24/7 presencial sedes fisicas hibrida flex aulas hyflex 360"
    ),
    "precios_tarifas_financiacion": (
        "precios tarifas costos valores mensualidad modulo regular 650000 COP intensivo 720000 COP pesos colombianos "
        "inversion total medios de pago autorizados pasarelas digitales PSE nequi daviplata tarjetas de credito y debito "
        "efecty corresponsales bancarios bancolombia financiacion directa plan 3 cuotas 40% 30% 30% sin intereses "
        "transferencias bancarias consignaciones consignar transferir plata dinero cuentas corrientes de ahorros bancolombia davivienda datofonos datofono datafono efectivo reciben"
    ),
    "admisiones_sedes_matricula": (
        "admisiones sedes direcciones ubicacion telefonos bogota chico calle 100 chapinero medellin el poblado laureles "
        "cali barrio granada proceso de matricula inscripcion requisitos extranjeros placement test examen de clasificacion "
        "prueba nivelacion gratis agendar cita sucursales donde quedan"
    ),
    "becas_descuentos_convenios": (
        "becas auxilios educativos ayuda financiera subsidios aclaratoria oficial no becas propias merit based promedio "
        "descuentos y convenios vigentes convenio cajas de compensacion familiar 15% compensar colsubsidio cafam comfama comfandi "
        "descuento pago de contado 10% descuento familiar 15% segundo familiar matricula cero bono 100000 rebaja de una contado"
    ),
}

# 2. Micro-Intents Semantic Prototypes (18 Targeted specific intents)
MICRO_INTENTS_PROTOTYPES: Dict[str, Dict[str, Any]] = {
    # --- Precios, Medios de Pago & Financiación ---
    "medios_de_pago": {
        "text": (
            "medios de pago autorizados formas de pago como pagar opciones de pago pasarelas digitales PSE pagos seguros en linea "
            "billeteras virtuales nequi daviplata codigo qr tarjetas de credito debito visa mastercard amex diners corresponsales "
            "bancarios bancolombia davivienda puntos efecty counter datofonos datofono datafono pago en efectivo transferencias bancarias "
            "consignaciones consignar transferir plata dinero cuentas bancarias bancolombia davivienda consignar transferir como pagar reciben recibir recepcion"
        ),
        "canonical": "Que medios de pago digitales como PSE, Nequi, Daviplata y tarjetas estan habilitados?",
        "target_cluster": "10_03_medios_de_pago_digitales_y_efectivo.md",
        "pillar": "precios_tarifas_financiacion",
        "buttons": [
            {"label": "3.3 Plan 3 Cuotas 0%", "value": "3.3"},
            {"label": "3.2 Plan Contado 10% Dcto", "value": "3.2"},
            {"label": "2. Ver Horarios", "value": "2"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "financiacion_cuotas": {
        "text": (
            "plan de financiacion directa cuotas mensualidades pago diferido 3 cuotas sin intereses 40% inicial matricula "
            "30% semana 4 30% semana 7 pagar por partes credito educativo sin bancos"
        ),
        "canonical": "Como es el plan de financiacion directa en 3 cuotas sin interes y que porcentaje se paga?",
        "target_cluster": "10_02_plan_financiacion_3_cuotas.md",
        "pillar": "precios_tarifas_financiacion",
        "buttons": [
            {"label": "3.5 Medios de Pago (PSE/Nequi)", "value": "3.5"},
            {"label": "3.1 Tarifas Oficiales COP", "value": "3.1"},
            {"label": "2. Ver Horarios", "value": "2"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "tarifas_oficiales_cop": {
        "text": (
            "tarifas oficiales precios en pesos colombianos cop costo del modulo regular 650000 intensivo 720000 cuanto cuesta "
            "estudiar valor inversion total tarifas vigentes materiales y campus virtual incluido"
        ),
        "canonical": "Cuanto cuesta el modulo regular e intensivo en pesos colombianos (COP) y que incluye la tarifa?",
        "target_cluster": "03_precios_tarifas_y_financiacion.md",
        "pillar": "precios_tarifas_financiacion",
        "buttons": [
            {"label": "3.2 Plan Contado 10% Dcto", "value": "3.2"},
            {"label": "3.3 Plan 3 Cuotas 0%", "value": "3.3"},
            {"label": "3.4 Cajas Compensación 15%", "value": "3.4"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    # --- Descuentos & Becas ---
    "descuento_pago_contado": {
        "text": (
            "descuento pago de contado pronto pago 10% de descuento inmediato pagar todo completo de una solo pago "
            "modulo regular 585000 intensivo 648000 beneficio ahorro economico"
        ),
        "canonical": "Como funciona el 10% de descuento por pago de contado en modulos y paquetes de idiomas?",
        "target_cluster": "10_01_descuentos_pago_contado_10.md",
        "pillar": "becas_descuentos_convenios",
        "buttons": [
            {"label": "3.5 Medios de Pago (PSE/Nequi)", "value": "3.5"},
            {"label": "3.4 Cajas Compensación", "value": "3.4"},
            {"label": "2. Ver Horarios", "value": "2"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "convenios_cajas_compensacion": {
        "text": (
            "convenios con cajas de compensacion familiar 15% descuento compensar colsubsidio cafam comfama comfandi "
            "categorias a y b carnet afiliacion caja subsidio caja descuento empresarial"
        ),
        "canonical": "Cuales son los convenios del 15% de descuento con cajas de compensacion como Compensar o Colsubsidio?",
        "target_cluster": "12_01_convenios_cajas_compensacion.md",
        "pillar": "becas_descuentos_convenios",
        "buttons": [
            {"label": "12.3 Descuento Familiar 15%", "value": "3.4"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "4.1 Placement Test", "value": "4.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "descuento_familiar": {
        "text": (
            "descuento familiar convenio hermanos padres e hijos parejas segundo familiar matriculado simultaneamente "
            "15% de descuento grupo familiar estudiar en pareja familia"
        ),
        "canonical": "En que consiste el descuento familiar del 15% para dos o mas personas de la misma familia?",
        "target_cluster": "12_03_convenios_descuento_familiar.md",
        "pillar": "becas_descuentos_convenios",
        "buttons": [
            {"label": "3.4 Cajas Compensación 15%", "value": "3.4"},
            {"label": "1. Ver Cursos de Idiomas", "value": "1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "aclaratoria_becas": {
        "text": (
            "becas 100% beca completa merit based becas universitarias auxilios beca excelencia deportiva promedio "
            "aclaratoria oficial no becas propias ayuda postulacion becas externas chevening fulbright daad solo descuentos"
        ),
        "canonical": "Ofrecen becas completas del 100% o que opciones de becas y auxilios tienen?",
        "target_cluster": "12_04_becas_descuentos_aclaratoria.md",
        "pillar": "becas_descuentos_convenios",
        "buttons": [
            {"label": "3.4 Cajas Compensación 15%", "value": "3.4"},
            {"label": "3.2 Plan Contado 10% Dcto", "value": "3.2"},
            {"label": "3.3 Plan 3 Cuotas 0%", "value": "3.3"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    # --- Horarios & Franjas ---
    "franja_madrugadores": {
        "text": (
            "franja horaria de madrugadores early birds 6 a 8 am 6:00 a 8:00 a.m. clases en la madrugada manana temprano "
            "antes de entrar a trabajar antes del trabajo trabajar trabajo madrugador madrugadores profesionales ejecutivos lunes a viernes"
        ),
        "canonical": "Que horarios y caracteristicas tiene la franja de madrugadores de 6:00 a 8:00 a.m.?",
        "target_cluster": "07_01_franja_madrugadores_6_8am.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "2.3 Nocturno (6:30-8:30pm)", "value": "2.3"},
            {"label": "2.4 Sabatinos y Domingos", "value": "2.4"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "franjas_diurnas": {
        "text": (
            "franjas diurnas mananas y tardes de lunes a viernes 9 a 11 am 2 a 4 pm 4 a 6 pm horarios regulares "
            "clases en el dia tarde regular entre semana"
        ),
        "canonical": "Cuales son los horarios de las franjas diurnas de mananas y tardes de lunes a viernes?",
        "target_cluster": "07_02_franjas_diurnas_mananas_tardes.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "2.1 Madrugadores (6-8am)", "value": "2.1"},
            {"label": "2.3 Nocturno (6:30-8:30pm)", "value": "2.3"},
            {"label": "1. Ver Cursos", "value": "1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "franja_nocturna": {
        "text": (
            "franja nocturna after work 6:30 a 8:30 pm clases en la noche despues del trabajo universitarios "
            "profesionales lunes a viernes nocturno"
        ),
        "canonical": "Como funciona la franja nocturna after work de 6:30 a 8:30 p.m. de lunes a viernes?",
        "target_cluster": "07_03_franja_nocturna_after_work.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "2.4 Sabatinos y Domingos", "value": "2.4"},
            {"label": "2.1 Madrugadores (6-8am)", "value": "2.1"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "intensivos_fin_semana": {
        "text": (
            "cursos intensivos fin de semana sabatinos dominicales sabados 8 am a 1 pm 2 a 7 pm domingos 8:30 am a 1:30 pm "
            "estudiar fines de semana sabado domingo intensivo fin de semana"
        ),
        "canonical": "Cuales son los horarios y duracion de los cursos intensivos de fin de semana en sabados y domingos?",
        "target_cluster": "07_04_cursos_sabatinos_y_dominicales.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "2.5 Modalidad Virtual", "value": "2.5"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "4.1 Placement Test", "value": "4.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    # --- Modalidades ---
    "modalidad_virtual": {
        "text": (
            "modalidad 100% virtual sincronica clases en vivo plataforma zoom teams grabaciones 24/7 campus virtual "
            "estudiar online remoto desde casa en cualquier ciudad exterior"
        ),
        "canonical": "Cuales son las ventajas de la modalidad 100% virtual sincronica con clases en vivo y grabaciones?",
        "target_cluster": "08_01_modalidad_virtual_sincronica.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "2.6 Aulas HyFlex 360", "value": "2.6"},
            {"label": "2.4 Sabatinos y Domingos", "value": "2.4"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "modalidad_presencial": {
        "text": (
            "modalidad presencial sedes fisicas asistir a clases salones inteligentes aire acondicionado laboratorios "
            "acusticos biblioteca cafetería cultural sedes bogota medellin cali"
        ),
        "canonical": "Como funciona la modalidad presencial en las sedes fisicas y que tecnologia tienen las aulas?",
        "target_cluster": "08_02_modalidad_presencial_sedes.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "4.3 Sedes Bogotá", "value": "4.3"},
            {"label": "4.4 Sedes Medellín", "value": "4.4"},
            {"label": "4.5 Sede Cali", "value": "4.5"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "modalidad_hibrida": {
        "text": (
            "aulas hibridas hyflex flex 360 camaras inteligentes 360 grados 50% presencial 50% virtual alternar "
            "asistencia remota y fisica flexibilidad total"
        ),
        "canonical": "En que consisten las aulas hibridas HyFlex con camaras inteligentes 360 grados?",
        "target_cluster": "08_03_modalidad_hibrida_hyflex_360.md",
        "pillar": "horarios_modalidades_franjas",
        "buttons": [
            {"label": "2.5 Modalidad Virtual", "value": "2.5"},
            {"label": "2.1 Horarios Madrugadores", "value": "2.1"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    # --- Sedes & Admisiones ---
    "sedes_bogota": {
        "text": (
            "sedes bogota cundinamarca sede chico calle 100 carrera 15 sede chapinero carrera 7 calle 53 direcciones "
            "telefonos horarios counter salas estudio bogota capital donde quedan sedes de bogota donde estan"
        ),
        "canonical": "Donde estan ubicadas las sedes de Bogota (Chico y Chapinero) y cuales son sus direcciones y telefonos?",
        "target_cluster": "16_01_sedes_bogota_chico_chapinero.md",
        "pillar": "admisiones_sedes_matricula",
        "buttons": [
            {"label": "4.1 Placement Test Gratis", "value": "4.1"},
            {"label": "2. Horarios y Modalidades", "value": "2"},
            {"label": "3. Precios y Tarifas", "value": "3"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "sedes_medellin": {
        "text": (
            "sedes medellin antioquia sede el poblado parque lleras avenida poblado sede laureles segundo parque "
            "direcciones telefonos como llegar medellin"
        ),
        "canonical": "Donde quedan las sedes de Medellin en El Poblado y Laureles y como llegar?",
        "target_cluster": "16_02_sedes_medellin_poblado_laureles.md",
        "pillar": "admisiones_sedes_matricula",
        "buttons": [
            {"label": "4.1 Placement Test Gratis", "value": "4.1"},
            {"label": "2. Horarios y Modalidades", "value": "2"},
            {"label": "3. Precios y Tarifas", "value": "3"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "sede_cali": {
        "text": (
            "sede cali valle del cauca barrio granada zona rosa avenida 9 norte direccion telefono llegar cali sucursal"
        ),
        "canonical": "Donde esta ubicada la sede de Cali en el barrio Granada y como contactarla?",
        "target_cluster": "16_03_sede_cali_barrio_granada.md",
        "pillar": "admisiones_sedes_matricula",
        "buttons": [
            {"label": "4.1 Placement Test Gratis", "value": "4.1"},
            {"label": "2. Horarios y Modalidades", "value": "2"},
            {"label": "3. Precios y Tarifas", "value": "3"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "placement_test": {
        "text": (
            "examen de clasificacion placement test prueba de nivelacion saber nivel diagnostico diagnostica gratis "
            "gratuito agendar cita online o presencial entrevista oral gramatica"
        ),
        "canonical": "Como agendo el examen de clasificacion (placement test) gratuito y en que consiste?",
        "target_cluster": "18_02_tutorias_1a1_y_talleres_apoyo.md",
        "pillar": "admisiones_sedes_matricula",
        "buttons": [
            {"label": "4.2 Proceso de Matrícula", "value": "4.2"},
            {"label": "1. Ver Cursos & Niveles", "value": "1"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
    "proceso_matricula": {
        "text": (
            "proceso de matricula como matricularse inscripcion paso a paso requisitos documentos extranjeros documento "
            "de identidad pago matricula formulario admision formalizacion"
        ),
        "canonical": "Cual es el paso a paso para inscribirse y matricularse en linea o de forma presencial?",
        "target_cluster": "04_proceso_inscripcion_y_admision.md",
        "pillar": "admisiones_sedes_matricula",
        "buttons": [
            {"label": "4.1 Placement Test Gratis", "value": "4.1"},
            {"label": "3.5 Medios de Pago", "value": "3.5"},
            {"label": "3.1 Ver Tarifas COP", "value": "3.1"},
            {"label": "0. Menú Principal", "value": "0"},
        ],
    },
}


class SemanticIntentRouter:
    """
    Universal Vectorized Intent Router with 2-Level Hierarchy:
    - 5 Macro-Pillars
    - 18 Micro-Intents
    Precomputes and normalizes prototype embeddings at startup (warm_up)
    for sub-millisecond dot-product classification.
    """

    def __init__(self):
        self._macro_vectors: Dict[str, List[float]] = {}
        self._micro_vectors: Dict[str, List[float]] = {}
        self._warmed_up = False

    def warm_up(self) -> None:
        """Precomputes and caches normalized prototype vectors for all macro and micro intents."""
        if self._warmed_up:
            return

        # 1. Macro-pillars
        for pillar_name, text in MACRO_PILLARS_PROTOTYPES.items():
            emb = vector_store.embed_query(text)
            if emb and any(v != 0.0 for v in emb):
                self._macro_vectors[pillar_name] = self._normalize_vec(emb)

        # 2. Micro-intents
        for intent_name, data in MICRO_INTENTS_PROTOTYPES.items():
            emb = vector_store.embed_query(data["text"])
            if emb and any(v != 0.0 for v in emb):
                self._micro_vectors[intent_name] = self._normalize_vec(emb)

        self._warmed_up = True

    @staticmethod
    def _normalize_vec(v: List[float]) -> List[float]:
        norm = math.sqrt(sum(x * x for x in v))
        if norm > 0:
            return [x / norm for x in v]
        return v

    @staticmethod
    def _dot_product(v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        return sum(a * b for a, b in zip(v1, v2))

    def classify(self, query: str) -> IntentMatch:
        """
        Embeds the query and computes cosine similarity against all prototype vectors.
        Detects primary macro pillar, primary micro intent, and composite multi-intents.
        """
        if not self._warmed_up:
            self.warm_up()

        q_clean = query.strip().lower()
        # Normalize English loanwords to Spanish
        loanword_replacements = [
            (r"\bschedules?\b", "horarios"),
            (r"\bavailable\b", "disponibles"),
            (r"\bprices?\b", "precios"),
            (r"\bfees?\b", "tarifas"),
            (r"\bcosts?\b", "costos"),
            (r"\bcourses?\b", "cursos"),
            (r"\bclasses?\b", "clases"),
            (r"\bcampus(?:es)?\b", "sedes"),
            (r"\blocations?\b", "ubicacion"),
            (r"\brequirements?\b", "requisitos"),
        ]
        for pattern, replacement in loanword_replacements:
            q_clean = re.sub(pattern, replacement, q_clean, flags=re.IGNORECASE)

        # Remove extreme punctuation while preserving words
        q_clean = re.sub(r"[^a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ\s]", " ", q_clean)
        q_clean = re.sub(r"\s+", " ", q_clean).strip()

        q_vec = vector_store.embed_query(q_clean)
        if not q_vec or not any(v != 0.0 for v in q_vec):
            return IntentMatch(
                top_macro_pillar="cursos_idiomas_niveles",
                macro_score=0.0,
                action_buttons=[
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "4. Admisiones & Sedes", "value": "4"},
                    {"label": "0. Menú Principal", "value": "0"},
                ],
            )

        q_norm = self._normalize_vec(q_vec)

        # 1. Macro-pillar matching
        best_macro = "cursos_idiomas_niveles"
        best_macro_score = 0.0
        for pillar, p_vec in self._macro_vectors.items():
            score = self._dot_product(q_norm, p_vec)
            if score > best_macro_score:
                best_macro_score = score
                best_macro = pillar

        # 2. Micro-intent matching
        ranked_micros: List[Tuple[str, float]] = []
        for intent_name, i_vec in self._micro_vectors.items():
            score = self._dot_product(q_norm, i_vec)
            ranked_micros.append((intent_name, score))

        ranked_micros.sort(key=lambda x: x[1], reverse=True)

        top_micro, top_micro_score = ranked_micros[0] if ranked_micros else (None, 0.0)
        sec_micro, sec_micro_score = ranked_micros[1] if len(ranked_micros) > 1 else (None, 0.0)

        # Hierarchical macro-micro alignment: if micro matches with confidence, ensure parent macro consistency
        if top_micro and top_micro_score >= 0.15:
            micro_parent_pillar = MICRO_INTENTS_PROTOTYPES[top_micro]["pillar"]
            if best_macro_score < top_micro_score or best_macro_score == 0.0:
                best_macro = micro_parent_pillar
                best_macro_score = max(best_macro_score, top_micro_score)

        # 3. Multi-intent detection:
        # If the top two micro intents have strong similarity (> 0.40) and are very close (difference < 0.12)
        # from different macro domains or different themes
        is_multi = False
        if top_micro and sec_micro and top_micro_score >= 0.40 and sec_micro_score >= 0.38:
            diff = top_micro_score - sec_micro_score
            top_pillar = MICRO_INTENTS_PROTOTYPES[top_micro]["pillar"]
            sec_pillar = MICRO_INTENTS_PROTOTYPES[sec_micro]["pillar"]
            if diff <= 0.12 and top_pillar != sec_pillar:
                is_multi = True

        # Extract metadata for the top micro intent
        canonical = None
        target_cluster = None
        buttons = []
        if top_micro and top_micro_score >= 0.15:
            meta = MICRO_INTENTS_PROTOTYPES[top_micro]
            canonical = meta["canonical"]
            target_cluster = meta["target_cluster"]
            buttons = meta["buttons"]
        else:
            # Fallback default navigation buttons
            buttons = [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Admisiones & Sedes", "value": "4"},
                {"label": "0. Menú Principal", "value": "0"},
            ]

        return IntentMatch(
            top_macro_pillar=best_macro,
            macro_score=round(best_macro_score, 4),
            top_micro_intent=top_micro if top_micro_score >= 0.15 else None,
            micro_score=round(top_micro_score, 4),
            canonical_query=canonical,
            target_cluster=target_cluster,
            is_multi_intent=is_multi,
            secondary_micro_intent=sec_micro if is_multi else None,
            secondary_score=round(sec_micro_score, 4),
            action_buttons=buttons,
        )


semantic_intent_router = SemanticIntentRouter()
