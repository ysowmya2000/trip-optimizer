"""
BM25 keyword retrieval over the same document corpus used by semantic
search. Complements dense embeddings: semantic search can blur across
cities (e.g. "temples in Bangkok" pulling in a Hanoi temple - see the
retrieval baseline eval), while BM25's term-frequency scoring rewards
exact keyword/city-name matches.
"""
from typing import Dict, List

from rank_bm25 import BM25Okapi

from app.db.vector_store import travel_kb


class BM25Retriever:
    def __init__(self):
        self._ids: List[str] = []
        self._documents: List[str] = []
        self._metadatas: List[Dict] = []
        self._bm25 = None

    def _ensure_index(self):
        if self._bm25 is not None:
            return
        corpus = travel_kb.get_all_documents()
        self._ids = corpus["ids"]
        self._documents = corpus["documents"]
        self._metadatas = corpus["metadatas"]
        tokenized = [doc.lower().split() for doc in self._documents]
        self._bm25 = BM25Okapi(tokenized) if tokenized else None

    def refresh(self):
        """Force a rebuild - call after the underlying corpus changes."""
        self._bm25 = None
        self._ensure_index()

    def search(self, query: str, top_k: int = 20) -> List[Dict]:
        self._ensure_index()
        if not self._documents or self._bm25 is None:
            return []

        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)

        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [
            {
                "id": self._ids[i],
                "document": self._documents[i],
                "metadata": self._metadatas[i],
                "score": float(scores[i]),
            }
            for i in ranked if scores[i] > 0
        ]


bm25_retriever = BM25Retriever()
