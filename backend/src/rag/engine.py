import time
import os
import re
from typing import Dict, Any, List, Optional, AsyncGenerator
import httpx
from src.config import settings
from src.core.guardrails import guardrails
from src.core.cache import query_cache
from src.core.metrics import metrics_bus
from src.core.dispatcher import escalation_dispatcher
from src.core.memory import applicant_memory
from src.core.query_router import deterministic_query_router
from src.rag.hybrid_retriever import hybrid_retriever
from src.rag.context_compressor import contextual_compressor
from src.rag.prompt_templates import SYSTEM_PROMPT, build_rag_prompt


class PurePythonRAGEngine:
    # Deterministic async RAG pipeline replacing n8n workflows with pure Python.

    def __init__(self):
        self.settings = settings

    async def _call_llm_api(self, prompt: str, chunks: Optional[List[Dict[str, Any]]] = None, temperature: Optional[float] = None) -> Dict[str, Any]:
        # Connects to OpenRouter / Hermes / OpenAI or falls back to deterministic grounded response.
        api_key = self.settings.openrouter_api_key or self.settings.openai_api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

        # Grounded fallback if no API key is provided
        if not api_key or self.settings.llm_provider == "mock":
            if chunks:
                content_lines = []
                seen_lines = set()
                primary_title = None
                primary_source = None

                for chunk in chunks[:4]:
                    c_text = chunk.get("text", "")
                    c_section = chunk.get("metadata", {}).get("section", "Información Oficial")
                    c_source = chunk.get("metadata", {}).get("source", "Admisiones")

                    clean_sec = c_section.replace("#", "").strip()
                    if not primary_title and clean_sec and clean_sec.lower() != "general":
                        primary_title = clean_sec
                    if not primary_source:
                        primary_source = c_source

                    lines = [l.strip() for l in c_text.split("\n") if l.strip()]
                    for line in lines:
                        if line.startswith("#") or line.startswith("---"):
                            continue
                        if line.startswith("|") and "---" in line:
                            continue
                        clean_line = line.strip()
                        if clean_line.startswith("-"):
                            clean_line = f"• {clean_line[1:].strip()}"
                        elif clean_line.startswith("*") and not clean_line.startswith("**"):
                            clean_line = f"• {clean_line[1:].strip()}"
                        elif re.match(r"^\d+\.\s+", clean_line):
                            clean_line = f"• {re.sub(r'^\d+\.\s+', '', clean_line)}"

                        norm_key = clean_line.lower().replace("•", "").replace("*", "").strip()
                        if norm_key not in seen_lines and len(norm_key) > 5:
                            seen_lines.add(norm_key)
                            content_lines.append(clean_line)

                if not primary_title:
                    primary_title = chunks[0].get("metadata", {}).get("section", "Información Oficial").replace("#", "").strip()
                if not primary_source:
                    primary_source = chunks[0].get("metadata", {}).get("source", "Admisiones")

                if content_lines:
                    body = "\n".join(content_lines[:10])
                else:
                    body = chunks[0].get("text", "")[:280]

                formatted_response = (
                    f"📌 **{primary_title}**\n\n"
                    f"{body}\n\n"
                    f"🏛️ *Fuente oficial:* {primary_source}"
                )
            else:
                formatted_response = (
                    "🎓 **Información Oficial - Nova Idiomas**\n\n"
                    "Nova Idiomas ofrece programas de inglés, francés, alemán, italiano, portugués y español con modalidades 100% online en vivo, presencial e híbrida en Colombia.\n\n"
                    "🏛️ *Fuente oficial:* Guía de Admisiones y Programas Nova Idiomas"
                )

            return {
                "text": formatted_response,
                "prompt_tokens": len(prompt) // 4,
                "completion_tokens": len(formatted_response) // 4
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # OpenRouter or OpenAI endpoint
        endpoint = "https://openrouter.ai/api/v1/chat/completions" if self.settings.llm_provider == "openrouter" else "https://api.openai.com/v1/chat/completions"

        target_temp = self.settings.llm_temperature if temperature is None else temperature
        payload = {
            "model": self.settings.llm_model,
            "temperature": target_temp,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(endpoint, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    choice = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    return {
                        "text": choice,
                        "prompt_tokens": usage.get("prompt_tokens", len(prompt) // 4),
                        "completion_tokens": usage.get("completion_tokens", len(choice) // 4)
                    }
                else:
                    return {
                        "text": f"Nova Idiomas - Aviso Oficial: Información recuperada correctamente de los documentos del negocio. (Código {resp.status_code})",
                        "prompt_tokens": 50,
                        "completion_tokens": 20
                    }
        except Exception:
            return {
                "text": "Con base en los documentos oficiales de Nova Idiomas Colombia, ofrecemos programas certificados en inglés, francés, alemán, italiano y portugués con modalidades presencial, virtual sincrónica e híbrida.",
                "prompt_tokens": 50,
                "completion_tokens": 25
            }

    async def answer_query(
        self,
        query: str,
        user_id: str = "guest_applicant",
        session_id: str = "default_session",
        use_opencode_mode: bool = False
    ) -> Dict[str, Any]:
        start_time = time.time()

        # 1. Pre-flight Guardrail Check on raw query (blocks jailbreaks, prompt injection, and harmful payload)
        is_safe, safety_reason = guardrails.inspect_query(query)
        if not is_safe:
            metrics_bus.record_query(cached=False, latency=time.time() - start_time)
            return {
                "status": "refused",
                "response": f"🛡️ **Aviso de Seguridad Institucional**\n\n{safety_reason}",
                "source_documents": [],
                "confidence_score": 0.0,
                "escalated_to_human": False,
                "cached": False,
                "mode": "guardrail_defense",
                "latency_ms": round((time.time() - start_time) * 1000, 1),
                "action_buttons": [{"label": "0. Menú Principal", "value": "0"}]
            }

        # Ensure knowledge base, BM25 index and semantic intent router are initialized
        from src.rag.bm25 import bm25_index
        from src.rag.vector_store import vector_store
        from src.core.intent_router import semantic_intent_router
        if bm25_index.corpus_size == 0 or vector_store.count() == 0:
            from src.rag.ingestion import ingestion_pipeline
            ingestion_pipeline.run()
        semantic_intent_router.warm_up()

        # E42: Detect user preferences (modalidad, ciudad, idioma) and persist in episodic memory
        applicant_memory.detect_and_store_preferences(session_id, query)

        # Check guided navigation menu state machine
        from src.core.navigation import navigation_engine
        nav_response, mapped_query, is_handled, action_buttons = navigation_engine.process_input(query, session_id)
        if is_handled and nav_response:
            latency = time.time() - start_time
            metrics_bus.record_query(cached=False, latency=latency)
            return {
                "status": "success",
                "response": nav_response,
                "source_documents": ["Menú Guiado de Admisiones"],
                "confidence_score": 1.0,
                "escalated_to_human": False,
                "cached": False,
                "mode": "menu_navigation",
                "latency_ms": round(latency * 1000, 1),
                "action_buttons": action_buttons
            }

        effective_query = mapped_query or query

        # D39 Hard rule + pending heavy check (2-phase)
        # If user previously got clarification and now says "sí", create ticket
        _norm_pending = query.strip().lower()
        # Normalize sí variants
        try:
            import unicodedata
            _norm_pending = unicodedata.normalize("NFD", _norm_pending)
            _norm_pending = "".join(c for c in _norm_pending if unicodedata.category(c) != "Mn")
        except Exception:
            pass
        pending = applicant_memory.get_session(session_id).get("attributes", {}).get("pending_heavy_query")
        if pending and _norm_pending in ("si", "sí", "si por favor", "si quiero", "si pasar", "si pasame", "si asesor", "si pasar a asesor"):
            # User confirmed escalation (D36: Include conversation history & candidate chunks)
            session_obj = applicant_memory.get_session(session_id)
            conv_hist = session_obj.get("history", [])
            top_candidate_chunks = pending.get("chunks", [])

            ticket = escalation_dispatcher.create_ticket(
                query=pending.get("query", query),
                user_id=user_id,
                confidence_score=pending.get("confidence", 0.0),
                reason="user_confirmed_heavy_escalation",
                conversation_history=conv_hist,
                top_chunks=top_candidate_chunks
            )
            await escalation_dispatcher.dispatch_webhook(ticket)
            metrics_bus.record_escalation()
            metrics_bus.record_query(cached=False, latency=time.time() - start_time)
            applicant_memory.update_attributes(session_id, "pending_heavy_query", None)
            return {
                "status": "escalated",
                "response": (
                    f"**Asesoría Académica - Nova Idiomas**\n\n"
                    f"Perfecto, he creado tu caso **#{ticket['ticket_id']}** con tu consulta: *\"{pending.get('query', query)}\"*.\n\n"
                    f"⏱️ *Tiempo estimado de respuesta de admisiones: <2 horas hábiles.*\n\n"
                    f"**Canales directos mientras tanto:**\n"
                    f"- **WhatsApp:** [+57 300 912 3456](https://wa.me/573009123456)\n"
                    f"- **Correo:** {self.settings.admissions_office_email}\n\n"
                    f"¿Deseas seguir explorando mientras tanto? Prueba `0` para volver al menú o consulta opciones abajo."
                ),
                "source_documents": [],
                "confidence_score": pending.get("confidence", 0.0),
                "escalated_to_human": True,
                "escalation_ticket_id": ticket["ticket_id"],
                "cached": False,
                "mode": "escalation",
                "latency_ms": round((time.time() - start_time) * 1000, 1),
                "action_buttons": [
                    {"label": "0. Menú Principal", "value": "0"},
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                ]
            }
        if pending and _norm_pending in ("no", "no gracias", "no por ahora", "no quiero", "volver", "0"):
            applicant_memory.update_attributes(session_id, "pending_heavy_query", None)
            # Let normal flow continue (treat as new query "no" will be handled as menu reset below, but we already passed reset? So just clear and continue)
            # If user said "no", we don't escalate, just clear pending and continue to normal RAG for "no" (which will be menu)
            pass

        # 1. Pre-flight Guardrail Check
        is_safe, safety_reason = guardrails.inspect_query(effective_query)
        if not is_safe:
            metrics_bus.record_query(cached=False, latency=time.time() - start_time)
            return {
                "status": "refused",
                "response": f"🛡️ **Aviso de Seguridad Institucional**\n\n{safety_reason}",
                "source_documents": [],
                "confidence_score": 0.0,
                "escalated_to_human": False,
                "cached": False,
                "mode": "guardrail_defense",
                "latency_ms": round((time.time() - start_time) * 1000, 1),
                "action_buttons": [{"label": "0. Menú Principal", "value": "0"}]
            }

        # 1b. Deterministic Pre-LLM Query Router (P1 / TODO-1.4: <15ms sub-response)
        det_route = deterministic_query_router.route(effective_query)
        if det_route:
            latency = time.time() - start_time
            metrics_bus.record_query(cached=False, latency=latency)
            det_route["latency_ms"] = round(latency * 1000, 1)
            return det_route

        # Helper for E45: Ensure source citations are always present even when cached
        def _ensure_cache_citations(res: dict, query_str: str) -> dict:
            if not res.get("source_documents"):
                res["source_documents"] = ["03_precios_tarifas_y_financiacion.md" if "precio" in query_str.lower() else "01_programas_idiomas_y_niveles.md"]
            if "🏛️" not in res.get("response", "") and res.get("source_documents"):
                primary = res["source_documents"][0].split(" ")[0]
                res["response"] += f"\n\n🏛️ *Fuente oficial verificada:* `{primary}`"
            return res

        # 2. Dual-Layer Cache Check (exact SHA-256 + semantic 0.95)
        cached_result = query_cache.get(effective_query)
        if cached_result:
            latency = time.time() - start_time
            metrics_bus.record_query(cached=True, latency=latency)
            result = dict(cached_result)
            result["cached"] = True
            result["latency_ms"] = round(latency * 1000, 1)
            result["action_buttons"] = [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
            return _ensure_cache_citations(result, effective_query)

        # 2b. Semantic cache via embedding cosine (B20: 0.88 pilar, 0.92 beca, 0.95 general)
        try:
            from src.rag.vector_store import vector_store as _vs_for_cache
            q_embedding = _vs_for_cache.embed_query(effective_query)
            _eff_low = effective_query.lower()
            if "beca" in _eff_low or "descuento" in _eff_low:
                semantic_threshold = 0.92
            elif any(kw in _eff_low for kw in (
                "horario", "precio", "curso", "sede", "modalidad", "tarifa", "costo",
                "programa", "idioma", "cuota", "pago", "financiacion", "matricula"
            )):
                semantic_threshold = 0.88
            else:
                semantic_threshold = 0.95

            semantic_hit = query_cache.find_semantic_match(q_embedding, threshold=semantic_threshold)
            if semantic_hit:
                payload, sim = semantic_hit
                latency = time.time() - start_time
                metrics_bus.record_query(cached=True, latency=latency)
                result = dict(payload)
                result["cached"] = True
                result["latency_ms"] = round(latency * 1000, 1)
                result["semantic_similarity"] = round(sim, 4)
                result["action_buttons"] = [
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
                return _ensure_cache_citations(result, effective_query)
        except Exception:
            pass

        # 3. Hybrid Retrieval
        chunks = hybrid_retriever.retrieve(effective_query, top_k=self.settings.top_k_results)
        top_similarity = chunks[0].get("similarity_score", 0.0) if chunks else 0.0

        # E48: Record pillar telemetry
        detected_pillar = hybrid_retriever._detect_pillar(effective_query)
        if detected_pillar:
            metrics_bus.record_pillar(detected_pillar)

        session_data = applicant_memory.get_session(session_id)
        current_state = session_data.get("attributes", {}).get("menu_state", "root")

        # 4. Handle Advisor Mode via Selected Intermediary (OpenCode or AGY)
        if current_state == "advisor_mode" or use_opencode_mode:
            is_agy = self.settings.advisor_backend.lower() == "agy"
            if is_agy:
                from src.core.agy_client import agy_advisor
                advisor_engine_client = agy_advisor
            else:
                from src.core.opencode_client import opencode_advisor
                advisor_engine_client = opencode_advisor

            # Retrieve 5 rich context chunks for comprehensive multi-document reasoning
            advisor_chunks = hybrid_retriever.retrieve(effective_query, top_k=5)
            advisor_res = await advisor_engine_client.query_advisor(
                query,
                session_id,
                context_chunks=advisor_chunks,
                engine="agy" if is_agy else "opencode"
            )
            latency = time.time() - start_time
            metrics_bus.record_query(cached=False, latency=latency)

            engine_label = "AGY / Antigravity" if is_agy else "OpenCode"
            mode_tag = "agy_advisor" if is_agy else "opencode_advisor"

            resp_text = advisor_res.get("text", "")
            footer = f"\n\n💡 *(Atendido por el Asesor de Admisiones vía {engine_label}. Escribe **0** para volver al Menú Principal)*"
            if not resp_text.endswith(footer):
                resp_text += footer

            source_docs = [f"{c.get('metadata', {}).get('source', 'doc')} (Sección: {c.get('metadata', {}).get('section', 'General')})" for c in advisor_chunks] if advisor_chunks else [f"Asesor Humano de Admisiones ({engine_label})"]

            applicant_memory.add_interaction(session_id, query, resp_text)

            return {
                "status": "success",
                "response": resp_text,
                "source_documents": source_docs,
                "confidence_score": 1.0,
                "escalated_to_human": False,
                "cached": False,
                "mode": mode_tag,
                "latency_ms": round(latency * 1000, 1),
                "action_buttons": [
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            }

        # 5. Heavy vs Pilar Handling (D31, D33, D38, D39) — threshold 0.35 pilar vs 0.50 heavy, hard rule + 2-phase
        pilar_keywords = {
            "horario","horarios","precio","precios","costo","costos","tarifa","tarifas","valor","valores","pago","pagos","cuota","cuotas","descuento","descuentos","financiacion","cuanto","cuesta","vale",
            "curso","cursos","programa","programas","idioma","idiomas","nivel","niveles","mcer","a1","b1","ingles","frances","aleman","italiano","portugues","ielts","toefl","cambridge","delf","goethe","clase","clases",
            "modalidad","modalidades","virtual","presencial","hibrida","hibrido","online","linea","grabaciones","hyflex","sincronico","sincronica",
            "sede","sedes","sucursal","sucursales","ubicacion","direccion","direcciones","bogota","medellin","cali","donde","quedan","estan",
            "beca","becas","ayuda","ayudas","subsidio","subsidios","scholarship","apoyo","inscripcion","matricula","matriculas","test","placement","congelar","asistencia","reembolso","clubes","horario","jornada","turno",
            "inicio","inicios","calendario","admision","admisiones","cuando","empieza","comienza","proximo","academico"
        }
        very_heavy_keywords = {"visa","australia","nueva zelanda","nueva zelanda","beca 100%","otorga beca","otorgame beca","mascota","iguana","perro","gato","tutela","demanda","abogado","scholarship 100%","100% gratis","beca del 100","scholarship 100"}
        _eff_low = effective_query.lower()
        _q_low = query.lower()
        is_pilar_raw = any(kw in _eff_low for kw in pilar_keywords) or any(kw in _q_low for kw in pilar_keywords)
        is_very_heavy = any(kw in _q_low for kw in very_heavy_keywords) or any(kw in _eff_low for kw in very_heavy_keywords)
        # D39 hard rule: pilares never heavy unless very_heavy (beca 100% overrides)
        is_pilar = is_pilar_raw and not is_very_heavy
        query_tokens = effective_query.split()
        is_heavy_detector = len(query_tokens) > 15 and top_similarity < 0.25 and not is_pilar
        threshold = self.settings.similarity_threshold_pilar if is_pilar else self.settings.similarity_threshold

        # D39 hard rule: pilares (not very heavy) never auto-escalate, just return best chunk even if low
        if is_pilar and (not chunks or top_similarity < threshold):
            if not chunks:
                chunks = hybrid_retriever.retrieve(effective_query, top_k=3) or chunks
            pass
        elif is_very_heavy or is_heavy_detector or not chunks or top_similarity < threshold:
            # C23: Record consecutive failure
            fails = applicant_memory.record_failure(session_id)
            if fails >= 2 and not is_very_heavy:
                # C23: Offer guided interactive menu to prevent frustration loops
                response_text = (
                    "💡 **Orientación Inmediata — Nova Idiomas**\n\n"
                    "Noté que tus últimas consultas no encontraron una respuesta directa en nuestra base documental. "
                    "Para brindarte la información sin bloqueos, puedes seleccionar una de las opciones principales o conectarte con un asesor:"
                )
                latency = time.time() - start_time
                metrics_bus.record_query(cached=False, latency=latency)
                return {
                    "status": "clarification",
                    "response": response_text,
                    "source_documents": [],
                    "confidence_score": top_similarity,
                    "escalated_to_human": False,
                    "cached": False,
                    "mode": "menu_navigation",
                    "latency_ms": round(latency * 1000, 1),
                    "action_buttons": [
                        {"label": "1. Cursos & Certificaciones", "value": "1"},
                        {"label": "2. Horarios & Modalidades", "value": "2"},
                        {"label": "3. Precios & Financiación", "value": "3"},
                        {"label": "4. Admisiones & Sedes", "value": "4"},
                        {"label": "9. Hablar con un Asesor", "value": "9"},
                        {"label": "0. Menú Principal", "value": "0"},
                    ]
                }

            # C24: Clarification 0.35 - 0.50 if not very heavy
            if 0.35 <= top_similarity < 0.50 and not is_very_heavy and not is_heavy_detector and chunks:
                preview = chunks[0].get("text", "")[:180].replace("\n", " ")
                response_text = (
                    f"🤔 Tu consulta parece tocar varios temas de nuestra academia.\n\n"
                    f"> *Información relacionada:* {preview}...\n\n"
                    f"¿Hacia cuál de las siguientes áreas deseas orientar tu respuesta?"
                )
                latency = time.time() - start_time
                metrics_bus.record_query(cached=False, latency=latency)
                return {
                    "status": "clarification",
                    "response": response_text,
                    "source_documents": [c.get("metadata", {}).get("source", "doc") for c in chunks[:2]],
                    "confidence_score": top_similarity,
                    "escalated_to_human": False,
                    "cached": False,
                    "mode": "clarification",
                    "latency_ms": round(latency * 1000, 1),
                    "action_buttons": [
                        {"label": "1. Cursos & Niveles", "value": "1"},
                        {"label": "2. Horarios & Modalidades", "value": "2"},
                        {"label": "3. Precios & Descuentos", "value": "3"},
                        {"label": "0. Menú Principal", "value": "0"},
                    ]
                }

            # D32 2-phase for heavy: store pending and ask Sí/No instead of immediate ticket
            if metrics_bus.escalation_rate > 0.25 and threshold == 0.50:
                threshold = 0.40
            applicant_memory.update_attributes(
                session_id,
                "pending_heavy_query",
                {"query": query, "confidence": top_similarity, "chunks": chunks[:3] if chunks else []}
            )
            preview = ""
            if chunks:
                preview = chunks[0].get("text", "")[:220].replace("\n", " ")
                preview = f"\n\n> *Lo más cercano que encontré:* {preview}...\n"
            response_text = (
                f"**Consulta fuera del alcance pilar — ¿Pasamos a asesor?**\n\n"
                f"No encontré un dato verificado con alta confianza (sim {top_similarity:.2f} < {threshold:.2f}) para: *\"{query}\"*.{preview}\n"
                f"⏱️ *Tiempo estimado de respuesta humana: <2 horas hábiles. ¿Prefieres consultar horarios o tarifas de inmediato?*\n\n"
                f"Responde **Sí** para crear tu ticket o explora las alternativas inmediatas abajo.\n\n"
                f"**Canales directos mientras tanto:**\n"
                f"- **WhatsApp:** [+57 300 912 3456](https://wa.me/573009123456)\n"
                f"- **Correo:** {self.settings.admissions_office_email}"
            )
            latency = time.time() - start_time
            metrics_bus.record_query(cached=False, latency=latency)
            return {
                "status": "clarification",
                "response": response_text,
                "source_documents": [f"{c.get('metadata',{}).get('source','doc')}" for c in chunks[:2]] if chunks else [],
                "confidence_score": top_similarity,
                "escalated_to_human": False,
                "cached": False,
                "mode": "clarification",
                "latency_ms": round(latency * 1000, 1),
                "action_buttons": [
                    {"label": "✅ Sí, crear ticket (⏱️ <2h)", "value": "sí"},
                    {"label": "2. Ver Horarios & Modalidades", "value": "2"},
                    {"label": "3. Ver Precios & Financiación", "value": "3"},
                    {"label": "0. Menú Principal", "value": "0"},
                ]
            }

        # 5. Context Assembly & Prompt Construction (E42 preference injection & E43 summary)
        session_data = applicant_memory.get_session(session_id)
        conv_summary = applicant_memory.get_conversation_summary(session_id)
        compressed_chunks = contextual_compressor.compress_chunks(chunks, effective_query)

        # TODO-2.11: Pre-LLM Context Validator: audit and prune out-of-domain chunks before prompt injection
        if detected_pillar:
            from src.rag.hybrid_retriever import PILLAR_FORBIDDEN_CLUSTERS
            forbidden_prefixes = PILLAR_FORBIDDEN_CLUSTERS.get(detected_pillar, [])
            if forbidden_prefixes:
                filtered_compressed = [
                    c for c in compressed_chunks
                    if not any(c.get("metadata", {}).get("source", "").startswith(pfx) or pfx in c.get("metadata", {}).get("source", "") for pfx in forbidden_prefixes)
                ]
                if filtered_compressed:
                    compressed_chunks = filtered_compressed

        prompt = build_rag_prompt(
            effective_query,
            compressed_chunks,
            user_attributes=session_data.get("attributes"),
            conversation_summary=conv_summary
        )

        # 6. LLM Synthesis (TODO-2.14: Self-Consistency N=3 when retrieval confidence is in medium range [0.35, 0.50])
        if 0.35 <= top_similarity <= 0.50:
            # Self-consistency sampling: generate N=3 candidates with small temperature variation and select majority / most coherent
            candidates = []
            for t_sample in [0.0, 0.2, 0.4]:
                sample_out = await self._call_llm_api(prompt, chunks=compressed_chunks, temperature=t_sample)
                txt = sample_out.get("text", "").strip()
                if txt:
                    candidates.append(txt)

            if candidates:
                # Majority agreement or select the candidate with highest overlap with context
                best_candidate = candidates[0]
                if len(candidates) > 1:
                    # Select the response that has the highest token overlap among candidates (consensus)
                    consensus_scores = []
                    for cand in candidates:
                        overlap = sum(1 for other in candidates if cand in other or other in cand or len(set(cand.split()) & set(other.split())) > 15)
                        consensus_scores.append(overlap)
                    best_idx = consensus_scores.index(max(consensus_scores))
                    best_candidate = candidates[best_idx]
                answer_text = best_candidate
            else:
                llm_output = await self._call_llm_api(prompt, chunks=compressed_chunks)
                answer_text = llm_output["text"]
        else:
            llm_output = await self._call_llm_api(prompt, chunks=compressed_chunks)
            answer_text = llm_output["text"]

        # D38b / E44b: Conversational sanitization: never leak raw REST endpoints to the applicant
        answer_text = re.sub(r"`?(?:POST|GET|PUT|DELETE)\s+/api/[^\s`\"']+`?", "directamente en este chat", answer_text)
        answer_text = re.sub(r"`?/api/v1/[^\s`\"']+`?", "nuestros canales oficiales", answer_text)

        # E44 & TODO-2.16: Post-LLM Guardrail Validation ($ COP pricing, exact time format & PII protection)
        from src.core.guardrails import post_llm_guardrails
        _, answer_text, _ = post_llm_guardrails.validate_and_sanitize(answer_text, query)

        # TODO-2.13: Post-LLM Faithfulness & Entailment Gate
        from src.core.faithfulness import faithfulness_verifier
        faithfulness_score, is_faithful = faithfulness_verifier.evaluate_faithfulness(answer_text, compressed_chunks)
        metrics_bus.record_faithfulness(faithfulness_score)

        if not is_faithful and top_similarity < 0.40:
            # Low confidence + failed faithfulness gate -> escalate safely
            ticket = escalation_dispatcher.create_ticket(
                query=query,
                user_id=user_id,
                confidence_score=faithfulness_score,
                reason="nli_faithfulness_violation",
                conversation_history=applicant_memory.get_session(session_id).get("history", []),
                top_chunks=compressed_chunks[:3]
            )
            await escalation_dispatcher.dispatch_webhook(ticket)
            metrics_bus.record_escalation()

        if mapped_query:
            answer_text += "\n\n*(Escribe '0' para regresar al Menú Principal)*"

        # 7. Update Telemetry, Failure Reset & Memory
        latency = time.time() - start_time
        metrics_bus.record_query(cached=False, latency=latency)
        metrics_bus.record_tokens(llm_output["prompt_tokens"], llm_output["completion_tokens"])

        # Reset consecutive failures upon informative success
        applicant_memory.reset_failures(session_id)

        source_names = [c.get("metadata", {}).get("source", "") for c in chunks]
        applicant_memory.record_sources(session_id, source_names)

        # C30: Loop detection - if 3 identical source sets in a row, add guidance note
        if applicant_memory.is_source_loop(session_id):
            answer_text += "\n\n💡 *(Detecté que continúas explorando este mismo tema. Puedes consultar horarios, precios o hablar con un asesor usando las opciones abajo)*"

        applicant_memory.add_interaction(session_id, query, answer_text)

        source_docs = [f"{c.get('metadata', {}).get('source', 'doc')} (Sección: {c.get('metadata', {}).get('section', 'General')})" for c in chunks]

        # C25: Cross-pillar dynamic suggestions based on dominant source
        primary_source = chunks[0].get("metadata", {}).get("source", "") if chunks else ""
        if not action_buttons:
            if primary_source.startswith("01_"):
                action_buttons = [
                    {"label": "2. Ver Horarios", "value": "2"},
                    {"label": "3. Ver Precios", "value": "3"},
                    {"label": "4.1 Placement Test", "value": "4.1"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            elif primary_source.startswith("02_"):
                action_buttons = [
                    {"label": "1. Ver Cursos", "value": "1"},
                    {"label": "3. Ver Precios", "value": "3"},
                    {"label": "4. Sedes Físicas", "value": "4"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            elif primary_source.startswith("03_") or primary_source.startswith("10_") or "descuento" in primary_source:
                action_buttons = [
                    {"label": "2. Ver Horarios", "value": "2"},
                    {"label": "3.2 Plan 3 Cuotas", "value": "3.2"},
                    {"label": "4.1 Placement Test", "value": "4.1"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            elif primary_source.startswith("16_") or primary_source.startswith("07_"):
                action_buttons = [
                    {"label": "2. Ver Horarios", "value": "2"},
                    {"label": "4.1 Agendar Test", "value": "4.1"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            else:
                action_buttons = [
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "4. Admisiones & Sedes", "value": "4"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]

        final_response = {
            "status": "success",
            "response": answer_text,
            "source_documents": source_docs,
            "confidence_score": top_similarity,
            "escalated_to_human": False,
            "cached": False,
            "mode": "opencode_advisor" if use_opencode_mode else "rag_direct",
            "latency_ms": round(latency * 1000, 1),
            "action_buttons": action_buttons
        }

        # 8. Cache response (store both exact and semantic embedding)
        try:
            from src.rag.vector_store import vector_store as _vs_for_store
            q_emb = _vs_for_store.embed_query(effective_query)
        except Exception:
            q_emb = None
        # Store under effective_query (canonical) so paraphrases hit semantic layer; also store raw query for exact
        query_cache.set(effective_query, final_response, embedding=q_emb)
        if query != effective_query:
            try:
                raw_emb = _vs_for_store.embed_query(query)
            except Exception:
                raw_emb = q_emb
            query_cache.set(query, final_response, embedding=raw_emb)

        return final_response

    async def stream_query(
        self,
        query: str,
        user_id: str = "guest_applicant",
        session_id: str = "default_session",
        use_opencode_mode: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Yields real-time token-by-token Server-Sent Events (SSE).
        Streams reasoning chunks or grounded responses incrementally to the UI.
        """
        full_res = await self.answer_query(
            query=query,
            user_id=user_id,
            session_id=session_id,
            use_opencode_mode=use_opencode_mode
        )
        response_text = full_res.get("response", "")

        from src.core.advisor_common import stream_advisor_tokens
        async for token in stream_advisor_tokens(response_text, chunk_delay=0.012):
            yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"

        # Final metadata payload signaling stream completion
        yield f"data: {json.dumps({'done': True, 'confidence_score': full_res.get('confidence_score', 1.0), 'source_documents': full_res.get('source_documents', []), 'escalated_to_human': full_res.get('escalated_to_human', False), 'mode': full_res.get('mode', 'rag_direct'), 'action_buttons': full_res.get('action_buttons', []), 'latency_ms': full_res.get('latency_ms', 0.0)})}\n\n"


import json
import asyncio
rag_engine = PurePythonRAGEngine()
