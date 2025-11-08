from fastapi import UploadFile,HTTPException
import json
from sqlalchemy.exc import IntegrityError
from ..models.news import News
from ..schemas.news_schema import NewsCreate, NewsUpdate
import json
from sqlalchemy.future import select
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from pathlib import Path

UPLOAD_DIR = Path("media/news")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class NewsService():
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_news(
        self, 
        data: str, 
        image: UploadFile = None
    ):
        parsed = json.loads(data)
        news_data = NewsCreate(**parsed) 

        image_path = None
        if image:
            ext = Path(image.filename).suffix
            filename = f"{uuid.uuid4()}{ext}"
            image_path = UPLOAD_DIR / filename
            with image_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
                
        new_db = News(
            title=news_data.title,
            content=news_data.content,
            image_url=str(image_path.as_posix()) if image_path else None
        )
        
        self.db.add(new_db)
        await self.db.commit()
        await self.db.refresh(new_db)

        return new_db
    
    async def delete_new(
        self,
        new_id: int
    ):
        res = await self.db.execute(select(News).where(News.id == new_id))
        new =res.scalars().first()
        
        await self.db.delete(new)
        await self.db.commit()
        
        return {"message": "New was delete"}
        

    async def update_news(
        self,
        news_id: int,
        data: str,
        image_url: UploadFile = None
    ):
        # Buscar noticia existente
        res = await self.db.execute(select(News).where(News.id == news_id))
        news = res.scalars().first()
        if not news:
            raise HTTPException(status_code=404, detail="News not found")

        # Parsear los datos entrantes
        parsed = json.loads(data)
        update_data = NewsUpdate(**parsed)  # schema de actualización

        # Si viene una nueva imagen
        if image_url:
            # Eliminar la imagen anterior si existe
            if news.image_url and Path(news.image_url).exists():
                Path(news.image_url).unlink()

            # Guardar la nueva imagen
            ext = Path(image_url.filename).suffix
            filename = f"{uuid.uuid4()}{ext}"
            image_path = UPLOAD_DIR / filename
            with image_path.open("wb") as buffer:
                shutil.copyfileobj(image_url.file, buffer)
            news.image_url = str(image_path.as_posix())

        # Actualizar solo los campos enviados
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(news, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(news)
            return news
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Error updating news")
        
    async def get_all_news(self):
        res = await self.db.execute(select(News))
        
        news = res.scalars().all()
        return news
        
        