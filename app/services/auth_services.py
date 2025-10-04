from datetime import timedelta
from fastapi import HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..utils import auth


class AuthService: 
    def __init__(self, db: AsyncSession):
        self.db=db
    
    async def login(self,username: str, password: str):
        res = await self.db.execute(select(User).where(User.name == username))
        user = res.scalars().first()
        
        if not user or not auth.verify_password(password, user.hashed_password):
            return None

        token = auth.create_access_token(
            {"sub": str(user.id)},
            expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = auth.create_refresh_token({"sub": str(user.id)})

        return {
            "message": "Login exitoso",
            "user": {"id": user.id, "username": user.name, "email": user.email},
            "access_token": token,
            "refresh_token": refresh_token
        }
    
    async def refresh_token(
        self,
        request: Request,
        response: Response
    ):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

        payload = auth.decoe_access_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido o expirado")

        user_id = payload.get("sub")

        # Crear un nuevo access token
        new_access_token = auth.create_access_token(
            {"sub": user_id},
            expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=60*15, # 15 minutos
            path="/"
        )

        return {"message": "Token refrescado"}
    
    async def get_me(
        self, 
        request: Request
    ):
        token = request. cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token")
        payload = auth.decoe_access_token(token)
        if not payload:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        res = await self.db.execute(select(User).where(User.id==user_id))
        user = res.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        return {"id": user.id, "username": user.name, "email": user.email}
