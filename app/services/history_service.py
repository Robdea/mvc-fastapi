
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.history_sold import Transaction

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_transactions(self):
        result = await self.db.execute(select(Transaction))
        transactions = result.scalars().unique().all()
        return transactions