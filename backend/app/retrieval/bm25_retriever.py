"""
BM25 keyword retrieval over the same document corpus used by semantic
search. Complements dense embeddings: semantic search can blur across
cities (e.g. "temples in Bangkok" pulling in a Hanoi temple - see the
retrieval baseline eval), while BM25's term-frequency scoring rewards
exact keyword/city-name matches.
"""
import re
from typing import Dict, List

from rank_bm25 import BM25Okapi

from app.db.vector_store import travel_kb

# Corpus mixes short generic tips with structured attraction descriptions,
# so common words (in, the, of, at) get erratic BM25Okapi IDF on this small
# (~230 doc) heterogeneous set and let unrelated short docs outscore actual
# matches. Stripping them keeps scoring on real content words.
_STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "of", "to", "for", "and", "or",
    "is", "are", "was", "were", "be", "with", "as", "by", "this", "that",
    "it", "from", "near",
}


def _normalize(token: str) -> str:
    """Light suffix stripping so 'temples' matches 'temple', 'museums'
    matches 'museum', etc. Plain .split() tokenization without this makes
    BM25 miss the exact-match cases it's supposed to be good at - e.g. no
    document in the corpus contains the literal substring "temples", only
    "temple" ("The Temple of the Emerald Buddha"), so a query for "temples
    in Bangkok" degenerates to scoring on "bangkok" alone and lets
    unrelated Bangkok docs (nightclubs, bars) rank alongside actual
    temples. No nltk dependency for a single-purpose plural strip."""
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [_normalize(w) for w in words if w not in _STOPWORDS]


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
        tokenized = [_tokenize(doc) for doc in self._documents]
        self._bm25 = BM25Okapi(tokenized) if tokenized else None

    def refresh(self):
        """Force a rebuild - call after the underlying corpus changes."""
        self._bm25 = None
        self._ensure_index()

    def search(self, query: str, top_k: int = 20) -> List[Dict]:
        self._ensure_index()
        if not self._documents or self._bm25 is None:
            return []

        tokenized_query = _tokenize(query)
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
