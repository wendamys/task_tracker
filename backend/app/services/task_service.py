"""
Task business logic
"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.task import Task
from backend.app.schemas.task import TaskCreate, TaskUpdate
from backend.app.models.user import User


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


def create_task(
        task_data: TaskCreate,
        db: Session,
) -> Task:
    """
    Create new task
    
    Args:
        task_data: validated request data
        db: database session
    
    Returns:
        Created Task ORM object
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

    return task


def update_task(
        task_id: int,
        task_data: TaskUpdate,
        db: Session,
) -> Task:
        """
        Update task

        Args:
            task_id: task identifier
            task_data: validated update data
            db: database session

        Returns:
            Update task
        """

        task = get_task_or_404(
            task_id,
            db,
        )

        if task_data.assignee_id is not None:
            user = db.scalar(
                select(User).where(
                    User.id == task_data.assignee_id
                )
            )

            if user is None:
                raise HTTPException(
                    status_code=400,
                    detail="User not found"
                )

            task.assignee_id = task_data.assignee_id

        if task_data.status is not None:
            task.status = task_data.status


        db.commit()
        db.refresh(task)

        return task


def delete_task(
        task_id: int,
        db: Session,
) -> None:
    """
    Delete task by id

    Args:
        task_id: task identifier
        db: database session
    """

    task = get_task_or_404(
        task_id,
        db,
    )

    db.delete(task)
    db.commit()