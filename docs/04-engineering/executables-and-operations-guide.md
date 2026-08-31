# Guía Técnica de Ejecutables, Instalador y Supervisor de Procesos

- **Documento:** `docs/04-engineering/executables-and-operations-guide.md`
- **Versión:** 2.6.0
- **Fecha:** 2026-08-30 (America/Bogota)
- **Archivos:** `run.py`, `installer.py`, `start.bat`, `install.bat`, `start.sh`, `install.sh`

---

## 1. Arquitectura de Supervisión y Control de Procesos

Para ofrecer una experiencia de arranque inmediata de un solo clic, el proyecto incluye un supervisor en Python que controla concurrentemente los tres subprocesos del sistema:

```text
                               [Usuario / Evaluador]
                                         │
                         (start.bat / start.sh / python run.py)
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │   Supervisor de Procesos (run.py)     │
                     └───────────────────┬───────────────────┘
                                         │
           ┌─────────────────────────────┼─────────────────────────────┐
           │                             │                             │
           ▼                             ▼                             ▼
┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│ OpenCode Daemon     │       │ FastAPI Backend     │       │ Next.js Frontend    │
│ Puerto 4096         │       │ Puerto 8000         │       │ Puerto 3000         │
│ opencode serve      │       │ uvicorn src.main:app│       │ npm run dev         │
└─────────────────────┘       └─────────────────────┘       └─────────────────────┘
           │                             │                             │
           └─────────────────────────────┼─────────────────────────────┘
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │ Apertura Automática del Navegador     │
                     │ http://localhost:3000                 │
                     │ Cierre Limpio ante SIGINT / Ctrl+C    │
                     └───────────────────────────────────────┘
```

---

## 2. Código Fuente de los Ejecutables y Funcionamiento

### 2.1 `run.py` — Supervisor Multi-Proceso y Captura de Señales
Monitorea la disponibilidad de puertos, lanza los subprocesos y captura la señal de interrupción del teclado para cerrar los tres servidores de forma sincronizada.

```python
# run.py (Fragmento clave)
import subprocess
import signal
import sys
import os
import webbrowser
import time

processes = []

def cleanup_processes(signum=None, frame=None):
    print("\n🛑 Cerrando todos los servicios de forma limpia...")
    for p in processes:
        if p and p.poll() is None:
            if os.name == "nt":
                # Terminación en árbol forzada para Windows
                subprocess.run(f"taskkill /F /T /PID {p.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                p.terminate()
    print("✨ Todos los procesos han finalizado exitosamente.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup_processes)
signal.signal(signal.SIGTERM, cleanup_processes)
```
* **Para qué sirve:** Evita tener que abrir tres terminales manuales y previene que queden procesos huérfanos o puertos ocupados al cerrar la consola.
* **Optimización Aplicada:**
  - En Windows, utiliza `taskkill /F /T` para asegurar que tanto el proceso padre como los subprocesos de Node.js y Python se terminen por completo.
  - Verifica mediante sockets TCP (`is_port_in_use`) antes de intentar abrir cada puerto.
  - Abre automáticamente el navegador predeterminado en `http://localhost:3000`.

---

### 2.2 `installer.py` — Instalador Interactivo Multiplataforma
Detecta el sistema operativo, valida las versiones de Python y Node.js, crea el entorno virtual e instala todas las dependencias.

```python
# installer.py (Fragmento clave)
import platform
import subprocess
import sys
import shutil

def detect_os():
    system = platform.system().lower()
    if "windows" in system: return "windows"
    elif "linux" in system: return "linux"
    elif "darwin" in system: return "macos"
    return "unknown"

def main():
    detected = detect_os()
    print(f"Sistema detectado: {detected.upper()}")
    # 1. Crear entorno virtual: python -m venv venv
    # 2. Instalar requirements.txt: pip install -r requirements.txt
    # 3. Indexar base de datos RAG inicial: python -m src.rag.ingestion
    # 4. Instalar paquetes de frontend: cd frontend && npm install
    ...
```
* **Para qué sirve:** Configura el entorno de ejecución desde cero con un solo comando o doble clic.
* **Por qué se diseñó así:** Permite a cualquier evaluador técnico clonar el repositorio y dejar todo funcionando en menos de 2 minutos sin configuraciones manuales complejas.

---

### 2.3 Envoltorios de Ejecución Rápida

| Script | Sistema Operativo | Comando Interno |
| :--- | :--- | :--- |
| `install.bat` | Windows | `@echo off` ➔ Ejecuta `python installer.py` con pausa final. |
| `start.bat` | Windows | `@echo off` ➔ Ejecuta `python run.py`. |
| `install.sh` | Linux / macOS | `#!/usr/bin/env bash` ➔ Da permisos y ejecuta `python3 installer.py`. |
| `start.sh` | Linux / macOS | `#!/usr/bin/env bash` ➔ Ejecuta `python3 run.py`. |
