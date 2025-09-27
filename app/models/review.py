from sqlalchemy import Column, CHAR,  Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..db.mysql_bd import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    product_id = Column(CHAR(36), ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # por ejemplo 1 a 5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    product = relationship("Product", back_populates="reviews")
    user = relationship("User")
    