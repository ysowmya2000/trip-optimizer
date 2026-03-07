"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import research, trips

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered travel itinerary planning with real-time optimization using 5 specialized agents",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to TripOptimizer API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "agents": [
            "Research Agent",
            "Planning Agent",
            "Optimization Agent", 
            "Budget Agent",
            "Weather Agent"
        ],
        "orchestrator": "Multi-Agent Orchestrator"
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "agents_active": 5
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"🚀 {settings.APP_NAME} starting up...")
    print(f"📝 Debug mode: {settings.DEBUG}")
    print(f"📚 API docs available at: http://localhost:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"👋 {settings.APP_NAME} shutting down...")
