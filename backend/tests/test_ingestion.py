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
