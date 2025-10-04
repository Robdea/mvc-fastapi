from sqlalchemy import Column, String, CHAR, Text
from sqlalchemy.orm import relationship
import uuid

from ..db.mysql_bd import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)

    # Relación con productos
    products = relationship("Product", back_populates="category")

