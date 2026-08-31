import os
from pathlib import Path

DOCS_DIR = Path("data/documents")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# 80 Distinct, Detailed, and Functional University Documents for Nova Tech University

DOCUMENTS = [
    # --- CLUSTER 1: SYLLABUS & CURRICULUM PER SUBJECT (1 to 20) ---
    ("silabo_algoritmos_y_estructuras_de_datos.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Algoritmos y Estructuras de Datos Avanzadas (CS-201)

### 1. Información General del Curso
- **Código:** CS-201
- **Créditos:** 4 Créditos Académicos (64 Horas Teórico-Prácticas)
- **Prerrequisito:** CS-101 Introducción a la Programación (Calificación mínima 75/100)
- **Modalidades:** 100% Online, Híbrida y Presencial
- **Departamento:** Facultad de Ingeniería de Software y Ciencias de la Computación

### 2. Descripción del Curso y Competencias
Este curso profundiza en el diseño, análisis de complejidad asintótica (Big-O, Big-Omega, Big-Theta) y optimización de estructuras de datos lineales y no lineales en memoria principal. Los estudiantes implementan soluciones de alto rendimiento para sistemas distribuidos y procesamiento masivo de información.

### 3. Unidades de Aprendizaje y Temas Clave
- **Unidad 1: Estructuras Lineales y Complejidad:** Listas doblemente enlazadas, colas de prioridad circulares, pilas y amortización de costos en arreglos dinámicos.
- **Unidad 2: Árboles y Grafos:** Árboles binarios de búsqueda autobalanceados (AVL y Red-Black Trees), Tries para autocompletado y B-Trees para motores de bases de datos.
- **Unidad 3: Algoritmos en Grafos:** Búsqueda en anchura (BFS), profundidad (DFS), algoritmo de Dijkstra, Bellman-Ford y algoritmos de flujo máximo (Ford-Fulkerson).
- **Unidad 4: Tablas Hash y Concurrencia:** Funciones hash criptográficas, manejo de colisiones por direccionamiento abierto y cuckoo hashing libre de bloqueos.

### 4. Sistema de Evaluación
- **Laboratorios Prácticos Semanales (40%):** 8 entregas de código con pruebas automatizadas en GitHub Classroom.
- **Examen Parcial Técnico (25%):** Resolución de problemas algorítmicos en tiempo real bajo plataforma estilo LeetCode.
- **Proyecto Final Capstone (25%):** Motor de búsqueda indexado en memoria con árbol Trie y grafos de ranking.
- **Participación y Quizzes (10%):** Evaluaciones diagnósticas continuas.
"""),

    ("silabo_arquitectura_de_software_y_microservicios.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Arquitectura de Software y Sistemas Distribuidos (SE-302)

### 1. Información General del Curso
- **Código:** SE-302
- **Créditos:** 4 Créditos Académicos
- **Prerrequisito:** SE-202 Ingeniería Web y Bases de Datos
- **Departamento:** Departamento de Ingeniería de Software

### 2. Objetivos de Aprendizaje
Dominar los patrones de arquitectura empresarial, diseño guiado por el dominio (Domain-Driven Design - DDD), microservicios independientes, mensajería asíncrona y orquestación con Kubernetes en nubes públicas (AWS, GCP, Azure).

### 3. Contenido Programático
- **Módulo 1: Fundamentos de Arquitectura:** Monolitos modulares vs microservicios, teorema CAP, latencia y consistencia eventual.
- **Módulo 2: Comunicación y Mensajería:** APIs RESTful, gRPC con Protocol Buffers, GraphQL y brokers de mensajería (Apache Kafka y RabbitMQ).
- **Módulo 3: Resiliencia y Patrones de Fallo:** Circuit Breaker, Retry con Exponential Backoff, Bulkhead y Rate Limiting con Redis.
- **Módulo 4: Observabilidad:** Distributed Tracing con OpenTelemetry, métricas con Prometheus y logging centralizado en Grafana Loki.

### 4. Entregables Obligatorios
- Implementación de un clúster de microservicios con arquitectura Event-Driven desplegado en AWS EKS con pipelines CI/CD en GitHub Actions.
"""),

    ("silabo_inteligencia_artificial_y_deep_learning.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Inteligencia Artificial y Deep Learning (AI-401)

### 1. Información General
- **Código:** AI-401
- **Créditos:** 5 Créditos Académicos (Laboratorio GPU dedicado)
- **Prerrequisito:** MAT-203 Álgebra Lineal y Cálculo Multivariable + CS-201
- **Departamento:** Facultad de Inteligencia Artificial

### 2. Enfoque del Programa
Capacitar a los estudiantes en el entrenamiento, ajuste fino (fine-tuning) y despliegue en producción de modelos de aprendizaje profundo utilizando PyTorch, Transformers (Hugging Face) y aceleración por GPU NVIDIA CUDA.

### 3. Contenidos Troncales
- **Redes Neuronales Densas:** Backpropagation, funciones de pérdida y optimizadores (AdamW, SGD).
- **Visión por Computador (CV):** Redes Convolucionales (CNNs), Vision Transformers (ViT) y modelos de segmentación YOLOv9.
- **Procesamiento del Lenguaje Natural (NLP):** Mecanismos de Auto-Atención, arquitecturas Transformer, Tokenización Byte-Pair y LoRA/QLoRA para LLMs.
- **Modelos Generativos:** Diffusion Models, Generative Adversarial Networks (GANs) y Retrieval-Augmented Generation (RAG).

### 4. Recursos Disponibles
Cada estudiante recibe acceso a 150 horas de cómputo en clústeres GPU NVIDIA H100 a través del portal de computación de Nova Tech.
"""),

    ("silabo_ciberseguridad_defensiva_y_soc.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Ciberseguridad Defensiva y Operaciones SOC (SEC-305)

### 1. Información General
- **Código:** SEC-305
- **Créditos:** 4 Créditos
- **Prerrequisito:** NET-201 Redes y Protocolos de Comunicación
- **Departamento:** Facultad de Ciberseguridad y Cloud

### 2. Competencias Desarrolladas
Formación de especialistas en detección de amenazas, gestión de incidentes de seguridad (SIEM/SOAR), análisis forense digital y endurecimiento de infraestructuras críticas bajo el marco NIST Cybersecurity Framework.

### 3. Temario Oficial
- **Análisis de Vulnerabilidades:** Escaneo con Nessus, OpenVAS y gestión de CVEs.
- **Monitoreo y SIEM:** Implementación de reglas de correlación en Wazuh, Splunk y Elastic Security.
- **Forense Digital:** Adquisición de memoria RAM con Volatility, análisis de discos con Autopsy y cadena de custodia.
- **Threat Hunting:** Búsqueda proactiva de indicadores de compromiso (IoCs) mapeados al marco MITRE ATT&CK.
"""),

    ("silabo_cloud_computing_y_devops.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Cloud Computing y Metodologías DevOps (CC-303)

### 1. Información General
- **Código:** CC-303 | **Créditos:** 4 Créditos | **Departamento:** Ciberseguridad y Cloud

### 2. Objetivos
Automatizar el ciclo de vida del software mediante Infraestructura como Código (IaC), contenedores y despliegues continuos sin tiempo de inactividad (Zero-Downtime Deployments).

### 3. Módulos Temáticos
- **Contenedores:** Docker avanzado, multi-stage builds y seguridad en imágenes de contenedor.
- **Infraestructura como Código:** Terraform, AWS CloudFormation y gestión de estado remoto en S3.
- **Pipelines CI/CD:** GitHub Actions, GitLab CI y pruebas de integración automáticas.
- **Estrategias de Despliegue:** Blue/Green Deployments, Canary Releases y GitOps con ArgoCD.
"""),

    ("silabo_bases_de_datos_nosql_y_vectoriales.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Bases de Datos NoSQL y Vectoriales (DB-204)

### 1. Datos del Curso
- **Código:** DB-204 | **Créditos:** 3 Créditos | **Prerrequisito:** DB-101 Bases de Datos Relacionales

### 2. Contenido
- **Modelos NoSQL:** Clave-Valor (Redis), Documentales (MongoDB), Familia de Columnas (Cassandra) y Grafos (Neo4j).
- **Bases de Datos Vectoriales:** Indexación HNSW, IVF-PQ, búsqueda por similitud de coseno en ChromaDB, Pinecone y Qdrant para aplicaciones de Inteligencia Artificial.
- **Escalabilidad y Sharding:** Particionamiento horizontal, replicación maestro-esclavo y consistencia de datos.
"""),

    ("silabo_desarrollo_web_fullstack_moderno.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Desarrollo Web Full Stack Moderno (WD-205)

### 1. Datos Generales
- **Código:** WD-205 | **Créditos:** 4 Créditos | **Departamento:** Ingeniería de Software

### 2. Tecnologías y Enfoque
Dominio de React 19, Next.js App Router, TypeScript estricto, Tailwind CSS, Server Actions, WebSockets bidireccionales y autenticación segura con JWT y OAuth 2.0.
"""),

    ("silabo_computacion_cuantica_introductoria.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Introducción a la Computación Cuántica (QC-405)

### 1. Datos del Curso
- **Código:** QC-405 | **Créditos:** 3 Créditos Electivos | **Prerrequisito:** Álgebra Lineal y Mecánica Cuántica Básica

### 2. Temas
Qubits, superposición, entrelazamiento cuántico, compuertas lógicas cuánticas (Hadamard, CNOT), algoritmos de Deutsch-Jozsa, Grover y Shor implementados en Qiskit de IBM Quantum.
"""),

    ("silabo_sistemas_operativos_y_concurrencia.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Sistemas Operativos y Programación Concurrente (CS-202)

### 1. Resumen
Gestión de procesos e hilos en Linux/POSIX, exclusión mutua, semáforos, monitores, detección de interbloqueos (deadlocks), gestión de memoria virtual paginada y sistemas de archivos journaling (ext4, ZFS).
"""),

    ("silabo_etica_y_gobernanza_de_la_ia.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Ética, Privacidad y Gobernanza de la Inteligencia Artificial (ETH-301)

### 1. Enfoque
Evaluación de sesgos algorítmicos, explicabilidad de modelos (XAI con SHAP y LIME), cumplimiento normativo (EU AI Act, GDPR, CCPA) y protección de derechos fundamentales en la era de los modelos generativos.
"""),

    ("silabo_matematicas_discretas_para_computacion.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Matemáticas Discretas para Ciencias de la Computación (MAT-102)

### 1. Contenido
Lógica proposicional y de predicados, teoría de conjuntos, relaciones de equivalencia, combinatoria, teoría de números, criptografía RSA y grafos aplicados al análisis de redes informáticas.
"""),

    ("silabo_ingenieria_de_requisitos_y_agile.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Ingeniería de Requisitos y Gestión Ágil (SE-201)

### 1. Contenido
Metodologías Scrum, Kanban, historias de usuario con criterios INVEST, prototipado de alta fidelidad en Figma, estimación de puntos de historia y especificaciones de software bajo estándar IEEE 830.
"""),

    ("silabo_computacion_grafica_y_motores_de_juegos.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Computación Gráfica y Motores de Videojuegos (CG-308)

### 1. Contenido
Renderizado por hardware, shaders en GLSL/HLSL, pipeline de gráficos 3D, iluminación PBR, física computacional y desarrollo de experiencias interactivas en Unreal Engine 5 y Unity C#.
"""),

    ("silabo_internet_de_las_cosas_y_sistemas_embebidos.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Internet de las Cosas y Sistemas Embebidos (IOT-304)

### 1. Contenido
Arquitecturas ARM Cortex-M, ESP32, protocolos de comunicación IoT (MQTT, CoAP, BLE, LoRaWAN), integración de sensores/actuadores y seguridad en dispositivos de hardware conectados.
"""),

    ("silabo_procesamiento_de_audio_y_reconocimiento_de_voz.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Procesamiento Digital de Audio y Modelos de Voz (AI-406)

### 1. Contenido
Transformada Rápida de Fourier (FFT), espectrogramas Mel, modelos de Reconocimiento Automático de Voz (ASR con Whisper), síntesis de voz (TTS) y clonación vocal ética.
"""),

    ("silabo_redes_neuronales_recurrentes_y_series_temporales.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Análisis de Series Temporales y Modelos Secuenciales (AI-407)

### 1. Contenido
Modelos LSTM, GRU, Transformers temporales (PatchTST), predicción financiera de series temporales, detección de anomalías en telemetría industrial y forecasting de demanda energética.
"""),

    ("silabo_go_y_sistemas_de_alta_concurrencia.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Programación en Go para Sistemas de Ultra-Baja Latencia (SE-310)

### 1. Contenido
Goroutines, canales, patrones de concurrencia CSP, perfiles de memoria (pprof), recolección de basura optimizada y construcción de microservicios con latencias P99 inferiores a 5 milisegundos.
"""),

    ("silabo_seguridad_en_aplicaciones_web_owasp.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Seguridad en Aplicaciones Web y OWASP Top 10 (SEC-312)

### 1. Contenido
Prevención de inyección SQL, Cross-Site Scripting (XSS), Server-Side Request Forgery (SSRF), autenticación rota, CORS mal configurado y pruebas de penetración automatizadas con Burp Suite y OWASP ZAP.
"""),

    ("silabo_analisis_estatico_y_calidad_de_codigo.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Calidad de Software, Pruebas y Análisis Estático (SE-208)

### 1. Contenido
Pruebas unitarias con PyTest y Jest, pruebas de mutación, análisis estático con SonarQube, métricas de complejidad ciclomática de McCabe y cobertura de código superior al 85%.
"""),

    ("silabo_gestion_de_proyectos_tecnologicos_capstone.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Sílabo Oficial: Proyecto Integrador Capstone de Grado (CAP-402)

### 1. Contenido
Desarrollo multidisciplinario de una solución tecnológica de nivel industrial para una empresa asociada, defendida ante un tribunal evaluador compuesto por directores de ingeniería de la industria tech.
"""),

    # --- CLUSTER 2: SPECIALIZED LABS & RESEARCH FACILITIES (21 to 30) ---
    ("laboratorio_cluster_gpu_nvidia.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Normativa y Guía de Uso: Clúster de Supercómputo GPU NVIDIA H100

### 1. Infraestructura del Clúster
Nova Tech University cuenta con el clúster *Nova Titan Cluster*, equipado con 64 GPUs NVIDIA H100 Tensor Core de 80GB interconectadas mediante NVIDIA Quantum-2 InfiniBand a 400 Gbps.

### 2. Políticas de Acceso y Asignación de Cuotas
- **Estudiantes de Grado:** Asignación automática de 50 horas mensuales de GPU para asignaturas de IA y Deep Learning.
- **Estudiantes de Tesis y Posgrado:** Asignación ampliada de hasta 200 horas mensuales previa solicitud del tutor docente.
- **Gestor de Trabajos:** La programación de tareas se gestiona mediante el orquestador Slurm (`sbatch`, `squeue`, `scancel`).
"""),

    ("laboratorio_makerspace_e_impresion_3d.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Guía de Uso del MakerSpace y Laboratorio de Prototipado 3D

### 1. Maquinaria y Equipamiento Disponible
- 12 Impresoras 3D FDM Bambu Lab X1-Carbon con capacidad de impresión en fibra de carbono y nylon.
- 4 Impresoras 3D de Resina SLA Formlabs Form 4 para piezas de alta precisión microscópica.
- 2 Cortadoras láser CNC de CO2 de 150W para madera, acrílico y cuero.
- 6 Estaciones de soldadura y microscopios de inspección SMD para microelectrónica.

### 2. Normas de Seguridad Obligatorias
Uso indispensable de gafas protectoras, cabello recogido y prohibición de operar maquinaria sin la inducción de seguridad certificada.
"""),

    ("laboratorio_ciberseguridad_y_red_team.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Laboratorio de Red Team y Cyber Range Aislado

### 1. Entorno de Pruebas Aislado
Red física desmilitarizada e hipervisor Proxmox dedicado para simulación de ciberataques reales, ejercicios Red Team vs Blue Team y pruebas con malware en entornos controlados sin conexión a internet externa.
"""),

    ("laboratorio_realidad_virtual_y_metaverso.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Laboratorio de Tecnologías Inmersivas y Realidad Mixta (XR Lab)

### 1. Equipamiento
Visores Meta Quest 3, Apple Vision Pro, trajes de captura de movimiento hápticos Manus Prime y estaciones de trabajo con tarjetas gráficas RTX 4090 para desarrollo de simuladores médicos e industriales en 3D.
"""),

    ("laboratorio_redes_y_telecomunicaciones_cisco.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Laboratorio de Redes Físicas y Certificación Cisco Networking

### 1. Infraestructura
Racks con routers Cisco Catalyst 9300, switches capa 3, puntos de acceso Wi-Fi 6E y servidores de emulación Cisco CML y GNS3 para preparación de certificaciones CCNA y CCNP Enterprise.
"""),

    ("laboratorio_robotica_autonoma_y_drones.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Laboratorio de Robótica Móvil, Drones y Sistemas Autónomos

### 1. Equipamiento
Brazos robóticos industriales Universal Robots UR5e, robots cuadrúpedos tipo perro Unitree Go2 y drones autónomos con navegación SLAM por visión lidar para investigación en logística y rescate.
"""),

    ("laboratorio_acustica_y_procesamiento_de_senales.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Cámara Anecóica y Laboratorio de Acústica Computacional

### 1. Características
Cámara completamente aislada de ruido ambiental con atenuación superior a 90 dB para calibración de micrófonos, pruebas de audio espacial y desarrollo de algoritmos de cancelación activa de ruido por IA.
"""),

    ("laboratorio_cloud_hibrido_y_servidores.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Centro de Datos Académico y Laboratorio de Nube Híbrida

### 1. Infraestructura
Tres racks de servidores blade Dell PowerEdge con 1.5 TB de memoria RAM y 200 TB de almacenamiento NVMe gestionados con OpenStack y Kubernetes para prácticas de DevOps y arquitecturas de centros de datos.
"""),

    ("laboratorio_quimica_computacional_y_bioinformatica.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Laboratorio de Bioinformática y Plegamiento de Proteínas

### 1. Enfoque
Simulaciones de dinámica molecular con GROMACS y predicción de estructuras de proteínas utilizando AlphaFold 3 para diseño computacional de fármacos y biotecnología.
"""),

    ("laboratorio_iot_smart_campus_testbed.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Smart Campus Living Lab y Red de Sensores IoT

### 1. Red de Sensores en Campus
Más de 500 sensores distribuidos en el campus midiendo calidad del aire, consumo eléctrico, ocupación de aulas y nivel de ruido, conectados a través de LoRaWAN y accesibles mediante API REST para investigación estudiantil.
"""),

    # --- CLUSTER 3: INTERNATIONAL PROCEDURES & MOBILITY (31 to 40) ---
    ("guia_visas_estudiantiles_internacionales.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Guía de Trámite de Visa de Estudiante y Permisos de Residencia

### 1. Requisitos para Postulantes Extranjeros
Los postulantes internacionales admitidos en modalidad presencial o híbrida reciben la **Carta Oficial de Admisión y Formulario I-20 / Certificado de Elegibilidad** para solicitar la visa de estudiante ante la embajada o consulado correspondiente.

### 2. Pasos del Trámite Consular
1. Recibir la Carta de Aceptación Incondicional tras abonar la reserva de matrícula ($250 USD).
2. Pagar la tasa de registro estudiantil internacional.
3. Agendar cita consular y presentar estados de cuenta bancarios que demuestren solvencia económica para el primer año académico.
4. Notificar a la Oficina de Relaciones Internacionales (internacional@novatech.edu) en cuanto la visa sea aprobada.
"""),

    ("programa_intercambio_alemania_tum.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Intercambio Bilateral: Technical University of Munich (TUM)

### 1. Beneficios y Condiciones
Convenio de intercambio semestral para estudiantes de Ingeniería de Software e IA que hayan completado al menos el 50% de sus créditos con promedio GPA >= 3.5. Las materias cursadas en Alemania se homologan al 100% sin pago de matrícula extra en TUM.
"""),

    ("programa_intercambio_japon_tokyo_tech.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Movilidad Académica: Tokyo Institute of Technology (Tokyo Tech)

### 1. Requisitos y Becas JASSO
Estancia de 1 o 2 semestres en Tokio, Japón, con cursos en inglés y opción de pasantía en laboratorios de robótica. Los estudiantes seleccionados pueden postular a la Beca JASSO de 80,000 JPY mensuales.
"""),

    ("programa_intercambio_usa_berkeley.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa Académico de Verano: UC Berkeley Silicon Valley Immersion

### 1. Descripción
Programa intensivo de 6 semanas en Silicon Valley sobre emprendimiento tecnológico, capital de riesgo y visitas a sedes de Google, Apple, Meta y NVIDIA.
"""),

    ("guia_alojamiento_estudiantes_extranjeros.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Guía de Alojamiento y Bienvenida para Estudiantes Internacionales

### 1. Asignación Prioritaria de Dormitorio
Todos los estudiantes internacionales de primer ingreso tienen cupo garantizado en las residencias del campus (Studio Tech o Departamentos Compartidos) si reservan antes del 1 de junio.
"""),

    ("seguro_medico_internacional_obligatorio.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Política de Seguro Médico Internacional para Alumnos Extranjeros

### 1. Cobertura Sanitaria Completa
Póliza médica internacional obligatoria con cobertura de emergencias médicas, hospitalización, repatriación y cobertura dental de urgencia por hasta $100,000 USD anuales.
"""),

    ("programa_doble_titulacion_espana_upm.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Convenio de Doble Titulación con la Universidad Politécnica de Madrid (UPM)

### 1. Modalidad 3+1
Cursar los 3 primeros años en Nova Tech University y el 4to año en la UPM en Madrid, obteniendo el título oficial de Grado en Ingeniería Informática en la Unión Europea y en América.
"""),

    ("club_estudiantes_internacionales_buddy_program.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Acompañamiento Internacional (Buddy Program)

### 1. Mentoría Cultural
A cada estudiante extranjero se le asigna un estudiante local de semestres avanzados para orientarlo en trámites locales, transporte público, apertura de cuentas bancarias y vida social en la ciudad.
"""),

    ("convalidacion_certificados_ingles_toefl_ielts.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Tabla de Equivalencias de Certificaciones de Idioma Inglés

### 1. Puntajes Aceptados
- **TOEFL iBT:** Mínimo 80 puntos para pregrado; 90 puntos para posgrado.
- **IELTS Académico:** Banda mínima 6.5 global.
- **Cambridge English:** C1 Advanced o C2 Proficiency (mínimo 176 puntos).
- **Duolingo English Test (DET):** Mínimo 115 puntos.
"""),

    ("homologacion_apostilla_de_la_haya_documentos.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Requisitos de Apostilla de La Haya y Legalización de Títulos

### 1. Legalización Documental
Los títulos de bachillerato o diplomas universitarios emitidos fuera del país deben estar debidamente apostillados bajo el Convenio de La Haya o legalizados por vía diplomática consular para su validez legal definitiva.
"""),

    # --- CLUSTER 4: FINANCIAL POLICIES & BANKING (41 to 50) ---
    ("convenios_bancarios_y_metodos_de_pago.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Convenios Bancarios Oficiales y Pasarelas de Pago Autorizadas

### 1. Canales de Pago Disponibles
- **Tarjetas de Crédito y Débito:** Visa, Mastercard, American Express (hasta 12 cuotas sin recargo con bancos aliados).
- **Transferencia Bancaria Directa (ACH / SWIFT):** Cuentas corrientes institucionales en Chase Bank, Santander y Banco Davivienda.
- **Pasarelas Digitales:** Stripe, PayPal y transferencias seguras mediante PSE y PIX.
- **Criptoactivos Regulados:** Pagos aceptados en stablecoins USDC a través de la pasarela institucional auditada.
"""),

    ("plan_financiacion_cuotas_sin_interes.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Reglamento del Plan B de Financiación en 4 Cuotas Semestrales

### 1. Estructura de Pagos
El Plan B divide el arancel semestral en 4 cuotas mensuales iguales con 0% de tasa de interés:
- **Cuota 1:** 25% al formalizar la matrícula.
- **Cuota 2:** 25% a los 30 días de inicio de clases.
- **Cuota 3:** 25% a los 60 días de inicio de clases.
- **Cuota 4:** 25% a los 90 días de inicio de clases.
"""),

    ("beca_al_merito_academico_turing.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Bases y Reglamento de la Beca de Excelencia Alan Turing (50% Cobertura)

### 1. Criterios de Selección
- Promedio acumulado de secundaria o bachillerato de al menos 9.2 sobre 10 (o GPA >= 3.8/4.0).
- Examen de aptitud matemática y lógica computacional con percentil superior al 90%.
- Ensayo de motivación sobre el impacto social de la tecnología.
"""),

    ("beca_women_in_tech_ada_lovelace.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Beca Mujeres en Tecnología 'Ada Lovelace' (35% Descuento)

### 1. Objetivo y Requisitos
Fomentar la participación femenina en carreras de Ingeniería de Software, IA y Ciberseguridad. Otorga un 35% de descuento en todos los semestres manteniendo un promedio mínimo regular de 3.2 GPA.
"""),

    ("programa_trabajo_estudio_on_campus.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Ayudantías Trabajo-Estudio (Work-Study Program)

### 1. Remuneración y Horarios
Los estudiantes matriculados pueden trabajar hasta **15 horas semanales** como asistentes de laboratorio, monitores de biblioteca o desarrolladores junior en el departamento de TI, con una remuneración de $12 USD por hora aplicable directamente a su colegiatura.
"""),

    ("politica_de_reembolsos_y_devoluciones.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Política Oficial de Cancelación, Reembolsos y Devoluciones de Matrícula

### 1. Plazos de Reembolso
- **Retiro antes de inicio de clases:** Devolución del 100% del arancel pagado (menos tarifa administrativa de $50 USD).
- **Retiro en la Semana 1 o 2 de clases:** Devolución del 75% del valor del semestre.
- **Retiro en la Semana 3 de clases:** Devolución del 50% del valor del semestre.
- **Posterior a la Semana 4:** No aplica reembolso económico.
"""),

    ("descuentos_familiares_y_hermanos.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Política de Descuentos por Hermanos y Familiares Directos

### 1. Beneficio
Descuento del 15% sobre la colegiatura semestral para el segundo hermano matriculado simultáneamente en la universidad, y del 20% para el tercer hermano en adelante.
"""),

    ("financiacion_educativa_prestamos_icetex_finae.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Créditos Educativos con Entidades Financieras Aliadas

### 1. Entidades en Convenio
Convenios directos con ICETEX, Fina-E, Banco Pichincha y entidades de microcrédito educativo con tasas preferenciales y períodos de gracia hasta 6 meses después de la graduación.
"""),

    ("auditoria_financiera_y_facturacion_electronica.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Emisión de Facturación Electrónica y Certificados Tributarios

### 1. Facturación
Todas las matrículas generan factura electrónica con valor fiscal y deducibilidad tributaria para empresas o padres de familia, disponible para descarga en el portal financiero en 24 horas.
"""),

    ("beca_deportiva_y_atletas_de_alto_rendimiento.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Beca para Deportistas Destacados y Atletas de Alto Rendimiento

### 1. Beneficio
Descuento del 25% al 50% en aranceles para atletas federados que representen a Nova Tech University en torneos universitarios nacionales e internacionales de fútbol, natación, baloncesto o e-Sports.
"""),

    # --- CLUSTER 5: STUDENT LIFE, HEALTH & SPORTS (51 to 60) ---
    ("centro_medico_y_atencion_de_primeros_auxilios.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Centro de Atención Médica y Primeros Auxilios del Campus

### 1. Servicios Gratuitos
Atención médica general gratuita, enfermería continua de 7:00 AM a 10:00 PM, botiquín de emergencias, vacunación estacional y ambulancia de traslado para urgencias hospitalarias.
"""),

    ("gimnasio_universitario_y_clases_deportivas.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Instalaciones del Gimnasio Universitario y Entrenamiento Funcional

### 1. Equipamiento y Horarios
Abierto de lunes a sábado de 6:00 AM a 10:00 PM. Cuenta con máquinas de pesas, zona de crossfit, pista de atletismo y clases dirigidas de Yoga, Pilates, Spinning y Boxeo recreativo sin costo adicional.
"""),

    ("cafeterias_y_planes_de_alimentacion_saludable.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Restaurantes del Campus y Planes de Alimentación (Meal Plans)

### 1. Opciones Gastronómicas
Cuatro cafeterías universitarias con menús balanceados supervisados por nutricionistas, opciones vegetarianas, veganas y libres de gluten. Plan de 20 almuerzos mensuales por $90 USD.
"""),

    ("club_de_esports_y_arena_gamer.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Arena Gamer Oficial y Club de Deportes Electrónicos (Nova eSports)

### 1. Equipamiento
Arena gamer con 30 computadoras de competición (monitores 240Hz, RTX 4080) para torneos de League of Legends, Valorant, Rocket League y Counter-Strike 2.
"""),

    ("talleres_culturales_teatro_musica_y_fotografia.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Talleres Artísticos, Banda Universitaria y Fotografía Digital

### 1. Actividades
Talleres extracurriculares gratuitos de producción musical digital, fotografía, club de cine debate y elenco de teatro universitario con presentaciones semestrales.
"""),

    ("asociacion_estudiantil_y_gobierno_universitario.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Consejo Estudiantil y Participación Democrática Universitaria

### 1. Rol y Elección
El Consejo Central de Estudiantes (CCE) representa a los alumnos ante el Consejo Directivo de la Universidad, organizando semanas de integración y gestionando peticiones académicas.
"""),

    ("politicas_de_inclusion_y_accesibilidad_universal.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Política de Accesibilidad e Inclusión para Personas con Discapacidad

### 1. Infraestructura Inclusiva
Campus 100% adaptado con rampas mecánicas, ascensores táctiles, señalética en braille, software lector de pantalla en todos los laboratorios y apoyo de intérpretes de lengua de señas.
"""),

    ("voluntariado_y_responsabilidad_social_universitaria.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Voluntariado 'Nova Tech Solidaria'

### 1. Proyectos Sociales
Talleres de alfabetización digital y programación básica con Scratch en escuelas públicas, donación y reacondicionamiento de computadoras para comunidades vulnerables.
"""),

    ("servicio_de_transporte_y_rutas_universitarias.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Rutas de Transporte Universitario Gratuito (Nova Shuttle)

### 1. Horarios y Recorridos
Flota de autobuses eléctricos con 4 rutas circulares que conectan el campus con las principales estaciones de tren y metro de la ciudad de 6:30 AM a 10:30 PM.
"""),

    ("parqueaderos_y_estaciones_de_carga_electrica.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Parqueaderos del Campus y Estaciones de Carga para Autos Eléctricos

### 1. Tarifas y Estaciones
Parqueadero techado gratuito para bicicletas y scooters eléctricos con cargadores solares. Parqueadero para autos con 16 cargadores rápidos para vehículos eléctricos a tarifa preferencial.
"""),

    # --- CLUSTER 6: EMPLOYABILITY, STARTUPS & PARTNERS (61 to 70) ---
    ("incubadora_de_startups_nova_ventures.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Incubadora y Aceleradora de Startups: Nova Ventures

### 1. Capital Semilla y Mentoría
Fondo anual de $100,000 USD en capital semilla para proyectos de software e IA creados por estudiantes, con espacio de coworking gratuito y asesoría legal para constitución de empresas en Delaware y Latinoamérica.
"""),

    ("convenio_empresarial_microsoft_learn.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Alianza Universitaria Oficial con Microsoft Learn y Azure

### 1. Beneficios
Vouchers de certificación 100% gratuitos para exámenes Microsoft Certified: Azure Fundamentals (AZ-900), Azure AI Engineer (AI-102) y suscripción con $100 USD de créditos mensuales en Azure Cloud.
"""),

    ("convenio_empresarial_aws_academy.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Convenio AWS Academy y Certificaciones en la Nube

### 1. Cobertura
Acceso a laboratorios interactivos oficiales de Amazon Web Services para preparación de AWS Certified Cloud Practitioner y AWS Certified Solutions Architect Associate con 50% de descuento en el examen.
"""),

    ("convenio_empresarial_google_cloud_education.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Alianza con Google Cloud for Higher Education

### 1. Capacitación
Cursos oficiales de Google Cloud en Vertex AI, BigQuery y Kubernetes Engine con acceso ilimitado a la plataforma Google Cloud Skills Boost.
"""),

    ("feria_laboral_anual_tech_career_expo.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Tech Career Expo: Feria Anual de Reclutamiento de Talento

### 1. Empresas Participantes
Más de 60 empresas nacionales e internacionales (Globant, Mercado Libre, IBM, Oracle, Rappi, Amazon) realizan entrevistas presenciales y virtuales contratando directamente a estudiantes de 6to a 8vo semestre.
"""),

    ("mentorias_con_ingenieros_de_silicon_valley.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Mentoría con Ingenieros de Silicon Valley

### 1. Dinámica
Cada estudiante de último año puede ser emparejado con un mentor profesional que trabaje en empresas líderes de EE.UU. o Europa para recibir retroalimentación de código y consejos de carrera.
"""),

    ("pasantias_remuneradas_en_empresas_unicornio.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Política y Registro de Pasantías Profesionales Remuneradas

### 1. Salarios Promedio
Las pasantías tecnológicas gestionadas a través del *Nova Career Hub* son obligatoriamente remuneradas, con estipendios mensuales que oscilan entre $600 USD y $1,400 USD según la empresa y modalidad.
"""),

    ("red_de_egresados_alumni_network.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Red Global de Graduados: Nova Tech Alumni Network

### 1. Comunidad
Comunidad de más de 4,000 graduados con presencia en más de 25 países, capítulos regionales en San Francisco, Madrid, Bogotá, CDMX y São Paulo, y eventos de networking trimestrales.
"""),

    ("certificaciones_profesionales_incluidas_en_la_carrera.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Certificaciones de la Industria Incluidas sin Costo en la Malla

### 1. Certificaciones Cubiertas
- CompTIA Security+ (Carrera de Ciberseguridad)
- AWS Solutions Architect Associate (Ingeniería de Software y Cloud)
- TensorFlow Developer Certificate / GitHub Foundations (IA Aplicada)
"""),

    ("portal_de_empleo_exclusivo_nova_career_hub.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Manual del Portal de Empleo Exclusivo: Nova Career Hub

### 1. Funcionalidades
Plataforma interna donde empresas publican vacantes exclusivas para estudiantes y egresados de Nova Tech, con sistema de matching automático por habilidades técnicas de GitHub y LinkedIn.
"""),

    # --- CLUSTER 7: REGULATIONS, ETHICS & POSTGRADUATE (71 to 80) ---
    ("reglamento_disciplinario_y_codigo_de_honor.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Código de Honor y Reglamento Disciplinario Estudiantil

### 1. Política de Integridad Académica
Tolerancia cero con el plagio de código, copia en evaluaciones o uso no autorizado de IA generativa para resolver exámenes. Sanciones van desde amonestación escrita hasta expulsión definitiva según la gravedad.
"""),

    ("procedimiento_defensa_de_tesis_y_capstone.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Guía y Rúbrica para la Defensa de Proyecto Capstone y Tesis

### 1. Formato de Defensa
Presentación oral de 30 minutos con demostración de software en vivo ante un jurado de tres docentes, seguida de 15 minutos de preguntas técnicas sobre arquitectura y escalabilidad.
"""),

    ("maestria_en_inteligencia_artificial_generativa.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Posgrado: Maestría en IA Generativa y LLMs (M.Sc.)

### 1. Duración y Costos
- **Duración:** 3 Semestres (18 Meses) | Modalidad 100% Online o Híbrida
- **Arancel:** $4,500 USD por semestre. Descuento del 20% automático para egresados de Nova Tech.
- **Enfoque:** Arquitecturas Transformer avanzadas, agentes autónomos, RAG empresarial y fine-tuning masivo.
"""),

    ("maestria_en_ciberseguridad_ofensiva_y_cloud.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Programa de Posgrado: Maestría en Ciberseguridad Ofensiva (M.Sc.)

### 1. Duración y Enfoque
- **Duración:** 3 Semestres | Modalidad Online Asíncrona con Laboratorios Prácticos
- **Preparación:** Certificaciones OSCP (Offensive Security Certified Professional) y CISSP.
"""),

    ("comite_de_etica_en_investigacion_tecnologica.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Comité Institucional de Ética en Investigación Científica (CIE)

### 1. Funciones
Revisión obligatoria de todo proyecto de investigación que involucre datos sensibles de usuarios, modelos de reconocimiento facial o análisis masivo de comportamiento humano.
"""),

    ("derechos_de_propiedad_intelectual_y_patentes.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Política de Propiedad Intelectual y Registro de Software

### 1. Titularidad Estudiantil
El código fuente y las invenciones desarrolladas por los estudiantes en proyectos de clase o tesis son **100% propiedad exclusiva de los estudiantes**, con apoyo legal gratuito de la universidad para el registro de patentes y marcas.
"""),

    ("normativa_de_asistencia_y_justificacion_de_faltas.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Normativa de Asistencia y Justificación de Ausencias

### 1. Asistencia Mínima
- **Modalidad Presencial e Híbrida:** 80% de asistencia obligatoria.
- **Modalidad 100% Online:** Cumplimiento del 100% de las actividades asíncronas en la plataforma sin requisito de conexión en vivo simultánea.
- **Justificaciones:** Trámites médicos o laborales se justifican dentro de los 5 días hábiles siguientes al evento en el portal del estudiante.
"""),

    ("reglamento_de_biblioteca_prestamos_y_recursos_digitales.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Reglamento de Préstamo de Libros y Equipos de Biblioteca

### 1. Préstamo de Hardware
Estudiantes pueden solicitar en préstamo temporal laptops de alta gama, tarjetas de desarrollo Raspberry Pi / Arduino y visores VR por períodos de hasta 15 días renovables.
"""),

    ("homologacion_de_materias_por_experiencia_laboral.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Convalidación de Asignaturas por Trayectoria Laboral Demostrada (RPL)

### 1. Requisitos
Aspirantes con más de 3 años de experiencia comprobada como desarrolladores de software o ingenieros DevOps pueden convalidar hasta 18 créditos rindiendo un examen técnico de suficiencia práctica.
"""),

    ("protocolo_de_seguridad_y_evacuacion_del_campus.md", """# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Plan de Emergencias, Evacuación y Seguridad en Campus

### 1. Protocolos
Puntos de encuentro seguros señalizados en jardines centrales, brigadas contra incendios en cada edificio y simulacros de evacuación semestrales coordinados con la defensa civil.
""")
]

print(f"Total documents to write: {len(DOCUMENTS)}")
written_count = 0
for filename, content in DOCUMENTS:
    filepath = DOCS_DIR / filename
    filepath.write_text(content.strip(), encoding="utf-8")
    written_count += 1

print(f"Successfully generated {written_count} official detailed documents in {DOCS_DIR}!")
