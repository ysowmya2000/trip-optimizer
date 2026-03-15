"""
Pydantic schemas for trip data models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import time


class Attraction(BaseModel):
    """Individual attraction/place."""
    name: str
    address: Optional[str] = None
    rating: float = 0.0
    user_ratings_total: int = 0
    types: List[str] = []
    location: Dict = {}
    place_id: Optional[str] = None
    price_level: int = 0
    relevance_score: float = 0.0


class Activity(BaseModel):
    """Single activity in itinerary."""
    time: str = Field(..., description="Time of activity (e.g., '9:00 AM')")
    activity_type: str = Field(..., description="Type: attraction, meal, travel, rest")
    name: str
    description: Optional[str] = None
    duration_minutes: int = 60
    attraction: Optional[Attraction] = None
    notes: Optional[str] = None


class DayPlan(BaseModel):
    """Plan for a single day."""
    day_number: int
    date: Optional[str] = None
    title: str = Field(..., description="Theme/title for the day")
    activities: List[Activity]
    total_attractions: int = 0
    estimated_cost: float = 0.0
    notes: Optional[str] = None


class Itinerary(BaseModel):
    """Complete trip itinerary."""
    destination: str
    trip_duration: int
    interests: List[str]
    days: List[DayPlan]
    total_attractions: int = 0
    estimated_total_cost: float = 0.0
    created_by: str = "Planning Agent"


class TripRequest(BaseModel):
    """Request to create a trip."""
    destination: str = Field(..., example="Tokyo, Japan")
    interests: List[str] = Field(..., example=["temples", "food", "culture"])
    trip_duration: int = Field(default=7, ge=1, le=30)
    budget: Optional[float] = Field(None, description="Budget amount")
    currency: Optional[str] = Field(default="USD", description="Currency code (USD, EUR, INR, etc.)")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")


class TripResponse(BaseModel):
    """Response containing trip itinerary."""
    success: bool
    trip_request: TripRequest
    itinerary: Optional[Itinerary] = None
    error: Optional[str] = None
