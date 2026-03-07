"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import research, trips, knowledge

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered travel planning with RAG, multi-agent coordination, and real-time optimization",
    version="2.0.0",
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
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to TripOptimizer API v2.0",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "features": [
            "5 AI Agents (Research, Planning, Optimization, Budget, Weather)",
            "Multi-Agent Orchestration",
            "RAG-based Knowledge System",
            "Vector Database (ChromaDB)",
            "Semantic Search"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "agents_active": 5,
        "rag_enabled": True
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"🚀 {settings.APP_NAME} v2.0 starting up...")
    print(f"📝 Debug mode: {settings.DEBUG}")
    print(f"📚 API docs available at: http://localhost:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"👋 {settings.APP_NAME} shutting down...")
