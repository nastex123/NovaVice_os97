import math
import re
from typing import List, Dict, Any, Optional, Tuple
from src.rag.vector_store import vector_store
from src.rag.bm25 import bm25_index
from src.core.intent_router import semantic_intent_router
from src.rag.reranker import local_reranker


# B19: Spanglish and English-Spanish terminology mapping
SPANGLISH_REPLACEMENTS = [
    (r"\bschedules?\b", "horario"),
    (r"\btimetables?\b", "horario"),
    (r"\bhoraios?\b", "horarios"),
    (r"\bhoraros?\b", "horarios"),
    (r"\bnocturnos?\b", "nocturno"),
    (r"\bnocturnas?\b", "nocturna"),
    (r"\bnight\b", "noche nocturno"),
    (r"\bfees?\b", "precios"),
    (r"\bprices?\b", "precio"),
    (r"\bcosts?\b", "costo"),
    (r"\bdiscounts?\b", "descuento"),
    (r"\bcourses?\b", "curso"),
    (r"\bclasses?\b", "clases"),
    (r"\bcampus(?:es)?\b", "sede"),
    (r"\blocations?\b", "ubicacion"),
    (r"\bplacement\s+tests?\b", "examen clasificacion"),
    (r"\blevels?\b", "niveles"),
    (r"\bscholarships?\b", "beca descuento"),
    (r"\bfinancial\s+aid\b", "financiacion cuotas"),
    (r"\brequirements?\b", "requisitos"),
    (r"\bregistrations?\b", "matricula inscripcion"),
]

# B11 / B13: Pillar clusters mapping
PILLAR_CLUSTERS = {
    "becas_descuentos": ["12_04", "12_01", "12_02", "12_03", "10_01", "09_03", "12_"],
    "precios": ["03_", "09_", "10_", "12_04", "12_"],
    "horarios": ["02_", "07_01", "07_02", "07_03", "07_04", "07_05", "08_"],
    "cursos": ["01_", "04_0", "05_", "06_"],
    "sedes": ["04_proceso", "07_sedes", "13_", "14_", "15_", "16_", "17_", "18_", "19_", "20_"]
}

# TODO-2.11: Strict Domain Masking to eliminate cross-pillar hallucination / contamination
PILLAR_STRICT_CLUSTERS = {
    "cursos": ["01_", "04_0", "05_", "06_"],
    "precios": ["03_", "09_", "10_", "12_04", "12_"],
    "horarios": ["02_", "07_01", "07_02", "07_03", "07_04", "07_05", "08_"],
    "sedes": ["04_proceso", "07_sedes", "13_", "14_", "15_", "16_", "17_", "18_", "19_", "20_"],
    "becas_descuentos": ["12_04", "12_01", "12_02", "12_03", "10_01", "09_03", "12_"]
}

PILLAR_FORBIDDEN_CLUSTERS = {
    "cursos": ["07_sedes", "13_", "14_", "15_", "16_", "17_", "02_", "03_"],
    "precios": ["02_", "07_sedes", "13_", "14_", "15_", "16_", "17_"],
    "sedes": ["03_", "01_", "05_", "06_"],
    "horarios": ["03_", "13_", "14_", "15_", "16_", "17_"],
    "becas_descuentos": ["07_sedes", "13_", "14_", "15_", "16_", "17_"]
}

# Pillar detection keyword sets
PILLAR_KEYWORDS = {
    "becas_descuentos": {"beca", "becas", "descuento", "descuentos", "subsidio", "subsidios", "bono", "bonos", "convenio", "convenios", "caja", "cajas", "compensacion"},
    "precios": {"precio", "precios", "costo", "costos", "tarifa", "tarifas", "valor", "valores", "pago", "pagos", "cuota", "cuotas", "financiacion", "financiamiento", "inversion", "cuesta", "cuestan", "vale", "valen", "cuanto", "modulo"},
    "horarios": {"horario", "horarios", "horaios", "nocturno", "nocturna", "nocturnos", "nocturnas", "franja", "franjas", "jornada", "jornadas", "turno", "turnos", "modalidad", "modalidades", "virtual", "presencial", "hibrida", "sabados", "domingos", "manana", "tarde", "noche", "noches", "after", "work", "madrugador", "madrugadores"},
    "cursos": {"curso", "cursos", "programa", "programas", "idioma", "idiomas", "nivel", "niveles", "mcer", "a1", "a2", "b1", "b2", "c1", "ingles", "frances", "aleman", "italiano", "portugues", "ielts", "toefl", "cambridge", "delf", "goethe", "clase", "clases", "academico"},
    "sedes": {"sede", "sedes", "sucursal", "sucursales", "ubicacion", "ubicaciones", "direccion", "direcciones", "bogota", "medellin", "cali", "chico", "chapinero", "poblado", "laureles", "granada", "matricula", "inscripcion", "examen", "placement", "test", "inicio", "inicios", "calendario", "admision", "admisiones", "cuando", "empieza", "comienza", "proximo"}
}

# B16: Canonical definition texts for the 5 pillar centroids
PILLAR_CANONICAL_TEXTS = {
    "cursos": "cursos programas academicos oferta idiomas ingles frances aleman italiano portugues niveles marco comun europeo mcer a1 a2 b1 b2 c1 certificaciones internacionales ielts toefl cambridge delf goethe",
    "horarios": "horarios jornadas turnos franjas manana tarde noche sabados domingos modalidades presencial virtual sincronico grabaciones plataforma lms asistencia",
    "precios": "precios costos tarifas inversion colombianos cop mensualidad planes de pago financiacion cuotas interes tarjetas debito credito transferencias",
    "sedes": "sedes sucursales ubicacion direcciones bogota chico chapinero medellin poblado laureles cali granada admisiones matricula inscripcion test examen clasificacion nivelacion",
    "becas_descuentos": "becas no merit scholarships becas disponibles descuentos pago contado diez por ciento convenios cajas compensacion familiar amigos bono matricula aclaratoria 12_04"
}


class HybridRetriever:
    # Combines dense vector retrieval with BM25 lexical search using Reciprocal Rank Fusion,
    # pillar centroid blending, intent boosting, cluster re-ranking, and relaxed fallback.

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k
        self._centroids: Dict[str, List[float]] = {}

    def _ensure_bm25_populated(self):
        if bm25_index.corpus_size == 0:
            docs = vector_store.get_all_documents()
            if docs:
                bm25_index.fit(docs)

    def _normalize_spanglish(self, text: str) -> str:
        # B19: Normalizes English loanwords and Spanglish terms into canonical Spanish equivalents
        normalized = text
        for pattern, replacement in SPANGLISH_REPLACEMENTS:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        return normalized

    def _expand_query(self, query: str) -> str:
        # B17: Lexical query expansion for key admissions intents
        expanded = query
        q_low = query.lower()
        if re.search(r"\bbecas?\b", q_low):
            expanded += " descuento subsidio beneficio aclaratoria 12_04"
        if re.search(r"\b(precio|precios|costo|costos|tarifa|tarifas|cuanto\s+cuesta|cuanto\s+vale)\b", q_low):
            expanded += " inversion planes de pago cuotas mensualidad"
        if re.search(r"\b(horario|horarios|franja|franjas|jornada|turnos?)\b", q_low):
            expanded += " manana tarde noche sabados domingos"
        if re.search(r"\b(curso|cursos|programa|programas|idioma|idiomas)\b", q_low):
            expanded += " niveles intensivo semi-intensivo"
        if re.search(r"\b(sede|sedes|sucursal|sucursales|ubicacion|donde\s+estan)\b", q_low):
            expanded += " direccion bogota chico chapinero medellin poblado laureles cali granada"
        return expanded

    def _detect_negations(self, query: str) -> Dict[str, bool]:
        # B18: Detect negative modality constraints (e.g., 'no virtual' -> penalize 02_05)
        q_low = query.lower()
        return {
            "no_virtual": bool(re.search(r"\bno\s+(?:virtual|online|en\s+l[ií]nea|remoto)\b", q_low)),
            "no_presencial": bool(re.search(r"\bno\s+(?:presencial|en\s+sede|en\s+persona)\b", q_low))
        }

    def _detect_exact_entities(self, query: str) -> Dict[str, bool]:
        # P1 / TODO-1.1: Detect exact entity patterns requiring higher lexical BM25 precision
        q_low = query.lower()
        has_financial = bool(re.search(r"(\$|\bcop\b|\bpesos\b|\bcuotas?\b|\bdescuentos?\b|\b10%|\b15%|\b40/30/30\b|\bcontado\b|\b\d{2,}\b)", q_low))
        has_code_or_cert = bool(re.search(r"\b(a1|a2|b1|b2|c1|c2|ielts|toefl|delf|dalf|goethe|cambridge)\b", q_low))
        has_schedule_entity = bool(re.search(r"(\b\d{1,2}:\d{2}\b|\b6:00\b|\b6:30\b|\b8:00\b|\b8:30\b|\bam\b|\bpm\b|\bmadrugadores?\b|\bafter\s+work\b)", q_low))
        has_specific_campus = bool(re.search(r"\b(chic[oó]|chapinero|poblado|laureles|granada)\b", q_low))
        return {
            "financial": has_financial,
            "certification": has_code_or_cert,
            "schedule": has_schedule_entity,
            "campus": has_specific_campus,
            "has_any_exact": has_financial or has_code_or_cert or has_schedule_entity or has_specific_campus
        }

    def _get_adaptive_rrf_params(self, entities: Dict[str, bool]) -> Tuple[int, int, float, float]:
        # P1 / TODO-1.1: Compute adaptive RRF smoothing parameters and weighting factors
        # Returns: (k_dense, k_bm25, weight_dense, weight_bm25)
        if entities.get("has_any_exact", False):
            # Prioritize lexical exact match for financial figures, codes, or specific campus venues
            return 75, 40, 0.9, 1.25
        # Standard balanced RRF for open conceptual questions
        return self.rrf_k, self.rrf_k, 1.0, 1.0

    def _detect_pillar(self, query: str) -> Optional[str]:
        q_tokens = set(re.findall(r"\b[a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]{2,}\b", query.lower()))
        # Prioritize becas_descuentos if beca/descuento is present
        if any(w in q_tokens for w in PILLAR_KEYWORDS["becas_descuentos"]):
            return "becas_descuentos"
        for pillar, kw_set in PILLAR_KEYWORDS.items():
            if any(w in q_tokens for w in kw_set):
                return pillar
        return None

    def _get_pillar_centroids(self) -> Dict[str, List[float]]:
        # B16: Precompute / lazily compute centroid embeddings for the 5 pillars
        if not self._centroids:
            for pillar_name, canon_text in PILLAR_CANONICAL_TEXTS.items():
                emb = vector_store.embed_query(canon_text)
                if emb and any(v != 0.0 for v in emb):
                    self._centroids[pillar_name] = emb
        return self._centroids

    @staticmethod
    def _cosine(v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 <= 0.0 or norm2 <= 0.0:
            return 0.0
        return dot / (norm1 * norm2)

    def _score_candidates(
        self,
        doc_map: Dict[str, Dict[str, Any]],
        bm25_score_map: Dict[str, float],
        query_tokens: List[str],
        detected_pillar: Optional[str],
        negations: Dict[str, bool],
        query_embedding: List[float],
        intent_match: Optional[Any] = None
    ) -> None:
        num_query_tokens = max(1, len(query_tokens))
        centroids = self._get_pillar_centroids() if detected_pillar else {}

        for doc_id, item in doc_map.items():
            bm_score = bm25_score_map.get(doc_id, 0.0)
            doc_text_lower = item["text"].lower()
            source_name = item.get("metadata", {}).get("source", "")
            matching_tokens = sum(1 for tok in query_tokens if tok in doc_text_lower)
            coverage = matching_tokens / float(num_query_tokens)

            # B11: Coverage * 1.4 boost when a pillar is detected
            if detected_pillar:
                coverage = min(1.0, coverage * 1.4)

            # Weighted normalization requiring sufficient query coverage
            if bm_score > 0 and matching_tokens > 0:
                base_norm = min(1.0, bm_score / 3.0)
                norm_bm = base_norm * coverage
                if coverage >= 0.5:
                    norm_bm = min(1.0, norm_bm * 1.25)
            else:
                norm_bm = 0.0

            dense_sim = item.get("similarity_score", 0.0)
            fused_sim = round(max(dense_sim, norm_bm), 4)

            # B16: Centroid blending (0.7 * similarity + 0.3 * centroid_cosine)
            if detected_pillar and detected_pillar in centroids and query_embedding:
                target_prefixes = PILLAR_CLUSTERS.get(detected_pillar, [])
                is_pillar_doc = any(source_name.startswith(pfx) for pfx in target_prefixes)
                if is_pillar_doc:
                    c_sim = self._cosine(query_embedding, centroids[detected_pillar])
                    if c_sim > 0.0:
                        fused_sim = round(0.7 * fused_sim + 0.3 * c_sim, 4)

            # B11: Cluster affinity boost (+0.15) if document belongs to target pillar cluster
            if detected_pillar:
                target_prefixes = PILLAR_CLUSTERS.get(detected_pillar, [])
                if any(source_name.startswith(pfx) for pfx in target_prefixes):
                    fused_sim = min(1.0, round(fused_sim + 0.15, 4))

            # Targeted micro-intent cluster boost (+0.12)
            if intent_match and intent_match.target_cluster and source_name == intent_match.target_cluster:
                fused_sim = min(1.0, round(fused_sim + 0.12, 4))

            # B18: Negation adjustment (no virtual penalizes 02_05; no presencial penalizes physical)
            if negations["no_virtual"] and ("02_05" in source_name or "virtual" in source_name):
                fused_sim = round(fused_sim * 0.3, 4)
            if negations["no_presencial"] and any(p in source_name for p in ("02_01", "02_02", "02_03", "02_04")):
                fused_sim = round(fused_sim * 0.3, 4)

            item["similarity_score"] = fused_sim

    def retrieve(self, query: str, top_k: int = 4, candidate_k: int = 15) -> List[Dict[str, Any]]:
        self._ensure_bm25_populated()

        # B19: Normalize Spanglish loanwords
        clean_query = self._normalize_spanglish(query)

        # Detect pillar and negative filters
        detected_pillar = self._detect_pillar(clean_query)
        negations = self._detect_negations(clean_query)

        # Vectorized Intent Router Classification
        macro_to_pillar = {
            "cursos_idiomas_niveles": "cursos",
            "horarios_modalidades_franjas": "horarios",
            "precios_tarifas_financiacion": "precios",
            "admisiones_sedes_matricula": "sedes",
            "becas_descuentos_convenios": "becas_descuentos",
        }
        intent_match = semantic_intent_router.classify(clean_query)
        semantic_pillar = macro_to_pillar.get(intent_match.top_macro_pillar)
        if not detected_pillar and semantic_pillar and intent_match.macro_score >= 0.20:
            detected_pillar = semantic_pillar

        # B17: Expand query for enhanced semantic & lexical recall
        expanded_query = self._expand_query(clean_query)

        # 1. Dense retrieval using vector store
        dense_results = vector_store.query(expanded_query, top_k=candidate_k)
        query_embedding = vector_store.embed_query(expanded_query)

        # 2. Lexical BM25 retrieval
        bm25_results = bm25_index.search(expanded_query, top_k=candidate_k)

        # If BM25 is not populated, fallback to dense results
        if not bm25_results:
            return dense_results[:top_k]

        # 3. Build candidate lookup map
        dense_ranks = {item["id"]: rank for rank, item in enumerate(dense_results)}
        bm25_ranks = {doc_id: rank for rank, (doc_id, score) in enumerate(bm25_results)}
        bm25_score_map = {doc_id: score for doc_id, score in bm25_results}

        doc_map = {item["id"]: dict(item) for item in dense_results}
        all_docs = vector_store.get_all_documents()
        all_docs_dict = {d["id"]: d for d in all_docs}

        for doc_id, (did, score) in enumerate(bm25_results):
            if did not in doc_map and did in all_docs_dict:
                d = all_docs_dict[did]
                doc_map[did] = {
                    "id": did,
                    "text": d["text"],
                    "metadata": d["metadata"],
                    "similarity_score": 0.0
                }

        query_tokens = bm25_index._tokenize(expanded_query)

        # Initial scoring pass (B11, B16, B18, Micro-Intents)
        self._score_candidates(
            doc_map,
            bm25_score_map,
            query_tokens,
            detected_pillar,
            negations,
            query_embedding,
            intent_match=intent_match
        )

        # B12: Relaxed BM25 fallback (b=0.6, candidate_k=30) if top candidate similarity < 0.50
        current_top_sim = max((item.get("similarity_score", 0.0) for item in doc_map.values()), default=0.0)
        if current_top_sim < 0.50:
            relaxed_bm25_results = bm25_index.search(expanded_query, top_k=30, b=0.6)
            for doc_id, score in relaxed_bm25_results:
                if doc_id not in bm25_ranks:
                    bm25_ranks[doc_id] = len(bm25_ranks)
                    bm25_score_map[doc_id] = score
                if doc_id not in doc_map and doc_id in all_docs_dict:
                    d = all_docs_dict[doc_id]
                    doc_map[doc_id] = {
                        "id": doc_id,
                        "text": d["text"],
                        "metadata": d["metadata"],
                        "similarity_score": 0.0
                    }
            # Re-score with relaxed candidates
            self._score_candidates(
                doc_map,
                bm25_score_map,
                query_tokens,
                detected_pillar,
                negations,
                query_embedding,
                intent_match=intent_match
            )

        # P1 / TODO-1.1: Recalibrate RRF smoothing factors & weights adaptively based on detected exact entities
        exact_entities = self._detect_exact_entities(clean_query)
        k_dense, k_bm25, w_dense, w_bm25 = self._get_adaptive_rrf_params(exact_entities)

        # 4. Reciprocal Rank Fusion (RRF) with adaptive entity weighting & cluster bonuses
        rrf_scores: Dict[str, float] = {}
        for doc_id, rank in dense_ranks.items():
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (w_dense / (k_dense + rank + 1))

        for doc_id, rank in bm25_ranks.items():
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (w_bm25 / (k_bm25 + rank + 1))

        # B13: Soft cluster re-ranking bonus (+0.015 RRF score) for docs matching detected pillar
        if detected_pillar:
            target_prefixes = PILLAR_CLUSTERS.get(detected_pillar, [])
            for doc_id in doc_map:
                source_name = doc_map[doc_id].get("metadata", {}).get("source", "")
                if any(source_name.startswith(pfx) for pfx in target_prefixes):
                    rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 0.015

        # Targeted micro-intent document RRF bonus (+0.025)
        if intent_match and intent_match.target_cluster:
            for doc_id in doc_map:
                source_name = doc_map[doc_id].get("metadata", {}).get("source", "")
                if source_name == intent_match.target_cluster:
                    rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 0.025

        # Multi-intent composite RRF bonus for secondary pillar
        if intent_match and intent_match.is_multi_intent and intent_match.secondary_micro_intent:
            from src.core.intent_router import MICRO_INTENTS_PROTOTYPES
            sec_meta = MICRO_INTENTS_PROTOTYPES.get(intent_match.secondary_micro_intent, {})
            sec_pillar_raw = sec_meta.get("pillar", "")
            sec_pillar = macro_to_pillar.get(sec_pillar_raw)
            if sec_pillar:
                sec_prefixes = PILLAR_CLUSTERS.get(sec_pillar, [])
                for doc_id in doc_map:
                    source_name = doc_map[doc_id].get("metadata", {}).get("source", "")
                    if any(source_name.startswith(pfx) for pfx in sec_prefixes):
                        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 0.015

        # Sort by RRF, tie-break by fused similarity
        sorted_candidates = sorted(
            rrf_scores.items(),
            key=lambda item: (item[1], doc_map.get(item[0], {}).get("similarity_score", 0.0)),
            reverse=True
        )

        # Gather top-20 candidates for cross-encoder re-ranking (P1 / TODO-1.3 & TODO-2.15)
        candidate_count = max(top_k * 4, 20)
        initial_candidates = []
        for doc_id, rrf_score in sorted_candidates[:candidate_count]:
            if doc_id in doc_map:
                item = dict(doc_map[doc_id])
                item["rrf_score"] = round(rrf_score, 5)
                initial_candidates.append(item)

        # TODO-2.11 Hard Domain Mask & Intent Compatibility Score:
        # Eradicate cross-pillar hallucination by vetoing 100% of forbidden clusters
        if detected_pillar and detected_pillar in PILLAR_FORBIDDEN_CLUSTERS:
            forbidden_prefixes = PILLAR_FORBIDDEN_CLUSTERS[detected_pillar]
            strict_allowed = PILLAR_STRICT_CLUSTERS.get(detected_pillar, [])

            # Filter candidates: reject any forbidden source unless explicitly multi-intent
            if not (intent_match and intent_match.is_multi_intent):
                filtered_candidates = []
                for cand in initial_candidates:
                    s_name = cand.get("metadata", {}).get("source", "")
                    # Check if candidate contains forbidden prefix
                    is_forbidden = any(s_name.startswith(pfx) or pfx in s_name for pfx in forbidden_prefixes)
                    if not is_forbidden:
                        # Boost intent compatibility score
                        is_strict = any(s_name.startswith(pfx) for pfx in strict_allowed)
                        cand["intent_match_score"] = 1.0 if is_strict else 0.5
                        filtered_candidates.append(cand)

                if filtered_candidates:
                    initial_candidates = filtered_candidates

        # Cross-Encoder re-ranking via FlashRank (CPU ONNX)
        final_results = local_reranker.rerank(clean_query, initial_candidates, top_k=top_k)

        # Secondary safety pass: if a pure single-pillar intent was detected, ensure no forbidden leak
        if detected_pillar and detected_pillar in PILLAR_FORBIDDEN_CLUSTERS and not (intent_match and intent_match.is_multi_intent):
            forbidden_prefixes = PILLAR_FORBIDDEN_CLUSTERS[detected_pillar]
            final_results = [
                r for r in final_results
                if not any(r.get("metadata", {}).get("source", "").startswith(pfx) or pfx in r.get("metadata", {}).get("source", "") for pfx in forbidden_prefixes)
            ]

        return final_results


hybrid_retriever = HybridRetriever()

