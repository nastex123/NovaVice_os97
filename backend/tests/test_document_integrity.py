import re
from pathlib import Path
import pytest
from src.config import settings

def test_documents_count_and_extensions():
    # P1 / TODO-1.11: Validate total document count and extensions
    docs_dir = settings.documents_dir
    files = list(docs_dir.glob("*.md"))
    assert len(files) >= 80, f"Expected at least 80 markdown documents, found {len(files)}"

def test_document_headers_and_structure():
    # Every markdown file must have at least one top-level header and non-empty content
    docs_dir = settings.documents_dir
    files = sorted(list(docs_dir.glob("*.md")))

    for f in files:
        content = f.read_text(encoding="utf-8").strip()
        assert len(content) > 50, f"Document {f.name} is too short or empty"
        assert content.startswith("#"), f"Document {f.name} must begin with a markdown header (#)"

def test_markdown_structural_elements():
    # P1 / TODO-1.11: Validate list items, bullet points and proper markdown syntax across documents
    docs_dir = settings.documents_dir
    files = sorted(list(docs_dir.glob("*.md")))
    total_bullet_items = 0
    total_paragraphs = 0

    for f in files:
        lines = f.read_text(encoding="utf-8").split("\n")
        file_elements = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s+", stripped):
                total_bullet_items += 1
                file_elements += 1
            elif len(stripped) > 40 and not stripped.startswith("#"):
                total_paragraphs += 1
                file_elements += 1
            # If line is a markdown table row, verify balanced pipe syntax
            if stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1:
                cols = stripped.split("|")[1:-1]
                assert len(cols) >= 1, f"Empty table row in {f.name}"
        assert file_elements >= 1, f"Document {f.name} should contain structured content"

    assert total_bullet_items >= 150, f"Expected at least 150 bullet items across corpus, found {total_bullet_items}"
    assert total_paragraphs >= 50, f"Expected substantive paragraphs across corpus, found {total_paragraphs}"
