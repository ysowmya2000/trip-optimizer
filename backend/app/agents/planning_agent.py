"""
Planning Agent - Creates day-by-day itineraries.
Takes attractions from Research Agent and organizes them into a logical trip plan.
"""
from typing import List, Dict
from app.schemas.trip import Itinerary, DayPlan, Activity, Attraction
from app.external.llm import llm_smart
import json


class PlanningAgent:
    """
    Agent responsible for creating optimized day-by-day itineraries.
    """
    
    def __init__(self):
        """Initialize Planning Agent."""
        self.name = "Planning Agent"
        print(f"📅 {self.name} initialized")
    
    def create_itinerary(
        self,
        destination: str,
        interests: List[str],
        attractions: List[Dict],
        trip_duration: int,
        budget: float = None
    ) -> Itinerary:
        """
        Create a complete day-by-day itinerary.
        
        Args:
            destination: City/location
            interests: User interests
            attractions: List of attractions from Research Agent
            trip_duration: Number of days
            budget: Optional budget in USD
            
        Returns:
            Complete Itinerary object
        """
        print(f"\n📅 {self.name}: Creating {trip_duration}-day itinerary for {destination}...")
        
        # Convert dict attractions to Attraction objects
        attraction_objects = [
            Attraction(**attr) for attr in attractions
        ]
        
        # Limit attractions to reasonable number per day (3-4 per day)
        max_attractions = trip_duration * 4
        top_attractions = attraction_objects[:max_attractions]
        
        # Create day plans
        days = self._create_day_plans(
            destination=destination,
            interests=interests,
            attractions=top_attractions,
            trip_duration=trip_duration,
            budget=budget
        )
        
        # Calculate totals
        total_attractions = sum(day.total_attractions for day in days)
        total_cost = sum(day.estimated_cost for day in days)
        
        itinerary = Itinerary(
            destination=destination,
            trip_duration=trip_duration,
            interests=interests,
            days=days,
            total_attractions=total_attractions,
            estimated_total_cost=total_cost,
            created_by=self.name
        )
        
        print(f"✅ {self.name}: Created itinerary with {len(days)} days, {total_attractions} attractions")
        return itinerary
    
    def _create_day_plans(
        self,
        destination: str,
        interests: List[str],
        attractions: List[Attraction],
        trip_duration: int,
        budget: float = None
    ) -> List[DayPlan]:
        """Create individual day plans."""
        days = []
        attractions_per_day = len(attractions) // trip_duration if trip_duration > 0 else 3
        attractions_per_day = max(2, min(attractions_per_day, 4))
        
        for day_num in range(1, trip_duration + 1):
            start_idx = (day_num - 1) * attractions_per_day
            end_idx = start_idx + attractions_per_day
            day_attractions = attractions[start_idx:end_idx]
            
            day_plan = self._create_single_day(
                day_number=day_num,
                destination=destination,
                attractions=day_attractions,
                interests=interests,
                budget_per_day=budget / trip_duration if budget else None
            )
            days.append(day_plan)
        
        return days
    
    def _create_single_day(
        self,
        day_number: int,
        destination: str,
        attractions: List[Attraction],
        interests: List[str],
        budget_per_day: float = None
    ) -> DayPlan:
        """Create a plan for a single day."""
        activities = []
        
        # Morning attraction
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
        
        # Lunch
        activities.append(Activity(
            time="12:00 PM",
            activity_type="meal",
            name="Lunch",
            description=f"Local restaurant in {destination}",
            duration_minutes=60,
            notes="Try local cuisine"
        ))
        
        # Afternoon attraction
        if len(attractions) > 1:
            activities.append(Activity(
                time="1:30 PM",
                activity_type="attraction",
                name=attractions[1].name,
                description=f"Explore {attractions[1].name}",
                duration_minutes=120,
                attraction=attractions[1],
                notes=f"Rating: {attractions[1].rating}/5.0"
            ))
        
        # Optional third attraction
        if len(attractions) > 2:
            activities.append(Activity(
                time="4:00 PM",
                activity_type="attraction",
                name=attractions[2].name,
                description=f"Visit {attractions[2].name}",
                duration_minutes=90,
                attraction=attractions[2],
                notes=f"Rating: {attractions[2].rating}/5.0"
            ))
        
        # Dinner
        activities.append(Activity(
            time="7:00 PM",
            activity_type="meal",
            name="Dinner",
            description="Dinner at local restaurant",
            duration_minutes=90,
            notes="Relax and enjoy the evening"
        ))
        
        day_title = self._generate_day_theme(day_number, attractions, interests)
        estimated_cost = self._estimate_day_cost(attractions)
        
        return DayPlan(
            day_number=day_number,
            title=day_title,
            activities=activities,
            total_attractions=len([a for a in activities if a.activity_type == "attraction"]),
            estimated_cost=estimated_cost,
            notes=f"Day {day_number} of your {destination} adventure"
        )
    
    def _generate_day_theme(self, day_number: int, attractions: List[Attraction], interests: List[str]) -> str:
        """Generate day theme."""
        if not llm_smart.available:
            if len(attractions) > 0:
                main_type = attractions[0].types[0] if attractions[0].types else "exploration"
                return f"Day {day_number}: {main_type.replace('_', ' ').title()}"
            return f"Day {day_number}: Exploration"
        
        attraction_names = [a.name for a in attractions]
        system_message = "You are a travel writer. Create a short catchy title (3-6 words) for a day of travel. Return ONLY the title."
        user_message = f"Day {day_number} attractions: {', '.join(attraction_names[:3])}. Create title:"
        
        try:
            title = llm_smart.chat(user_message, system_message=system_message)
            title = title.strip().strip('"').strip("'")
            if len(title) > 50:
                title = title[:47] + "..."
            return title
        except:
            return f"Day {day_number}: Adventure"
    
    def _estimate_day_cost(self, attractions: List[Attraction]) -> float:
        """Estimate daily cost."""
        cost_map = {0: 0, 1: 10, 2: 25, 3: 50, 4: 100}
        total = sum(cost_map.get(a.price_level, 15) for a in attractions)
        total += 40  # Meals
        total += 20  # Transport
        return round(total, 2)


# Create global instance
planning_agent = PlanningAgent()
