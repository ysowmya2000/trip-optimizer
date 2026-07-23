"""
Seed ChromaDB with real attraction-level documents pulled from Google Places API.

The knowledge base originally shipped with 12 generic travel-tip documents
covering only Tokyo/Paris/Barcelona, which isn't enough to run a meaningful
retrieval eval or build a BM25 index. This pulls real attraction data for the
cities used in the eval harness and stores per-attraction documents so
semantic search, BM25, and reranking all have something real to work with.

Run manually: python -m app.db.seed_attractions
"""
from typing import Dict, List, Tuple

from app.external.google_places import google_places_client
from app.db.vector_store import travel_kb

# destination -> list of (category label, search query) pairs.
# Categories double as the labels used by the retrieval eval queries.
CITY_QUERIES: Dict[str, List[Tuple[str, str]]] = {
    "Bangkok": [
        ("temples", "temples in Bangkok"),
        ("food", "street food in Bangkok"),
        ("nightlife", "nightlife in Bangkok"),
    ],
    "Hanoi": [
        ("food", "street food in Hanoi"),
        ("temples", "temples in Hanoi"),
    ],
    "Prague": [
        ("nature", "nature parks in Prague"),
        ("nightlife", "nightlife in Prague"),
    ],
    "Paris": [
        ("nightlife", "nightlife in Paris"),
        ("food", "cafes in Paris"),
        ("museums", "museums in Paris"),
    ],
    "Rome": [
        ("museums", "museums in Rome"),
        ("nature", "parks in Rome"),
    ],
    "Bali": [
        ("nature", "beaches in Bali"),
        ("nature", "nature attractions in Bali"),
    ],
    "Mumbai": [
        ("food", "street food in Mumbai"),
        ("markets", "markets in Mumbai"),
    ],
    "Barcelona": [
        ("architecture", "architecture landmarks in Barcelona"),
        ("food", "local food in Barcelona"),
    ],
    "Tokyo": [
        ("shopping", "shopping in Tokyo"),
        ("nature", "gardens in Tokyo"),
        ("temples", "temples in Tokyo"),
    ],
    "Lisbon": [
        ("nature", "viewpoints in Lisbon"),
        ("food", "food in Lisbon"),
    ],
    "Dubai": [
        ("historical", "historical sites in Dubai"),
        ("nightlife", "rooftop bars in Dubai"),
    ],
}


def build_document_text(place: Dict, destination: str) -> str:
    """Compose searchable text from Google Places fields.

    Places' nearby-search response has no long-form description, so this is
    the honest text corpus available (name + category + address + rating) -
    it's documented as such rather than dressed up as richer content.
    """
    types = ", ".join(place.get("types", [])) or "attraction"
    address = place.get("address") or destination
    rating = place.get("rating", 0)
    return f"{place['name']}. Category: {types}. Located at {address}, {destination}. Rating: {rating}/5."


def seed() -> int:
    seen_place_ids = set()
    texts, metadatas, ids = [], [], []

    for destination, queries in CITY_QUERIES.items():
        for category, query in queries:
            results = google_places_client.search_attractions(
                location=destination, query=query, max_results=10
            )
            for place in results:
                place_id = place.get("place_id")
                if not place_id or place_id in seen_place_ids or not place.get("name"):
                    continue
                seen_place_ids.add(place_id)
                texts.append(build_document_text(place, destination))
                metadatas.append({
                    "destination": destination,
                    "category": category,
                    "place_id": place_id,
                })
                ids.append(f"attr_{place_id}")

    print(f"Collected {len(texts)} unique attraction documents across {len(CITY_QUERIES)} cities")

    if texts:
        # upsert (not add_knowledge/collection.add) so reruns don't fail on duplicate ids
        travel_kb.collection.upsert(documents=texts, metadatas=metadatas, ids=ids)
        print(f"Upserted {len(texts)} documents into '{travel_kb.collection.name}'")

    return len(texts)


if __name__ == "__main__":
    seed()
