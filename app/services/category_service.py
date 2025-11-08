from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.cactegory import Category
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from ..schemas import category_schema
from pathlib import Path
import os
from fastapi import UploadFile
import uuid
import shutil
import json

UPLOAD_DIR = Path("media/category")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def create_category(
    data: str,
    db: AsyncSession,
    image: UploadFile = None
    ):
    parsed = json.loads(data)
    category = category_schema.CategoryCreate(**parsed) 
    
    image_path = None

    if image:
        ext = Path(image.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        image_path = UPLOAD_DIR / filename
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    new_category = Category(
        name=category.name,
        description=category.description,
        image=str(image_path.as_posix()) if image_path else None
    )
    db.add(new_category)
    try:
        await db.commit()
        await db.refresh(new_category)
        return new_category
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Category name already exists")


async def get_category_by_id(category_id: str, db: AsyncSession):
    res = await db.execute(select(Category).where(Category.id == category_id))
    category = res.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
# delete

async def delete_category(
    category_id: str,
    db: AsyncSession
):
   category = await get_category_by_id(category_id, db)
   
   if category.image:
       image_path = Path(category.image)
       
       if image_path.exists():
            try:
                os.remove(image_path)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"No se pudo eliminar la imagen: {str(e)}"
                )
                
   await db.delete(category)
   await db.commit()
   
   return {"message": "Category deleted successfully"}

# update
async def patch_category(
    category_id: str,
    data: str,
    db: AsyncSession,
    image: UploadFile = None
):
    parsed = json.loads(data)
    update_data = category_schema.CategoryUpdate(**parsed)

    # Buscar categoría existente
    res = await db.execute(select(Category).where(Category.id == category_id))
    category = res.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Manejo de imagen
    if image:
        # Eliminar imagen anterior si existía
        if category.image and Path(category.image).exists():
            Path(category.image).unlink()

        # Guardar nueva imagen
        ext = Path(image.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        image_path = UPLOAD_DIR / filename
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        category.image = str(image_path.as_posix())

    # Actualizar solo los campos enviados
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    try:
        await db.commit()
        await db.refresh(category)
        return category
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Category name already exists")
  
async def get_categories(
    db: AsyncSession
):
    res = await db.execute(select(Category))
    
    categories = res.scalars().all()
    return categories