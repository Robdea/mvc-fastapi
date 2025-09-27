from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from ..db import mysql_bd
from ..services import auth_services

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    resp: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    user_data = await auth_services.login(form_data.username, form_data.password, db)
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
