"""
Research API endpoints.
Provides endpoints to test the Research Agent.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.research_agent import research_agent

# Create router
router = APIRouter()


class ResearchRequest(BaseModel):
    """Request model for destination research."""
    destination: str
    interests: List[str]
    trip_duration: int = 7
    
    class Config:
        json_schema_extra = {
            "example": {
                "destination": "Tokyo, Japan",
                "interests": ["temples", "food", "shopping"],
                "trip_duration": 5
            }
        }


class QuickSummaryRequest(BaseModel):
    """Request model for quick destination summary."""
    destination: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "destination": "Paris, France"
            }
        }


@router.post("/research")
async def research_destination(request: ResearchRequest):
    """
    Research a destination and find attractions.
    
    This endpoint uses the Research Agent to:
    1. Generate search queries based on interests
    2. Search Google Places API
    3. Rank and return relevant attractions
    """
    try:
        result = research_agent.research_destination(
            destination=request.destination,
            interests=request.interests,
            trip_duration=request.trip_duration
        )
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summary")
async def get_destination_summary(request: QuickSummaryRequest):
    """
    Get a quick AI-generated summary about a destination.
    """
    try:
        summary = research_agent.get_quick_summary(request.destination)
        return {
            "success": True,
            "destination": request.destination,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_research_agent():
    """
    Test endpoint to verify Research Agent is working.
    """
    return {
        "agent": "Research Agent",
        "status": "operational",
        "message": "Research Agent is ready to find attractions!",
        "endpoints": {
            "research": "POST /api/research/research",
            "summary": "POST /api/research/summary"
        }
    }
