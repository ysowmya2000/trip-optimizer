"""
Knowledge Base API endpoints.
Allows querying the RAG-based travel knowledge base.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.db.vector_store import travel_kb

router = APIRouter()


class KnowledgeQuery(BaseModel):
    """Query model for knowledge base search."""
    query: str
    destination: Optional[str] = None
    n_results: int = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "best temples in Tokyo",
                "destination": "Tokyo",
                "n_results": 3
            }
        }


class AddKnowledgeRequest(BaseModel):
    """Request to add knowledge to the base."""
    text: str
    destination: str
    category: str
    tip_type: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Visit the fish market early at 5 AM for the tuna auction",
                "destination": "Tokyo",
                "category": "food",
                "tip_type": "insider_tip"
            }
        }


@router.post("/search")
async def search_knowledge(query: KnowledgeQuery):
    """
    Search the travel knowledge base using semantic search.
    """
    filter_metadata = None
    if query.destination:
        filter_metadata = {"destination": query.destination}
    
    results = travel_kb.search(
        query=query.query,
        n_results=query.n_results,
        filter_metadata=filter_metadata
    )
    
    return {
        "success": True,
        "query": query.query,
        "results": [
            {
                "text": doc,
                "metadata": meta,
                "relevance": 1 - dist
            }
            for doc, meta, dist in zip(
                results["documents"],
                results["metadatas"],
                results["distances"]
            )
        ]
    }


@router.post("/add")
async def add_knowledge(request: AddKnowledgeRequest):
    """
    Add new knowledge to the travel knowledge base.
    """
    import time
    
    travel_kb.add_knowledge(
        texts=[request.text],
        metadatas=[{
            "destination": request.destination,
            "category": request.category,
            "tip_type": request.tip_type
        }],
        ids=[f"user_{int(time.time())}"]
    )
    
    return {
        "success": True,
        "message": "Knowledge added successfully",
        "total_documents": travel_kb.collection.count()
    }


@router.get("/tips/{destination}")
async def get_destination_tips(destination: str, limit: int = 5):
    """
    Get travel tips for a specific destination.
    """
    tips = travel_kb.get_tips_for_destination(destination, n_results=limit)
    
    return {
        "success": True,
        "destination": destination,
        "tips": tips,
        "count": len(tips)
    }


@router.get("/stats")
async def get_knowledge_stats():
    """
    Get statistics about the knowledge base.
    """
    return {
        "total_documents": travel_kb.collection.count(),
        "collections": ["travel_knowledge"],
        "rag_enabled": True
    }
