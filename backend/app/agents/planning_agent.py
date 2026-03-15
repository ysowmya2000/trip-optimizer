"""
Planning Agent - Creates BUDGET-AWARE day-by-day itineraries.
"""
from typing import List, Dict
from app.schemas.trip import Itinerary, DayPlan, Activity, Attraction
from app.utils.city_costs import city_cost_analyzer
from app.utils.currency_converter import currency_converter
from app.utils.budget_calculator import budget_calculator


class PlanningAgent:
    """Agent responsible for creating budget-aware itineraries."""
    
    KNOWN_ATTRACTION_PRICES = {
        'eiffel tower': 3, 'louvre': 3, 'arc de triomphe': 2, 'notre-dame': 2,
        'sainte-chapelle': 2, 'panthéon': 2, 'versailles': 4, 'musée d\'orsay': 3,
    }
    
    SUNSET_KEYWORDS = ['tower', 'viewpoint', 'observation', 'panoramic', 'rooftop', 'sky', 'eiffel']
    NIGHT_KEYWORDS = ['nightlife', 'bar', 'club', 'disco', 'pub', 'cruise', 'show', 'theater', 'cabaret', 'moulin']
    MORNING_KEYWORDS = ['garden', 'park', 'market']
    
    def __init__(self):
        self.name = "Planning Agent"
        print(f"📅 {self.name} initialized")
    
    def create_itinerary(
        self,
        destination: str,
        interests: List[str],
        attractions: List[Dict],
        trip_duration: int,
        budget: float = None,
        destination_currency: str = "USD"
    ) -> Itinerary:
        """Create budget-aware itinerary - FIT attractions to budget!"""
        print(f"\n📅 {self.name}: Creating {trip_duration}-day itinerary for {destination}...")
        
        # Get city cost multiplier
        city_multiplier = city_cost_analyzer.get_cost_multiplier(destination)
        tier_info = city_cost_analyzer.get_tier_info(city_multiplier)
        print(f"   {tier_info['emoji']} City tier: {tier_info['description']} (×{city_multiplier})")
        
        # Convert budget to USD for internal calculations
        if budget and destination_currency != "USD":
            budget_usd = currency_converter.convert(budget, destination_currency, "USD")
            print(f"   💰 Budget: {currency_converter.format_currency(budget, destination_currency)} = ${budget_usd:.2f} USD")
        else:
            budget_usd = budget
        
        attraction_objects = [Attraction(**attr) for attr in attractions]
        
        # BUDGET-AWARE: Find optimal attractions per day
        optimal_attractions_per_day = self._find_optimal_attractions_per_day(
            budget_usd=budget_usd,
            trip_duration=trip_duration,
            city_multiplier=city_multiplier
        )
        
        days = self._create_day_plans(
            destination=destination,
            interests=interests,
            attractions=attraction_objects,
            trip_duration=trip_duration,
            budget=budget_usd,
            city_multiplier=city_multiplier,
            attractions_per_day=optimal_attractions_per_day
        )
        
        total_attractions = sum(day.total_attractions for day in days)
        total_cost = sum(day.estimated_cost for day in days)
        
        print(f"✅ {self.name}: Created itinerary with {len(days)} days, {total_attractions} attractions")
        print(f"   💰 Total estimated cost: ${total_cost:.2f} USD")
        
        return Itinerary(
            destination=destination,
            trip_duration=trip_duration,
            interests=interests,
            days=days,
            total_attractions=total_attractions,
            estimated_total_cost=total_cost,
            created_by=self.name
        )
    
    def _find_optimal_attractions_per_day(self, budget_usd: float, trip_duration: int, city_multiplier: float) -> int:
        """Find how many attractions per day fit in budget using budget_calculator."""
        if not budget_usd:
            return 5  # No budget limit
        
        attractions_per_day, tier_name, can_add_premium = budget_calculator.calculate_optimal_attractions_per_day(
            budget_usd=budget_usd,
            trip_duration=trip_duration,
            city_multiplier=city_multiplier
        )
        
        budget_per_day = budget_usd / trip_duration
        print(f"   🎯 {tier_name} Tier: {attractions_per_day} attractions/day (${budget_per_day:.0f}/day)")
        if can_add_premium:
            print(f"   ✨ Budget allows premium experiences!")
        
        return attractions_per_day
    

    def _categorize_by_best_time(self, attraction: Attraction) -> str:
        """Determine best time for attraction."""
        name_lower = attraction.name.lower()
        types_lower = ' '.join(attraction.types or []).lower()
        combined = f"{name_lower} {types_lower}"
        
        if any(kw in combined for kw in self.NIGHT_KEYWORDS):
            return 'night'
        if any(kw in combined for kw in self.SUNSET_KEYWORDS):
            return 'evening'
        if any(kw in combined for kw in self.MORNING_KEYWORDS):
            return 'morning'
        
        return 'anytime'
    
    def _get_smart_price_level(self, attraction: Attraction) -> int:
        """Get smart price level."""
        name_lower = attraction.name.lower()
        for known, price in self.KNOWN_ATTRACTION_PRICES.items():
            if known in name_lower:
                return price
        
        types = [t.lower() for t in (attraction.types or [])]
        if any(t in types for t in ['park', 'garden', 'square']):
            return 0
        if any(t in types for t in ['museum', 'monument']):
            return 2
        return attraction.price_level if attraction.price_level else 2
    
    def _create_day_plans(
        self,
        destination: str,
        interests: List[str],
        attractions: List[Attraction],
        trip_duration: int,
        budget: float = None,
        city_multiplier: float = 1.0,
        attractions_per_day: int = 5
    ) -> List[DayPlan]:
        """Create day plans with FIXED attractions per day."""
        
        categorized = {'morning': [], 'anytime': [], 'evening': [], 'night': []}
        
        for attr in attractions:
            best_time = self._categorize_by_best_time(attr)
            categorized[best_time].append(attr)
        
        print(f"\n📊 Categorized: Morning={len(categorized['morning'])}, Anytime={len(categorized['anytime'])}, Evening={len(categorized['evening'])}, Night={len(categorized['night'])}")
        print(f"🎯 Creating {trip_duration} days with {attractions_per_day} attractions each\n")
        
        # Budget-based sorting
        if budget:
            budget_per_day = budget / trip_duration
            if budget_per_day < 200:
                for category in categorized.values():
                    category.sort(key=lambda x: self._get_smart_price_level(x))
            elif budget_per_day > 400:
                for category in categorized.values():
                    category.sort(key=lambda x: -self._get_smart_price_level(x))
        
        days = []
        
        for day_num in range(1, trip_duration + 1):
            day_attractions = []
            
            # Collect attractions based on attractions_per_day
            # Always get morning slot first
            if categorized['morning']:
                day_attractions.append(categorized['morning'].pop(0))
            elif categorized['anytime']:
                day_attractions.append(categorized['anytime'].pop(0))
            
            # Fill remaining slots
            slots_needed = attractions_per_day - 1
            for _ in range(slots_needed):
                if categorized['anytime']:
                    day_attractions.append(categorized['anytime'].pop(0))
                elif categorized['morning']:
                    day_attractions.append(categorized['morning'].pop(0))
                elif categorized['evening']:
                    day_attractions.append(categorized['evening'].pop(0))
                elif categorized['night']:
                    day_attractions.append(categorized['night'].pop(0))
            
            # Create activities
            activities = self._create_activities(day_attractions, destination, attractions_per_day)
            
            day_title = self._generate_day_theme(day_num)
            estimated_cost = self._calculate_cost(day_attractions, city_multiplier, budget / trip_duration if budget else None)
            
            day_plan = DayPlan(
                day_number=day_num,
                title=day_title,
                activities=activities,
                total_attractions=len(day_attractions),
                estimated_cost=estimated_cost,
                notes=f"Full day: 9 AM - 11 PM"
            )
            days.append(day_plan)
        
        return days
    
    def _create_activities(self, attractions: List[Attraction], destination: str, max_attractions: int) -> List[Activity]:
        """Create activity list based on number of attractions."""
        activities = []
        
        # 9 AM - Always have morning attraction
        if len(attractions) > 0:
            activities.append(Activity(
                time="9:00 AM",
                activity_type="attraction",
                name=attractions[0].name,
                description=f"Visit {attractions[0].name}",
                duration_minutes=120,
                attraction=attractions[0],
                notes=f"Rating: {attractions[0].rating}/5.0"
            ))
        
        # 12 PM - Always have lunch
        activities.append(Activity(
            time="12:00 PM",
            activity_type="meal",
            name="Lunch",
            description=f"Local restaurant in {destination}",
            duration_minutes=60,
            notes="Try local cuisine"
        ))
        
        # 1:30 PM - If we have 2+ attractions
        if len(attractions) >= 2:
            activities.append(Activity(
                time="1:30 PM",
                activity_type="attraction",
                name=attractions[1].name,
                description=f"Explore {attractions[1].name}",
                duration_minutes=120,
                attraction=attractions[1],
                notes=f"Rating: {attractions[1].rating}/5.0"
            ))
        
        # 4:00 PM - If we have 3+ attractions
        if len(attractions) >= 3:
            activities.append(Activity(
                time="4:00 PM",
                activity_type="attraction",
                name=attractions[2].name,
                description=f"Visit {attractions[2].name}",
                duration_minutes=90,
                attraction=attractions[2],
                notes=f"Rating: {attractions[2].rating}/5.0"
            ))
        
        # 7:00 PM - Always have dinner
        activities.append(Activity(
            time="7:00 PM",
            activity_type="meal",
            name="Dinner",
            description="Dinner at local restaurant",
            duration_minutes=60,
            notes="Enjoy local flavors"
        ))
        
        # 8:30 PM - If we have 4+ attractions
        if len(attractions) >= 4:
            activities.append(Activity(
                time="8:30 PM",
                activity_type="attraction",
                name=attractions[3].name,
                description=f"Evening visit to {attractions[3].name}",
                duration_minutes=90,
                attraction=attractions[3],
                notes=f"🌆 Evening! Rating: {attractions[3].rating}/5.0"
            ))
        
        # 10:00 PM - If we have 5 attractions
        if len(attractions) >= 5:
            activities.append(Activity(
                time="10:00 PM",
                activity_type="attraction",
                name=attractions[4].name,
                description=f"Night at {attractions[4].name}",
                duration_minutes=60,
                attraction=attractions[4],
                notes=f"🌙 Night! Rating: {attractions[4].rating}/5.0"
            ))
        
        return activities
    
    def _generate_day_theme(self, day_number: int) -> str:
        """Generate day theme."""
        themes = ["Iconic Landmarks", "Cultural Exploration", "Historic Treasures", "Local Flavors", "Hidden Gems"]
        return themes[(day_number - 1) % len(themes)]
    
    def _calculate_cost(self, attractions: List[Attraction], city_multiplier: float, budget_per_day: float = None) -> float:
        """Calculate day cost in USD."""
        # Meals
        if budget_per_day and budget_per_day < 100:
            meals_cost = (10 + 8) * city_multiplier + 10
        elif budget_per_day and budget_per_day < 200:
            meals_cost = (20 + 15) * city_multiplier + 10
        elif budget_per_day and budget_per_day < 300:
            meals_cost = (35 + 25) * city_multiplier + 10
        else:
            meals_cost = (50 + 40) * city_multiplier + 10
        
        # Attractions
        base_cost_map = {0: 0, 1: 15, 2: 30, 3: 50, 4: 85}
        attractions_total = sum(
            base_cost_map.get(self._get_smart_price_level(a), 30) * city_multiplier 
            for a in attractions
        )
        
        # Transport
        transport_cost = 10 * city_multiplier
        
        return round(meals_cost + attractions_total + transport_cost, 2)


planning_agent = PlanningAgent()
