"""
Application entry point

Creates FastAPI application and registers routers
"""

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependecies import get_db
from app.database.db import engine
from app.database.base import Base

from app.schemas.task import TaskCreate, TaskResponse


# IMPORTANT:
# Import models before create_all()
# so SQLAlchemy knows about them
from app.models.task import Task
from app.models.user import User


app = FastAPI(
    title="Task Tracker",
    description="Simple task management system",
    version="1.0.0",
)

@app.on_event("startup")
def startup() -> None:
    """Drop and Create all database tables

    Currently, there are no models,
    but later table will be created here
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root() -> dict[str, str]:
    """
     Health check endpoint

    Returns:
        dict[str, str]: API status message
    """
    return {"message": "Task Tracker API is running"}

@app.post("/tasks")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create new task
    :param task_data:
    :param db:
    :return:
    """

    task = Task(
        title=task_data.title,
        description=task_data.description,
        requester=task_data.requester,
        assignee_id=task_data.assignee_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "message": "Task created",
    }

@app.get(
    "/tasks",
    response_model=list[TaskResponse],
)
def get_tasks(
        status: str | None = None,
        db: Session = Depends(get_db)
):
    """
    Get tasks list

    Optional filtering by status
    """

    query = select(Task)

    if status is not None:
        query = query.where(Task.status == status)

    tasks = db.scalars(query).all()

    return tasks

















