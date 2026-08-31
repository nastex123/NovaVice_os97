#!/usr/bin/env python3
"""
Nova Tech University - Admissions Assistant RAG
Unified Multi-Process Program Launcher
Launches:
 1. OpenCode Daemon (:4096)
 2. FastAPI Backend Core (:8000)
 3. Next.js + PixiJS Frontend (:3000)
"""

import os
import sys
import time
import signal
import platform
import shutil
import subprocess
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
VENV_DIR = BASE_DIR / "venv"

IS_WINDOWS = platform.system() == "Windows"
processes = []

def get_python_executable():
    if IS_WINDOWS:
        candidate = VENV_DIR / "Scripts" / "python.exe"
    else:
        candidate = VENV_DIR / "bin" / "python"
    
    if candidate.exists():
        return str(candidate)
    return sys.executable

def start_opencode():
    opencode_bin = shutil.which("opencode")
    if opencode_bin:
        print("[1/3] 🤖 Iniciando Servidor OpenCode en http://127.0.0.1:4096 ...")
        cmd = ["opencode", "serve", "--port", "4096"]
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=IS_WINDOWS
        )
        processes.append(("OpenCode Daemon", p))
        return True
    else:
        print("[1/3] ℹ️ OpenCode no está instalado en PATH. Se usará el modo dinámico de contingencia.")
        return False

def start_fastapi(py_exec):
    print("[2/3] 🐍 Iniciando Backend FastAPI en http://127.0.0.1:8000 ...")
    cmd = [py_exec, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"]
    p = subprocess.Popen(
        cmd,
        cwd=str(BASE_DIR),
        shell=IS_WINDOWS
    )
    processes.append(("FastAPI Backend", p))

def start_nextjs():
    if FRONTEND_DIR.exists() and (FRONTEND_DIR / "package.json").exists():
        print("[3/3] ⚡ Iniciando Frontend Moderno Next.js + PixiJS en http://localhost:3000 ...")
        cmd = ["npm", "run", "dev"]
        p = subprocess.Popen(
            cmd,
            cwd=str(FRONTEND_DIR),
            shell=True
        )
        processes.append(("Next.js Frontend", p))
        return True
    else:
        print("[3/3] ℹ️ Frontend Next.js no detectado; utilizando la interfaz web estática en http://127.0.0.1:8000")
        return False

def wait_and_open_browser(has_nextjs):
    time.sleep(3)
    target_url = "http://localhost:3000" if has_nextjs else "http://127.0.0.1:8000"
    print(f"\n✨ ¡Todos los servicios han iniciado con éxito!")
    print(f"🌐 Abriendo aplicación en tu navegador: {target_url}")
    print("=" * 70)
    print("  Presiona Ctrl+C en cualquier momento para detener todos los servicios.")
    print("=" * 70)
    try:
        webbrowser.open(target_url)
    except Exception:
        pass

def cleanup_processes(signum=None, frame=None):
    print("\n\n🛑 Deteniendo todos los servicios de Nova Tech University...")
    for name, p in processes:
        try:
            print(f"  [-] Cerrando {name}...")
            if IS_WINDOWS:
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                p.terminate()
                p.wait(timeout=2)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass
    print("✓ Todos los servicios se han detenido limpiamente. ¡Hasta pronto!\n")
    sys.exit(0)

def main():
    print("=" * 70)
    print("  🎓 NOVA TECH UNIVERSITY - LANZADOR DEL SISTEMA COMPLETO")
    print("=" * 70)

    # Register exit signal handlers
    signal.signal(signal.SIGINT, cleanup_processes)
    signal.signal(signal.SIGTERM, cleanup_processes)

    py_exec = get_python_executable()

    start_opencode()
    start_fastapi(py_exec)
    has_nextjs = start_nextjs()

    wait_and_open_browser(has_nextjs)

    try:
        # Keep supervisor alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup_processes()

if __name__ == "__main__":
    main()
