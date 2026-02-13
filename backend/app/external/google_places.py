"""
Google Places API wrapper.
Handles all interactions with Google Places API.
"""
from typing import List, Dict, Optional
from app.core.config import settings


class GooglePlacesClient:
    """Client for Google Places API."""
    
    def __init__(self):
        """Initialize Google Maps client."""
        # Only initialize if we have a real API key (not placeholder)
        if settings.GOOGLE_PLACES_API_KEY and not settings.GOOGLE_PLACES_API_KEY.startswith("placeholder"):
            try:
                import googlemaps
                self.client = googlemaps.Client(key=settings.GOOGLE_PLACES_API_KEY)
                self.available = True
                print("✅ Google Places API initialized")
            except Exception as e:
                self.client = None
                self.available = False
                print(f"⚠️  Google Places API error: {e}")
        else:
            self.client = None
            self.available = False
            print("⚠️  Google Places API key not found. Using mock data.")
    
    def search_attractions(
        self, 
        location: str, 
        query: str = "tourist attractions",
        radius: int = 5000,
        max_results: int = 20
    ) -> List[Dict]:
        """Search for attractions in a location."""
        
        # If no API key, return mock data
        if not self.available:
            print(f"📍 Using mock data for: {location} - {query}")
            return self._get_mock_data(location, query)
        
        try:
            # Geocode the location
            geocode_result = self.client.geocode(location)
            if not geocode_result:
                print(f"❌ Could not find location: {location}")
                return self._get_mock_data(location, query)
            
            lat_lng = geocode_result[0]['geometry']['location']
            
            # Search for places
            places_result = self.client.places_nearby(
                location=lat_lng,
                radius=radius,
                keyword=query
            )
            
            # Extract and format results
            attractions = []
            for place in places_result.get('results', [])[:max_results]:
                attraction = {
                    'name': place.get('name'),
                    'address': place.get('vicinity'),
                    'rating': place.get('rating', 0),
                    'user_ratings_total': place.get('user_ratings_total', 0),
                    'types': place.get('types', []),
                    'location': place.get('geometry', {}).get('location', {}),
                    'place_id': place.get('place_id'),
                    'price_level': place.get('price_level', 0),
                    'opening_hours': place.get('opening_hours', {})
                }
                attractions.append(attraction)
            
            return attractions
            
        except Exception as e:
            print(f"❌ Error searching Google Places: {e}")
            return self._get_mock_data(location, query)
    
    def _get_mock_data(self, location: str, query: str) -> List[Dict]:
        """Return mock data for testing without API key."""
        return [
            {
                'name': f'Popular Attraction in {location}',
                'address': f'123 Main Street, {location}',
                'rating': 4.5,
                'user_ratings_total': 1234,
                'types': ['tourist_attraction', 'point_of_interest'],
                'location': {'lat': 35.6762, 'lng': 139.6503},
                'place_id': 'mock_place_1',
                'price_level': 2,
                'opening_hours': {'open_now': True}
            },
            {
                'name': f'Historic Site in {location}',
                'address': f'456 Park Avenue, {location}',
                'rating': 4.8,
                'user_ratings_total': 5678,
                'types': ['museum', 'point_of_interest'],
                'location': {'lat': 35.6895, 'lng': 139.6917},
                'place_id': 'mock_place_2',
                'price_level': 1,
                'opening_hours': {'open_now': True}
            },
            {
                'name': f'Top Restaurant in {location}',
                'address': f'789 Food Street, {location}',
                'rating': 4.7,
                'user_ratings_total': 3456,
                'types': ['restaurant', 'food'],
                'location': {'lat': 35.6950, 'lng': 139.7010},
                'place_id': 'mock_place_3',
                'price_level': 2,
                'opening_hours': {'open_now': True}
            }
        ]


# Create global instance
google_places_client = GooglePlacesClient()
