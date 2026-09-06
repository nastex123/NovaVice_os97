# Evidencias de Certificación de Competencias Laborales SENA
## Sistema de Información y Admisiones: "Nova Idiomas OS '97" (NovaVice_os97)

- **Entidad Evaluadora:** Servicio Nacional de Aprendizaje (SENA)
- **Sector:** Tecnologías de la Información y las Comunicaciones / Desarrollo de Software
- **Proyecto:** Asistente Inteligente de Admisiones con RAG Híbrido y Terminal Retro ("Nova OS '97")
- **Organización / Caso de Estudio:** Nova Idiomas Colombia
- **Fecha de Elaboración:** 2026-09-02 (Zona Horaria: `America/Bogota`)
- **Estado de las Evidencias:** Completas, Auditadas y Listas para Radicación

---

## 🏛️ Estructura General de las Evidencias en `SENA/`

El conjunto de evidencias se encuentra estructurado en dos partes independientes, correspondientes a las dos Normas Sectoriales de Competencia Laboral solicitadas:

```text
SENA/
├── README.md                                     # Ficha maestra institucional y matriz de trazabilidad
│
├── html_mockups/                                 # Prototipos interactivos HTML (Retro UI Windows/Mac '97)
│   ├── 01_pantalla_principal.html                # Terminal interactiva CRT con diálogo RAG y menú de pilares
│   ├── 02_gestion_proyectos.html                 # Catálogo académico y simulador de matrícula con descuentos COP
│   ├── 03_gestion_tareas.html                    # Bandeja de tickets de admisiones (ESC-XXXX) y transcripción
│   └── 04_formulario_creacion_edicion.html       # Formularios de Placement Test y radicación de escalamiento
│
├── img/                                          # Recursos gráficos de alta resolución (PNG) incrustados
│   ├── diagrama_arquitectura.png                 # Arquitectura multicapa desacoplada (Clean Architecture)
│   ├── diagrama_casos_uso.png                    # Diagrama de casos de uso (16 CU en 3 subsistemas)
│   ├── diagrama_clases.png                       # Diagrama de clases de dominio y componentes RAG
│   ├── diagrama_secuencia_rag.png                # Secuencia de consulta RAG y resolución en caché
│   ├── diagrama_secuencia_escalamiento.png       # Secuencia de escalamiento humano en 2 fases
│   ├── diagrama_actividades.png                  # Diagrama de flujo de actividades y bifurcaciones
│   ├── diagrama_erd_bd.png                       # Diagrama entidad-relación (ERD) en 3FN
│   ├── diagrama_flujo_sistema.png                # Ciclo de vida y flujo de procesamiento del sistema
│   ├── diagrama_despliegue_procesos.png          # Arquitectura de ejecución multi-proceso sincronizada
│   ├── ss_pantalla_principal.png                 # Captura UI: Terminal interactiva en modo CRT
│   ├── ss_gestion_proyectos.png                  # Captura UI: Catálogo de oferta académica y simulador
│   ├── ss_gestion_tareas.png                     # Captura UI: Bandeja de tickets de admisiones
│   └── ss_formulario_creacion_edicion.png        # Captura UI: Formularios de pruebas y escalamiento
│
├── part1/                                        # NORMA: 220501095 (Diseño de la solución de software)
│   ├── 00_GUIA_ENTREGA_PARTE_1.md                # Ficha técnica, rúbrica de evaluación y formulario de radicación
│   ├── 01_DOCUMENTO_DISENO_SOFTWARE.md           # Requisitos RF/RNF, arquitectura N-Capas, módulos y justificación
│   ├── 02_DIAGRAMAS_UML.md                       # Diagramas de casos de uso, clases, secuencia y actividad en Mermaid
│   ├── 03_PROTOTIPO_SOLUCION_SOFTWARE.md         # Wireframes, mockups, flujos de navegación y formularios de interacción
│   └── 04_MODELO_BASE_DATOS.md                   # Diagrama ERD, diccionario de datos y script DDL SQL relacional
│
└── part2/                                        # NORMA: 220501096 (Desarrollo de la solución de software)
    ├── 00_GUIA_ENTREGA_PARTE_2.md                # Ficha técnica, rúbrica de evaluación y formulario de radicación
    ├── 01_DOCUMENTO_TECNICO_CODIGO_FUENTE.md     # Estructura del código, módulos, algoritmos matemáticos y lógica de optimización
    ├── 02_INSTRUCTIVO_USO_SOLUCION_SOFTWARE.md   # Manual de usuario, instalación (install.bat), ejecución (start.bat/run.py) y vistas
    └── 03_ENTREGA_SOLUCION_SOFTWARE.md           # Ficha del proyecto funcional: repositorio GitHub, endpoints API y validación (27/27 tests)
```

---

## 📊 Matriz Consolidada de Normas y Formularios de Entrega

| Parte | Código Norma | Denominación Oficial de la Norma | Productos Entregados | Archivo Word Institucional Diligenciado | Enlace al Formulario Oficial de Radicación |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **Parte 1** | **220501095** | *Diseñar la solución de software de acuerdo con procedimientos y requisitos técnicos.* | 1. Documento de diseño de software<br>2. Diagramas UML<br>3. Prototipo de solución de software<br>4. Modelo de base de datos | [`FORMATO DE PRODUCTO_NORMA 220501095 _ Carranza Rangel - Brandon Jose.docx`](FORMATO%20DE%20PRODUCTO_NORMA%20220501095%20_%20Carranza%20Rangel%20-%20Brandon%20Jose.docx) | [Formulario Unificado Guía SENA](https://forms.gle/VGn4RpzHb79v1QLs6)<br>*(Alt: [Formulario Parte 1](https://forms.gle/xtd48BgaPFEHzRAJ7))* |
| **Parte 2** | **220501096** | *Desarrollar solución de software de acuerdo con especificaciones de diseño y marcos de referencia.* | 1. Documento técnico de código fuente<br>2. Instructivo de uso de la solución<br>3. Solución de software funcional | [`FORMATO DE PRODUCTO_NORMA 220501096 _ Carranza Rangel - Brandon Jose.docx`](FORMATO%20DE%20PRODUCTO_NORMA%20220501096%20_%20Carranza%20Rangel%20-%20Brandon%20Jose.docx) | [Formulario Unificado Guía SENA](https://forms.gle/VGn4RpzHb79v1QLs6)<br>*(Alt: [Formulario Parte 2](https://forms.gle/485g3veWL9CnBGKC7))* |

---

## 📋 Datos del Candidato / Aprendiz

- **Nombre del Candidato:** `Brandon Jose Carranza Rangel`
- **Documento de Identidad:** `C.C. 1007892884`
- **Número de Ficha / Grupo:** `[Ficha SENA]`
- **Centro de Formación:** `[Centro de Formación SENA]`
- **Regional:** `[Regional SENA]`
- **Repositorio Oficial del Proyecto:** `https://github.com/nastex123/NovaVice_os97.git`
