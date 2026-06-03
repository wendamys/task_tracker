"""
Task schemas

Contains:
- Create schema
- Update schema
- Response schema
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum


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

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
    )

    status: str | None = Field(
        default=None,
        max_length=50,
    )

class TaskResponse(BaseModel):
    """
    Schema returned to clients
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    title: str
    description: str
    status: str
    requester: str
    assignee_id: int | None
    created_at: datetime
    updated_at: datetime

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"