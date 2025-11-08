from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.item_schema import Item 
from ..models.history_sold import Transaction
from ..models.user import User
from sqlalchemy.orm import selectinload

class SoldService():
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_all(
        self
    ):
        res = await self.db.execute(select(Transaction))
        solds = res.scalars().all()
        return solds
    
    async def get_by_id(self, user_id: str):
        query = (
            select(Transaction)
            .options(selectinload(Transaction.items))  # 🔹 carga los items
            .where(Transaction.user_id == user_id)
        )
        res = await self.db.execute(query)
        transactions = res.scalars().unique().all()  # 🔹 usa .unique() para evitar duplicados
        return transactions