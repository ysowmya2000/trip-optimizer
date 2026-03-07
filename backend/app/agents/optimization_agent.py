"""
Optimization Agent - Optimizes routes and minimizes travel time.
"""
from typing import List, Dict
from app.schemas.trip import Itinerary, DayPlan, Attraction
from app.core.optimization import (
    nearest_neighbor_tsp,
    calculate_total_distance,
    estimate_travel_time
)


class OptimizationAgent:
    """Agent responsible for optimizing routes and minimizing travel time."""
    
    def __init__(self):
        """Initialize Optimization Agent."""
        self.name = "Optimization Agent"
        print(f"🎯 {self.name} initialized")
    
    def optimize_itinerary(self, itinerary: Itinerary) -> Itinerary:
        """
        Optimize an itinerary by reordering attractions to minimize travel.
        
        Args:
            itinerary: Original itinerary from Planning Agent
            
        Returns:
            Optimized itinerary with better routes
        """
        print(f"\n🎯 {self.name}: Optimizing itinerary for {itinerary.destination}...")
        
        optimized_days = []
        total_time_saved = 0
        
        for day in itinerary.days:
            optimized_day = self._optimize_day(day)
            optimized_days.append(optimized_day)
            
            # Calculate improvement (optional - for reporting)
            original_distance = self._calculate_day_distance(day)
            optimized_distance = self._calculate_day_distance(optimized_day)
            time_saved = estimate_travel_time(original_distance - optimized_distance)
            total_time_saved += time_saved
        
        # Create new optimized itinerary
        optimized_itinerary = Itinerary(
            destination=itinerary.destination,
            trip_duration=itinerary.trip_duration,
            interests=itinerary.interests,
            days=optimized_days,
            total_attractions=itinerary.total_attractions,
            estimated_total_cost=itinerary.estimated_total_cost,
            created_by=f"{itinerary.created_by} + {self.name}"
        )
        
        print(f"✅ {self.name}: Optimized! Estimated {total_time_saved} min saved in travel")
        return optimized_itinerary
    
    def _optimize_day(self, day: DayPlan) -> DayPlan:
        """Optimize a single day's route."""
        # Extract attractions from activities
        attraction_activities = [
            act for act in day.activities 
            if act.activity_type == "attraction" and act.attraction
        ]
        
        if len(attraction_activities) <= 1:
            return day
        
        # Get attraction objects
        attractions = [act.attraction for act in attraction_activities]
        
        # Convert to dict for optimization
        attr_dicts = [
            {
                'name': attr.name,
                'location': attr.location,
                'rating': attr.rating,
                'price_level': attr.price_level
            }
            for attr in attractions
        ]
        
        # Optimize order using TSP
        optimized_attrs = nearest_neighbor_tsp(attr_dicts)
        
        # Rebuild activities with optimized order
        new_activities = []
        time_slots = ["9:00 AM", "1:30 PM", "4:00 PM"]
        
        for i, attr_dict in enumerate(optimized_attrs):
            # Find original attraction object
            original_attr = next(
                (a for a in attractions if a.name == attr_dict['name']),
                None
            )
            
            if original_attr and i < len(time_slots):
                # Create new activity with optimized time
                from app.schemas.trip import Activity
                new_activities.append(Activity(
                    time=time_slots[i],
                    activity_type="attraction",
                    name=original_attr.name,
                    description=f"Visit {original_attr.name}",
                    duration_minutes=120 if i == 0 else (120 if i == 1 else 90),
                    attraction=original_attr,
                    notes=f"Rating: {original_attr.rating}/5.0 (Optimized route)"
                ))
        
        # Add meals back
        from app.schemas.trip import Activity
        new_activities.insert(1, Activity(
            time="12:00 PM",
            activity_type="meal",
            name="Lunch",
            description="Local restaurant",
            duration_minutes=60,
            notes="Try local cuisine"
        ))
        
        new_activities.append(Activity(
            time="7:00 PM",
            activity_type="meal",
            name="Dinner",
            description="Dinner at local restaurant",
            duration_minutes=90,
            notes="Relax and enjoy"
        ))
        
        # Create optimized day
        return DayPlan(
            day_number=day.day_number,
            title=day.title + " (Optimized)",
            activities=new_activities,
            total_attractions=day.total_attractions,
            estimated_cost=day.estimated_cost,
            notes=f"{day.notes} - Route optimized for minimal travel time"
        )
    
    def _calculate_day_distance(self, day: DayPlan) -> float:
        """Calculate total travel distance for a day."""
        attractions = [
            act.attraction for act in day.activities 
            if act.activity_type == "attraction" and act.attraction
        ]
        
        if len(attractions) <= 1:
            return 0.0
        
        attr_dicts = [{'location': a.location} for a in attractions]
        return calculate_total_distance(attr_dicts)


# Create global instance
optimization_agent = OptimizationAgent()
