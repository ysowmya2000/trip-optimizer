"""
Trips API endpoints.
Combines Research Agent + Planning Agent to create complete trip itineraries.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.trip import TripRequest, TripResponse, Itinerary
from app.agents.research_agent import research_agent
from app.agents.planning_agent import planning_agent

# Create router
router = APIRouter()


@router.post("/create", response_model=TripResponse)
async def create_trip(request: TripRequest):
    """
    Create a complete trip itinerary.
    
    This endpoint orchestrates:
    1. Research Agent - finds attractions
    2. Planning Agent - creates day-by-day itinerary
    
    Returns a complete trip plan with daily schedules.
    """
    try:
        print(f"\n🚀 Creating trip to {request.destination}...")
        
        # Step 1: Research attractions
        print("Step 1: Researching attractions...")
        research_result = research_agent.research_destination(
            destination=request.destination,
            interests=request.interests,
            trip_duration=request.trip_duration
        )
        
        attractions = research_result.get('top_attractions', [])
        
        if not attractions:
            return TripResponse(
                success=False,
                trip_request=request,
                error="No attractions found for this destination"
            )
        
        # Step 2: Create itinerary
        print("Step 2: Creating itinerary...")
        itinerary = planning_agent.create_itinerary(
            destination=request.destination,
            interests=request.interests,
            attractions=attractions,
            trip_duration=request.trip_duration,
            budget=request.budget
        )
        
        print(f"✅ Trip created successfully!")
        
        return TripResponse(
            success=True,
            trip_request=request,
            itinerary=itinerary
        )
        
    except Exception as e:
        print(f"❌ Error creating trip: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_trips_endpoint():
    """Test endpoint to verify trips API is working."""
    return {
        "status": "operational",
        "message": "Trips API is ready!",
        "endpoints": {
            "create_trip": "POST /api/trips/create"
        }
    }
