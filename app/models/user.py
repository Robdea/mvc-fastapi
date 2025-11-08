import uuid
from sqlalchemy import Column, String, DateTime, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR  
from sqlalchemy.orm import relationship
from ..db.mysql_bd import Base
from ..utils.enums.rol import Rol 

class User(Base):
    __tablename__="users"
    
    id =  Column(CHAR(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(SAEnum(Rol), default=Rol.USER, nullable=False)  
    address = Column(String(180), nullable=False)
    register_time = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", back_populates="user",cascade="all, delete-orphan",lazy="selectin")

