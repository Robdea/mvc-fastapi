from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.user import User
from ..utils import auth


async def login(username: str, password: str, db: AsyncSession):
    res = await db.execute(select(User).where(User.name == username))
    user = res.scalars().first()
    
    if not user or not auth.verify_password(password, user.hashed_password):
        return None

    token = auth.create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = auth.create_refresh_token({"sub": str(user.id)})

    return {
        "message": "Login exitoso",
        "user": {"id": user.id, "username": user.name, "email": user.email},
        "access_token": token,
        "refresh_token": refresh_token
    }