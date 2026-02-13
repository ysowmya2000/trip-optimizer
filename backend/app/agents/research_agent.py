"""
Research Agent - Gathers information about destinations.
Uses LLM + Google Places API to find relevant attractions.
"""
from typing import Dict, List
from app.external.llm import llm_mini
from app.external.google_places import google_places_client


class ResearchAgent:
    """
    Agent responsible for researching destinations and finding attractions.
    """
    
    def __init__(self):
        """Initialize Research Agent."""
        self.name = "Research Agent"
        print(f"🔍 {self.name} initialized")
    
    def research_destination(
        self, 
        destination: str,
        interests: List[str],
        trip_duration: int
    ) -> Dict:
        """
        Research a destination and find relevant attractions.
        
        Args:
            destination: City/location name (e.g., "Tokyo, Japan")
            interests: List of user interests (e.g., ["temples", "food", "nature"])
            trip_duration: Number of days for the trip
            
        Returns:
            Dictionary with research results
        """
        print(f"\n🔍 {self.name}: Researching {destination}...")
        
        # Step 1: Use LLM to understand what to search for
        search_queries = self._generate_search_queries(destination, interests, trip_duration)
        
        # Step 2: Search Google Places for each query
        all_attractions = []
        for query in search_queries:
            attractions = google_places_client.search_attractions(
                location=destination,
                query=query,
                max_results=10
            )
            all_attractions.extend(attractions)
        
        # Step 3: Use LLM to analyze and rank attractions
        ranked_attractions = self._rank_attractions(all_attractions, interests, trip_duration)
        
        # Step 4: Compile research report
        report = {
            "destination": destination,
            "interests": interests,
            "trip_duration": trip_duration,
            "search_queries": search_queries,
            "total_attractions_found": len(all_attractions),
            "top_attractions": ranked_attractions[:trip_duration * 3],  # 3 per day
            "status": "complete"
        }
        
        print(f"✅ {self.name}: Found {len(all_attractions)} attractions")
        return report
    
    def _generate_search_queries(
        self, 
        destination: str, 
        interests: List[str],
        trip_duration: int
    ) -> List[str]:
        """
        Use LLM to generate relevant search queries based on interests.
        
        Returns:
            List of search queries
        """
        system_message = """You are a travel research expert. 
Given a destination and user interests, generate 3-5 specific search queries 
that will help find the best attractions.

Be specific and diverse. For example:
- If interest is "food", search for "authentic local restaurants", "street food markets", "cooking classes"
- If interest is "temples", search for "historic temples", "zen gardens", "shrines"

Return ONLY a comma-separated list of queries, nothing else."""
        
        user_message = f"""Destination: {destination}
Interests: {', '.join(interests)}
Trip duration: {trip_duration} days

Generate search queries:"""
        
        response = llm_mini.chat(user_message, system_message=system_message)
        
        # Parse response into list
        queries = [q.strip() for q in response.split(',')]
        
        # Fallback to basic queries if LLM fails
        if not queries or len(queries) == 0:
            queries = interests + ["tourist attractions", "restaurants"]
        
        return queries[:5]  # Max 5 queries
    
    def _rank_attractions(
        self, 
        attractions: List[Dict],
        interests: List[str],
        trip_duration: int
    ) -> List[Dict]:
        """
        Rank attractions by relevance to user interests.
        
        For now: Simple ranking by rating and number of reviews.
        Later: Can use LLM for smarter ranking.
        """
        # Remove duplicates (same place_id)
        seen_ids = set()
        unique_attractions = []
        for attraction in attractions:
            place_id = attraction.get('place_id')
            if place_id not in seen_ids:
                seen_ids.add(place_id)
                unique_attractions.append(attraction)
        
        # Sort by rating * log(reviews) - favors highly rated + popular places
        import math
        for attraction in unique_attractions:
            rating = attraction.get('rating', 0)
            reviews = attraction.get('user_ratings_total', 1)
            # Score formula: rating * log(reviews + 1)
            score = rating * math.log(reviews + 1)
            attraction['relevance_score'] = score
        
        # Sort by score descending
        ranked = sorted(
            unique_attractions, 
            key=lambda x: x.get('relevance_score', 0), 
            reverse=True
        )
        
        return ranked
    
    def get_quick_summary(self, destination: str) -> str:
        """
        Get a quick LLM-generated summary about a destination.
        
        Args:
            destination: City/location name
            
        Returns:
            Brief summary string
        """
        system_message = "You are a travel expert. Provide a brief, enthusiastic 2-3 sentence summary about a destination."
        user_message = f"Tell me about {destination} as a travel destination:"
        
        summary = llm_mini.chat(user_message, system_message=system_message)
        return summary


# Create global instance
research_agent = ResearchAgent()
