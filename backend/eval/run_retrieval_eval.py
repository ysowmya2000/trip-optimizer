"""
Computes precision@5 for retrieval, against the manually labeled queries
in retrieval_test_queries.py.

Supports three modes via --mode, so Phase 3 can attribute improvement to
each component separately:
  semantic  - current ChromaDB semantic search only (the baseline)
  hybrid    - BM25 + semantic fused with RRF, no reranking
  reranked  - hybrid candidates reranked with the cross-encoder

Phase 1c only needs 'semantic' (the baseline); the other two modes exist
for Phase 3's comparison run but the retrieval code isn't wired up yet
until Phase 2 lands.

Run: python -m eval.run_retrieval_eval --mode semantic
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.retrieval_test_queries import RETRIEVAL_TEST_QUERIES
from app.db.vector_store import travel_kb


def precision_at_5(retrieved_ids: list, correct_ids: set) -> float:
    top5 = retrieved_ids[:5]
    if not top5:
        return 0.0
    hits = sum(1 for doc_id in top5 if doc_id in correct_ids)
    return hits / len(top5)


def get_semantic_ids(query: str, n_results: int = 5) -> list:
    """Runs the current TravelKnowledgeBase.search() and returns doc ids in
    rank order. search() doesn't return ids directly, so this queries the
    underlying collection the same way to recover them."""
    results = travel_kb.collection.query(query_texts=[query], n_results=n_results)
    return results["ids"][0] if results.get("ids") else []


def run_mode(mode: str) -> dict:
    if mode == "semantic":
        retrieve_fn = get_semantic_ids
    elif mode == "hybrid":
        from app.retrieval.hybrid_retriever import hybrid_search_ids
        # top_k=20 is the fusion candidate pool size (cast a wide net);
        # final_k=n_results is what actually gets scored for precision@5.
        # Passing n_results as top_k here was a bug - it capped the RRF
        # fusion pool at 5 candidates per retriever instead of 20, which
        # defeats the point of hybrid retrieval before reranking even runs.
        retrieve_fn = lambda q, n_results=5: hybrid_search_ids(q, top_k=20, rerank=False, final_k=n_results)
    elif mode == "reranked":
        from app.retrieval.hybrid_retriever import hybrid_search_ids
        retrieve_fn = lambda q, n_results=5: hybrid_search_ids(q, top_k=20, rerank=True, final_k=n_results)
    else:
        raise ValueError(f"unknown mode: {mode}")

    per_query = []
    for q in RETRIEVAL_TEST_QUERIES:
        retrieved_ids = retrieve_fn(q["query"], 5)
        correct_ids = set(q["correct_ids"])
        p_at_5 = precision_at_5(retrieved_ids, correct_ids)
        per_query.append({
            "query": q["query"],
            "destination": q["destination"],
            "category": q["category"],
            "retrieved_ids": retrieved_ids,
            "precision_at_5": round(p_at_5, 3),
        })

    mean_p5 = round(sum(r["precision_at_5"] for r in per_query) / len(per_query), 3)
    return {"mode": mode, "mean_precision_at_5": mean_p5, "per_query_results": per_query}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["semantic", "hybrid", "reranked"], default="semantic")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    report = run_mode(args.mode)

    default_names = {
        "semantic": "retrieval_eval_baseline.json",
        "hybrid": "retrieval_eval_hybrid.json",
        "reranked": "retrieval_eval_reranked.json",
    }
    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent / "results" / default_names[args.mode]
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nMode: {args.mode}")
    print(f"Mean precision@5: {report['mean_precision_at_5']}")
    print(f"Full report: {out_path}")


if __name__ == "__main__":
    main()
