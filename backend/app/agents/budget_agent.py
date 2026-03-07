"""
Budget Agent - Tracks spending and manages budget constraints.
"""
from typing import List, Dict, Optional
from app.schemas.trip import Itinerary, DayPlan, Attraction


class BudgetAgent:
    """Agent responsible for budget tracking and cost optimization."""
    
    def __init__(self):
        """Initialize Budget Agent."""
        self.name = "Budget Agent"
        print(f"💰 {self.name} initialized")
    
    def analyze_budget(
        self, 
        itinerary: Itinerary, 
        budget: Optional[float] = None
    ) -> Dict:
        """
        Analyze itinerary budget and provide recommendations.
        
        Args:
            itinerary: Trip itinerary
            budget: Total budget in USD (optional)
            
        Returns:
            Budget analysis with recommendations
        """
        print(f"\n💰 {self.name}: Analyzing budget for {itinerary.destination}...")
        
        total_cost = itinerary.estimated_total_cost
        daily_costs = [day.estimated_cost for day in itinerary.days]
        
        analysis = {
            "total_estimated_cost": total_cost,
            "daily_breakdown": [
                {
                    "day": i + 1,
                    "cost": cost,
                    "percentage": round((cost / total_cost * 100), 1) if total_cost > 0 else 0
                }
                for i, cost in enumerate(daily_costs)
            ],
            "budget_status": "unknown",
            "over_budget_amount": 0,
            "savings_needed": 0,
            "recommendations": []
        }
        
        if budget:
            analysis["budget"] = budget
            difference = total_cost - budget
            
            if difference > 0:
                analysis["budget_status"] = "over_budget"
                analysis["over_budget_amount"] = round(difference, 2)
                analysis["savings_needed"] = round(difference, 2)
                analysis["recommendations"] = self._generate_savings_recommendations(
                    itinerary, 
                    difference
                )
            elif difference < -50:
                analysis["budget_status"] = "under_budget"
                analysis["recommendations"] = [
                    f"You have ${abs(difference):.2f} remaining in your budget",
                    "Consider upgrading accommodations or dining experiences",
                    "Add extra activities or extend your trip"
                ]
            else:
                analysis["budget_status"] = "on_budget"
                analysis["recommendations"] = [
                    "Budget is well-balanced!",
                    "Costs are within your target range"
                ]
        else:
            analysis["budget_status"] = "no_budget_set"
            analysis["recommendations"] = [
                f"Estimated total cost: ${total_cost:.2f}",
                f"Average daily cost: ${total_cost / len(daily_costs):.2f}",
                "Set a budget to get personalized recommendations"
            ]
        
        print(f"✅ {self.name}: Budget analysis complete - {analysis['budget_status']}")
        return analysis
    
    def _generate_savings_recommendations(
        self, 
        itinerary: Itinerary, 
        amount_to_save: float
    ) -> List[str]:
        """Generate recommendations to reduce costs."""
        recommendations = []
        
        recommendations.append(
            f"⚠️ You are ${amount_to_save:.2f} over budget"
        )
        
        # Suggest reducing expensive attractions
        expensive_days = sorted(
            itinerary.days, 
            key=lambda d: d.estimated_cost, 
            reverse=True
        )
        
        if expensive_days:
            most_expensive = expensive_days[0]
            recommendations.append(
                f"Day {most_expensive.day_number} is most expensive (${most_expensive.estimated_cost:.2f}). "
                "Consider replacing some activities with free alternatives."
            )
        
        # General cost-saving tips
        savings_per_day = amount_to_save / itinerary.trip_duration
        
        recommendations.extend([
            f"Reduce daily spending by ${savings_per_day:.2f} to meet budget",
            "💡 Cost-saving tips:",
            "  - Choose local street food over restaurants ($15-20/day savings)",
            "  - Visit free attractions (parks, temples, markets)",
            "  - Use public transit instead of taxis ($10-15/day savings)",
            "  - Look for combination tickets for multiple attractions"
        ])
        
        return recommendations
    
    def suggest_cheaper_alternatives(
        self, 
        attractions: List[Attraction],
        max_results: int = 3
    ) -> List[Attraction]:
        """
        Suggest cheaper alternatives from attraction list.
        
        Args:
            attractions: List of attractions
            max_results: Number of alternatives to return
            
        Returns:
            Cheaper attractions (sorted by price_level)
        """
        # Sort by price level (0 = free, 1 = cheap, etc.)
        sorted_attrs = sorted(attractions, key=lambda a: a.price_level)
        return sorted_attrs[:max_results]
    
    def calculate_savings(
        self, 
        original_cost: float, 
        new_cost: float
    ) -> Dict:
        """Calculate savings from cost changes."""
        savings = original_cost - new_cost
        percentage = (savings / original_cost * 100) if original_cost > 0 else 0
        
        return {
            "original_cost": round(original_cost, 2),
            "new_cost": round(new_cost, 2),
            "savings": round(savings, 2),
            "savings_percentage": round(percentage, 1)
        }


# Create global instance
budget_agent = BudgetAgent()
