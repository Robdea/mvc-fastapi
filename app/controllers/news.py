from fastapi import APIRouter, Depends, UploadFile, File, Form
from ..schemas.news_schema import NewsOut
from ..services.news_service import NewsService
from ..utils.service_factory import service_factory


router = APIRouter(prefix="/news", tags=["news"])

@router.post("/")
async def create_new(
    service: NewsService = Depends(service_factory(NewsService)),
    data: str = Form(...),
    image: UploadFile = File(None)
):
    return await service.create_news(data, image)

@router.get("/", response_model=list[NewsOut])
async def get_all_news(
    service: NewsService = Depends(service_factory(NewsService)),
):
    return await service.get_all_news()