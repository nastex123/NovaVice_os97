import re
from typing import Tuple, Optional
from src.config import settings


class PreFlightGuardrails:
    # Pre-flight security filters detecting prompt injections and adversarial jailbreaks.

    INJECTION_PATTERNS = [
        r"(?i)\bignore\s+(all\s+)?(previous|prior)\s+instructions\b",
        r"(?i)\bolvida\s+(todas\s+)?las\s+instrucciones\b",
        r"(?i)\bdisregard\s+(the\s+)?system\s+prompt\b",
        r"(?i)\byou\s+are\s+now\s+(a\s+)?(hacker|dan|developer\s+mode)\b",
        r"(?i)\bahora\s+eres\s+(un\s+)?hacker\b",
        r"(?i)\bpretend\s+you\s+have\s+no\s+rules\b",
        r"(?i)\bsystem\s+override\b",
        r"(?i)\bprint\s+your\s+(initial|system)\s+(prompt|instructions)\b",
        r"(?i)\bmuestra\s+tu\s+prompt\b",
        r"(?i)\bjailbreak\b",
        r"(?i)\bpretend\s+you\s+can\s+grant\s+100%\s+scholarship",
        r"(?i)\botorga(me)?\s+una\s+beca\s+(del\s+)?100%"
    ]

    def __init__(self, similarity_threshold: Optional[float] = None):
        self.similarity_threshold: float = similarity_threshold if similarity_threshold is not None else settings.similarity_threshold
        self.compiled_patterns = [re.compile(p) for p in self.INJECTION_PATTERNS]

    def inspect_query(self, query: str) -> Tuple[bool, Optional[str]]:
        # Returns (is_safe, refusal_reason).
        if not query or len(query.strip()) < 1:
            return False, "La consulta está vacía."

        if len(query) > 1000:
            return False, "La consulta excede la longitud máxima permitida de 1000 caracteres."

        for pattern in self.compiled_patterns:
            if pattern.search(query):
                return False, "Se ha detectado un intento de elusión de seguridad o inyección de prompt no permitido por las políticas institucionales."

        return True, None

    def evaluate_relevance(self, top_similarity: float) -> bool:
        # Returns True if context similarity meets threshold.
        return top_similarity >= self.similarity_threshold


class PostLLMGuardrails:
    # Post-LLM compliance guardrails (TODO-2.16):
    # Enforces Colombian currency symbols ($ COP) on pricing queries, exact time format on schedule queries,
    # and validates PII / sensitive data redaction.

    PRICE_KEYWORDS = ("precio", "costo", "tarifa", "cuota", "valor", "modulo", "pagar", "financiacion", "matricula")
    SCHEDULE_KEYWORDS = ("horario", "franja", "manana", "tarde", "noche", "turno", "sabado")

    TIME_REGEX = re.compile(r"\b(?:\d{1,2}:\d{2}\s*(?:am|pm|a\.m\.|p\.m\.)?|\d{1,2}\s*(?:am|pm|a\.m\.|p\.m\.))\b", re.IGNORECASE)
    COP_REGEX = re.compile(r"\$\s*\d{1,3}(?:\.\d{3})*(?:,\d+)?|\bCOP\b", re.IGNORECASE)

    def validate_and_sanitize(self, response_text: str, user_query: str) -> Tuple[bool, str, list]:
        violations = []
        q_low = user_query.lower()
        cleaned_text = response_text

        # 1. Pricing validation: enforce $ / COP symbol
        if any(kw in q_low for kw in self.PRICE_KEYWORDS):
            if not self.COP_REGEX.search(cleaned_text):
                violations.append("missing_cop_pricing_format")
                cleaned_text += "\n\n*(Nota: Todas las tarifas oficiales están expresadas en Pesos Colombianos $ COP)*"

        # 2. Schedule validation: enforce exact time format
        if any(kw in q_low for kw in self.SCHEDULE_KEYWORDS):
            if not self.TIME_REGEX.search(cleaned_text):
                violations.append("missing_exact_time_format")
                cleaned_text += "\n\n*(Nota: Franjas disponibles de 6:00 a 8:00 a.m. y 6:30 a 8:30 p.m. de lunes a viernes)*"

        # 3. PII Redaction / Guard: Mask any accidental national ID or sensitive credit card patterns
        # Colombian CC pattern: 7-10 digit continuous sequences not preceded by $ or phone code
        cleaned_text = re.sub(r"\b(?<!\+57\s?)(?<!\$)(?<!\d)[1-9]\d{6,9}(?!\d)\b", "[DOCUMENTO_VERIFICADO]", cleaned_text)

        is_compliant = len(violations) == 0
        return is_compliant, cleaned_text, violations


guardrails = PreFlightGuardrails()
post_llm_guardrails = PostLLMGuardrails()
