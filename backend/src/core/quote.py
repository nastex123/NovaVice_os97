"""PROP-195: Cotizacion oficial en PDF generada 100% en local.

Sin pasarela ni servicios externos y sin dependencias nuevas (writer PDF 1.4
minimalista con fuentes estandar Helvetica/Helvetica-Bold, coherente con la
arquitectura pure-python de ADR-001).

Fuentes canonicas de negocio (backend/data/documents):
- Tarifas: `03_precios_tarifas_y_financiacion.md`,
  `09_01_tarifas_oficiales_modulos_2026.md`
- Pronto pago 10%: `10_01_descuentos_pago_contado_10.md`
- Financiacion 3 cuotas 40/30/30: `10_02_plan_financiacion_3_cuotas.md`
- Convenio cajas 15%: `12_01_convenios_cajas_de_compensacion.md`
- Convenio universitario 15%: `12_02_convenios_universitarios_y_colegios.md`
- Familiar 15%: `12_03_convenios_descuentos_familiares.md`
- Bono referido $100.000: `03_...` (Descuento por Referidos),
  `09_03_promociones_temporada_y_descuentos.md`
- Aclaratoria becas=descuentos: `12_04_becas_descuentos_aclaratoria.md`
"""

import time

# --- Catalogo institucional (COP) -------------------------------------------
TARIFFS = {
    "regular": {
        "label": "Curso Regular Bimestral (40 horas)",
        "base": 650000,
    },
    "intensivo": {
        "label": "Curso Intensivo Mensual (40 horas aceleradas)",
        "base": 720000,
    },
    "sabatino": {
        "label": "Curso Sabatino / Dominical (40 horas)",
        "base": 650000,
    },
}

DISCOUNTS = {
    "ninguno": {"label": "Sin descuento", "pct": 0},
    "contado": {"label": "Pago de contado", "pct": 10},
    "caja": {"label": "Convenio caja de compensacion", "pct": 15},
    "universidad": {"label": "Convenio universitario / estudiantil", "pct": 15},
    "familiar": {"label": "Descuento familiar (2do miembro)", "pct": 15},
}

BONO_REFERIDO_COP = 100000
CUOTA_SPLIT = (40, 30, 30)
VIGENCIA_DIAS = 30

QUOTE_SOURCES = (
    "03_precios_tarifas_y_financiacion.md",
    "09_01_tarifas_oficiales_modulos_2026.md",
    "10_01_descuentos_pago_contado_10.md",
    "10_02_plan_financiacion_3_cuotas.md",
    "12_01_convenios_cajas_de_compensacion.md",
    "12_02_convenios_universitarios_y_colegios.md",
    "12_03_convenios_descuentos_familiares.md",
    "09_03_promociones_temporada_y_descuentos.md",
    "12_04_becas_descuentos_aclaratoria.md",
)


class QuoteError(ValueError):
    """Parametros de cotizacion invalidos (programa/descuento desconocido)."""


def fmt_cop(amount: int) -> str:
    """Formato moneda es-CO: 585000 -> '$585.000 COP'."""
    return "$" + f"{int(amount):,}".replace(",", ".") + " COP"


def build_quote(programa: str = "regular", descuento: str = "ninguno", referidos: int = 0) -> dict:
    """Arma el detalle de cotizacion con la politica institucional vigente."""
    prog_key = (programa or "").strip().lower()
    if prog_key not in TARIFFS:
        raise QuoteError(
            f"Programa desconocido: {programa!r}. "
            f"Programas validos: {', '.join(sorted(TARIFFS))}."
        )
    desc_key = (descuento or "").strip().lower()
    if desc_key not in DISCOUNTS:
        raise QuoteError(
            f"Descuento desconocido: {descuento!r}. "
            f"Descuentos validos: {', '.join(sorted(DISCOUNTS))}."
        )
    try:
        n_ref = int(referidos)
    except (TypeError, ValueError):
        raise QuoteError(f"Referidos debe ser un entero >= 0, llego: {referidos!r}.")
    if n_ref < 0:
        raise QuoteError(f"Referidos debe ser un entero >= 0, llego: {referidos!r}.")

    base = TARIFFS[prog_key]["base"]
    pct = DISCOUNTS[desc_key]["pct"]
    descuento_valor = base * pct // 100
    subtotal = base - descuento_valor
    bono_valor = min(n_ref * BONO_REFERIDO_COP, subtotal)
    total = subtotal - bono_valor
    c1 = total * CUOTA_SPLIT[0] // 100
    c2 = total * CUOTA_SPLIT[1] // 100
    c3 = total - c1 - c2
    now = time.strftime("%Y-%m-%d %H:%M")
    quote_id = f"NQ-{time.strftime('%Y%m%d')}-{prog_key[:3].upper()}-{total:06d}"
    return {
        "quote_id": quote_id,
        "emitida": now,
        "vigencia_dias": VIGENCIA_DIAS,
        "moneda": "COP",
        "programa": prog_key,
        "programa_label": TARIFFS[prog_key]["label"],
        "tarifa_base": base,
        "descuento": desc_key,
        "descuento_label": DISCOUNTS[desc_key]["label"],
        "descuento_pct": pct,
        "descuento_valor": descuento_valor,
        "referidos": n_ref,
        "bono_valor": bono_valor,
        "total": total,
        "cuotas": [c1, c2, c3],
        "cuotas_pct": list(CUOTA_SPLIT),
        "fuentes": list(QUOTE_SOURCES),
    }


def _pdf_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def render_quote_pdf(quote: dict) -> bytes:
    """Renderiza la cotizacion como PDF 1.4 de una pagina (stream sin comprimir)."""
    parts: list = []

    def rect(x, y, w, h, r, g, b):
        parts.append(f"{r:.3f} {g:.3f} {b:.3f} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")

    def box(x, y, w, h):
        parts.append(f"0.000 0.000 0.000 RG 1.2 w {x:.1f} {y:.1f} {w:.1f} {h:.1f} re S")

    def rule(x1, y, x2):
        parts.append(f"0.000 0.000 0.000 RG 0.8 w {x1:.1f} {y:.1f} m {x2:.1f} {y:.1f} l S")

    def text(font, size, x, y, s, white=False):
        if white:
            parts.append("1.000 1.000 1.000 rg")
        else:
            parts.append("0.000 0.000 0.000 rg")
        parts.append(
            f"BT /{font} {size} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({_pdf_escape(s)}) Tj ET"
        )

    navy = (0.070, 0.100, 0.300)
    pink = (0.950, 0.250, 0.450)

    # Banda institucional superior + franja de acento.
    rect(0, 722, 612, 70, *navy)
    rect(0, 716, 612, 6, *pink)
    text("F1", 11, 48, 768, "NOVA IDIOMAS COLOMBIA - ADMISIONES", white=True)
    text("F2", 22, 48, 740, "COTIZACION OFICIAL", white=True)
    text("F1", 9, 430, 770, f"No. {quote['quote_id']}", white=True)
    text("F1", 9, 430, 756, f"Emitida: {quote['emitida']}", white=True)
    text("F1", 9, 430, 742, f"Vigencia: {quote['vigencia_dias']} dias", white=True)

    # Detalle de valores.
    y = 684
    text("F2", 13, 48, y, "DETALLE DE LA COTIZACION")
    y -= 26
    rows = [
        ("Programa:", quote["programa_label"]),
        ("Tarifa base:", fmt_cop(quote["tarifa_base"])),
        (
            f"Descuento ({quote['descuento_label']} {quote['descuento_pct']}%):",
            f"-{fmt_cop(quote['descuento_valor'])}",
        ),
        (
            f"Bono referidos ({quote['referidos']} x {fmt_cop(BONO_REFERIDO_COP)}):",
            f"-{fmt_cop(quote['bono_valor'])}",
        ),
    ]
    for label, value in rows:
        text("F1", 11, 60, y, label)
        text("F1", 11, 400, y, value)
        y -= 20
    rule(48, y + 6, 564)
    y -= 14
    text("F2", 14, 60, y, "TOTAL A PAGAR:")
    text("F2", 14, 400, y, fmt_cop(quote["total"]))

    # Plan de financiacion 3 cuotas sin interes.
    y -= 44
    text("F2", 13, 48, y, "PLAN DE FINANCIACION - 3 CUOTAS SIN INTERES (40/30/30)")
    y -= 18
    box_h = 24 + 22 * len(quote["cuotas"])
    box(48, y - box_h + 14, 516, box_h)
    y -= 12
    for i, (monto, pct) in enumerate(zip(quote["cuotas"], quote["cuotas_pct"]), start=1):
        momento = (
            "al matricularte" if i == 1 else ("semana 4" if i == 2 else "semana 7")
        )
        text("F1", 11, 64, y, f"Cuota {i} ({pct}% - {momento}):  {fmt_cop(monto)}")
        y -= 22

    # Notas institucionales.
    y -= 18
    text("F2", 11, 48, y, "NOTAS")
    y -= 18
    notes = [
        "Valores en Pesos Colombianos (COP), tarifas oficiales 2026,",
        "materiales y campus virtual incluidos.",
        "El descuento aplica sobre la tarifa base del modulo.",
        "No existen becas del 100%: la ayuda financiera opera",
        "como descuentos (contado 10%, convenios 15%, familiar 15%)",
        "y bono de $100.000 COP por referido que se matricule.",
        "Financiacion directa sin fiador ni centrales de riesgo.",
    ]
    for note in notes:
        text("F1", 9, 60, y, note)
        y -= 14

    # Fuentes y pie.
    y -= 10
    text("F1", 8, 48, y, "Fuentes: " + ", ".join(quote["fuentes"][:3]))
    y -= 13
    text("F1", 8, 48, y, "         " + ", ".join(quote["fuentes"][3:6]))
    y -= 13
    text("F1", 8, 48, y, "         " + ", ".join(quote["fuentes"][6:]))
    y -= 24
    rule(48, y + 8, 564)
    text(
        "F1",
        8,
        48,
        y - 6,
        "Documento generado localmente por NovaVice OS97. Sin pasarelas ni servicios externos.",
    )

    try:
        stream = "\n".join(parts).encode("latin-1")
    except UnicodeEncodeError as e:
        raise QuoteError(f"Contenido de cotizacion no codificable en PDF: {e}")

    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    out = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii") + body + b"\nendobj\n"
    xref_at = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_at}\n%%EOF\n"
    ).encode("ascii")
    return out
