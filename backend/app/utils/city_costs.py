"""
City Cost Intelligence - Determines cost multipliers for any destination.
Uses hybrid approach: RAG → Hardcoded → Web Search → Default
"""
from typing import Dict, Optional
import re


class CityCostAnalyzer:
    """Analyzes and determines cost multipliers for cities worldwide."""
    
    # Tier 1: Expensive cities (1.5+)
    EXPENSIVE_CITIES = {
        'paris': 1.5, 'london': 1.6, 'tokyo': 1.7, 'new york': 1.5, 'nyc': 1.5,
        'singapore': 1.4, 'hong kong': 1.5, 'sydney': 1.5, 'zurich': 1.8,
        'geneva': 1.7, 'oslo': 1.6, 'copenhagen': 1.6, 'stockholm': 1.5,
        'dubai': 1.8, 'abu dhabi': 1.7, 'san francisco': 1.5, 'los angeles': 1.4,
        'boston': 1.4, 'seattle': 1.4, 'miami': 1.3, 'chicago': 1.3,
        'toronto': 1.3, 'vancouver': 1.4, 'melbourne': 1.4, 'amsterdam': 1.4,
        'brussels': 1.3, 'vienna': 1.3, 'munich': 1.4, 'berlin': 1.2
    }
    
    # Tier 2: Moderate cities (0.8-1.2)
    MODERATE_CITIES = {
        'barcelona': 1.1, 'madrid': 1.0, 'rome': 1.1, 'milan': 1.2,
        'lisbon': 0.9, 'porto': 0.8, 'athens': 0.9, 'prague': 0.8,
        'budapest': 0.7, 'krakow': 0.7, 'warsaw': 0.8, 'dublin': 1.2,
        'edinburgh': 1.1, 'manchester': 1.0, 'seoul': 1.0, 'taipei': 0.9,
        'shanghai': 1.0, 'beijing': 1.0, 'montreal': 1.1, 'austin': 1.1,
        'denver': 1.1, 'portland': 1.2, 'san diego': 1.2, 'phoenix': 1.0
    }
    
    # Tier 3: Budget-friendly cities (0.3-0.7)
    BUDGET_CITIES = {
        'bangkok': 0.4, 'bali': 0.3, 'chiang mai': 0.35, 'hanoi': 0.4,
        'ho chi minh': 0.4, 'siem reap': 0.35, 'phnom penh': 0.35,
        'manila': 0.5, 'jakarta': 0.4, 'kuala lumpur': 0.5, 'penang': 0.45,
        'mumbai': 0.4, 'delhi': 0.4, 'bangalore': 0.45, 'goa': 0.4,
        'kathmandu': 0.35, 'colombo': 0.4, 'mexico city': 0.5,
        'cancun': 0.6, 'playa del carmen': 0.6, 'lima': 0.5, 'quito': 0.45,
        'bogota': 0.5, 'buenos aires': 0.6, 'cairo': 0.4, 'marrakech': 0.5,
        'istanbul': 0.6, 'tbilisi': 0.4, 'bucharest': 0.6, 'sofia': 0.5
    }
    
    def __init__(self, vector_store=None):
        """Initialize with optional vector store for RAG."""
        self.vector_store = vector_store
        self.all_cities = {**self.EXPENSIVE_CITIES, **self.MODERATE_CITIES, **self.BUDGET_CITIES}
    
    def get_cost_multiplier(self, destination: str) -> float:
        """
        Get cost multiplier for destination using hybrid approach.
        Returns multiplier (0.3 = very cheap, 1.0 = average, 1.8 = very expensive)
        """
        destination_lower = destination.lower().strip()
        
        # Step 1: Try RAG lookup
        if self.vector_store:
            rag_multiplier = self._get_from_rag(destination_lower)
            if rag_multiplier:
                print(f"   💾 RAG: Found {destination} multiplier = {rag_multiplier}")
                return rag_multiplier
        
        # Step 2: Check hardcoded cities
        hardcoded = self._get_hardcoded_multiplier(destination_lower)
        if hardcoded:
            print(f"   📋 Hardcoded: {destination} multiplier = {hardcoded}")
            return hardcoded
        
        # Step 3: Web search (if needed - placeholder for now)
        # web_multiplier = self._get_from_web_search(destination_lower)
        # if web_multiplier:
        #     return web_multiplier
        
        # Step 4: Default fallback
        print(f"   🌍 Default: {destination} multiplier = 1.0 (standard)")
        return 1.0
    
    def _get_hardcoded_multiplier(self, destination: str) -> Optional[float]:
        """Check hardcoded city multipliers."""
        # Direct match
        if destination in self.all_cities:
            return self.all_cities[destination]
        
        # Partial match (e.g., "paris, france" matches "paris")
        for city, multiplier in self.all_cities.items():
            if city in destination or destination in city:
                return multiplier
        
        return None
    
    def _get_from_rag(self, destination: str) -> Optional[float]:
        """Query RAG for city cost information (placeholder)."""
        # TODO: Implement RAG query
        # query = f"average cost of living and tourist expenses in {destination}"
        # results = self.vector_store.query(query)
        # Parse results and extract multiplier
        return None
    
    def get_tier_info(self, multiplier: float) -> Dict:
        """Get budget tier information based on multiplier."""
        if multiplier >= 1.5:
            return {
                'tier': 'expensive',
                'description': 'High-cost destination',
                'emoji': '💎'
            }
        elif multiplier >= 1.0:
            return {
                'tier': 'moderate',
                'description': 'Moderate-cost destination',
                'emoji': '🏙️'
            }
        elif multiplier >= 0.6:
            return {
                'tier': 'affordable',
                'description': 'Affordable destination',
                'emoji': '🌴'
            }
        else:
            return {
                'tier': 'budget',
                'description': 'Budget-friendly destination',
                'emoji': '🎒'
            }


# Singleton instance
city_cost_analyzer = CityCostAnalyzer()
