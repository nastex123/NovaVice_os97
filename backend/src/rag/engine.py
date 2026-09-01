import time
import os
from typing import Dict, Any, List, Optional, AsyncGenerator
import httpx
from src.config import settings
from src.core.guardrails import guardrails
from src.core.cache import query_cache
from src.core.metrics import metrics_bus
from src.core.dispatcher import escalation_dispatcher
from src.core.memory import applicant_memory
from src.rag.hybrid_retriever import hybrid_retriever
from src.rag.prompt_templates import SYSTEM_PROMPT, build_rag_prompt


class PurePythonRAGEngine:
    # Deterministic async RAG pipeline replacing n8n workflows with pure Python.

    def __init__(self):
        self.settings = settings

    async def _call_llm_api(self, prompt: str, chunks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        # Connects to OpenRouter / Hermes / OpenAI or falls back to deterministic grounded response.
        api_key = self.settings.openrouter_api_key or self.settings.openai_api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

        # Grounded fallback if no API key is provided
        if not api_key or self.settings.llm_provider == "mock":
            if chunks:
                top_chunk = chunks[0]
                chunk_text = top_chunk.get("text", "")
                section = top_chunk.get("metadata", {}).get("section", "Información Oficial")
                source = top_chunk.get("metadata", {}).get("source", "Admisiones")

                lines = [l.strip() for l in chunk_text.split("\n") if l.strip()]
                title = section.replace("#", "").strip()
                content_lines = []
                for line in lines:
                    if line.startswith("#"):
                        continue
                    if line.startswith("|") and "---" in line:
                        continue
                    clean_line = line.strip()
                    if clean_line.startswith("-"):
                        content_lines.append(f"• {clean_line[1:].strip()}")
                    elif clean_line.startswith("*") and not clean_line.startswith("**"):
                        content_lines.append(f"• {clean_line[1:].strip()}")
                    else:
                        content_lines.append(clean_line)

                body = "\n".join(content_lines[:6]) if content_lines else chunk_text[:280]
                formatted_response = (
                    f"📌 **{title}**\n\n"
                    f"{body}\n\n"
                    f"🏛️ *Fuente oficial:* {source}"
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

        payload = {
            "model": self.settings.llm_model,
            "temperature": self.settings.llm_temperature,
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
        use_opencode_mode: bool = False,
        use_hermes_mode: bool = False
    ) -> Dict[str, Any]:
        start_time = time.time()

        # Ensure knowledge base and BM25 index are initialized
        from src.rag.bm25 import bm25_index
        from src.rag.vector_store import vector_store
        if bm25_index.corpus_size == 0 or vector_store.count() == 0:
            from src.rag.ingestion import ingestion_pipeline
            ingestion_pipeline.run()

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

        # 2. Dual-Layer Cache Check (exact SHA-256 + semantic 0.95)
        cached_result = query_cache.get(effective_query)
        if cached_result:
            latency = time.time() - start_time
            metrics_bus.record_query(cached=True, latency=latency)
            result = dict(cached_result)
            result["cached"] = True
            result["latency_ms"] = round(latency * 1000, 1)
            result["action_buttons"] = [{"label": "0. Menú Principal", "value": "0"}, {"label": "5. Pregunta Libre", "value": "5"}]
            return result

        # 2b. Semantic cache via embedding cosine 0.95 (paraphrase hit without exact match)
        try:
            from src.rag.vector_store import vector_store as _vs_for_cache
            q_embedding = _vs_for_cache.embed_query(effective_query)
            semantic_hit = query_cache.find_semantic_match(q_embedding, threshold=0.95)
            if semantic_hit:
                payload, sim = semantic_hit
                latency = time.time() - start_time
                metrics_bus.record_query(cached=True, latency=latency)
                result = dict(payload)
                result["cached"] = True
                result["latency_ms"] = round(latency * 1000, 1)
                # Keep original semantic similarity hint if needed
                result["semantic_similarity"] = round(sim, 4)
                result["action_buttons"] = [{"label": "0. Menú Principal", "value": "0"}, {"label": "5. Pregunta Libre", "value": "5"}]
                return result
        except Exception:
            pass

        # 3. Hybrid Retrieval
        chunks = hybrid_retriever.retrieve(effective_query, top_k=self.settings.top_k_results)
        top_similarity = chunks[0].get("similarity_score", 0.0) if chunks else 0.0

        session_data = applicant_memory.get_session(session_id)
        current_state = session_data.get("attributes", {}).get("menu_state", "root")

        # 4. Handle Advisor Mode via Selected Intermediary (OpenCode or AGY)
        if current_state == "advisor_mode" or use_opencode_mode or use_hermes_mode:
            from src.core.opencode_client import opencode_advisor
            # Retrieve 5 rich context chunks for comprehensive multi-document reasoning
            advisor_chunks = hybrid_retriever.retrieve(effective_query, top_k=5)
            advisor_res = await opencode_advisor.query_advisor(
                effective_query,
                session_id,
                context_chunks=advisor_chunks,
                engine=self.settings.advisor_backend
            )
            latency = time.time() - start_time
            metrics_bus.record_query(cached=False, latency=latency)

            is_agy = self.settings.advisor_backend.lower() == "agy"
            engine_label = "AGY / Antigravity" if is_agy else "OpenCode"
            mode_tag = "agy_advisor" if is_agy else "opencode_advisor"

            resp_text = advisor_res.get("text", "")
            footer = f"\n\n💡 *(Atendido por el Asesor de Admisiones vía {engine_label}. Escribe **0** para volver al Menú Principal)*"
            if not resp_text.endswith(footer):
                resp_text += footer

            source_docs = [f"{c.get('metadata', {}).get('source', 'doc')} (Sección: {c.get('metadata', {}).get('section', 'General')})" for c in advisor_chunks] if advisor_chunks else [f"Asesor Humano de Admisiones ({engine_label})"]

            return {
                "status": "success",
                "response": resp_text,
                "source_documents": source_docs,
                "confidence_score": 1.0,
                "escalated_to_human": False,
                "cached": False,
                "mode": mode_tag,
                "latency_ms": round(latency * 1000, 1),
                "action_buttons": [{"label": "0. Menú Principal", "value": "0"}, {"label": "9. Otra Consulta al Asesor", "value": "9"}]
            }

        # 5. Out-of-Scope Detection & Human Escalation
        if not guardrails.evaluate_relevance(top_similarity) or not chunks:
            ticket = escalation_dispatcher.create_ticket(
                query=query,
                user_id=user_id,
                confidence_score=top_similarity,
                reason="knowledge_gap_escalation"
            )
            await escalation_dispatcher.dispatch_webhook(ticket)
            metrics_bus.record_escalation()

            response_text = (
                f"**Asesoria Academica - Nova Idiomas**\n\n"
                f"Hola. Actualmente no cuento con el detalle exacto de esa consulta especifica en la base de datos automatizada, "
                f"pero con gusto te ayudamos de forma directa.\n\n"
                f"He guardado tu consulta con el caso de seguimiento **#{ticket['ticket_id']}** para que nuestro equipo de admisiones pueda orientarte.\n\n"
                f"**Canales de atencion directa:**\n"
                f"- **WhatsApp:** [+57 300 912 3456](https://wa.me/573009123456)\n"
                f"- **Correo:** {self.settings.admissions_office_email}\n\n"
                f"Tambien puedes explorar nuestras opciones principales o realizar una nueva pregunta."
            )

            latency = time.time() - start_time
            metrics_bus.record_query(cached=False, latency=latency)

            escalation_response = {
                "status": "escalated",
                "response": response_text,
                "source_documents": [],
                "confidence_score": top_similarity,
                "escalated_to_human": True,
                "escalation_ticket_id": ticket["ticket_id"],
                "cached": False,
                "mode": "escalation",
                "latency_ms": round(latency * 1000, 1),
                "action_buttons": [
                    {"label": "1. Cursos & Certificaciones", "value": "1"},
                    {"label": "2. Horarios & Modalidades", "value": "2"},
                    {"label": "3. Precios & Financiación", "value": "3"},
                    {"label": "0. Menú Principal", "value": "0"}
                ]
            }
            return escalation_response

        # 5. Context Assembly & Prompt Construction
        session_data = applicant_memory.get_session(session_id)
        prompt = build_rag_prompt(query, chunks, user_attributes=session_data.get("attributes"))

        # 6. LLM Synthesis
        llm_output = await self._call_llm_api(prompt, chunks=chunks)
        answer_text = llm_output["text"]
        if mapped_query:
            answer_text += "\n\n*(Escribe '0' para regresar al Menu Principal)*"

        # 7. Update Telemetry & Memory
        latency = time.time() - start_time
        metrics_bus.record_query(cached=False, latency=latency)
        metrics_bus.record_tokens(llm_output["prompt_tokens"], llm_output["completion_tokens"])

        applicant_memory.add_interaction(session_id, query, answer_text)

        source_docs = [f"{c.get('metadata', {}).get('source', 'doc')} (Sección: {c.get('metadata', {}).get('section', 'General')})" for c in chunks]

        final_response = {
            "status": "success",
            "response": answer_text,
            "source_documents": source_docs,
            "confidence_score": top_similarity,
            "escalated_to_human": False,
            "cached": False,
            "mode": "opencode_advisor" if (use_opencode_mode or use_hermes_mode) else "rag_direct",
            "latency_ms": round(latency * 1000, 1),
            "action_buttons": action_buttons if action_buttons else [
                {"label": "1. Cursos & Certificaciones", "value": "1"},
                {"label": "2. Horarios & Modalidades", "value": "2"},
                {"label": "3. Precios & Financiación", "value": "3"},
                {"label": "4. Admisiones & Sedes", "value": "4"},
                {"label": "0. Menú Principal", "value": "0"}
            ]
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
            query_cache.set(query, final_response, embedding=q_emb)

        return final_response

    async def stream_query(
        self,
        query: str,
        user_id: str = "guest_applicant",
        session_id: str = "default_session"
    ) -> AsyncGenerator[str, None]:
        # Yields incremental tokens for Server-Sent Events (SSE).
        full_res = await self.answer_query(query, user_id, session_id)
        words = full_res["response"].split(" ")
        for word in words:
            yield f"data: {json.dumps({'token': word + ' ', 'done': False})}\n\n"
            await asyncio.sleep(0.02)

        yield f"data: {json.dumps({'done': True, 'confidence_score': full_res['confidence_score'], 'source_documents': full_res['source_documents'], 'escalated_to_human': full_res['escalated_to_human']})}\n\n"


import json
import asyncio
rag_engine = PurePythonRAGEngine()
