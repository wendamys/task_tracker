"""
Application entry point

Creates FastAPI application and registers routers
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.db import engine
from app.database.base import Base

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.user import UserResponse

from app.services.task_mapper import task_to_response


# IMPORTANT:
# Import models before create_all()
# so SQLAlchemy knows about them
from app.models.task import Task
from app.models.user import User

from app.routers.task_router import router as task_router
from app.routers.user_router import router as user_router



app = FastAPI(
    title="Task Tracker",
    description="Simple task management system",
    version="1.0.0",
)

app.include_router(task_router)
app.include_router(user_router)

@app.on_event("startup")
def startup() -> None:
    """Drop and Create all database tables

    Currently, there are no models,
    but later table will be created here
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        db.add_all(
            [
                User(
                    name="Alex",
                    email="alex@example.ru"
                ),
                User(
                    name="John",
                    email="john@yandex.ru"
                ),
            ]
        )
        db.commit()

@app.get("/")
def root() -> dict[str, str]:
    """
     Health check endpoint

    Returns:
        dict[str, str]: API status message
    """
    return {"message": "Task Tracker API is running"}











