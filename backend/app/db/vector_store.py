"""
Vector Store for RAG-based travel recommendations.
Uses ChromaDB to store and retrieve travel knowledge.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os


class TravelKnowledgeBase:
    """Vector store for travel tips, reviews, and local knowledge."""
    
    def __init__(self, persist_directory: str = "./data/chroma"):
        """Initialize ChromaDB vector store."""
        self.persist_directory = persist_directory
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="travel_knowledge",
            metadata={"description": "Travel tips, reviews, and local knowledge"}
        )
        
        print(f"📚 Vector store initialized: {self.collection.count()} documents")
    
    def add_knowledge(
        self, 
        texts: List[str], 
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ):
        """
        Add travel knowledge to vector store.
        
        Args:
            texts: List of text content (tips, reviews, etc.)
            metadatas: List of metadata dicts (destination, category, etc.)
            ids: Optional list of unique IDs
        """
        if not ids:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Added {len(texts)} documents to knowledge base")
    
    def search(
        self, 
        query: str, 
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Search for relevant travel knowledge.
        
        Args:
            query: Search query (e.g., "best temples in Tokyo")
            n_results: Number of results to return
            filter_metadata: Optional metadata filter (e.g., {"destination": "Tokyo"})
            
        Returns:
            Search results with documents, distances, and metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata
        )
        
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }
    
    def get_tips_for_destination(self, destination: str, n_results: int = 5) -> List[str]:
        """Get travel tips for a specific destination."""
        results = self.search(
            query=f"travel tips for {destination}",
            n_results=n_results,
            filter_metadata={"destination": destination}
        )
        return results["documents"]
    
    def get_local_recommendations(self, destination: str, interest: str) -> List[str]:
        """Get local recommendations based on interests."""
        results = self.search(
            query=f"{interest} in {destination}",
            n_results=3
        )
        return results["documents"]
    
    def seed_initial_data(self):
        """Seed vector store with initial travel knowledge."""
        
        # Sample travel knowledge for popular destinations
        knowledge_data = [
            # Tokyo
            {
                "text": "Visit Senso-ji Temple early morning (6-7 AM) to avoid crowds. The nearby Nakamise shopping street opens around 9 AM with traditional snacks and souvenirs.",
                "metadata": {"destination": "Tokyo", "category": "temples", "tip_type": "timing"}
            },
            {
                "text": "For authentic ramen, try small local shops in Shinjuku or Ikebukuro. Look for places with lines of locals - that's always a good sign.",
                "metadata": {"destination": "Tokyo", "category": "food", "tip_type": "local_favorite"}
            },
            {
                "text": "Purchase a Suica or Pasmo card for easy metro travel. Tokyo's public transit is efficient but can be confusing - download Google Maps offline.",
                "metadata": {"destination": "Tokyo", "category": "transportation", "tip_type": "practical"}
            },
            
            # Paris
            {
                "text": "Book Eiffel Tower tickets online weeks in advance. Visit at sunset for best photos and smaller crowds on the upper levels.",
                "metadata": {"destination": "Paris", "category": "landmarks", "tip_type": "timing"}
            },
            {
                "text": "Skip touristy cafes near attractions. Head to local neighborhoods like Le Marais or Canal Saint-Martin for authentic French cafe culture.",
                "metadata": {"destination": "Paris", "category": "food", "tip_type": "local_favorite"}
            },
            {
                "text": "Museums are free on first Sunday of each month but expect huge crowds. Consider Paris Museum Pass for skip-the-line access.",
                "metadata": {"destination": "Paris", "category": "museums", "tip_type": "money_saving"}
            },
            
            # Barcelona
            {
                "text": "La Sagrada Familia requires advance booking - tickets sell out weeks ahead. Visit early morning for best light in the interior.",
                "metadata": {"destination": "Barcelona", "category": "architecture", "tip_type": "timing"}
            },
            {
                "text": "Avoid restaurants on La Rambla - overpriced and touristy. Explore El Born or Gracia neighborhoods for authentic tapas.",
                "metadata": {"destination": "Barcelona", "category": "food", "tip_type": "local_favorite"}
            },
            {
                "text": "Barcelona beaches get crowded after 11 AM. Visit early or head to quieter beaches like Bogatell instead of Barceloneta.",
                "metadata": {"destination": "Barcelona", "category": "beaches", "tip_type": "timing"}
            },
            
            # General tips
            {
                "text": "Street food markets offer authentic local cuisine at lower prices than restaurants. Look for markets popular with locals, not just tourists.",
                "metadata": {"destination": "general", "category": "food", "tip_type": "money_saving"}
            },
            {
                "text": "Free walking tours are available in most major cities. Tip-based, usually 10-15 euros per person, great for orientation on first day.",
                "metadata": {"destination": "general", "category": "tours", "tip_type": "money_saving"}
            },
            {
                "text": "Download offline maps and save important addresses before traveling. Public WiFi isn't always reliable in tourist areas.",
                "metadata": {"destination": "general", "category": "practical", "tip_type": "practical"}
            }
        ]
        
        texts = [item["text"] for item in knowledge_data]
        metadatas = [item["metadata"] for item in knowledge_data]
        ids = [f"seed_{i}" for i in range(len(texts))]
        
        self.add_knowledge(texts, metadatas, ids)


# Create global instance
travel_kb = TravelKnowledgeBase()

# Seed initial data if empty
if travel_kb.collection.count() == 0:
    print("📚 Seeding travel knowledge base with initial data...")
    travel_kb.seed_initial_data()
