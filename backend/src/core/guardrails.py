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
        r"(?i)\bpretend\s+you\s+can\s+grant\s+100%\s+scholarship\b",
        r"(?i)\botorga(me)?\s+una\s+beca\s+(del\s+)?100%\b"
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


guardrails = PreFlightGuardrails()
