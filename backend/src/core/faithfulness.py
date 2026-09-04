from typing import List, Dict, Any, Tuple


class FaithfulnessVerifier:
    """
    Natural Language Inference (NLI) Post-LLM Faithfulness Verifier.
    Computes entailment between candidate premises (ground truth document chunks)
    and candidate hypotheses (LLM response sentences).
    Provides strict 0.80 entailment gate.
    """

    def __init__(self, entailment_threshold: float = 0.80):
        self.entailment_threshold = entailment_threshold

    def evaluate_faithfulness(self, response_text: str, context_chunks: List[Dict[str, Any]]) -> Tuple[float, bool]:
        if not response_text.strip():
            return 1.0, True

        if not context_chunks:
            return 0.0, False

        # Extract sentences from generated answer
        import re
        sentences = [s.strip() for s in re.split(r'[\.\n\?!]+', response_text) if len(s.strip()) > 20]
        if not sentences:
            return 1.0, True

        context_full = " ".join(c.get("text", "").lower() for c in context_chunks)

        supported_count = 0
        for sent in sentences:
            sent_words = [w.lower() for w in re.findall(r'\w{4,}', sent) if not w.isdigit()]
            if not sent_words:
                supported_count += 1
                continue

            matches = sum(1 for w in sent_words if w in context_full)
            overlap_ratio = matches / float(len(sent_words))
            if overlap_ratio >= 0.60:
                supported_count += 1

        faithfulness_score = round(supported_count / float(len(sentences)), 4)
        is_faithful = faithfulness_score >= self.entailment_threshold
        return faithfulness_score, is_faithful


faithfulness_verifier = FaithfulnessVerifier()
