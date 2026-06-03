"""
User router
"""

from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.schemas.user import UserResponse
from app.models.user import User
from app.database.dependencies import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
        db: Session = Depends(get_db)
):
    """
    Get all users
    """

    users = db.scalars(
        select(User)
    ).all()

    return users
