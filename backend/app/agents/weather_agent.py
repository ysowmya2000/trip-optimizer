"""
Weather Agent - Monitors weather and suggests activity adaptations.
"""
from typing import List, Dict
from app.schemas.trip import Itinerary, DayPlan
from app.external.weather import weather_client


class WeatherAgent:
    """Agent responsible for weather monitoring and activity adaptation."""
    
    def __init__(self):
        """Initialize Weather Agent."""
        self.name = "Weather Agent"
        print(f"🌤️  {self.name} initialized")
    
    def check_weather(self, itinerary: Itinerary) -> Dict:
        """
        Check weather forecast for trip and provide recommendations.
        
        Args:
            itinerary: Trip itinerary
            
        Returns:
            Weather analysis with recommendations
        """
        print(f"\n🌤️  {self.name}: Checking weather for {itinerary.destination}...")
        
        # Get forecast
        forecast = weather_client.get_forecast(
            itinerary.destination, 
            days=itinerary.trip_duration
        )
        
        # Analyze each day
        daily_weather = []
        rainy_days = []
        
        for i, day in enumerate(itinerary.days):
            if i < len(forecast):
                day_forecast = forecast[i]
                daily_weather.append({
                    "day_number": day.day_number,
                    "date": day_forecast.get("date"),
                    "condition": day_forecast.get("condition"),
                    "temp_high": day_forecast.get("temp_high"),
                    "temp_low": day_forecast.get("temp_low"),
                    "is_rainy": day_forecast.get("is_rainy", False)
                })
                
                if day_forecast.get("is_rainy"):
                    rainy_days.append(day.day_number)
        
        # Generate recommendations
        recommendations = self._generate_weather_recommendations(
            itinerary, 
            daily_weather,
            rainy_days
        )
        
        analysis = {
            "destination": itinerary.destination,
            "forecast": daily_weather,
            "rainy_days": rainy_days,
            "recommendations": recommendations,
            "needs_adaptation": len(rainy_days) > 0
        }
        
        print(f"✅ {self.name}: Weather check complete - {len(rainy_days)} rainy days detected")
        return analysis
    
    def _generate_weather_recommendations(
        self,
        itinerary: Itinerary,
        daily_weather: List[Dict],
        rainy_days: List[int]
    ) -> List[str]:
        """Generate weather-based recommendations."""
        recommendations = []
        
        if not rainy_days:
            recommendations.append("☀️ Great news! Weather looks good throughout your trip!")
            return recommendations
        
        recommendations.append(f"🌧️ Rain expected on {len(rainy_days)} day(s): Day {', '.join(map(str, rainy_days))}")
        recommendations.append("💡 Suggested adaptations:")
        
        for day_num in rainy_days:
            # Find the day
            day = next((d for d in itinerary.days if d.day_number == day_num), None)
            if day:
                # Count outdoor activities
                outdoor_activities = [
                    act for act in day.activities 
                    if act.activity_type == "attraction"
                ]
                
                if outdoor_activities:
                    recommendations.append(
                        f"  Day {day_num} ({day.title}): Consider indoor alternatives"
                    )
                    recommendations.append(
                        "    - Museums, galleries, shopping malls"
                    )
                    recommendations.append(
                        "    - Indoor markets, cooking classes"
                    )
                    recommendations.append(
                        "    - Cafes, restaurants with extended stays"
                    )
        
        recommendations.append("☂️ Pack: Umbrella, rain jacket, waterproof shoes")
        
        return recommendations
    
    def suggest_indoor_alternatives(self, outdoor_activity: str) -> List[str]:
        """Suggest indoor alternatives for outdoor activities."""
        indoor_alternatives = {
            "park": ["Museum", "Art gallery", "Shopping mall", "Aquarium"],
            "temple": ["Indoor shrine", "Cultural center", "History museum"],
            "market": ["Indoor market", "Department store", "Shopping arcade"],
            "beach": ["Aquarium", "Oceanographic museum", "Spa", "Indoor pool"],
            "garden": ["Botanical conservatory", "Indoor garden", "Museum"]
        }
        
        # Default alternatives
        default = ["Museum", "Gallery", "Shopping center", "Indoor attraction"]
        
        for keyword, alternatives in indoor_alternatives.items():
            if keyword in outdoor_activity.lower():
                return alternatives
        
        return default


# Create global instance
weather_agent = WeatherAgent()
