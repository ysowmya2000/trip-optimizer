"""
Itinerary quality eval: scores 3 dimensions (0-100) for each generated
itinerary in the same test set used by run_budget_eval.py.

- Time-slot appropriateness: does each attraction's clock-time slot match
  its own keyword-derived category, using planning_agent's own
  _categorize_by_best_time() as ground truth (not a re-implementation of
  the rule) - i.e. checking whether the itinerary honors its own stated
  logic, since pool-depletion fallback in _create_day_plans can place a
  "night" attraction in a morning slot when the anytime/morning pools run
  dry.
- Attraction diversity: penalizes a primary category appearing 3+ times
  in one itinerary.
- Interest-match rate: % of attractions whose types/name loosely match
  the requested interests via a keyword map (Places categories don't
  literally contain words like "culture", so this needs a mapping, not a
  literal substring check).

Uses eval._mock_places.use_mock_places() for the same reason as the
budget eval - avoids live Google Places billing.

Run: python -m eval.run_quality_eval
"""
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.test_cases import TEST_CASES
from eval._mock_places import use_mock_places
from app.agents.orchestrator import trip_orchestrator
from app.agents.planning_agent import planning_agent
from app.schemas.trip import Attraction

DEFAULT_INTERESTS = ["culture", "food", "sightseeing"]

# Places-category keywords loosely associated with each requested interest.
# Places taxonomy doesn't contain words like "culture" directly, so interest-
# match needs this mapping rather than a literal substring check.
INTEREST_KEYWORD_MAP = {
    "culture": ["museum", "temple", "place_of_worship", "historic", "landmark", "monument"],
    "food": ["restaurant", "food", "cafe", "market", "meal"],
    "sightseeing": ["tourist_attraction", "viewpoint", "park", "garden", "square", "point_of_interest"],
    "nature": ["park", "garden", "beach", "nature"],
    "nightlife": ["bar", "nightlife", "club", "pub"],
    "shopping": ["shopping_mall", "store", "market"],
}

# clock-time bucket by activity index, mirroring _create_activities' fixed
# time slots (9AM, 12PM lunch, 1:30PM, 4PM, 7PM dinner, 8:30PM, 10PM)
ATTRACTION_INDEX_TO_CLOCK_BUCKET = {0: "morning", 1: "afternoon", 2: "afternoon", 3: "evening", 4: "night"}

COMPATIBLE_KEYWORDS = {
    "morning": {"morning", "anytime"},
    "afternoon": {"anytime", "morning", "evening"},
    "evening": {"evening", "anytime"},
    "night": {"night", "anytime"},
}


def score_time_slot_appropriateness(itinerary: dict) -> dict:
    total, compatible = 0, 0
    mismatches = []

    for day in itinerary.get("days", []):
        attraction_idx = 0
        for activity in day.get("activities", []):
            if activity.get("activity_type") != "attraction" or not activity.get("attraction"):
                continue
            clock_bucket = ATTRACTION_INDEX_TO_CLOCK_BUCKET.get(attraction_idx, "afternoon")
            attraction_idx += 1

            attr = Attraction(**activity["attraction"])
            keyword_bucket = planning_agent._categorize_by_best_time(attr)

            total += 1
            if keyword_bucket in COMPATIBLE_KEYWORDS[clock_bucket]:
                compatible += 1
            else:
                mismatches.append({
                    "attraction": attr.name,
                    "keyword_bucket": keyword_bucket,
                    "scheduled_clock_bucket": clock_bucket,
                    "day": day.get("day_number"),
                })

    score = round(compatible / total * 100, 1) if total else None
    return {"score": score, "total_attractions": total, "mismatches": mismatches}


def score_diversity(itinerary: dict) -> dict:
    all_attractions = []
    for day in itinerary.get("days", []):
        for activity in day.get("activities", []):
            if activity.get("activity_type") == "attraction" and activity.get("attraction"):
                all_attractions.append(activity["attraction"])

    if not all_attractions:
        return {"score": None, "total_attractions": 0, "category_counts": {}}

    def primary_category(attr: dict) -> str:
        types = [t for t in attr.get("types", []) if t not in ("point_of_interest", "establishment")]
        return types[0] if types else "uncategorized"

    categories = [primary_category(a) for a in all_attractions]
    counts = Counter(categories)

    # attractions beyond the 2nd occurrence of a category count as redundant
    redundant = sum(max(0, count - 2) for count in counts.values())
    total = len(all_attractions)
    score = round(100 - (redundant / total * 100), 1)

    return {"score": score, "total_attractions": total, "category_counts": dict(counts)}


def score_interest_match(itinerary: dict, interests: list) -> dict:
    keywords = set()
    for interest in interests:
        keywords.update(INTEREST_KEYWORD_MAP.get(interest.lower(), [interest.lower()]))

    all_attractions = []
    for day in itinerary.get("days", []):
        for activity in day.get("activities", []):
            if activity.get("activity_type") == "attraction" and activity.get("attraction"):
                all_attractions.append(activity["attraction"])

    if not all_attractions:
        return {"score": None, "total_attractions": 0}

    matched = 0
    for attr in all_attractions:
        haystack = " ".join(attr.get("types", []) + [attr.get("name", "")]).lower()
        if any(kw in haystack for kw in keywords):
            matched += 1

    score = round(matched / len(all_attractions) * 100, 1)
    return {"score": score, "total_attractions": len(all_attractions), "matched": matched}


async def run_case(case: dict) -> dict:
    request = {
        "destination": case["destination"],
        "interests": DEFAULT_INTERESTS,
        "trip_duration": case["trip_duration"],
        "budget": case["budget"],
        "currency": case["currency"],
        "start_date": "2026-09-01",
    }

    try:
        response = await trip_orchestrator.create_trip(request)
    except Exception as e:
        return {"id": case["id"], "destination": case["destination"], "error": str(e)}

    if not response.get("success", True):
        return {"id": case["id"], "destination": case["destination"], "error": response.get("error")}

    itinerary = response.get("itinerary", {})

    return {
        "id": case["id"],
        "destination": case["destination"],
        "time_slot_appropriateness": score_time_slot_appropriateness(itinerary),
        "diversity": score_diversity(itinerary),
        "interest_match": score_interest_match(itinerary, DEFAULT_INTERESTS),
    }


async def main():
    results = []
    with use_mock_places():
        for case in TEST_CASES:
            print(f"Running {case['id']} - {case['destination']}...")
            results.append(await run_case(case))

    scored = [r for r in results if "error" not in r]

    def mean_score(key):
        scores = [r[key]["score"] for r in scored if r[key]["score"] is not None]
        return round(sum(scores) / len(scores), 1) if scores else None

    report = {
        "total_cases": len(results),
        "cases_completed_without_error": len(scored),
        "mean_time_slot_appropriateness": mean_score("time_slot_appropriateness"),
        "mean_diversity_score": mean_score("diversity"),
        "mean_interest_match_rate": mean_score("interest_match"),
        "per_case_results": results,
    }

    out_path = Path(__file__).resolve().parent / "results" / "quality_eval_report.json"
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print("ITINERARY QUALITY EVAL SUMMARY")
    print("=" * 60)
    print(f"Total cases:                    {len(results)}")
    print(f"Completed without error:        {len(scored)}")
    print(f"Time-slot appropriateness:      {report['mean_time_slot_appropriateness']}/100")
    print(f"Attraction diversity:           {report['mean_diversity_score']}/100")
    print(f"Interest-match rate:            {report['mean_interest_match_rate']}/100")
    print(f"\nFull report: {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
