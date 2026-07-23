"""
Runs eval/test_cases.py through the real orchestrator pipeline and scores
tier assignment, attractions-per-day, and budget-status accuracy.

Uses eval._mock_places.use_mock_places() to avoid live Google Places
billing while still exercising the real agent pipeline (Groq calls,
budget/planning/optimization/budget-analysis logic all run for real).

Run: python -m eval.run_budget_eval
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.test_cases import TEST_CASES
from eval._mock_places import use_mock_places
from app.agents.orchestrator import trip_orchestrator
from app.utils.currency_converter import currency_converter

TIER_BY_ATTRACTIONS_PER_DAY = {
    1: "Ultra Budget",
    2: "Budget",
    3: "Standard",
    4: "Comfortable",
    5: "Luxury",  # Premium also resolves to 5/day; not distinguishable from output alone
}

DEFAULT_INTERESTS = ["culture", "food", "sightseeing"]


def actual_tier_from_itinerary(itinerary: dict) -> str:
    days = itinerary.get("days", [])
    if not days:
        return "Unknown"
    counts = [d.get("total_attractions", 0) for d in days]
    mode_count = max(set(counts), key=counts.count)
    return TIER_BY_ATTRACTIONS_PER_DAY.get(mode_count, f"Unknown({mode_count})")


async def run_case(case: dict) -> dict:
    request = {
        "destination": case["destination"],
        "interests": DEFAULT_INTERESTS,
        "trip_duration": case["trip_duration"],
        "budget": case["budget"],
        "currency": case["currency"],
        "start_date": "2026-09-01",
    }

    result = {"id": case["id"], "destination": case["destination"], "is_boundary_case": case["is_boundary_case"]}

    try:
        response = await trip_orchestrator.create_trip(request)
    except Exception as e:
        result.update({"error": str(e), "pass": False})
        return result

    if not response.get("success", True):
        result.update({"error": response.get("error", "unknown_failure"), "pass": False})
        return result

    itinerary = response.get("itinerary", {})
    budget_analysis = response.get("budget_analysis", {})

    actual_tier = actual_tier_from_itinerary(itinerary)
    days = itinerary.get("days", [])
    actual_attractions_per_day = days[0].get("total_attractions") if days else None
    actual_status = budget_analysis.get("status")
    actual_cost_user = budget_analysis.get("estimated_cost_user")

    tier_correct = actual_tier == case["expected_tier"]
    attractions_correct = actual_attractions_per_day == case["expected_attractions_per_day"]
    status_correct = actual_status == case["expected_budget_status"]

    result.update({
        "expected_tier": case["expected_tier"],
        "actual_tier": actual_tier,
        "tier_correct": tier_correct,
        "expected_attractions_per_day": case["expected_attractions_per_day"],
        "actual_attractions_per_day": actual_attractions_per_day,
        "attractions_per_day_correct": attractions_correct,
        "expected_budget_status": case["expected_budget_status"],
        "actual_budget_status": actual_status,
        "budget_status_correct": status_correct,
        "actual_cost_user": actual_cost_user,
        "pass": tier_correct and attractions_correct and status_correct,
    })
    return result


def cost_estimate_check(results: list, cases_by_id: dict) -> dict:
    """
    Hand-verified cost check for the non-boundary 'standard_zone' subset
    (one per city, 11 cases). Expected range is derived from
    budget_calculator's tier-cost formula with a +/-30% tolerance band,
    since the live pipeline computes cost via a related but not identical
    formula in planning_agent._calculate_cost (see test_cases.py docstring
    for why the two formulas diverge). Deviation is measured from the
    range midpoint, in USD, to keep currencies comparable.
    """
    deviations = []
    subset = []

    for r in results:
        case = cases_by_id.get(r["id"])
        if not case or case["is_boundary_case"] or "standard_zone" not in case.get("notes", ""):
            continue
        if r.get("actual_cost_user") is None:
            continue

        tier_daily_cost_usd = float(case["notes"].split("selected_tier_daily_cost_usd=")[-1])
        expected_total_usd = tier_daily_cost_usd * case["trip_duration"]
        low, high = expected_total_usd * 0.7, expected_total_usd * 1.3

        actual_cost_usd = currency_converter.convert(r["actual_cost_user"], case["currency"], "USD")
        pct_dev = abs(actual_cost_usd - expected_total_usd) / expected_total_usd * 100

        deviations.append(pct_dev)
        subset.append({
            "id": r["id"],
            "destination": case["destination"],
            "expected_cost_range_usd": [round(low, 2), round(high, 2)],
            "actual_cost_usd": round(actual_cost_usd, 2),
            "in_range": low <= actual_cost_usd <= high,
            "pct_deviation_from_midpoint": round(pct_dev, 1),
        })

    return {
        "subset_size": len(deviations),
        "mean_pct_deviation": round(sum(deviations) / len(deviations), 1) if deviations else None,
        "cases": subset,
    }


async def main():
    cases_by_id = {c["id"]: c for c in TEST_CASES}
    results = []

    with use_mock_places():
        for case in TEST_CASES:
            print(f"Running {case['id']} - {case['destination']} ({case['currency']} {case['budget']})...")
            results.append(await run_case(case))

    total = len(results)
    scored = [r for r in results if "tier_correct" in r]
    tier_accuracy = sum(1 for r in scored if r["tier_correct"]) / len(scored) if scored else 0
    attractions_accuracy = sum(1 for r in scored if r["attractions_per_day_correct"]) / len(scored) if scored else 0
    status_accuracy = sum(1 for r in scored if r["budget_status_correct"]) / len(scored) if scored else 0
    overall_pass_rate = sum(1 for r in results if r.get("pass")) / total if total else 0

    cost_check = cost_estimate_check(results, cases_by_id)

    report = {
        "total_cases": total,
        "cases_completed_without_error": len(scored),
        "tier_assignment_accuracy": round(tier_accuracy, 3),
        "attractions_per_day_accuracy": round(attractions_accuracy, 3),
        "budget_status_accuracy": round(status_accuracy, 3),
        "overall_pass_rate": round(overall_pass_rate, 3),
        "cost_estimate_check": cost_check,
        "per_case_results": results,
    }

    out_path = Path(__file__).resolve().parent / "results" / "budget_eval_report.json"
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print("BUDGET / TIER EVAL SUMMARY")
    print("=" * 60)
    print(f"Total cases:                  {total}")
    print(f"Completed without error:      {len(scored)}")
    print(f"Tier assignment accuracy:     {tier_accuracy*100:.1f}%")
    print(f"Attractions/day accuracy:     {attractions_accuracy*100:.1f}%")
    print(f"Budget status accuracy:       {status_accuracy*100:.1f}%")
    print(f"Overall pass rate:            {overall_pass_rate*100:.1f}%")
    if cost_check["mean_pct_deviation"] is not None:
        print(f"Cost estimate mean deviation: {cost_check['mean_pct_deviation']}% (n={cost_check['subset_size']})")
    print(f"\nFull report: {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
