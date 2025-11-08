from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from ..schemas.stripe_schema import PaymentRequest
from ..services.pay_services import PayServices
from ..utils.service_factory import service_factory


router = APIRouter(prefix="/pays", tags=["pays"])

@router.post("/")
async def pay_test(
    data: PaymentRequest,
    request: Request,
    service: PayServices = Depends(service_factory(PayServices))
):
    return await service.create_payment_intent(data, request)
    

