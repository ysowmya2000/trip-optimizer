"""
Cross-encoder reranking stage: scores (query, candidate) pairs with
cross-encoder/ms-marco-MiniLM-L-6-v2 and returns candidates sorted by that
score. Second stage of a standard two-stage retrieval pattern - hybrid
retrieval casts a wide net (top-20), this narrows it precisely (top-5).

Loaded via the ONNX Runtime backend (quantized weights) rather than the
default PyTorch backend - found by reproducing a free-tier deploy OOM
locally with `docker run --memory=512m`: an unconstrained run peaked at
~540MB, just over the free tier's ~512MB ceiling. The quantized ONNX
model is a fraction of the full fp32 PyTorch weights' size and avoids
PyTorch's inference-time overhead (autograd graph, intermediate
activation tensors), even though the `sentence-transformers` package
still imports torch itself as a side effect of import.
"""
from typing import Dict, List

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder
        _model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            backend="onnx",
            # avx2 quantized variant - avx512 isn't guaranteed available on
            # arbitrary cloud CPUs, avx2 is close to universal on x86_64
            model_kwargs={"file_name": "onnx/model_quint8_avx2.onnx"},
        )
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
