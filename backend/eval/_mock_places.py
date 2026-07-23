"""
Context manager to force Research Agent's Google Places calls onto the
built-in mock-data path (see app/external/google_places.py._get_mock_data)
during eval runs.

Eval harnesses execute the full pipeline dozens of times. The budget/tier
and quality evals don't need real attraction content - they depend on
counts and cost math (budget_calculator, planning_agent), not on which
specific places come back. Retrieval-focused evals use the ChromaDB corpus
seeded separately (app/db/seed_attractions.py), not live Places calls.
Using mock data here avoids incurring further per-request billing on the
configured GOOGLE_PLACES_API_KEY while still exercising the real
orchestrator/agent pipeline end to end.
"""
from contextlib import contextmanager

from app.external.google_places import google_places_client


@contextmanager
def use_mock_places():
    original = google_places_client.available
    google_places_client.available = False
    try:
        yield
    finally:
        google_places_client.available = original
