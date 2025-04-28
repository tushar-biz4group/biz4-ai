"""
Main FastAPI application instance and configuration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, base
from app.database.init_db import init_db

# Initialize database tables
init_db()

# Create FastAPI app
app = FastAPI(
    title="Biz4AI API",
    description="Backend API for Biz4AI application",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefix
app.include_router(base.router)
app.include_router(auth.router, prefix=settings.API_V1_STR)

# Add health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Dict with status
    """
    return {"status": "ok"}
