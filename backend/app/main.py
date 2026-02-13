"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered travel itinerary planning with real-time optimization",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS middleware - allows frontend to call our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to TripOptimizer API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME
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
