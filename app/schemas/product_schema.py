from pydantic import BaseModel, Field
from typing import Optional

from .category_schema import CategoryOut

    
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)  # debe ser > 0
    stock: int = Field(0, ge=0)      # debe ser >= 0

class ProductCreate(ProductBase):
    category_id:  Optional[str] = None

class ProductOut(ProductBase):
    id: str
    category: Optional[CategoryOut] = None  # relación expandida
    class Config:
        orm_mode = True


