from fastapi import APIRouter, Depends
from ..utils.service_factory import service_factory
from ..services.user_service import UserSerive
from ..schemas import user_schema

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/")
async def create_user(
    user: user_schema.UserCreate,
    service: UserSerive = Depends(service_factory(UserSerive))
): 
    created_user = await service.create_user(user=user)
    return created_user 
@router.get("/{user_id}")
async def get_user(
    user_id: str,
    service: UserSerive = Depends(service_factory(UserSerive))
):
    return await service.get_user_by_id(user_id)

@router.get("/", response_model=list[user_schema.UserOut])
async def get_all_user(
    service: UserSerive = Depends(service_factory(UserSerive))
):
    return await service.get_all_users()