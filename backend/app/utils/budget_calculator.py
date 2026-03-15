"""
Budget Calculator - Determines minimum budgets and scales attractions.
"""
from typing import Dict, Tuple
from app.utils.city_costs import city_cost_analyzer
from app.utils.currency_converter import currency_converter


class BudgetCalculator:
    """Calculates minimum budgets and optimal attraction counts."""
    
    # Base costs in USD (will be multiplied by city multiplier)
    BASE_COSTS = {
        'meal_ultra_budget': 18,      # $10 lunch + $8 dinner
        'meal_budget': 35,             # $20 lunch + $15 dinner
        'meal_standard': 60,           # $35 lunch + $25 dinner
        'meal_comfortable': 90,        # $50 lunch + $40 dinner
        'meal_luxury': 180,            # $80 lunch + $100 dinner
        'transport_daily': 10,         # Daily transport
        'misc_daily': 10,              # Miscellaneous
        'attraction_avg': 30,          # Average attraction cost
    }
    
    def __init__(self):
        """Initialize budget calculator."""
        pass
    
    def calculate_minimum_budget(
        self, 
        destination: str, 
        trip_duration: int,
        user_currency: str = "USD"
    ) -> Dict:
        """Calculate minimum budget needed for destination."""
        
        # Get city multiplier
        city_multiplier = city_cost_analyzer.get_cost_multiplier(destination)
        destination_currency = currency_converter.get_destination_currency(destination)
        
        # Minimum = 1 attraction/day + ultra budget meals + transport
        daily_min_usd = (
            self.BASE_COSTS['meal_ultra_budget'] * city_multiplier +
            self.BASE_COSTS['transport_daily'] * city_multiplier +
            self.BASE_COSTS['misc_daily'] * city_multiplier +
            self.BASE_COSTS['attraction_avg'] * city_multiplier
        )
        
        total_min_usd = daily_min_usd * trip_duration
        
        # Convert to user's currency
        total_min_user = currency_converter.convert(total_min_usd, "USD", user_currency)
        
        return {
            'minimum_budget_usd': round(total_min_usd, 2),
            'minimum_budget_user': round(total_min_user, 2),
            'daily_minimum_usd': round(daily_min_usd, 2),
            'daily_minimum_user': round(total_min_user / trip_duration, 2),
            'user_currency': user_currency,
            'destination': destination,
            'trip_duration': trip_duration,
            'city_multiplier': city_multiplier
        }
    
    def calculate_optimal_attractions_per_day(
        self,
        budget_usd: float,
        trip_duration: int,
        city_multiplier: float
    ) -> Tuple[int, str, bool]:
        """
        Calculate optimal attractions per day based on budget.
        Returns: (attractions_per_day, tier_name, can_add_premium)
        """
        
        budget_per_day = budget_usd / trip_duration
        
        # Calculate cost for different tiers
        tiers = []
        
        # Tier 1: Ultra Budget (1 attraction, street food)
        tier1_cost = (
            self.BASE_COSTS['meal_ultra_budget'] * city_multiplier +
            self.BASE_COSTS['transport_daily'] * city_multiplier +
            self.BASE_COSTS['misc_daily'] * city_multiplier +
            1 * self.BASE_COSTS['attraction_avg'] * city_multiplier
        )
        tiers.append((1, tier1_cost, "Ultra Budget", False))
        
        # Tier 2: Budget (2 attractions, casual cafes)
        tier2_cost = (
            self.BASE_COSTS['meal_budget'] * city_multiplier +
            self.BASE_COSTS['transport_daily'] * city_multiplier +
            self.BASE_COSTS['misc_daily'] * city_multiplier +
            2 * self.BASE_COSTS['attraction_avg'] * city_multiplier
        )
        tiers.append((2, tier2_cost, "Budget", False))
        
        # Tier 3: Standard (3 attractions, restaurants)
        tier3_cost = (
            self.BASE_COSTS['meal_standard'] * city_multiplier +
            self.BASE_COSTS['transport_daily'] * city_multiplier +
            self.BASE_COSTS['misc_daily'] * city_multiplier +
            3 * self.BASE_COSTS['attraction_avg'] * city_multiplier
        )
        tiers.append((3, tier3_cost, "Standard", False))
        
        # Tier 4: Comfortable (4 attractions, nice restaurants)
        tier4_cost = (
            self.BASE_COSTS['meal_comfortable'] * city_multiplier +
            self.BASE_COSTS['transport_daily'] * city_multiplier +
            self.BASE_COSTS['misc_daily'] * city_multiplier +
            4 * self.BASE_COSTS['attraction_avg'] * city_multiplier
        )
        tiers.append((4, tier4_cost, "Comfortable", False))
        
        # Tier 5: Luxury (5 attractions, fine dining)
        tier5_cost = (
            self.BASE_COSTS['meal_luxury'] * city_multiplier +
            self.BASE_COSTS['transport_daily'] * city_multiplier +
            self.BASE_COSTS['misc_daily'] * city_multiplier +
            5 * self.BASE_COSTS['attraction_avg'] * city_multiplier
        )
        tiers.append((5, tier5_cost, "Luxury", False))
        
        # Tier 6: Premium (5 attractions + premium experiences)
        tier6_cost = tier5_cost * 1.5  # 50% more for premium experiences
        tiers.append((5, tier6_cost, "Premium", True))
        
        # Find best tier that fits budget (with 5% tolerance)
        selected_tier = tiers[0]  # Default to ultra budget
        
        for tier in reversed(tiers):  # Start from most expensive
            attractions, cost, name, premium = tier
            if budget_per_day >= cost * 0.95:  # Allow 5% under
                selected_tier = tier
                break
        
        attractions, _, tier_name, can_add_premium = selected_tier
        
        return attractions, tier_name, can_add_premium


# Singleton instance
budget_calculator = BudgetCalculator()
