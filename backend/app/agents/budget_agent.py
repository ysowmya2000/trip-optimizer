"""
Budget Agent - Analyzes trip budget with dual currency display.
"""
from typing import Dict
from app.utils.currency_converter import currency_converter


class BudgetAgent:
    """Agent for budget analysis."""
    
    def __init__(self):
        self.name = "Budget Agent"
        print(f"💰 {self.name} initialized")
    
    def analyze_budget(self, itinerary, budget: float = None, user_budget: float = None, 
                      user_currency: str = 'USD', destination_currency: str = 'USD') -> Dict:
        """Analyze budget - everything in user's currency."""
        user_budget = budget if budget is not None else user_budget
        
        # Get costs (already in user's currency from orchestrator)
        if isinstance(itinerary, dict):
            destination = itinerary.get('destination', 'destination')
            total_cost_user = itinerary.get('estimated_total_cost', 0)
            days = itinerary.get('days', [])
        else:
            destination = itinerary.destination
            total_cost_user = itinerary.estimated_total_cost
            days = itinerary.days
        
        # Convert to destination currency for display only
        total_cost_dest = currency_converter.convert(total_cost_user, user_currency, destination_currency)
        
        print(f"\n💰 {self.name}: Analyzing budget for {destination}...")
        print(f"   User budget: {currency_converter.format_currency(user_budget, user_currency)}")
        print(f"   Trip cost: {currency_converter.format_currency(total_cost_user, user_currency)} (≈ {currency_converter.format_currency(total_cost_dest, destination_currency)})")
        
        # Determine status (compare in user's currency)
        if user_budget is None:
            status = "on_budget"
        elif total_cost_user <= user_budget * 0.95:
            status = "under_budget"
        elif total_cost_user <= user_budget:
            status = "on_budget"
        else:
            status = "over_budget"
        
        print(f"✅ {self.name}: Budget analysis complete - {status}")
        
        return {
            "user_budget": user_budget,
            "user_currency": user_currency,
            "destination_currency": destination_currency,
            "estimated_cost_user": total_cost_user,
            "estimated_cost_destination": total_cost_dest,
            "status": status,
            "daily_average_user": total_cost_user / len(days) if days else 0,
            "daily_average_dest": total_cost_dest / len(days) if days else 0,
            "difference": (user_budget - total_cost_user) if user_budget else 0
        }


budget_agent = BudgetAgent()
