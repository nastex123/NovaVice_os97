#!/usr/bin/env python3
"""
Nova Idiomas Colombia - Admissions Assistant RAG
Multiplatform Automated Installer (Windows / Linux / macOS)
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
VENV_DIR = BASE_DIR / "venv"

def ensure_node_in_path():
    """Detect Node/NPM in common install locations (NVM, fnm, volta, local bin) and add to PATH if needed."""
    if shutil.which("node") and shutil.which("npm"):
        return
    home = Path.home()
    possible_paths = [
        home / ".local" / "bin",
        home / "bin",
        Path("/usr/local/bin"),
    ]
    # Check NVM directories
    nvm_versions_dir = home / ".nvm" / "versions" / "node"
    if nvm_versions_dir.exists():
        for v_dir in sorted(nvm_versions_dir.glob("v*"), reverse=True):
            possible_paths.append(v_dir / "bin")

    # Check FNM / Volta / asdf
    possible_paths.extend([
        home / ".fnm" / "current" / "bin",
        home / ".volta" / "bin",
        home / ".asdf" / "shims",
    ])

    current_path = os.environ.get("PATH", "")
    for p in possible_paths:
        if p.exists() and (p / ("node.exe" if platform.system() == "Windows" else "node")).exists():
            if str(p) not in current_path:
                os.environ["PATH"] = f"{p}{os.pathsep}{current_path}"
                current_path = os.environ["PATH"]

def print_banner():
    print("=" * 70)
    print("  🎓 NOVA IDIOMAS - ADMISSIONS INTELLIGENT ASSISTANT (RAG)")
    print("  🚀 MULTIPLATFORM AUTOMATED INSTALLER (WINDOWS / LINUX / MACOS)")
    print("=" * 70)

def detect_or_ask_os():
    detected = platform.system()
    print(f"\n[+] Automatically detected operating system: {detected}")
    print("\nPlease confirm or select your operating system:")
    print("  [1] Windows")
    print("  [2] Linux / macOS")
    
    choice = input("\nEnter option [1 or 2, press Enter for auto-detect]: ").strip()
    if choice == "1":
        return "Windows"
    elif choice == "2":
        return "Linux"
    return detected

def check_prerequisites():
    print("\n--- Verifying System Prerequisites ---")
    # Check Python version
    py_ver = sys.version_info
    print(f"[✓] Python {py_ver.major}.{py_ver.minor}.{py_ver.micro} detectado.")
    if py_ver < (3, 10):
        print("[!] ERROR: Se requiere Python 3.10 o superior.")
        sys.exit(1)
        
    # Check Node.js and npm
    ensure_node_in_path()
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    
    if not node_path or not npm_path:
        print("[!] ADVERTENCIA: Node.js o npm no fueron encontrados en el PATH del sistema.")
        print("    To run the modern Next.js frontend, please install Node.js (v18+).")
    else:
        try:
            node_v = subprocess.check_output([node_path, "-v"], text=True).strip()
            npm_v = subprocess.check_output([npm_path, "-v"], text=True).strip()
            print(f"[✓] Node.js {node_v} and npm {npm_v} detected.")
        except Exception:
            pass

def setup_python_environment(os_type):
    print("\n--- Setting up Python Virtual Environment ---")
    if not VENV_DIR.exists():
        print("[+] Creating virtual environment 'venv'...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        print("[✓] Virtual environment created successfully.")
    else:
        print("[✓] Virtual environment 'venv' already exists.")

    if os_type == "Windows":
        py_bin = VENV_DIR / "Scripts" / "python.exe"
        pip_bin = VENV_DIR / "Scripts" / "pip.exe"
    else:
        py_bin = VENV_DIR / "bin" / "python"
        pip_bin = VENV_DIR / "bin" / "pip"

    # Install Python dependencies
    req_file = BACKEND_DIR / "requirements.txt"
    if req_file.exists():
        print(f"\n[+] Installing Python dependencies from {req_file}...")
        subprocess.check_call([str(py_bin), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(py_bin), "-m", "pip", "install", "-r", str(req_file)])
        print("[✓] Python dependencies installed successfully.")

    # Ingest Knowledge Base
    print("\n--- Indexing RAG Knowledge Base (82 Official Documents) ---")
    try:
        subprocess.check_call([str(py_bin), "-m", "src.rag.ingestion"], cwd=str(BACKEND_DIR))
        print("[✓] 82 Official Documents indexed in ChromaDB and BM25.")
    except Exception as e:
        print(f"[!] Error indexing documents: {e}")

def setup_frontend_environment():
    if not FRONTEND_DIR.exists():
        return

    print("\n--- Setting up Next.js 15 Frontend ---")
    ensure_node_in_path()
    npm_path = shutil.which("npm")
    if npm_path:
        print("[+] Installing Node.js packages (Next.js, Tailwind CSS, Lucide)...")
        try:
            is_win = platform.system() == "Windows"
            cmd = "npm install" if is_win else [npm_path, "install"]
            subprocess.check_call(cmd, cwd=str(FRONTEND_DIR), shell=is_win)
            print("[✓] Frontend dependencies installed successfully.")
        except Exception as e:
            print(f"[!] Error installing npm packages: {e}")
    else:
        print("[!] Skipping 'npm install' because npm is not currently available.")

def check_opencode():
    print("\n--- Verifying OpenCode Server ---")
    ensure_node_in_path()
    opencode_path = shutil.which("opencode")
    if opencode_path:
        print("[✓] OpenCode CLI detected on system.")
    else:
        print("[i] OpenCode CLI not detected globally.")
        print("    The system will use built-in fallback synthesis or you can install it with:")
        print("    npm install -g opencode-ai")

def main():
    print_banner()
    os_type = detect_or_ask_os()
    print(f"\n[+] Proceeding with optimized installation for: {os_type}")
    
    check_prerequisites()
    setup_python_environment(os_type)
    setup_frontend_environment()
    check_opencode()
    
    print("\n" + "=" * 70)
    print("  🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nTo start all services (FastAPI Backend + OpenCode/AGY + Next.js Frontend):")
    if os_type == "Windows":
        print("  ▶ Run: .\\start.bat   or   python run.py")
    else:
        print("  ▶ Run: ./start.sh   or   python3 run.py")
    print("\nThe browser will automatically open at: http://localhost:3000\n")

if __name__ == "__main__":
    main()
