"""
Hybrid retrieval: fuses ChromaDB semantic search with BM25 keyword search
via Reciprocal Rank Fusion (RRF, k=60, standard default - no tuning),
then optionally reranks the fused candidates with a cross-encoder.
"""
from typing import Dict, List

from app.core.config import settings
from app.db.vector_store import travel_kb
from app.retrieval.bm25_retriever import bm25_retriever

RRF_K = 60


def _semantic_ranked_ids(query: str, top_k: int) -> List[str]:
    results = travel_kb.collection.query(query_texts=[query], n_results=top_k)
    return results["ids"][0] if results.get("ids") else []


def _bm25_ranked_ids(query: str, top_k: int) -> List[str]:
    return [r["id"] for r in bm25_retriever.search(query, top_k=top_k)]


def reciprocal_rank_fusion(ranked_lists: List[List[str]], k: int = RRF_K) -> List[str]:
    scores: Dict[str, float] = {}
    for ranked_ids in ranked_lists:
        for rank, doc_id in enumerate(ranked_ids, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return [doc_id for doc_id, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]


def hybrid_search(query: str, top_k: int = 20, rerank: bool = True, final_k: int = 5) -> List[Dict]:
    """
    Runs semantic + BM25, fuses with RRF, optionally reranks with the
    cross-encoder, and returns full document records (not just ids).
    """
    semantic_ids = _semantic_ranked_ids(query, top_k)
    bm25_ids = _bm25_ranked_ids(query, top_k)

    fused_ids = reciprocal_rank_fusion([semantic_ids, bm25_ids])[:top_k]

    corpus = travel_kb.get_all_documents()
    by_id = {
        id_: (doc, meta)
        for id_, doc, meta in zip(corpus["ids"], corpus["documents"], corpus["metadatas"])
    }

    candidates = [
        {"id": doc_id, "document": by_id[doc_id][0], "metadata": by_id[doc_id][1]}
        for doc_id in fused_ids if doc_id in by_id
    ]

    if rerank and candidates and settings.ENABLE_RERANKING:
        from app.retrieval.reranker import rerank_candidates
        candidates = rerank_candidates(query, candidates)

    return candidates[:final_k]


def hybrid_search_ids(query: str, top_k: int = 20, rerank: bool = True, final_k: int = 5) -> List[str]:
    """Same as hybrid_search but returns just ids, for the retrieval eval."""
    return [c["id"] for c in hybrid_search(query, top_k=top_k, rerank=rerank, final_k=final_k)]
