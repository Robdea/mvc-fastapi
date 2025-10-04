from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    product_id: str
    quantity: int

class TransactionRequest(BaseModel):
    user_id: str
    items: List[Item]

class Transaction(BaseModel):
    id: str
    user_id: str
    items: List[Item]
    total: float
    status: str  # pending, paid, cancelled
