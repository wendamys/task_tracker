"""
User schemas
"""

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """
    User response schema
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    email: str