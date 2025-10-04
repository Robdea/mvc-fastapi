from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..services.auth_services import AuthService
from ..utils.service_factory import service_factory
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    resp: Response,
    service: AuthService = Depends(service_factory(AuthService)),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_data = await service.login(form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    # Asumiendo que user_data contiene access_token y refresh_token
    resp.set_cookie(
        key="access_token",
        value=user_data["access_token"],
        httponly=True,
        secure=True,         # poner False si estás en HTTP local
        samesite="strict",
        max_age=60*15,       # 15 minutos
        path="/"
    )

    resp.set_cookie(
        key="refresh_token",
        value=user_data["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60*60*24*7,  # 7 días
        path="/"
    )
    return {"message": "Login exitoso", "user": user_data["user"]}

@router.post("/refresh")
async def refresh(
    request: Request, 
    response: Response,
    service: AuthService = Depends(service_factory(AuthService))
):
    refresh = await service.refresh_token(request, response)
    return refresh

@router.post("/me")
async def get_me(
    request: Request,
    service: AuthService = Depends(service_factory(AuthService))
):
    user = await service.get_me(request)
    return user

@router.post("/logout")
async def logout(resp: Response):
    resp.delete_cookie("access_token", path="/")
    resp.delete_cookie("refresh_token", path="/")
    return {"message": "Sesión cerrada correctamente"}