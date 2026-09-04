from src.rag.ingestion import DocumentIngestionPipeline
from pathlib import Path


def test_chunking_with_overlap():
    pipeline = DocumentIngestionPipeline(chunk_size=100, chunk_overlap=20)
    sample_text = (
        "## Academic Overview\n\n"
        "Nova Tech University offers cutting edge education in Artificial Intelligence, "
        "Cybersecurity, Software Engineering, and Cloud Architecture. Students receive practical "
        "training and real-world internship opportunities with global technology leaders."
    )

    chunks = pipeline._split_into_chunks(sample_text, "test_doc.md")
    assert len(chunks) >= 2

    # Verify metadata fields
    first_chunk = chunks[0]
    assert "id" in first_chunk
    assert first_chunk["metadata"]["source"] == "test_doc.md"
    assert first_chunk["metadata"]["section"] == "Academic Overview"


def test_directory_hash_calculation():
    pipeline = DocumentIngestionPipeline()
    h1 = pipeline.compute_directory_hash()
    assert len(h1) == 64


def test_atomic_table_chunking():
    # P2 / TODO-1.2: Validate atomic table preservation
    pipeline = DocumentIngestionPipeline()
    doc_with_table = (
        "# Tarifas Oficiales 2026\n\n"
        "A continuacion se presentan los valores en pesos colombianos para el programa intensivo.\n\n"
        "| Programa | Modalidad | Precio Contado COP | Plan 3 Cuotas |\n"
        "|---|---|---|---|\n"
        "| Ingles Intensivo A1 | Presencial Chicó | $ 1.350.000 | 40% inicial + 2 cuotas 30% |\n"
        "| Ingles Intensivo A2 | Presencial Chapinero | $ 1.350.000 | 40% inicial + 2 cuotas 30% |\n"
        "| Ingles Intensivo B1 | Virtual Sincronico | $ 1.215.000 | 40% inicial + 2 cuotas 30% |\n\n"
        "Todos los pagos de contado reciben un 10% de descuento automatico en matricula."
    )

    chunks = pipeline._split_into_chunks(doc_with_table, "03_01_tarifas_ingles.md")
    assert len(chunks) >= 2

    # Find the table chunk
    table_chunks = [c for c in chunks if c["metadata"].get("is_table_atomic") is True]
    assert len(table_chunks) == 1

    tbl = table_chunks[0]
    assert tbl["metadata"]["has_table"] is True
    assert tbl["metadata"]["table_rows"] == 5
    assert "$ 1.350.000" in tbl["text"]
    assert "Plan 3 Cuotas" in tbl["text"]


def test_large_table_header_preservation():
    # P2 / TODO-1.2: Large tables must preserve table headers across sub-chunks
    pipeline = DocumentIngestionPipeline()
    header = "| Modulo | Sede | Nivel | Horario | Tarifa COP |\n|---|---|---|---|---|\n"
    # Generate 40 rows to exceed table limit
    rows = "\n".join([f"| MOD-{i:02d} | Sede Chico | Nivel B2.{i%4} | 6:30 PM | $ 1.350.000 |" for i in range(40)])
    doc = f"# Horarios Extensos\n\n{header}{rows}\n\nInformacion adicional."

    chunks = pipeline._split_into_chunks(doc, "02_horarios_grandes.md")
    table_chunks = [c for c in chunks if c["metadata"].get("has_table") is True]
    assert len(table_chunks) >= 2

    # Each partition must contain the table header line
    for tc in table_chunks:
        assert "| Modulo | Sede | Nivel | Horario | Tarifa COP |" in tc["text"]

