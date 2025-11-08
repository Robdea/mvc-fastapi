import uuid
from sqlalchemy import Column, String, Float, Integer, CHAR, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.mysql_bd import Base

# Tabla principal de transacciones (ventas instantáneas)
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    user = relationship("User", back_populates="transactions", lazy="selectin")
    items = relationship(
        "TransactionItem", 
        back_populates="transaction", 
        cascade="all, delete-orphan",
        lazy="selectin"
    )

# Tabla de productos por transacción
class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(CHAR(36), ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(CHAR(36), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    product_name = Column(String(150), nullable=False)  # Guarda nombre al momento de la compra
    product_price = Column(Float, nullable=False)       # Guarda precio al momento de la compra
    quantity = Column(Integer, nullable=False, default=1)

    # Relaciones
    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product", lazy="selectin")
