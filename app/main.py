"""
Application entry point

Creates FastAPI application and registers routers
"""

from fastapi import FastAPI
from app.database.base import Base
from app.database.db import engine

app = FastAPI(
    title="Task Tracker",
    description="Simple task management system",
    version="1.0.0",
)

@app.on_event("startup")
def startup() -> None:
    """Create all database tables

    Currently, there are no models,
    but later table will be created here
    """
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict[str, str]:
    """
     Health check endpoint

    Returns:
        dict[str, str]: API status message
    """
    return {"message": "Task Tracker API is running"}