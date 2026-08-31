#!/usr/bin/env python3
"""
Nova Tech University - Admissions Assistant RAG
Cross-Platform Interactive Installer (Windows / Linux / macOS)
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
VENV_DIR = BASE_DIR / "venv"

def print_banner():
    print("=" * 70)
    print("  🎓 NOVA TECH UNIVERSITY - ASISTENTE INTELIGENTE DE ADMISIONES (RAG)")
    print("  🚀 INSTALADOR AUTOMÁTICO MULTIPLATAFORMA (WINDOWS / LINUX / MACOS)")
    print("=" * 70)

def detect_or_ask_os():
    detected = platform.system()
    print(f"\n[+] Sistema operativo detectado automáticamente: {detected}")
    print("\nPor favor confirma o selecciona tu sistema operativo:")
    print("  [1] Windows")
    print("  [2] Linux / macOS")
    
    choice = input("\nDigita una opción [1 o 2, Enter para autodetectar]: ").strip()
    if choice == "1":
        return "Windows"
    elif choice == "2":
        return "Linux"
    return detected

def check_prerequisites():
    print("\n--- Verificando Requisitos Previos ---")
    # Check Python version
    py_ver = sys.version_info
    print(f"[✓] Python {py_ver.major}.{py_ver.minor}.{py_ver.micro} detectado.")
    if py_ver < (3, 10):
        print("[!] ERROR: Se requiere Python 3.10 o superior.")
        sys.exit(1)
        
    # Check Node.js and npm
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    
    if not node_path or not npm_path:
        print("[!] ADVERTENCIA: Node.js o npm no fueron encontrados en el PATH del sistema.")
        print("    Para ejecutar el frontend moderno en Next.js, por favor instala Node.js (v18+).")
    else:
        try:
            node_v = subprocess.check_output([node_path, "-v"], text=True).strip()
            npm_v = subprocess.check_output([npm_path, "-v"], text=True).strip()
            print(f"[✓] Node.js {node_v} y npm {npm_v} detectados.")
        except Exception:
            pass

def setup_python_environment(os_type):
    print("\n--- Configurando Entorno Virtual de Python ---")
    if not VENV_DIR.exists():
        print("[+] Creando entorno virtual 'venv'...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        print("[✓] Entorno virtual creado exitosamente.")
    else:
        print("[✓] Entorno virtual 'venv' ya existe.")

    if os_type == "Windows":
        py_bin = VENV_DIR / "Scripts" / "python.exe"
        pip_bin = VENV_DIR / "Scripts" / "pip.exe"
    else:
        py_bin = VENV_DIR / "bin" / "python"
        pip_bin = VENV_DIR / "bin" / "pip"

    # Install Python dependencies
    req_file = BASE_DIR / "requirements.txt"
    if req_file.exists():
        print(f"\n[+] Instalando dependencias de Python desde requirements.txt...")
        subprocess.check_call([str(py_bin), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(py_bin), "-m", "pip", "install", "-r", str(req_file)])
        print("[✓] Dependencias de Python instaladas con éxito.")

    # Ingest Knowledge Base
    print("\n--- Indexando Base de Conocimiento RAG (87 Documentos Oficiales) ---")
    try:
        subprocess.check_call([str(py_bin), "-m", "src.rag.ingestion"], cwd=str(BASE_DIR))
        print("[✓] 87 Documentos Oficiales indexados en ChromaDB y BM25.")
    except Exception as e:
        print(f"[!] Error indexando documentos: {e}")

def setup_frontend_environment():
    if not FRONTEND_DIR.exists():
        return

    print("\n--- Configurando Frontend en Next.js + PixiJS ---")
    npm_path = shutil.which("npm")
    if npm_path:
        print("[+] Instalando paquetes de Node.js (Next.js, PixiJS, Tailwind CSS, Lucide, Framer Motion)...")
        try:
            subprocess.check_call(["npm", "install"], cwd=str(FRONTEND_DIR), shell=True)
            print("[✓] Dependencias del Frontend instaladas con éxito.")
        except Exception as e:
            print(f"[!] Error instalando dependencias de npm: {e}")
    else:
        print("[!] Omitiendo 'npm install' porque npm no está disponible en este momento.")

def check_opencode():
    print("\n--- Verificando Servidor OpenCode ---")
    opencode_path = shutil.which("opencode")
    if opencode_path:
        print("[✓] OpenCode CLI detectado en el sistema.")
    else:
        print("[i] OpenCode CLI no detectado globalmente.")
        print("    El sistema utilizará síntesis de contingencia instantánea o puedes instalarlo con:")
        print("    npm install -g opencode-ai")

def main():
    print_banner()
    os_type = detect_or_ask_os()
    print(f"\n[+] Procediendo con instalación optimizada para: {os_type}")
    
    check_prerequisites()
    setup_python_environment(os_type)
    setup_frontend_environment()
    check_opencode()
    
    print("\n" + "=" * 70)
    print("  🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!")
    print("=" * 70)
    print("\nPara iniciar todo el sistema (Backend FastAPI + OpenCode + Frontend Next.js):")
    if os_type == "Windows":
        print("  ▶ Ejecuta: .\\start.bat   o   python run.py")
    else:
        print("  ▶ Ejecuta: ./start.sh   o   python3 run.py")
    print("\nEl navegador se abrirá automáticamente en: http://localhost:3000\n")

if __name__ == "__main__":
    main()
