"""
Cross-encoder reranking stage: scores (query, candidate) pairs with
cross-encoder/ms-marco-MiniLM-L-6-v2 (CPU-friendly, sentence-transformers
was already a dependency) and returns candidates sorted by that score.
Second stage of a standard two-stage retrieval pattern - hybrid retrieval
casts a wide net (top-20), this narrows it precisely (top-5).
"""
from typing import Dict, List

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _model


def rerank_candidates(query: str, candidates: List[Dict]) -> List[Dict]:
    if not candidates:
        return candidates

    model = _get_model()
    pairs = [(query, c["document"]) for c in candidates]
    scores = model.predict(pairs)

    scored = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    reranked = []
    for candidate, score in scored:
        c = dict(candidate)
        c["rerank_score"] = float(score)
        reranked.append(c)
    return reranked
