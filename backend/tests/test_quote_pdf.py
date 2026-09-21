import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.core.quote import (
    QuoteError,
    build_quote,
    fmt_cop,
    render_quote_pdf,
)


def test_fmt_cop_uses_dot_thousands():
    assert fmt_cop(585000) == "$585.000 COP"
    assert fmt_cop(65000) == "$65.000 COP"
    assert fmt_cop(0) == "$0 COP"


def test_build_quote_contado_regular_matches_canonical():
    # 12_04 canonico: regular $650.000 COP -> $585.000 COP con 10% contado.
    q = build_quote("regular", "contado")
    assert q["tarifa_base"] == 650000
    assert q["descuento_pct"] == 10
    assert q["descuento_valor"] == 65000
    assert q["total"] == 585000
    assert q["cuotas"] == [234000, 175500, 175500]
    assert sum(q["cuotas"]) == q["total"]
    assert q["moneda"] == "COP"


def test_build_quote_intensivo_caja():
    q = build_quote("intensivo", "caja")
    assert q["tarifa_base"] == 720000
    assert q["descuento_pct"] == 15
    assert q["descuento_valor"] == 108000
    assert q["total"] == 612000
    assert sum(q["cuotas"]) == q["total"]


def test_build_quote_familiar_sabatino():
    q = build_quote("sabatino", "familiar")
    assert q["tarifa_base"] == 650000
    assert q["descuento_valor"] == 97500
    assert q["total"] == 552500
    assert sum(q["cuotas"]) == q["total"]


def test_build_quote_bono_referidos():
    q = build_quote("regular", "ninguno", referidos=2)
    assert q["bono_valor"] == 200000
    assert q["total"] == 450000
    assert sum(q["cuotas"]) == q["total"]


def test_build_quote_invalid_params_raise():
    with pytest.raises(QuoteError):
        build_quote("doctorado", "contado")
    with pytest.raises(QuoteError):
        build_quote("regular", "beca100")
    with pytest.raises(QuoteError):
        build_quote("regular", "ninguno", referidos=-1)


def test_render_quote_pdf_structure_and_tokens():
    pdf = render_quote_pdf(build_quote("regular", "contado"))
    assert pdf.startswith(b"%PDF-1.4")
    assert pdf.rstrip().endswith(b"%%EOF")
    for token in (
        b"COTIZACION OFICIAL",
        b"NOVA IDIOMAS",
        b"$585.000",
        b"$650.000",
        b"Regular",
        b"40/30/30",
        b"03_precios",
    ):
        assert token in pdf


@pytest.mark.asyncio
async def test_api_quote_json_and_pdf_e2e_download():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        detail = await client.get(
            "/api/v1/quote", params={"programa": "intensivo", "descuento": "familiar"}
        )
        assert detail.status_code == 200
        data = detail.json()
        assert data["total"] == 612000
        assert sum(data["cuotas"]) == data["total"]
        assert data["cuotas_pct"] == [40, 30, 30]

        pdf_resp = await client.get(
            "/api/v1/quote/pdf", params={"programa": "intensivo", "descuento": "familiar"}
        )
        assert pdf_resp.status_code == 200
        assert pdf_resp.headers["content-type"] == "application/pdf"
        assert "attachment" in pdf_resp.headers["content-disposition"]
        assert "cotizacion_nova_intensivo" in pdf_resp.headers["content-disposition"]
        assert pdf_resp.content.startswith(b"%PDF-1.4")
        assert pdf_resp.content.rstrip().endswith(b"%%EOF")
        assert b"$612.000" in pdf_resp.content

        bad = await client.get("/api/v1/quote/pdf", params={"programa": "doctorado"})
        assert bad.status_code == 422
        bad_json = await client.get("/api/v1/quote", params={"descuento": "beca100"})
        assert bad_json.status_code == 422
