"""
Research Agent - Gathers information about destinations.
Enhanced with RAG for local knowledge and insider tips.
"""
from typing import Dict, List
from app.external.llm import llm_mini
from app.external.google_places import google_places_client
from app.db.vector_store import travel_kb


class ResearchAgent:
    """
    Agent responsible for researching destinations and finding attractions.
    Enhanced with RAG-based local knowledge.
    """
    
    def __init__(self):
        """Initialize Research Agent."""
        self.name = "Research Agent"
        self.kb = travel_kb
        print(f"🔍 {self.name} initialized (RAG-enabled)")
    
    def research_destination(
        self, 
        destination: str,
        interests: List[str],
        trip_duration: int
    ) -> Dict:
        """
        Research a destination and find relevant attractions.
        Enhanced with RAG-based local knowledge.
        """
        print(f"\n🔍 {self.name}: Researching {destination} (with RAG)...")
        
        # Step 1: Get local knowledge from RAG
        local_tips = self._get_local_knowledge(destination, interests)
        
        # Step 2: Use LLM + RAG to generate search queries
        search_queries = self._generate_search_queries(
            destination, 
            interests, 
            trip_duration,
            local_tips
        )
        
        # Step 3: Search Google Places
        all_attractions = []
        for query in search_queries:
            attractions = google_places_client.search_attractions(
                location=destination,
                query=query,
                max_results=10
            )
            all_attractions.extend(attractions)
        
        # Step 4: Rank attractions
        ranked_attractions = self._rank_attractions(all_attractions, interests, trip_duration)
        
        # Step 5: Enhance with RAG insights
        enhanced_attractions = self._enhance_with_rag(ranked_attractions, destination)
        
        # Step 6: Compile research report
        report = {
            "destination": destination,
            "interests": interests,
            "trip_duration": trip_duration,
            "search_queries": search_queries,
            "local_tips": local_tips,
            "total_attractions_found": len(all_attractions),
            "top_attractions": enhanced_attractions[:trip_duration * 3],
            "rag_enabled": True,
            "status": "complete"
        }
        
        print(f"✅ {self.name}: Found {len(all_attractions)} attractions + {len(local_tips)} local tips")
        return report
    
    def _get_local_knowledge(self, destination: str, interests: List[str]) -> List[str]:
        """Get local tips from RAG knowledge base."""
        tips = []
        
        # Get general tips for destination
        general_tips = self.kb.get_tips_for_destination(destination, n_results=3)
        tips.extend(general_tips)
        
        # Get interest-specific recommendations
        for interest in interests[:2]:  # Limit to avoid too many queries
            interest_tips = self.kb.get_local_recommendations(destination, interest)
            tips.extend(interest_tips[:2])
        
        # Remove duplicates
        tips = list(dict.fromkeys(tips))
        
        return tips[:5]  # Max 5 tips
    
    def _generate_search_queries(
        self, 
        destination: str, 
        interests: List[str],
        trip_duration: int,
        local_tips: List[str]
    ) -> List[str]:
        """Generate search queries enhanced with RAG context."""
        
        system_message = """You are a travel research expert with local knowledge.
Generate 3-5 specific search queries based on interests and local tips.

Be specific and use insider knowledge from the tips provided.
Return ONLY a comma-separated list of queries."""
        
        # Include RAG tips in context
        tips_context = "\n".join([f"- {tip[:100]}" for tip in local_tips[:3]])
        
        user_message = f"""Destination: {destination}
Interests: {', '.join(interests)}
Trip duration: {trip_duration} days

Local insider tips:
{tips_context}

Generate search queries:"""
        
        response = llm_mini.chat(user_message, system_message=system_message)
        
        queries = [q.strip() for q in response.split(',')]
        
        if not queries or len(queries) == 0:
            queries = interests + ["tourist attractions", "restaurants"]
        
        return queries[:5]
    
    def _rank_attractions(
        self, 
        attractions: List[Dict],
        interests: List[str],
        trip_duration: int
    ) -> List[Dict]:
        """Rank attractions by relevance."""
        seen_ids = set()
        unique_attractions = []
        
        for attraction in attractions:
            place_id = attraction.get('place_id')
            if place_id not in seen_ids:
                seen_ids.add(place_id)
                unique_attractions.append(attraction)
        
        import math
        for attraction in unique_attractions:
            rating = attraction.get('rating', 0)
            reviews = attraction.get('user_ratings_total', 1)
            score = rating * math.log(reviews + 1)
            attraction['relevance_score'] = score
        
        ranked = sorted(
            unique_attractions, 
            key=lambda x: x.get('relevance_score', 0), 
            reverse=True
        )
        
        return ranked
    
    def _enhance_with_rag(self, attractions: List[Dict], destination: str) -> List[Dict]:
        """Enhance attractions with RAG-based insider tips."""
        enhanced = []
        
        for attraction in attractions:
            attr_name = attraction.get('name', '')
            
            # Search for specific tips about this attraction
            tips = self.kb.search(
                query=f"tips for {attr_name} in {destination}",
                n_results=1
            )
            
            # Add RAG tip if found and relevant
            if tips["documents"] and tips["distances"][0] < 0.7:  # Similarity threshold
                attraction['insider_tip'] = tips["documents"][0]
            
            enhanced.append(attraction)
        
        return enhanced
    
    def get_quick_summary(self, destination: str) -> str:
        """Get quick summary with RAG context."""
        # Get local knowledge
        tips = self.kb.get_tips_for_destination(destination, n_results=2)
        tips_text = " ".join(tips[:1]) if tips else ""
        
        system_message = f"""You are a travel expert. Provide a brief 2-3 sentence summary.
        
Local knowledge: {tips_text[:200]}"""
        
        user_message = f"Tell me about {destination} as a travel destination:"
        
        summary = llm_mini.chat(user_message, system_message=system_message)
        return summary


# Create global instance
research_agent = ResearchAgent()
