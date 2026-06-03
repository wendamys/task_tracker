from app.models.task import Task
from app.schemas.task import TaskResponse

def task_to_response(
        task: Task,
) -> TaskResponse:
    """
    Convert ORM Task
    to API response schema
    """

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        requester=task.requester,
        assignee_name=(
            task.assignee.name
            if task.assignee
            else None
        ),
        created_at=task.created_at,
        updated_at=task.updated_at,
    )