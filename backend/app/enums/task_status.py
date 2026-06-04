"""
Task status enum
"""

from enum import Enum

class TaskStatus(str, Enum):
    """
    Available task statuses
    """

    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"