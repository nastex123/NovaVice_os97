# ADR-006: Lanzador Supervisor Unificado y Suite de Instalación Multiplataforma

- **ID:** ADR-006
- **Título:** Arquitectura de Supervisión de Procesos y Suite de Instalación Multiplataforma para Windows y Linux
- **Fecha:** 2026-08-30 (America/Bogota)
- **Estado:** Accepted
- **Autores:** AI Backend & Full Stack Engineering Team

---

## 1. Contexto
El sistema completo requiere la ejecución coordinada de tres servicios independientes:
1. **OpenCode Daemon:** Servidor de razonamiento en puerto 4096.
2. **FastAPI Backend:** API REST y motor RAG en puerto 8000.
3. **Next.js Frontend:** Aplicación web en puerto 3000.

---

## 2. Problema
Exigir al evaluador o usuario abrir manualmente tres terminales separadas para ejecutar comandos independientes (`opencode serve`, `uvicorn`, `npm run dev`) es propenso a errores, genera fricción y a menudo deja procesos huérfanos o puertos bloqueados al cerrar la sesión.

---

## 3. Opciones Consideradas
1. **Opción A (Instrucciones Manuales):** Documentar en el README comandos independientes para 3 terminales. (Rechazada por mala experiencia de usuario).
2. **Opción B (Docker Compose Exclusivo):** Requerir Docker Desktop obligatorio. (Rechazada porque muchos evaluadores o entornos locales no tienen Docker instalado o habilitado).
3. **Opción C (Seleccionada - Supervisor en Python + Scripts Nativos):** Implementar:
   - `run.py`: Supervisor en Python que lanza los 3 subprocesos (`subprocess.Popen`), captura señales `SIGINT` / `Ctrl+C`, realiza terminación limpia en árbol (`taskkill /F /T` en Windows / `os.killpg` en Linux) y abre automáticamente el navegador en `http://localhost:3000`.
   - `installer.py`: Instalador interactivo con detección automática de SO y validación de requisitos.
   - Envoltorios nativos: `start.bat` e `install.bat` (Windows), `start.sh` e `install.sh` (Linux/macOS).

---

## 4. Decisión
Adoptar la arquitectura de supervisión basada en `run.py` e `installer.py`:
- Los scripts `.bat` y `.sh` actúan como ejecutables de un solo clic que invocan los scripts de Python correspondientes.
- `installer.py` realiza la creación del entorno virtual `venv`, instalación de `requirements.txt`, indexación inicial del RAG e instalación de paquetes en `frontend/`.
- `run.py` monitorea los 3 puertos (:4096, :8000, :3000), valida su estado y garantiza un cierre sincronizado y limpio sin puertos ocupados.

---

## 5. Justificación
- **Experiencia de Inicio Inmediata:** Doble clic en `install.bat` / `start.bat` o `./install.sh` / `./start.sh` y todo el ecosistema queda funcionando.
- **Tolerancia a Fallos:** Si el usuario presiona `Ctrl+C`, el supervisor finaliza los tres procesos secundarios inmediatamente.
- **Independencia de Plataforma:** Funciona nativamente en Windows 10/11, Linux (Ubuntu, Debian, Fedora) y macOS.

---

## 6. Consecuencias

### Positivas:
- Cero fricción para evaluadores técnicos y usuarios finales.
- Prevención de puertos bloqueados por procesos zombi.
- Pruebas automatizadas en `tests/test_executables.py` que validan la integridad de los scripts.

### Negativas / Mitigaciones:
- Requiere permisos para invocar subprocesos en el sistema operativo, los cuales son estándar en entornos de desarrollo.
