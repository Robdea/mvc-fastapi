from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsOut(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
        
class NewsCreate(BaseModel):
    title: str
    content: str
