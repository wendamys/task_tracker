"""
Task business logic
"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate


def get_task_or_404(
        task_id:int,
        db: Session,
):
    """
    Return task by id or raise 404
    """
    task = db.scalar(
        select(Task).where(Task.id == task_id)
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task