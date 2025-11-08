from pydantic import BaseModel
from typing import List
from datetime import datetime
from .product_schema import ProductOut, ProductWithoutCategoryOut

class TransactionItemCreate(BaseModel):
    product_id: str
    product_name: str
    product_price: float
    quantity: int

class TransactionCreate(BaseModel):
    user_id: str
    total: float
    items: List[TransactionItemCreate]

class TransactionItemRead(BaseModel):
    id: str
    product_name: str
    product_price: float
    quantity: int
    product: ProductWithoutCategoryOut
    
    class Config:
        orm_mode = True

class TransactionRead(BaseModel):
    id: str
    user_id: str
    total: float
    created_at: datetime   
    items: List[TransactionItemRead]

    class Config:
        orm_mode = True
