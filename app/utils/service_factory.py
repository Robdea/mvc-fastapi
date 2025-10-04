from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ..db.mysql_bd import get_db

def service_factory(ServiceClass: Type):
    def _get_service(db: AsyncSession = Depends(get_db)):
        return ServiceClass(db)
    return _get_service