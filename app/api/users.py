from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db_session, get_email_service
from app.schemas.user_schemas import UserCreate

router = APIRouter()

@router.post("/users/")
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    email_service = get_email_service()
    user = await UserService.create(db, user_data.dict(), email_service)
    return user

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db_session)):
    user = await UserService.get_by_id(db, user_id)
    return user
