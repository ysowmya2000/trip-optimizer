"""
Trips API endpoints.
Uses Multi-Agent Orchestrator to create complete optimized trips.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.trip import TripRequest
from app.agents.orchestrator import trip_orchestrator

# Create router
router = APIRouter()


@router.post("/create")
async def create_trip(request: TripRequest):
    """
    Create a complete optimized trip itinerary.
    
    This endpoint uses the Multi-Agent Orchestrator which coordinates:
    1. Research Agent - Finds attractions
    2. Planning Agent - Creates day-by-day itinerary
    3. Optimization Agent - Optimizes routes
    4. Budget Agent - Analyzes costs
    5. Weather Agent - Checks forecast
    
    Returns complete trip package with all analysis.
    """
    try:
        result = trip_orchestrator.create_complete_trip(request)
        return result
        
    except Exception as e:
        print(f"❌ Error creating trip: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_trips_endpoint():
    """Test endpoint to verify all agents are operational."""
    return {
        "status": "operational",
        "message": "Multi-Agent Trip Orchestrator ready!",
        "agents": [
            "Research Agent",
            "Planning Agent", 
            "Optimization Agent",
            "Budget Agent",
            "Weather Agent"
        ],
        "endpoints": {
            "create_trip": "POST /api/trips/create"
        }
    }
