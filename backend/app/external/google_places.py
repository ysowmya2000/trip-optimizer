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
    
    MOCK_TEMPLATES = [
        ('Grand Temple of {location}', ['tourist_attraction', 'place_of_worship', 'point_of_interest'], 4.6),
        ('{location} History Museum', ['museum', 'point_of_interest'], 4.5),
        ('{location} Street Food Market', ['restaurant', 'food', 'point_of_interest'], 4.4),
        ('{location} Central Park', ['park', 'tourist_attraction', 'point_of_interest'], 4.3),
        ('{location} Skyline Rooftop Bar', ['bar', 'nightlife', 'point_of_interest'], 4.2),
        ('{location} Panoramic Viewpoint', ['tourist_attraction', 'viewpoint', 'point_of_interest'], 4.7),
        ('{location} Old Town Square', ['tourist_attraction', 'point_of_interest'], 4.1),
        ('{location} Botanical Garden', ['garden', 'park', 'point_of_interest'], 4.5),
    ]

    def _get_mock_data(self, location: str, query: str) -> List[Dict]:
        """Return mock data for testing without an API key or live calls disabled.

        place_id/name vary by (location, query) so repeated searches across a
        research pass don't collapse to the same 3 items via place_id dedup -
        mirroring how a real API returns different results per query.
        """
        import hashlib
        seed = hashlib.md5(f"{location}_{query}".encode()).hexdigest()

        results = []
        for i, (name_tpl, types, rating) in enumerate(self.MOCK_TEMPLATES):
            if int(seed[i], 16) % 2 == 0:
                continue
            results.append({
                'name': name_tpl.format(location=location),
                'address': f'{100 + i} Sample Street, {location}',
                'rating': rating,
                'user_ratings_total': 500 + i * 137,
                'types': types,
                'location': {'lat': 0.0, 'lng': 0.0},
                'place_id': f'mock_{seed[:10]}_{i}',
                'price_level': i % 4,
                'opening_hours': {'open_now': True}
            })

        if not results:
            results.append({
                'name': f'Popular Attraction in {location}',
                'address': f'123 Main Street, {location}',
                'rating': 4.5,
                'user_ratings_total': 1234,
                'types': ['tourist_attraction', 'point_of_interest'],
                'location': {'lat': 0.0, 'lng': 0.0},
                'place_id': f'mock_{seed[:10]}_fallback',
                'price_level': 2,
                'opening_hours': {'open_now': True}
            })

        return results


# Create global instance
google_places_client = GooglePlacesClient()
