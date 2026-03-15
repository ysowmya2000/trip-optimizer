from fastapi import APIRouter, HTTPException
from app.schemas.trip import TripRequest
from app.agents.orchestrator import trip_orchestrator

router = APIRouter()

@router.post("/create")
async def create_trip(request: TripRequest):
    """Create a complete trip using all agents"""
    try:
        print(f"\n📥 Received request:")
        print(f"   Destination: {request.destination}")
        print(f"   Trip Duration: {request.trip_duration}")
        
        result = await trip_orchestrator.create_trip(request.dict())
        
        # Check if budget too low
        if not result.get('success', True):
            if result.get('error') == 'BUDGET_TOO_LOW':
                raise HTTPException(
                    status_code=400,
                    detail=result
                )
        
        return result
        
    except HTTPException:
        # Re-raise HTTPException as-is (don't catch and convert to 500)
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
