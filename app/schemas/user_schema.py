from pydantic import BaseModel, EmailStr
from ..utils.enums.rol import Rol 

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    address: str


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: str
    role: Rol

    class Config:
        orm_mode = True