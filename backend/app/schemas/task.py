"""
Task schemas

Contains:
- Create schema
- Update schema
- Response schema
"""

from pydantic import BaseModel, Field
from datetime import datetime
from backend.app.enums.task_status import TaskStatus


class TaskCreate(BaseModel):
    """
    Schema for task creation
    """

    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str = Field(
        min_length=1,
        max_length=1000,
    )

    requester: str = Field(
        min_length=1,
        max_length=50,
    )

    assignee_id: int | None = None

class TaskUpdate(BaseModel):
    """
    Schema for update task
    All fields are optional
    """

    status: TaskStatus | None = None
    assignee_id: int | None = None


class TaskResponse(BaseModel):
    """
    Schema returned to clients
    """

    id: int
    title: str
    description: str
    status: TaskStatus
    requester: str

    assignee_id: int | None = None
    assignee_name: str | None = None

    created_at: datetime
    updated_at: datetime

class DeleteResponse(BaseModel):
    id: int
    message: str



