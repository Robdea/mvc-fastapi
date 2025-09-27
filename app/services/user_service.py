from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User

from ..schemas import user_schema
from ..utils import auth


async def create_user(
    user: user_schema.UserCreate,
    db: AsyncSession 
):
    db_user = User(
        name=user.name, 
        email=user.email,
        phone=user.phone,
        address=user.address, 
        hashed_password=auth.hash_password(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
