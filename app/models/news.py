from sqlalchemy import Column, String, Integer, Text, DateTime
import datetime

from ..db.mysql_bd import Base

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(255))  # Aquí guardaremos la ruta de la imagen
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
