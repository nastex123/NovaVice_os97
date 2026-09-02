# Diagramas de Lenguaje Unificado de Modelado (UML)
## Sistema de Asistencia Inteligente de Admisiones: "Nova OS '97"
### Evidencia de Producto 2 — Norma SENA 220501095

- **Programa de Formación:** Análisis y Desarrollo de Software (ADSO)
- **Norma de Competencia:** 220501095 — *Diseñar la solución de software de acuerdo con procedimientos y requisitos técnicos.*
- **Candidato / Aprendiz:** `[Nombre del Aprendiz]`
- **Documento de Identidad:** `[C.C. / T.I. Número]`
- **Organización Beneficiaria:** Nova Idiomas Colombia
- **Fecha de Elaboración:** 2026-09-02 (Zona Horaria: `America/Bogota`)
- **Herramientas de Modelado:** Mermaid.js, compatible con Draw.io, Lucidchart y StarUML.

---

## 1. Diagrama de Casos de Uso del Sistema

Este diagrama modela las interacciones entre los tres actores principales (**Aspirante**, **Asesor de Admisiones** y **Administrador de TI**) y las funcionalidades provistas por el sistema de software.

```mermaid
graph LR
    %% Definición de Actores
    user((👤 Aspirante))
    advisor((👨‍💼 Asesor Humano))
    admin((🛠️ Administrador TI))

    %% Paquete de Casos de Uso del Aspirante
    subgraph Portal de Admisiones Nova OS 97
        CU01[CU-01: Explorar Oferta Académica]
        CU02[CU-02: Consultar Horarios y Sedes]
        CU03[CU-03: Cotizar Tarifas y Descuentos COP]
        CU04[CU-04: Navegar Menú Guiado Pilares 1..4]
        CU05[CU-05: Formular Consulta en Lenguaje Natural]
        CU06[CU-06: Solicitar Agendamiento Placement Test]
        CU07[CU-07: Solicitar Asesoría Humana]
        CU08[CU-08: Confirmar Escalamiento en 2 Fases]
    end

    %% Paquete de Casos de Uso del Asesor
    subgraph Módulo de Asesores y Soporte
        CU09[CU-09: Gestionar Bandeja de Tickets ESC-XXXX]
        CU10[CU-10: Consultar Historial y Transcripción]
        CU11[CU-11: Contactar Aspirante vía WhatsApp]
        CU12[CU-12: Cerrar Ticket de Escalamiento]
    end

    %% Paquete de Casos de Uso del Administrador
    subgraph Módulo de Administración y Mantenimiento
        CU13[CU-13: Cargar y Actualizar Documentos RAG]
        CU14[CU-14: Forzar Reindexación Vectorial]
        CU15[CU-15: Monitorear Métricas y Telemetría]
        CU16[CU-16: Auditar Tasa de Escalamiento y Costos]
    end

    %% Relaciones del Aspirante
    user --> CU01
    user --> CU02
    user --> CU03
    user --> CU04
    user --> CU05
    user --> CU06
    user --> CU07

    %% Inclusiones y Extensiones
    CU05 -.->|<<extend>>| CU07
    CU07 -.->|<<include>>| CU08

    %% Relaciones del Asesor
    advisor --> CU09
    advisor --> CU10
    advisor --> CU11
    advisor --> CU12
    CU09 -.->|<<include>>| CU10

    %% Relaciones del Administrador
    admin --> CU13
    admin --> CU14
    admin --> CU15
    admin --> CU16
    CU13 -.->|<<include>>| CU14
```

### Descripción de los Casos de Uso Principales:
- **CU-04 (Navegar Menú Guiado):** Permite al aspirante explorar los 4 pilares institucionales (Cursos, Horarios, Precios y Sedes) mediante selecciones directas numéricas (`1` al `4`) o botones de interfaz sin consumo de tokens de IA.
- **CU-05 (Formular Consulta en Lenguaje Natural):** Recibe preguntas abiertas del aspirante, las filtra mediante guardrails de seguridad y las resuelve a través del recuperador híbrido RAG.
- **CU-08 (Confirmar Escalamiento en 2 Fases):** Cuando una consulta cae por debajo del umbral de confianza o supera el alcance oficial, el sistema muestra el mejor fragmento disponible y solicita confirmación explícita (`¿Deseas escalar a asesor humano? Sí/No`) antes de crear el ticket.
- **CU-09 (Gestionar Bandeja de Tickets):** Permite al equipo humano revisar los casos radicados bajo identificadores estructurados `ESC-YYYYMMDD-XXXX`.

---

## 2. Diagrama de Clases del Dominio y Servicios

El diagrama de clases modela la arquitectura estática del backend en Python, mostrando las clases de datos Pydantic, los servicios del núcleo de seguridad y navegación, y los componentes del subsistema RAG híbrido.

```mermaid
classDiagram
    class ChatRequest {
        +str query
        +str user_id
        +str session_id
        +bool use_opencode_mode
    }

    class ChatResponse {
        +str status
        +str response
        +List~str~ source_documents
        +float confidence_score
        +bool escalated_to_human
        +bool cached
        +str mode
        +float latency_ms
        +List~ActionButton~ action_buttons
    }

    class ActionButton {
        +str label
        +str value
    }

    class PreFlightGuardrails {
        -List~str~ INJECTION_PATTERNS
        +validate_query(query: str) Tuple~bool, str~
        +evaluate_relevance(similarity_score: float, threshold: float) bool
    }

    class GuidedNavigationEngine {
        +str ROOT_MENU
        +Dict~str, str~ INTENT_SYNONYMS
        +Dict~str, str~ LEAF_QUERY_MAP
        +process_navigation(input_text: str, session_id: str) Dict
        -_levenshtein(s1: str, s2: str) int
        -_normalize(text: str) str
    }

    class InvalidationAwareQueryCache {
        -Dict exact_cache
        -List semantic_cache
        -str last_docs_hash
        -int ttl_seconds
        +get(query: str) Dict
        +set(query: str, response: Dict, embedding: List) None
        +check_and_invalidate() bool
    }

    class HybridRetriever {
        -int rrf_k
        -PureBM25 bm25_index
        -VectorStore vector_store
        +retrieve(query: str, top_k: int, candidate_k: int) List~ChunkResult~
        -_ensure_bm25_populated() None
        -_calculate_rrf_score(dense_rank: int, bm25_rank: int) float
    }

    class PureBM25 {
        -float k1
        -float b
        -Dict inverted_index
        -List doc_lengths
        -float avg_doc_len
        +fit(corpus: List~str~) None
        +search(query: str, top_k: int) List~Tuple~
        -_stem(word: str) str
        -_idf(term: str) float
    }

    class VectorStore {
        -str collection_name
        -str persist_directory
        +query(query: str, top_k: int) List~Dict~
        +get_all_documents() List~Dict~
        +embed_query(query: str) List~float~
    }

    class EscalationDispatcher {
        -str storage_file
        +create_ticket(query: str, user_id: str, confidence_score: float, reason: str) Dict
        +dispatch_webhook(ticket: Dict) bool
        -_persist(ticket: Dict) None
    }

    class TicketRecord {
        +str ticket_id
        +str query
        +str user_id
        +float confidence_score
        +str reason
        +str status
        +str created_at
    }

    %% Relaciones
    ChatResponse *-- ActionButton
    HybridRetriever o-- PureBM25
    HybridRetriever o-- VectorStore
    EscalationDispatcher ..> TicketRecord : crea y persiste
```

---

## 3. Diagramas de Secuencia

### 3.1 Diagrama de Secuencia 1: Flujo Exitoso de Consulta RAG con Caché Híbrida

Modela el ciclo de vida completo desde que el aspirante ingresa una pregunta en la terminal web hasta que recibe la respuesta fundamentada con citas institucionales.

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Aspirante
    participant UI as 💻 Frontend (Next.js 15)
    participant API as 🚪 FastAPI Gateway (/chat)
    participant Guard as 🛡️ PreFlightGuardrails
    participant Nav as 🧭 GuidedNavigationEngine
    participant Cache as ⚡ InvalidationAwareCache
    participant RAG as 📚 HybridRetriever (RRF)
    participant LLM as 🤖 Motor LLM / OpenCode

    User->>UI: Escribe "cuál es el precio del curso intensivo?"
    UI->>API: POST /api/v1/chat {query, session_id}
    
    API->>Guard: validate_query(query)
    Guard-->>API: (True, "") [Query Segura]

    API->>Nav: process_navigation(query, session_id)
    Nav-->>API: None [No es opción numérica 1..4]

    API->>Cache: get(query)
    alt Acierto en Caché Exacta (Hit < 25ms)
        Cache-->>API: response_payload [cached=True]
        API-->>UI: 200 OK (Respuesta Instantánea con citas)
        UI-->>User: Muestra respuesta en pantalla con viñetas
    else Fallo en Caché (Miss)
        API->>RAG: retrieve(query, top_k=4)
        activate RAG
        RAG->>RAG: Búsqueda Densa (ChromaDB)
        RAG->>RAG: Búsqueda Léxica (PureBM25 con Stemming)
        RAG->>RAG: Fusión RRF (k=60) + Cobertura de Tokens
        RAG-->>API: Top-4 Chunks Documentales (Score: 0.88 >= 0.35)
        deactivate RAG

        API->>LLM: Inyecta Contexto Oficial + Query + System Prompt
        LLM-->>API: Respuesta fundamentada en Markdown GFM
        
        API->>Cache: set(query, response, embedding)
        API-->>UI: 200 OK {response, source_documents, confidence_score: 0.88}
        UI-->>User: Renderiza respuesta formateada con badges
    end
```

---

### 3.2 Diagrama de Secuencia 2: Protocolo de Escalamiento Humano en Dos Fases

Modela el comportamiento cuando la pregunta no puede responderse con la documentación oficial o cae por debajo del umbral de corte ($<0.35$).

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Aspirante
    participant UI as 💻 Frontend (Next.js 15)
    participant API as 🚪 FastAPI Gateway (/chat)
    participant RAG as 📚 HybridRetriever
    participant Disp as 🎫 EscalationDispatcher
    actor Advisor as 👨‍💼 Asesor de Admisiones

    User->>UI: Escribe "tienen convenio con la embajada de Australia para visa de trabajo?"
    UI->>API: POST /api/v1/chat {query}
    API->>RAG: retrieve(query, top_k=4)
    RAG-->>API: Max Similarity Score = 0.22 (Bajo Umbral 0.35)

    Note over API: Fase 1 de Escalamiento: Solicitud de Confirmación
    API-->>UI: "Esta consulta requiere validación oficial. ¿Deseas ser contactado por un asesor humano? [Sí / No]"
    UI-->>User: Presenta botones interactivos de decisión

    User->>UI: Clic en "Sí, contactar asesor"
    UI->>API: POST /api/v1/escalate {query, user_id, contact_data}
    
    Note over API,Disp: Fase 2 de Escalamiento: Creación de Ticket
    API->>Disp: create_ticket(query, user_id, score=0.22, reason="Out of Scope")
    Disp->>Disp: Genera Ticket ID "ESC-20260902-8F12"
    Disp->>Disp: Persiste en data/escalations.json
    Disp->>Advisor: Notificación Webhook / Correo Institucional
    Disp-->>API: Ticket Confirmado

    API-->>UI: "Tu caso ha sido radicado con el ticket #ESC-20260902-8F12. Un asesor se comunicará contigo vía WhatsApp."
    UI-->>User: Muestra tarjeta de confirmación de radicación
```

---

## 4. Diagrama de Actividades / Flujo del Sistema

Modela el algoritmo de toma de decisiones implementado en el backend para clasificar y procesar cualquier interacción entrante.

```mermaid
flowchart TD
    Start([Inicio: Recepción de Consulta del Aspirante]) --> Sanitize[Normalización Unicode NFD y trim de espacios]
    Sanitize --> CheckGuard{¿Contiene inyección de prompt o comando malicioso?}
    
    CheckGuard -- Sí --> Reject[Retornar advertencia de seguridad y abortar consulta]
    CheckGuard -- No --> CheckNav{¿Coincide con dígito de menú 0..4 o subcódigo 1.1..4.6?}
    
    CheckNav -- Sí --> MenuAction[Recuperar respuesta determinística del árbol de navegación]
    MenuAction --> EmitButtons[Adjuntar botones de acción rápida] --> End([Fin: Retorno al Usuario])
    
    CheckNav -- No --> CheckCache{¿Existe en Caché Exacta SHA-256 o Semántica?}
    
    CheckCache -- Sí --> ReturnCached[Retornar respuesta desde memoria en sub-30ms] --> End
    
    CheckCache -- No --> ExecRAG[Ejecutar búsqueda concurrente: ChromaDB Densa + BM25 Léxica]
    ExecRAG --> ApplyRRF[Calcular Reciprocal Rank Fusion k=60 y Cobertura de Tokens]
    ApplyRRF --> EvalScore{¿Score de similitud >= Umbral 0.35 / 0.50?}
    
    EvalScore -- Sí --> BuildPrompt[Construir prompt con citas oficiales verificadas]
    BuildPrompt --> Synthesize[Sintetizar respuesta con modelo LLM / OpenCode]
    Synthesize --> StoreCache[Almacenar en Caché de Doble Capa] --> End
    
    EvalScore -- No --> EscalatePhase{¿El usuario confirma escalamiento?}
    EscalatePhase -- No --> OfferMenu[Mostrar opciones del menú principal para reorientar] --> End
    EscalatePhase -- Sí --> GenTicket[Generar ticket formal ESC-YYYYMMDD-XXXX]
    GenTicket --> PersistTicket[Persistir en escalations.json y emitir webhook]
    PersistTicket --> ConfirmUser[Entregar número de caso al aspirante] --> End
```
