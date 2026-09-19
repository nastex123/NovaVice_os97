from typing import Dict, List
# Lightweight Graph RAG DAG for certification itineraries (TODO-5.3).
# Nodes: MCER levels, edges: prerequisite progression with exam mapping.

DAG: Dict[str, List[str]] = {
    "A1": ["A2"],
    "A2": ["B1"],
    "B1": ["B2"],
    "B2": ["C1"],
    "C1": ["C2"],
    "C2": [],
}

EXAM_MAP: Dict[str, str] = {
    "A1": "Starters",
    "A2": "KET",
    "B1": "PET",
    "B2": "B2 First / IELTS 5.5 / TOEFL 72 / DELF B2",
    "C1": "C1 Advanced / IELTS 7.0 / DALF C1 / Goethe C1",
    "C2": "C2 Proficiency / IELTS 8.5",
}


def route_to(level: str) -> List[str]:
    # Return ordered path from A1 to target level following DAG edges.
    path = ["A1"]
    cur = "A1"
    while cur != level and DAG.get(cur):
        nxt = DAG[cur][0]
        path.append(nxt)
        cur = nxt
        if len(path) > 10:
            break
    return path
