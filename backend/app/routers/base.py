"""
Base router for root endpoints.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    """
    Root endpoint returns Hello World.
    
    Returns:
        Dict with welcome message
    """
    return {"message": "Hello World"}
