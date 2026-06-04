"""
Task router
"""

from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db

from backend.app.models.task import Task

from backend.app.schemas.task import (TaskCreate,
                                      TaskResponse,
                                      TaskUpdate,
                                      DeleteResponse,
                                      )

from backend.app.services.task_mapper import task_to_response
from backend.app.services.task_service import (
                                                get_task_or_404,
                                                create_task as create_task_service,
                                                update_task as update_task_service,
                                                delete_task as delete_task_service,
                                                )


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("",
             response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create new taska
    """

    task = create_task_service(
        task_data,
        db
    )

    return task_to_response(task)


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
    "/{id}",
    response_model=TaskResponse,
)
def get_task(
        id: int,
        db: Session = Depends(get_db),
):
    """
    Get task by ID
    """

    task = get_task_or_404(
        id,
        db,
    )

    return task_to_response(task)


@router.put(
    "/{id}",
    response_model=TaskResponse,
)
def update_task(
        id: int,
        task_data: TaskUpdate,
        db: Session = Depends(get_db)
):
    """
    Update task
    """

    task = update_task_service(
        id,
        task_data,
        db,
    )

    return task_to_response(task)


@router.delete(
    "/{id}",
    response_model=DeleteResponse)
def delete_task(
        id: int,
        db: Session = Depends(get_db)
):
    """
    Delete task by ID
    """

    delete_task_service(
        id,
        db,
    )

    return {
        "id": id,
        "message": "Task deleted",
    }