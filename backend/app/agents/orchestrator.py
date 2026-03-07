"""
Multi-Agent Orchestrator - Coordinates all agents to create optimized trips.
"""
from typing import Dict, Optional
from app.schemas.trip import TripRequest, Itinerary
from app.agents.research_agent import research_agent
from app.agents.planning_agent import planning_agent
from app.agents.optimization_agent import optimization_agent
from app.agents.budget_agent import budget_agent
from app.agents.weather_agent import weather_agent


class TripOrchestrator:
    """
    Orchestrates multiple agents to create complete, optimized trip itineraries.
    
    Workflow:
    1. Research Agent - Find attractions
    2. Planning Agent - Create initial itinerary
    3. Optimization Agent - Optimize routes
    4. Budget Agent - Analyze costs
    5. Weather Agent - Check forecast and adapt
    """
    
    def __init__(self):
        """Initialize orchestrator."""
        self.name = "Trip Orchestrator"
        print(f"🎭 {self.name} initialized")
        
        # Agent instances
        self.research = research_agent
        self.planning = planning_agent
        self.optimization = optimization_agent
        self.budget = budget_agent
        self.weather = weather_agent
    
    def create_complete_trip(self, request: TripRequest) -> Dict:
        """
        Create a complete, optimized trip using all agents.
        
        Args:
            request: Trip request with destination, interests, etc.
            
        Returns:
            Complete trip package with itinerary and analysis
        """
        print(f"\n{'='*60}")
        print(f"🎭 {self.name}: Creating complete trip")
        print(f"{'='*60}")
        
        result = {
            "success": False,
            "request": request.dict(),
            "itinerary": None,
            "optimization_report": None,
            "budget_analysis": None,
            "weather_forecast": None,
            "warnings": [],
            "recommendations": []
        }
        
        try:
            # PHASE 1: Research
            print(f"\n📍 PHASE 1: Research")
            research_result = self.research.research_destination(
                destination=request.destination,
                interests=request.interests,
                trip_duration=request.trip_duration
            )
            
            attractions = research_result.get('top_attractions', [])
            
            if not attractions:
                result["warnings"].append("No attractions found")
                return result
            
            # PHASE 2: Planning
            print(f"\n📍 PHASE 2: Planning")
            initial_itinerary = self.planning.create_itinerary(
                destination=request.destination,
                interests=request.interests,
                attractions=attractions,
                trip_duration=request.trip_duration,
                budget=request.budget
            )
            
            # PHASE 3: Optimization
            print(f"\n📍 PHASE 3: Route Optimization")
            optimized_itinerary = self.optimization.optimize_itinerary(
                initial_itinerary
            )
            
            result["itinerary"] = optimized_itinerary.dict()
            
            # PHASE 4: Budget Analysis
            print(f"\n📍 PHASE 4: Budget Analysis")
            budget_analysis = self.budget.analyze_budget(
                optimized_itinerary,
                budget=request.budget
            )
            
            result["budget_analysis"] = budget_analysis
            
            # Add budget warnings
            if budget_analysis.get("budget_status") == "over_budget":
                result["warnings"].append(
                    f"Trip is over budget by ${budget_analysis.get('over_budget_amount', 0):.2f}"
                )
            
            # PHASE 5: Weather Check
            print(f"\n📍 PHASE 5: Weather Forecast")
            weather_analysis = self.weather.check_weather(optimized_itinerary)
            
            result["weather_forecast"] = weather_analysis
            
            # Add weather warnings
            if weather_analysis.get("needs_adaptation"):
                rainy_days = weather_analysis.get("rainy_days", [])
                result["warnings"].append(
                    f"Rain expected on {len(rainy_days)} day(s)"
                )
            
            # PHASE 6: Generate Final Recommendations
            print(f"\n📍 PHASE 6: Final Recommendations")
            recommendations = self._generate_final_recommendations(
                optimized_itinerary,
                budget_analysis,
                weather_analysis
            )
            
            result["recommendations"] = recommendations
            result["success"] = True
            
            print(f"\n{'='*60}")
            print(f"✅ {self.name}: Trip creation complete!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ {self.name}: Error creating trip - {e}")
            result["error"] = str(e)
        
        return result
    
    def _generate_final_recommendations(
        self,
        itinerary: Itinerary,
        budget_analysis: Dict,
        weather_analysis: Dict
    ) -> list:
        """Generate final consolidated recommendations."""
        recommendations = []
        
        # Trip summary
        recommendations.append(
            f"📅 {itinerary.trip_duration}-day trip to {itinerary.destination}"
        )
        recommendations.append(
            f"🎯 {itinerary.total_attractions} attractions planned"
        )
        recommendations.append(
            f"💰 Estimated cost: ${itinerary.estimated_total_cost:.2f}"
        )
        
        # Budget recommendations
        if budget_analysis.get("budget_status") == "over_budget":
            recommendations.extend(budget_analysis.get("recommendations", [])[:3])
        
        # Weather recommendations
        if weather_analysis.get("needs_adaptation"):
            recommendations.extend(weather_analysis.get("recommendations", [])[:3])
        
        # General tips
        recommendations.extend([
            "",
            "📝 General Tips:",
            "  - Book accommodations in advance",
            "  - Download offline maps",
            "  - Learn basic local phrases",
            "  - Check visa requirements"
        ])
        
        return recommendations


# Create global instance
trip_orchestrator = TripOrchestrator()
