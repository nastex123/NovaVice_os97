import os
import sys
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_executable_files_exist():
    expected_files = [
        BASE_DIR / "installer.py",
        BASE_DIR / "install.bat",
        BASE_DIR / "install.sh",
        BASE_DIR / "run.py",
        BASE_DIR / "start.bat",
        BASE_DIR / "start.sh",
    ]
    for f in expected_files:
        assert f.exists(), f"Missing required executable script: {f.name}"
        assert f.stat().st_size > 0, f"Script is empty: {f.name}"

def test_installer_script_structure():
    installer_path = BASE_DIR / "installer.py"
    content = installer_path.read_text(encoding="utf-8")
    assert "def detect_or_ask_os" in content
    assert "def check_prerequisites" in content
    assert "def setup_python_environment" in content
    assert "def setup_frontend_environment" in content

def test_run_launcher_structure():
    run_path = BASE_DIR / "run.py"
    content = run_path.read_text(encoding="utf-8")
    assert "def prompt_advisor_selection" in content
    assert "def start_opencode" in content
    assert "def start_fastapi" in content
    assert "def start_nextjs" in content
    assert "def cleanup_processes" in content
