"""
Task router
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.task import Task
from app.models.user import User

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

from app.services.task_mapper import task_to_response
from app.services.task_service import get_task_or_404


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create new task
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

@router.get(
    "",
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

    return [
        task_to_response(task)
        for task in tasks
    ]

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
):
    """
    Get task by ID
    """

    query = select(Task).where(
        Task.id == task_id
    )

    task = get_task_or_404(
        task_id,
        db,
    )

    return task_to_response(task)

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
        task_id: int,
        task_data: TaskUpdate,
        db: Session = Depends(get_db)
):
    """
    Update task
    """

    task = get_task_or_404(
        task_id,
        db,
    )

    if task_data.status is not None:
        task.status = task_data.status

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

    db.commit()
    db.refresh(task)

    return task_to_response(task)


@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    """
    Delete task by ID
    """

    task = get_task_or_404(
        task_id,
        db,
    )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted",
        "id": task_id,
    }