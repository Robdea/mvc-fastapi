from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import user_service

from ..schemas import user_schema
from ..db import mysql_bd

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/")
async def create_user(
    user: user_schema.UserCreate,
    db: AsyncSession = Depends(mysql_bd.get_db)
): 
    created_user = await user_service.create_user(user=user, db=db)
    
    return created_user 
