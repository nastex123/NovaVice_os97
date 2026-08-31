"""
Herramientas y Skills personalizados para el Asistente de Nova Idiomas.
Permite realizar cálculos dinámicos de cotización, agendamiento de exámenes de nivelación
y consulta de disponibilidad de sedes.
"""

from typing import Dict, Any, Optional
import time
import uuid


def calcular_cotizacion_curso(
    idioma: str,
    modalidad: str = "regular",
    tipo_pago: str = "contado",
    es_familiar: bool = False
) -> Dict[str, Any]:
    """
    Calcula el costo exacto en COP para un curso de idiomas según modalidad y tipo de pago.
    
    Args:
        idioma: Idioma deseado (inglés, francés, alemán, italiano, portugués, español).
        modalidad: 'regular' (bimestral), 'intensivo' (mensual), 'sabatino' o 'privadas'.
        tipo_pago: 'contado' (10% descuento) o 'cuotas' (3 cuotas 0% interés).
        es_familiar: Si aplica el 15% de descuento por segundo familiar.
    """
    precios_base = {
        "regular": 650000,
        "intensivo": 720000,
        "sabatino": 650000,
        "dominical": 650000,
        "privadas_10h": 650000,
        "privadas_20h": 1200000,
        "paquete_b1": 1750000,
        "bilinguismo_total": 5500000
    }
    
    base = precios_base.get(modalidad.lower(), 650000)
    descuento_porcentaje = 0
    
    if tipo_pago.lower() == "contado":
        descuento_porcentaje += 10
    if es_familiar:
        descuento_porcentaje += 15
        
    valor_descuento = int(base * (descuento_porcentaje / 100.0))
    total_a_pagar = base - valor_descuento
    
    cuotas_detalle = []
    if tipo_pago.lower() == "cuotas":
        cuotas_detalle = [
            {"numero": 1, "porcentaje": "40%", "valor_cop": int(base * 0.40), "momento": "Al matricularse"},
            {"numero": 2, "porcentaje": "30%", "valor_cop": int(base * 0.30), "momento": "Semana 4 de clases"},
            {"numero": 3, "porcentaje": "30%", "valor_cop": int(base * 0.30), "momento": "Semana 7 de clases"}
        ]
        
    return {
        "idioma": idioma.capitalize(),
        "modalidad": modalidad,
        "precio_base_cop": base,
        "descuento_aplicado_pct": descuento_porcentaje,
        "descuento_valor_cop": valor_descuento,
        "total_a_pagar_cop": total_a_pagar,
        "tipo_pago": tipo_pago,
        "plan_cuotas": cuotas_detalle
    }


def agendar_examen_clasificacion(
    nombre_completo: str,
    correo: str,
    telefono: str,
    idioma: str,
    modalidad_examen: str = "virtual"
) -> Dict[str, Any]:
    """
    Genera un registro oficial para presentar el Examen de Clasificación (Placement Test) gratuito.
    """
    ticket_id = f"TEST-{time.strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
    return {
        "status": "agendado",
        "ticket_placement": ticket_id,
        "estudiante": nombre_completo,
        "correo": correo,
        "telefono": telefono,
        "idioma": idioma.capitalize(),
        "modalidad": modalidad_examen,
        "costo_cop": 0,
        "instrucciones": "Recibirás un enlace de acceso al correo con tus credenciales temporales para la sección escrita y de audio (35 min), seguido de una videollamada de 10 min con un docente evaluador.",
        "validez_dias": 15
    }


# Definiciones de herramientas para agentes tipo Hermes / OpenAI Tools
AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calcular_cotizacion_curso",
            "description": "Calcula el costo oficial en COP de un curso en Nova Idiomas con descuentos y plan de cuotas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "idioma": {"type": "string", "description": "Idioma a cotizar (ej. inglés, francés, alemán)."},
                    "modalidad": {"type": "string", "enum": ["regular", "intensivo", "sabatino", "privadas_10h", "paquete_b1", "bilinguismo_total"]},
                    "tipo_pago": {"type": "string", "enum": ["contado", "cuotas"]},
                    "es_familiar": {"type": "boolean", "description": "True si aplica descuento familiar del 15%."}
                },
                "required": ["idioma"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "agendar_examen_clasificacion",
            "description": "Agenda un Examen de Clasificación (Placement Test) 100% gratuito para evaluar el nivel MCER de un estudiante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_completo": {"type": "string", "description": "Nombre completo del postulante."},
                    "correo": {"type": "string", "description": "Correo electrónico de contacto."},
                    "telefono": {"type": "string", "description": "Número de teléfono o WhatsApp."},
                    "idioma": {"type": "string", "description": "Idioma a evaluar."},
                    "modalidad_examen": {"type": "string", "enum": ["virtual", "presencial_bogota", "presencial_medellin", "presencial_cali"]}
                },
                "required": ["nombre_completo", "correo", "telefono", "idioma"]
            }
        }
    }
]
