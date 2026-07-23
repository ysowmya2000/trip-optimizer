"""
Research Agent - Enhanced with RAG (Retrieval Augmented Generation)
Combines Google Places API with vector database for local insights
"""
from typing import List, Dict
from app.external.google_places import google_places_client
from app.db.vector_store import travel_kb
from app.external.llm import llm_smart


class ResearchAgent:
    """
    Agent that researches destinations and finds attractions.
    Enhanced with RAG for local knowledge and insider tips.
    """
    
    def __init__(self):
        self.name = "Research Agent"
        self.vector_store = travel_kb
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
        ALWAYS includes top iconic landmarks first!
        """
        print(f"\n🔍 {self.name}: Researching {destination} (with RAG)...")
        
        # Step 1: COMPREHENSIVE landmark search
        print(f"🗼 Fetching must-see landmarks for {destination}...")
        
        iconic_landmarks = []
        landmark_searches = [
            f"must see landmarks in {destination}",
            f"top tourist attractions {destination}",
            f"famous places {destination}",
            f"iconic monuments {destination}",
            f"best things to do {destination}",
            f"popular sights {destination}",
            f"{destination} bucket list attractions"
        ]
        
        seen_place_ids = set()
        for search_query in landmark_searches:
            results = google_places_client.search_attractions(
                location=destination,
                query=search_query,
                max_results=8
            )
            for result in results:
                place_id = result.get('place_id')
                if place_id and place_id not in seen_place_ids:
                    iconic_landmarks.append(result)
                    seen_place_ids.add(place_id)
                    
            # Stop if we have enough landmarks
            if len(iconic_landmarks) >= 15:
                break
        
        print(f"🗼 Found {len(iconic_landmarks)} iconic landmarks:")
        for i, landmark in enumerate(iconic_landmarks[:8]):
            print(f"   {i+1}. {landmark.get('name', 'Unknown')}")
        
        # Step 2: Get local knowledge from RAG
        local_tips = self._get_local_knowledge(destination, interests)
        
        # Step 3: Use LLM + RAG to generate search queries based on interests
        search_queries = self._generate_search_queries(
            destination, 
            interests, 
            trip_duration,
            local_tips
        )
        
        # Step 4: Search Google Places for interest-specific attractions
        interest_attractions = []
        for query in search_queries:
            attractions = google_places_client.search_attractions(
                location=destination,
                query=query,
                max_results=8
            )
            interest_attractions.extend(attractions)
        
        # Step 5: Combine - LANDMARKS FIRST, then interest-based
        combined_attractions = []
        
        # Add ALL iconic landmarks first (guaranteed to be included)
        for landmark in iconic_landmarks:
            if landmark.get('place_id') not in [a.get('place_id') for a in combined_attractions]:
                combined_attractions.append(landmark)
        
        # Then add interest-based attractions
        for attraction in interest_attractions:
            place_id = attraction.get('place_id')
            if place_id not in [a.get('place_id') for a in combined_attractions]:
                combined_attractions.append(attraction)
        
        print(f"📊 Total combined: {len(combined_attractions)} attractions")
        print(f"   Top 10 in final list:")
        for i, attr in enumerate(combined_attractions[:10]):
            print(f"   {i+1}. {attr.get('name', 'Unknown')}")
        
        # Step 6: Light ranking (preserve landmark priority)
        ranked_attractions = self._light_rank_attractions(combined_attractions, interests)
        
        # Step 7: Enhance with RAG insights
        enhanced_attractions = self._enhance_with_rag(ranked_attractions, destination)
        
        # Step 8: Compile report
        final_count = trip_duration * 5  # Increased from 3 to 4 per day
        print(f"📋 Selecting top {final_count} for {trip_duration}-day itinerary")
        
        report = {
            "destination": destination,
            "interests": interests,
            "trip_duration": trip_duration,
            "search_queries": search_queries,
            "local_tips": local_tips,
            "total_attractions_found": len(combined_attractions),
            "top_attractions": enhanced_attractions[:final_count],
            "rag_enabled": True,
            "status": "complete"
        }
        
        print(f"✅ {self.name}: Found {len(combined_attractions)} attractions + {len(local_tips)} local tips")
        return report
    
    def _get_local_knowledge(self, destination: str, interests: List[str]) -> List[str]:
        """Query RAG vector store for local knowledge"""
        try:
            query = f"insider tips for {destination} related to {', '.join(interests)}"
            results = self.vector_store.search(query=query, n_results=3)

            tips = []
            for doc in results.get('documents', []):
                if doc and len(doc) > 20:
                    tips.append(doc)

            return tips[:3]
        except:
            return []
    
    def _generate_search_queries(
        self, 
        destination: str, 
        interests: List[str],
        trip_duration: int,
        local_tips: List[str]
    ) -> List[str]:
        """Generate smart search queries using LLM"""
        
        if not llm_smart.available:
            queries = [f"{interest} in {destination}" for interest in interests[:3]]
            return queries
        
        context = f"Local tips: {'. '.join(local_tips[:2])}" if local_tips else ""
        prompt = f"""Generate 3 specific Google search queries to find attractions in {destination}.
User interests: {', '.join(interests)}
Trip duration: {trip_duration} days
{context}

Return ONLY the queries, one per line, no numbering."""
        
        try:
            response = llm_smart.chat(prompt, max_tokens=200)
            queries = [q.strip() for q in response.split('\n') if q.strip() and len(q.strip()) > 5]
            return queries[:3]
        except:
            return [f"{interest} in {destination}" for interest in interests[:3]]
    
    def _light_rank_attractions(
        self, 
        attractions: List[Dict], 
        interests: List[str]
    ) -> List[Dict]:
        """
        Light ranking that preserves landmark priority.
        """
        
        # Keep first 15 as-is (iconic landmarks), rank the rest
        top_landmarks = attractions[:15]
        rest = attractions[15:]
        
        def score_attraction(attr):
            score = 0
            rating = attr.get('rating', 0)
            score += rating * 10
            
            review_count = attr.get('user_ratings_total', 0)
            if review_count > 1000:
                score += 20
            elif review_count > 500:
                score += 10
            
            attr_types = attr.get('types', [])
            for interest in interests:
                if interest.lower() in ' '.join(attr_types).lower():
                    score += 15
            
            return score
        
        ranked_rest = sorted(rest, key=score_attraction, reverse=True)
        
        return top_landmarks + ranked_rest
    
    def _enhance_with_rag(self, attractions: List[Dict], destination: str) -> List[Dict]:
        """Enhance attraction info with RAG insights"""
        
        enhanced = []
        for attr in attractions:
            name = attr.get('name', '')
            
            try:
                tips_query = f"tips for visiting {name} in {destination}"
                tips_results = self.vector_store.search(query=tips_query, n_results=1)

                rag_tip = None
                for doc in tips_results.get('documents', []):
                    if doc and name.lower() in doc.lower():
                        rag_tip = doc[:200]
                        break

                attr_copy = attr.copy()
                if rag_tip:
                    attr_copy['rag_tip'] = rag_tip
                
                enhanced.append(attr_copy)
            except:
                enhanced.append(attr.copy())
        
        return enhanced


# Create singleton instance
research_agent = ResearchAgent()
