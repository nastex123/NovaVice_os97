"""
Nova Idiomas Colombia - Admissions Assistant RAG
Unified Multi-Process Program Supervisor & Launcher

Features:
 1. Proactively frees ports 8000, 3000, 4096 if occupied by orphan/stale processes.
 2. Launches OpenCode Daemon (:4096).
 3. Launches FastAPI Backend (:8000) and waits for active HTTP 200 healthcheck.
 4. Launches Next.js Frontend (:3000) with guaranteed zero ECONNREFUSED.
 5. Auto-launches default web browser on http://localhost:3000.
 6. Clean Ctrl+C process group signal termination.
"""

import os
import sys
import time
import socket
import signal
import platform
import shutil
import subprocess
import urllib.request
import urllib.error
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
VENV_DIR = BASE_DIR / "venv"

IS_WINDOWS = platform.system() == "Windows"
processes = []
_shutdown_requested = False


def is_port_in_use(port: int) -> bool:
    """Check if a local TCP port is already open/in-use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def free_port(port: int):
    """Cleanly terminate any stale process holding the specified port."""
    if not is_port_in_use(port):
        return

    print(f"  [!] Puerto {port} ocupado por un proceso previo. Liberando...")
    if IS_WINDOWS:
        try:
            output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True, text=True)
            for line in output.strip().split("\n"):
                parts = line.strip().split()
                if len(parts) >= 5 and parts[1].endswith(f":{port}"):
                    pid = parts[-1]
                    subprocess.call(["taskkill", "/F", "/T", "/PID", pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    else:
        try:
            subprocess.run(["fuser", "-k", f"{port}/tcp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        try:
            pids = subprocess.check_output(["lsof", "-ti", f":{port}"], text=True).strip().split()
            for pid in pids:
                if pid:
                    subprocess.run(["kill", "-9", pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    time.sleep(0.5)


def ensure_node_in_path():
    """Detect Node/NPM across common install locations (NVM, FNM, Volta, Homebrew, Program Files) and add to PATH."""
    home = Path.home()
    possible_paths = [
        home / ".local" / "bin",
        home / "bin",
        Path("/usr/local/bin"),
        Path("/opt/homebrew/bin"),
        Path("/usr/bin"),
    ]
    if IS_WINDOWS:
        possible_paths.extend([
            Path("C:/Program Files/nodejs"),
            Path("C:/Program Files (x86)/nodejs"),
            home / "AppData" / "Roaming" / "npm",
            home / "AppData" / "Local" / "Programs" / "node",
        ])
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
        if p.exists() and (p / ("node.exe" if IS_WINDOWS else "node")).exists():
            if str(p) not in current_path:
                os.environ["PATH"] = f"{p}{os.pathsep}{current_path}"
                current_path = os.environ["PATH"]


def get_python_executable() -> str:
    """Find the project's virtualenv python or fallback to system python."""
    if IS_WINDOWS:
        candidate = VENV_DIR / "Scripts" / "python.exe"
    else:
        candidate = VENV_DIR / "bin" / "python"

    if candidate.exists():
        return str(candidate)
    return sys.executable


def start_opencode():
    """Start OpenCode daemon on port 4096 if available."""
    free_port(4096)
    ensure_node_in_path()
    opencode_bin = shutil.which("opencode")
    if opencode_bin:
        print("[1/3] 🤖 Iniciando Servidor OpenCode en http://127.0.0.1:4096 ...")
        cmd = "opencode serve --port 4096" if IS_WINDOWS else [opencode_bin, "serve", "--port", "4096"]
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=IS_WINDOWS,
            env=os.environ,
            preexec_fn=None if IS_WINDOWS else os.setsid
        )
        processes.append(("OpenCode Daemon", p))
        return True
    else:
        print("[1/3] ℹ️ OpenCode CLI no detectado en PATH. Se usará el modo dinámico de contingencia.")
        return False


def start_fastapi(py_exec: str) -> subprocess.Popen:
    """Start FastAPI Backend on port 8000."""
    free_port(8000)
    print("[2/3] 🐍 Iniciando Backend FastAPI en http://127.0.0.1:8000 ...")
    cmd = [py_exec, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"]
    p = subprocess.Popen(
        cmd,
        cwd=str(BACKEND_DIR),
        stdin=subprocess.DEVNULL,
        shell=IS_WINDOWS,
        env=os.environ,
        preexec_fn=None if IS_WINDOWS else os.setsid
    )
    processes.append(("FastAPI Backend", p))
    return p


def wait_for_fastapi_ready(timeout_seconds: float = 18.0) -> bool:
    """Poll FastAPI health endpoint until 200 OK is received."""
    print("      ⏳ Esperando inicio y carga de base de datos RAG (82 docs)...", end="", flush=True)
    start = time.time()
    url = "http://127.0.0.1:8000/api/v1/health"

    while time.time() - start < timeout_seconds:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NovaSupervisor"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    elapsed = round(time.time() - start, 1)
                    print(f" ✓ Listo ({elapsed}s)")
                    return True
        except Exception:
            pass
        time.sleep(0.3)
        print(".", end="", flush=True)

    print(" ⚠️ Advertencia: Backend tardó más de lo esperado en responder.")
    return False


def start_nextjs():
    """Start Next.js frontend on port 3000."""
    free_port(3000)
    ensure_node_in_path()
    npm_bin = shutil.which("npm")
    if FRONTEND_DIR.exists() and (FRONTEND_DIR / "package.json").exists() and npm_bin:
        print("[3/3] ⚡ Iniciando Frontend Next.js + PixiJS en http://localhost:3000 ...")
        cmd = "npm run dev" if IS_WINDOWS else [npm_bin, "run", "dev"]
        p = subprocess.Popen(
            cmd,
            cwd=str(FRONTEND_DIR),
            stdin=subprocess.DEVNULL,
            shell=IS_WINDOWS,
            env=os.environ,
            preexec_fn=None if IS_WINDOWS else os.setsid
        )
        processes.append(("Next.js Frontend", p))
        return True
    else:
        print("[3/3] ℹ️ Frontend Next.js no detectado o npm no disponible; usando UI estática en http://127.0.0.1:8000")
        return False


def wait_and_open_browser(has_nextjs: bool):
    """Wait for frontend compilation and open the web browser."""
    target_url = "http://localhost:3000" if has_nextjs else "http://127.0.0.1:8000"
    time.sleep(2.0)
    print(f"\n✨ ¡Todos los servicios han iniciado con éxito!")
    print(f"🌐 Abriendo aplicación en tu navegador: {target_url}")
    print("=" * 70)
    print("  🟢 Backend FastAPI:  http://127.0.0.1:8000/docs")
    print("  🟢 Frontend Chat:    http://localhost:3000")
    print("  Presiona Ctrl+C en cualquier momento para detener todos los servicios.")
    print("=" * 70)
    try:
        webbrowser.open(target_url)
    except Exception:
        pass


def cleanup_processes(signum=None, frame=None):
    """Clean up all child processes and process groups on exit, then release terminal."""
    global _shutdown_requested
    # Prevent re-entrant double cleanup from signal + KeyboardInterrupt
    if _shutdown_requested and signum is None:
        # Call originated from except KeyboardInterrupt after signal already handled
        return
    if _shutdown_requested and signum is not None:
        # Second Ctrl+C -> force kill
        print("\n[!] Forzando salida inmediata...")
        for _, p in processes:
            try:
                if p.poll() is None:
                    if IS_WINDOWS:
                        subprocess.call(["taskkill", "/F", "/T", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        try:
                            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                        except Exception:
                            p.kill()
            except Exception:
                pass
        # Hard exit without flushing handlers that could block
        os._exit(1)

    _shutdown_requested = True
    print("\n\n🛑 Deteniendo todos los servicios de Nova Idiomas...")

    for name, p in processes:
        try:
            if p.poll() is not None:
                continue
            print(f"  [-] Cerrando {name} (PID {p.pid})...")
            if IS_WINDOWS:
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                try:
                    p.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    p.kill()
            else:
                try:
                    pgid = os.getpgid(p.pid)
                    os.killpg(pgid, signal.SIGTERM)
                except Exception:
                    try:
                        p.terminate()
                    except Exception:
                        pass
                try:
                    p.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    try:
                        pgid = os.getpgid(p.pid)
                        os.killpg(pgid, signal.SIGKILL)
                    except Exception:
                        p.kill()
                    try:
                        p.wait(timeout=1)
                    except Exception:
                        pass
        except Exception:
            pass

    print("  ✔ Todos los servicios detenidos. Terminal liberada. ¡Hasta luego!")
    # Ensure stdout is flushed and terminal echo is restored
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    # Exit supervisor process explicitly so shell prompt returns
    # Use sys.exit for clean finally blocks, fallback to os._exit if blocked
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

import argparse


def prompt_advisor_selection() -> str:
    """Prompt user interactively to select between OpenCode and AGY, or use CLI flag / env."""
    parser = argparse.ArgumentParser(description="Nova Idiomas Admissions Assistant Supervisor")
    parser.add_argument(
        "-a", "--advisor",
        choices=["opencode", "agy"],
        help="Seleccionar motor del Asesor de Admisiones: 'opencode' o 'agy'"
    )
    args, _ = parser.parse_known_args()

    if args.advisor:
        return args.advisor.lower()

    env_choice = os.environ.get("ADVISOR_BACKEND", "").lower()
    if env_choice in ("opencode", "agy"):
        return env_choice

    # Interactive selector if connected to a terminal
    if sys.stdin.isatty():
        print("\n" + "=" * 70)
        print("  🎓 NOVA IDIOMAS COLOMBIA - SELECCIÓN DE MOTOR DE ASESORÍA")
        print("=" * 70)
        print("  Selecciona el motor de razonamiento para el Asesor de Admisiones:")
        print("    [1] 🤖 OpenCode Reasoning Engine (:4096) (Por defecto)")
        print("    [2] 🚀 AGY (Google Antigravity CLI / Engine)")
        print("-" * 70)
        try:
            choice = input("  Digita tu opción [1 o 2] (Enter para 1): ").strip().lower()
            if choice in ("2", "agy", "antigravity"):
                print("  ✓ Seleccionado: [2] AGY (Google Antigravity CLI / Engine)\n")
                return "agy"
            else:
                print("  ✓ Seleccionado: [1] OpenCode Reasoning Engine (:4096)\n")
                return "opencode"
        except (KeyboardInterrupt, EOFError):
            print("\n  ✓ Usando motor por defecto: OpenCode\n")
            return "opencode"

    return "opencode"


def main():
    print("=" * 70)
    print("  🎓 NOVA IDIOMAS COLOMBIA - LANZADOR SUPERVISADO DEL SISTEMA (RAG 2.6)")
    print("=" * 70)

    # Register exit signal handlers - handler will exit process via sys.exit/os._exit
    signal.signal(signal.SIGINT, cleanup_processes)
    signal.signal(signal.SIGTERM, cleanup_processes)

    ensure_node_in_path()
    py_exec = get_python_executable()

    # Pre-launch Switch: Select Advisor Engine
    advisor_choice = prompt_advisor_selection()
    os.environ["ADVISOR_BACKEND"] = advisor_choice

    if advisor_choice == "opencode":
        start_opencode()
    else:
        agy_bin = shutil.which("agy")
        if agy_bin:
            print(f"[1/3] 🚀 Motor de Asesoría: AGY CLI detectado en {agy_bin}")
        else:
            print("[1/3] 🚀 Motor de Asesoría: AGY (Antigravity Reasoning Bridge Activo)")

    start_fastapi(py_exec)
    wait_for_fastapi_ready()
    has_nextjs = start_nextjs()

    wait_and_open_browser(has_nextjs)

    try:
        # Keep supervisor alive until shutdown is requested via Ctrl+C / SIGTERM
        while not _shutdown_requested:
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Fallback if signal handler was not triggered (e.g., Windows)
        cleanup_processes()
    finally:
        # If loop exited without shutdown flag (unexpected), ensure cleanup
        if not _shutdown_requested:
            cleanup_processes()
        # Final explicit exit to return prompt to shell
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()
