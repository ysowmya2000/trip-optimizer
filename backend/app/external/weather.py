"""
Weather API wrapper.
Handles interactions with OpenWeather API.
"""
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from app.core.config import settings


class WeatherClient:
    """Client for OpenWeather API."""
    
    def __init__(self):
        """Initialize Weather client."""
        if settings.OPENWEATHER_API_KEY and not settings.OPENWEATHER_API_KEY.startswith("placeholder"):
            self.api_key = settings.OPENWEATHER_API_KEY
            self.available = True
            print("✅ Weather API initialized")
        else:
            self.api_key = None
            self.available = False
            print("⚠️  Weather API key not found. Using mock data.")
    
    def get_forecast(self, location: str, days: int = 7) -> List[Dict]:
        """
        Get weather forecast for a location.
        
        Args:
            location: City name
            days: Number of days forecast
            
        Returns:
            List of daily forecasts
        """
        if not self.available:
            return self._get_mock_forecast(location, days)
        
        try:
            import requests
            
            # Get coordinates for location
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {"q": location, "limit": 1, "appid": self.api_key}
            geo_response = requests.get(geo_url, params=geo_params)
            geo_data = geo_response.json()
            
            if not geo_data:
                return self._get_mock_forecast(location, days)
            
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            
            # Get forecast
            forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
            forecast_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            forecast_response = requests.get(forecast_url, params=forecast_params)
            forecast_data = forecast_response.json()
            
            # Parse forecast (API gives 3-hour intervals, aggregate to daily)
            daily_forecasts = self._parse_forecast(forecast_data, days)
            return daily_forecasts
            
        except Exception as e:
            print(f"❌ Error fetching weather: {e}")
            return self._get_mock_forecast(location, days)
    
    def _parse_forecast(self, data: Dict, days: int) -> List[Dict]:
        """Parse OpenWeather API response into daily forecasts."""
        forecasts = []
        
        if "list" not in data:
            return []
        
        # Group by date
        daily_data = {}
        for item in data["list"][:days * 8]:  # 8 intervals per day
            date = item["dt_txt"].split(" ")[0]
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)
        
        # Aggregate to daily
        for date, items in list(daily_data.items())[:days]:
            temps = [item["main"]["temp"] for item in items]
            conditions = [item["weather"][0]["main"] for item in items]
            
            # Most common condition
            condition = max(set(conditions), key=conditions.count)
            
            forecasts.append({
                "date": date,
                "temp_high": round(max(temps), 1),
                "temp_low": round(min(temps), 1),
                "condition": condition,
                "description": items[0]["weather"][0]["description"],
                "is_rainy": condition in ["Rain", "Drizzle", "Thunderstorm"],
                "is_good_weather": condition in ["Clear", "Clouds"]
            })
        
        return forecasts
    
    def _get_mock_forecast(self, location: str, days: int) -> List[Dict]:
        """Return mock forecast data."""
        forecasts = []
        conditions = ["Clear", "Clouds", "Rain", "Clear", "Clear", "Clouds", "Clear"]
        
        for i in range(days):
            date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            condition = conditions[i % len(conditions)]
            
            forecasts.append({
                "date": date,
                "temp_high": 22 + (i % 5),
                "temp_low": 15 + (i % 5),
                "condition": condition,
                "description": condition.lower(),
                "is_rainy": condition == "Rain",
                "is_good_weather": condition in ["Clear", "Clouds"]
            })
        
        return forecasts


# Create global instance
weather_client = WeatherClient()
