from typing import List
# Hypothetical document embeddings for ultra-short queries (TODO-5.1).


def hyde_expand(query: str) -> List[str]:
    # Generate one-line synthetic hypotheses enriching short queries.
    q = query.strip().lower()
    if len(q.split()) > 4:
        return [query]
    extras = [query]
    if any(w in q for w in ("precio", "cuesta", "vale", "costo")):
        extras.append(query + " inversion planes de pago cuotas mensualidad cop")
    if any(w in q for w in ("horario", "hora", "cuando")):
        extras.append(query + " manana tarde noche sabados domingos modalidad")
    if any(w in q for w in ("beca", "descuento")):
        extras.append(query + " descuento subsidio beneficio aclaratoria 12_04")
    return extras
