"""
Main entry point for the FastAPI application.
"""
import uvicorn

from app.api import app
from app.database.init_db import init_db

# Initialize database
init_db()

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
