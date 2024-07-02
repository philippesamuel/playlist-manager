from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_active_user
from app.models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
