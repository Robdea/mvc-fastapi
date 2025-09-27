from fastapi import FastAPI
from .db.mysql_bd import Base, engine
from .controllers.auth import router as auth_router
from .controllers.user import router as user_router
from .controllers.category import router as category_router
from .controllers.product import router as product_router

app = FastAPI(title="Ecommerce API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
        
# @app.on_event
