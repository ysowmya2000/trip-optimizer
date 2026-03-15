"""
Weather Agent - Provides seasonal weather forecast based on travel dates.
"""
from datetime import datetime
from typing import Dict, Optional


class WeatherAgent:
    """Agent for seasonal weather forecasting."""
    
    # Seasonal weather data for major cities
    SEASONAL_WEATHER = {
        'bangkok': {
            'hot_season': {'months': [3, 4, 5], 'temp': '28-35°C', 'condition': 'Hot & Humid', 'advice': 'Pack light, breathable clothes. Stay hydrated.'},
            'rainy_season': {'months': [6, 7, 8, 9, 10], 'temp': '25-32°C', 'condition': 'Monsoon Rains', 'advice': 'Bring umbrella and rain jacket. Expect afternoon showers.'},
            'cool_season': {'months': [11, 12, 1, 2], 'temp': '20-30°C', 'condition': 'Warm & Pleasant', 'advice': 'Best time to visit! Pack light layers.'}
        },
        'paris': {
            'spring': {'months': [3, 4, 5], 'temp': '8-18°C', 'condition': 'Mild & Blooming', 'advice': 'Pack layers. Light jacket needed.'},
            'summer': {'months': [6, 7, 8], 'temp': '15-25°C', 'condition': 'Warm & Sunny', 'advice': 'Light summer clothes. Sunscreen recommended.'},
            'fall': {'months': [9, 10, 11], 'temp': '8-18°C', 'condition': 'Cool & Crisp', 'advice': 'Jacket and layers. Beautiful foliage.'},
            'winter': {'months': [12, 1, 2], 'temp': '1-8°C', 'condition': 'Cold & Occasional Snow', 'advice': 'Warm coat, scarf, gloves essential.'}
        },
        'london': {
            'spring': {'months': [3, 4, 5], 'temp': '6-15°C', 'condition': 'Mild & Rainy', 'advice': 'Umbrella essential. Light layers.'},
            'summer': {'months': [6, 7, 8], 'temp': '14-23°C', 'condition': 'Warm & Unpredictable', 'advice': 'Light clothes + rain jacket.'},
            'fall': {'months': [9, 10, 11], 'temp': '8-16°C', 'condition': 'Cool & Rainy', 'advice': 'Waterproof jacket. Warm layers.'},
            'winter': {'months': [12, 1, 2], 'temp': '2-8°C', 'condition': 'Cold & Damp', 'advice': 'Heavy coat, umbrella, warm layers.'}
        },
        'tokyo': {
            'spring': {'months': [3, 4, 5], 'temp': '10-20°C', 'condition': 'Cherry Blossoms & Mild', 'advice': 'Light jacket. Beautiful season!'},
            'summer': {'months': [6, 7, 8], 'temp': '22-32°C', 'condition': 'Hot & Humid', 'advice': 'Light clothes. Stay hydrated.'},
            'fall': {'months': [9, 10, 11], 'temp': '12-22°C', 'condition': 'Pleasant & Colorful', 'advice': 'Light layers. Great weather!'},
            'winter': {'months': [12, 1, 2], 'temp': '2-12°C', 'condition': 'Cold & Dry', 'advice': 'Warm coat and layers needed.'}
        }
    }
    
    def __init__(self):
        self.name = "Weather Agent"
        print(f"🌤️ {self.name} initialized")
    
    def get_seasonal_forecast(self, destination: str, start_date: Optional[str] = None) -> Dict:
        """Get seasonal weather forecast for destination and travel date."""
        print(f"\n🌤️ {self.name}: Getting seasonal forecast for {destination}...")
        
        # Parse travel month
        if start_date:
            try:
                date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                travel_month = date_obj.month
                month_name = date_obj.strftime('%B')
                print(f"   📅 Travel month: {month_name} (Month {travel_month})")
            except:
                travel_month = datetime.now().month
                month_name = datetime.now().strftime('%B')
        else:
            travel_month = datetime.now().month
            month_name = datetime.now().strftime('%B')
        
        # Get city-specific weather
        dest_lower = destination.lower()
        city_weather = None
        
        for city, seasons in self.SEASONAL_WEATHER.items():
            if city in dest_lower:
                city_weather = seasons
                break
        
        # Find matching season
        if city_weather:
            for season_name, season_data in city_weather.items():
                if travel_month in season_data['months']:
                    print(f"   ✅ Season: {season_name.replace('_', ' ').title()}")
                    return {
                        'destination': destination,
                        'month': month_name,
                        'season': season_name.replace('_', ' ').title(),
                        'temperature': season_data['temp'],
                        'condition': season_data['condition'],
                        'advice': season_data['advice']
                    }
        
        # Default forecast for unknown cities
        print(f"   ℹ️  Using general forecast")
        return {
            'destination': destination,
            'month': month_name,
            'season': 'Variable',
            'temperature': '15-25°C',
            'condition': 'Check local weather closer to travel date',
            'advice': 'Pack versatile clothing layers.'
        }


weather_agent = WeatherAgent()
