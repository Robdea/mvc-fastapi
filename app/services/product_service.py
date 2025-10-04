from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product import Product
from sqlalchemy.orm import selectinload
import uuid

from ..models.cactegory import Category
from sqlalchemy.future import select
from pathlib import Path
import json
import shutil

from ..schemas import product_schema

UPLOAD_DIR = Path("media/product")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_products(self):
        res = await self.db.execute(
            select(Product).options(selectinload(Product.category))
        )
        products = res.scalars().all()
        return products

    async def get_products_by_category(self, category_id: str):
        res = await self.db.execute(select(Category).where(Category.id == category_id))
        category = res.scalars().first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        res = await self.db.execute(select(Product).where(Product.category_id == category_id))
        return res.scalars().all()


    async def get_product_by_id(self, product_id: str):
        res = await self.db.execute(select(Product).where(Product.id == product_id))
        producto = res.scalars().first()
        if not producto:
            raise HTTPException(status_code=404, detail="Product not found")
        return producto

    async def delete_product(
        self, product_id: str
    ):
        product = await self.get_product_by_id(product_id)
        
        await self.db.delete(product)
        await self.db.commit()
        
        return {"message": "Product was delete"}

    async def create_product(
        self,
        data: str,
        image: str = None
    ):
        category = None

        parsed = json.loads(data)
        product = product_schema.ProductCreate(**parsed) 

        image_path = None

        if image:
            ext = Path(image.filename).suffix
            filename = f"{uuid.uuid4()}{ext}"
            image_path = UPLOAD_DIR / filename
            with image_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        
      
        if product.category_id:
            res = await self.db.execute(
                select(Category).where(Category.id == product.category_id)
            )
        
            category = res.scalars().first()
            if not category:
                raise HTTPException(status_code=404, detail="Product not found")
        
        new_product = Product(
            name = product.name,
            description = product.description,
            price = product.price,
            stock = product.stock,
            category=category,
            image = str(image_path.as_posix()) if image_path else None
        )
        
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product


