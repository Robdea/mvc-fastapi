from sqlalchemy import Column, String, CHAR, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
import uuid

from ..db.mysql_bd import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    image = Column(String(255), nullable=True)
    category_id = Column(CHAR(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    # Relaciones
    category = relationship("Category", back_populates="products", lazy="selectin")
    reviews = relationship("Review", back_populates="product")
