# Instructivo de Uso y Manual de Usuario de la Solución de Software
## Sistema de Asistencia Inteligente de Admisiones: "Nova OS '97"
### Evidencia de Producto 2 — Norma SENA 220501096

- **Programa de Formación:** Análisis y Desarrollo de Software (ADSO)
- **Norma de Competencia:** 220501096 — *Desarrollar solución de software de acuerdo con especificaciones de diseño y marcos de referencia.*
- **Candidato / Aprendiz:** `[Nombre del Aprendiz]`
- **Documento de Identidad:** `[C.C. / T.I. Número]`
- **Organización Beneficiaria:** Nova Idiomas Colombia
- **Fecha de Elaboración:** 2026-09-02 (Zona Horaria: `America/Bogota`)
- **Versión del Manual:** v2.6.0

---

## 1. Requisitos Técnicos del Sistema

Antes de iniciar la instalación o ejecución de la plataforma, verifique que la máquina host cumpla con los siguientes requerimientos:

### 1.1 Requisitos de Software
- **Sistema Operativo:** Windows 10/11 (64-bit), Ubuntu 20.04+ LTS / Debian 11+, o macOS 12+ (Monterey o superior).
- **Python:** Versión **3.10 o superior** (asegurar que la casilla *"Add Python to PATH"* esté marcada durante la instalación).
- **Node.js:** Versión **18.17.0+ LTS o 20.x+** (incluye gestor de paquetes `npm` 9+).
- **Git:** Versión 2.30+ para clonación del repositorio.
- **Navegador Web Recomendado:** Google Chrome, Microsoft Edge, Mozilla Firefox o Brave (con soporte para WebGL 2.0).

### 1.2 Requisitos Mínimos de Hardware
- **Procesador (CPU):** 2 núcleos a 2.0 GHz o superior (arquitectura x86_64 o Apple Silicon M1/M2/M3).
- **Memoria RAM:** Mínimo 4 GB de memoria RAM (recomendado 8 GB para ejecución concurrente de tests e inferencia).
- **Almacenamiento en Disco:** Al menos 1 GB de espacio libre disponible.
- **Conectividad:** Conexión a Internet para la descarga inicial de paquetes de dependencias (`pip` y `npm`).

---

## 2. Pasos para la Instalación del Sistema

El proyecto cuenta con una suite de scripts automatizados que detectan el sistema operativo e instalan todas las dependencias con un solo comando.

### 2.1 Método A: Instalación Automática en Windows (Recomendado)
1. Abra la carpeta raíz del proyecto clonado `NovaVice_os97/`.
2. Haga **doble clic** sobre el archivo ejecutable:
   ```cmd
   install.bat
   ```
3. El script ejecutará automáticamente `python installer.py`, el cual realizará:
   - Verificación de versiones de Python y Node.js.
   - Creación del entorno virtual aislado `venv/`.
   - Instalación de dependencias del backend: `pip install -r backend/requirements.txt`.
   - Indexación inicial de la base de conocimiento vectorial en `backend/data/chroma_db/`.
   - Instalación de módulos del frontend: `cd frontend && npm install`.
4. Al finalizar, la consola mostrará un mensaje indicando que el entorno está listo para ser ejecutado.

### 2.2 Método B: Instalación en Linux / macOS
1. Abra una terminal en la raíz del proyecto y asigne permisos de ejecución:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

---

## 3. Pasos para la Ejecución del Sistema

Para brindar la máxima comodidad al usuario o evaluador técnico, se diseñó el supervisor de procesos **`run.py`**, el cual lanza los servidores concurrentemente y abre el navegador sin necesidad de abrir múltiples terminales manuales.

### 3.1 Puesta en Marcha en un Clic
- **En Windows:** Haga doble clic en `start.bat` o ejecute en consola:
  ```cmd
  start.bat
  ```
- **En Linux / macOS:** Ejecute en terminal:
  ```bash
  ./start.sh
  ```

### 3.2 ¿Qué ocurre internamente durante el arranque?
El supervisor `run.py` realiza las siguientes acciones sincronizadas:
1. Valida que los puertos **8000** (FastAPI) y **3000** (Next.js) se encuentren disponibles.
2. Inicia el backend de FastAPI con servidor Uvicorn en segundo plano (`http://127.0.0.1:8000`).
3. Inicia la aplicación web Next.js 15 en modo desarrollo (`npm run dev`).
4. Espera a que ambos servicios respondan con código HTTP 200 en sus chequeos de salud (`/health`).
5. Abre automáticamente el navegador predeterminado del sistema operativo en:
   ```text
   http://localhost:3000
   ```
6. **Cierre Limpio (Graceful Shutdown):** Al presionar `Ctrl + C` en la terminal, el supervisor captura la señal `SIGINT` y finaliza en árbol todos los subprocesos de Python y Node.js sin dejar puertos bloqueados ni procesos zombi.

---

## 4. Manual de Funcionalidades Principales

### 4.1 Navegación Guiada por Menús Determinísticos
Al ingresar al sistema, el usuario visualiza el menú principal de bienvenida con 4 pilares:

```text
1️⃣ Cursos & Idiomas       : Inglés, Francés, Alemán, Portugués y certificaciones.
2️⃣ Horarios & Franjas     : Madrugadores, Diurnos, Nocturnos y Sabatinos.
3️⃣ Precios & Descuentos   : Tarifas en COP, 10% Contado, 15% Cajas de compensación.
4️⃣ Sedes & Ubicaciones    : Bogotá (Chicó/Chapinero), Medellín, Cali y Virtual.
```

- **Cómo utilizarlo:**
  - El usuario puede escribir simplemente el número del pilar (ej. `1`, `2`, `3` o `4`) en la caja de texto y presionar `Enter`.
  - También puede hacer clic directamente sobre los botones rápidos situados encima de la barra de entrada.
  - Para regresar al inicio en cualquier momento, escriba `0` o `menu`.

---

### 4.2 Consultas Libres en Lenguaje Natural con RAG Híbrido
El usuario puede formular cualquier inquietud abierta relacionada con la academia:

- **Ejemplo 1 (Horarios):** *"¿Qué opciones de horario tienen en la noche para estudiar inglés en Bogotá?"*
  - **Respuesta:** El sistema recupera los fragmentos oficiales y detalla la franja *After Work* (6:30 PM a 8:30 PM de lunes a jueves) en las sedes Chicó y Chapinero.
- **Ejemplo 2 (Precios y Descuentos):** *"¿Cuánto vale el curso intensivo y qué descuento tienen con Compensar?"*
  - **Respuesta:** El sistema cotiza la tarifa plena ($650.000 COP), calcula el 15% de descuento por convenio de caja de compensación ($97.500 COP) y entrega el valor neto final a pagar ($552.500 COP).
- **Ejemplo 3 (Política de Becas):** *"¿Tienen becas del 100%?"*
  - **Respuesta:** El guardrail institucional aclara que Nova Idiomas no ofrece becas universitarias de mérito, pero orienta al aspirante hacia los descuentos formales vigentes (10% de contado, 15% familiar/cajas y bono de $100.000 COP).

---

### 4.3 Control de Ergonomía Visual: Filtro CRT Óptico
- En la esquina superior derecha de la barra de título retro se encuentra el botón conmutador:
  ```text
  [CRT SCANLINES: ON / OFF]
  ```
- Al hacer clic, el usuario puede alternar instantáneamente entre la experiencia retro con líneas de escaneo y brillo fosforescente, y un modo moderno nítido de alta definición, garantizando accesibilidad y descanso visual.

---

### 4.4 Agendamiento del Examen de Clasificación (Placement Test)
1. Haga clic en el botón de acción rápida **`[🎯 Agendar Test]`** o escriba *"quiero agendar examen"*.
2. Se desplegará el modal interactivo de reserva.
3. Ingrese su nombre, correo electrónico, número de teléfono/WhatsApp, idioma de interés y seleccione la sede preferida (presencial o virtual).
4. Seleccione la fecha y franja horaria deseada.
5. Presione **"Confirmar y Agendar Cita"**. El sistema generará el registro en la base de datos y le enviará un mensaje de confirmación inmediato.

---

### 4.5 Solicitud de Asesor Humano y Escalamiento en Dos Fases
Cuando una consulta requiere soporte comercial avanzado o el usuario prefiere atención humana:
1. El aspirante hace clic en **`[👨‍💼 Asesor Humano]`** o formula una pregunta que cae bajo el umbral de confianza ($<0.35$).
2. El sistema aplica la **Fase 1**: Muestra el mejor fragmento normativo y pregunta explícitamente:
   > *"Esta consulta requiere validación oficial. ¿Deseas ser contactado por un asesor humano? [Sí / No]"*
3. Al presionar **"Sí"**, se activa la **Fase 2**: El sistema genera un ticket único estructurado:
   ```text
   Ticket Radicado: ESC-20260902-8F12
   Estado: Pendiente
   Canal de Contacto: WhatsApp (+57 312 456 7890)
   ```
4. El caso queda automáticamente registrado en `backend/data/escalations.json` para ser gestionado por el equipo de admisiones.

---

### 4.6 Inspección de Métricas y Rendimiento en Tiempo Real
1. En la barra de menú superior, haga clic en la opción **`[MÉTRICAS]`**.
2. Se desplegará el cuadro de telemetría institucional que expone:
   - **Total de Consultas Procesadas:** Contador acumulado de interacciones.
   - **Porcentaje de Aciertos en Caché (Hit Rate):** Proporción de consultas resueltas en sub-30ms.
   - **Latencia Promedio:** Tiempo de respuesta medio en milisegundos.
   - **Tasa de Escalamiento Humano:** Porcentaje de consultas derivadas a tickets de soporte.
   - **Estado de Salud de los Servicios:** Indicadores en verde para FastAPI (:8000) y Next.js (:3000).

---

## 5. Representación Visual de las Vistas del Sistema

### Vista 1: Interfaz Principal de Conversación en Modo CRT

```text
+---------------------------------------------------------------------------------------+
| [X] NOVA IDIOMAS OS '97 - ASISTENTE DE ADMISIONES                   [-] [口] [X]      |
+---------------------------------------------------------------------------------------+
| ARCHIVO   CONSULTAS   OFERTA   METRICAS   AYUDA                  HORA: 10:50 AM       |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  [SISTEMA]: Sesion iniciada correctamente con FastAPI Core.                           |
|                                                                                       |
|  [ASISTENTE]: Bienvenido a Nova Idiomas Colombia. ¿En que podemos orientarte hoy?     |
|   1. Programas y Cursos de Idiomas (Ingles, Frances, Aleman, Portugues)               |
|   2. Franjas Horarias (Madrugadores, Diurnos, Nocturnos y Sabatinos)                  |
|   3. Tarifas Oficiales en COP y Descuentos por Convenio                               |
|   4. Sedes Presenciales (Bogota, Medellin, Cali) y Modalidad Virtual Sincronica       |
|                                                                                       |
|  [USUARIO]: 3                                                                         |
|                                                                                       |
|  [ASISTENTE]: (Latencia: 18.2 ms | Resuelto via Cache Exacta SHA-256)                 |
|  TARIFAS OFICIALES 2026 (PESOS COLOMBIANOS):                                          |
|  - Curso General (40 hrs): $585.000 COP por ciclo.                                    |
|  - Curso Intensivo (80 hrs): $650.000 COP por ciclo.                                  |
|  DESCUENTOS VIGENTES (Documento Oficial 12_04):                                       |
|  * 10% por pago de contado.                                                           |
|  * 15% por afiliacion a Cajas de Compensacion (Compensar, Colsubsidio, Comfama).       |
|                                                                                       |
+---------------------------------------------------------------------------------------+
| ACCIONES: [1. Cursos]  [2. Horarios]  [3. Precios]  [4. Sedes]  [Agendar Test]        |
+---------------------------------------------------------------------------------------+
| > Ingrese su consulta...                                                [ENVIAR]      |
+---------------------------------------------------------------------------------------+
| Conectado: 127.0.0.1:8000                                         FILTRO CRT: [ACTIVO]|
+---------------------------------------------------------------------------------------+
```
