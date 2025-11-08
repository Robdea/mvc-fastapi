from fastapi import  HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product import Product
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from uuid import UUID
import uuid 
from ..utils.response_wrapper import api_response

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
            raise HTTPException(status_code=404, detail="product not found by only id")
        return producto

    async def delete_product(
        self, product_id: str
    ):
        product = await self.get_product_by_id(product_id)
        
        await self.db.delete(product)
        await self.db.commit()
        
        return {"message": "Product was delete"}
    
    
    async def update_product(
        self,
        product_id: str,
        data: str,
        image: UploadFile = None
    ):
        
    # Buscar producto existente
        res = await self.db.execute(select(Product).where(Product.id == product_id))
        product = res.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Parsear datos del formulario
        parsed = json.loads(data)
        update_data = product_schema.ProductUpdate(**parsed)

        # Si viene una nueva imagen
        if image:
            # Eliminar la imagen anterior si existe
            if product.image and Path(product.image).exists():
                Path(product.image).unlink()

            # Guardar nueva imagen
            ext = Path(image.filename).suffix
            filename = f"{uuid.uuid4()}{ext}"
            image_path = UPLOAD_DIR / filename
            with image_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            product.image = str(image_path.as_posix())

        # Si se envía category_id, buscar la categoría
        if update_data.category_id:
            res = await self.db.execute(
                select(Category).where(Category.id == update_data.category_id)
            )
            category = res.scalars().first()
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            product.category = category

        # Actualizar los demás campos enviados
        for key, value in update_data.dict(exclude_unset=True).items():
            if key != "category_id":  # ya manejamos category aparte
                setattr(product, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(product)
            return api_response(data=product, message="Product updated successfully")
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Integrity error while updating product")


    async def get_products_by_id(
        self, 
        product_id: list[str]
    ):
        if not product_id:
            return []
        
        res = await self.db.execute(
            select(Product)
            .where(Product.id.in_(product_id))
            .options(selectinload(Product.category))
        )
        products = res.scalars().all()
        
        if not products:
            raise HTTPException(status_code=404, detail="No products found for given IDs")
        return products
        
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
                raise HTTPException(status_code=404, detail="Category not found in create product")
        
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
        return api_response(data=new_product, message="Product created succes") 


