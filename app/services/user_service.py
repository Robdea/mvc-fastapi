from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User

from ..schemas import user_schema
from ..utils import auth

class UserSerive: 
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_user(
        self,
        user: user_schema.UserCreate,
    ):
        db_user = User(
            name=user.name, 
            email=user.email,
            phone=user.phone,
            address=user.address, 
            hashed_password=auth.hash_password(user.password),
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def get_user_by_id(self, user_id: str):
        return await self.db.get(User, user_id)
    
    async def get_all_users(self):
        res = await self.db.execute(select(User))
        return res.scalars().all()
