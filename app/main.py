from fastapi import FastAPI
from .db.mysql_bd import Base, engine
from .controllers.auth import router as auth_router
from .controllers.user import router as user_router
from .controllers.category import router as category_router
from .controllers.news import router as news_router
from .controllers.product import router as product_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Ecommerce API")
app.mount("/media", StaticFiles(directory="media"), name="media")

origins = ["http://127.0.0.1:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(news_router)
app.include_router(category_router)
app.include_router(product_router)
        
# @app.on_event
