from fastapi import UploadFile
import json
from ..models.news import News
from ..schemas.news_schema import NewsCreate
import json
from sqlalchemy.future import select
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from pathlib import Path
from fastapi import UploadFile

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
    
    async def get_all_news(self):
        res = await self.db.execute(select(News))
        
        news = res.scalars().all()
        return news
        
        