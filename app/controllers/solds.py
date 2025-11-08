from fastapi import APIRouter, Depends
from ..services.sold_service import SoldService
from ..utils.service_factory import service_factory
from ..schemas.transaction_schema import TransactionRead

router = APIRouter(prefix="/solds", tags=["solds"])

@router.get("/")
async def pay_test(
    service: SoldService = Depends(service_factory(SoldService))
):
    return await service.get_all()
    

@router.get("/{user_id}", response_model=list[TransactionRead])
async def pay_test(
    user_id: str,
    service: SoldService = Depends(service_factory(SoldService))
):
    return await service.get_by_id(user_id)
    

