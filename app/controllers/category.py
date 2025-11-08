from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import mysql_bd
from ..schemas import category_schema
from ..services import category_service

router = APIRouter(prefix="/category", tags=["category"])

@router.get("/", response_model=list[category_schema.CategoryOut])
async def get_all(
    db: AsyncSession = Depends(mysql_bd.get_db)
):
   categories = await category_service.get_categories(db=db)
   return categories

@router.delete("/{category_id}")
async def delete(
    category_id: str,
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    return await category_service.delete_category(category_id, db) 

@router.get("/{category_id}", response_model=category_schema.CategoryOut)
async def get_by_id(
    category_id: str,
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    category = await category_service.get_category_by_id(category_id=category_id, db=db)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.patch("/{category_id}")
async def patch_category(
    category_id: str,
    data: str = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    category = await category_service.patch_category(category_id,data,db,image)
    return category
    

@router.post("/", response_model=category_schema.CategoryOut)
async def create_category(
    data: str = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    created_category = await category_service.create_category(data=data, db=db, image=image)
    return created_category


    


