from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product import Product
from sqlalchemy.orm import selectinload

from ..models.cactegory import Category
from sqlalchemy.future import select

from ..schemas import product_schema

async def get_products(
    db: AsyncSession
):
    res = await db.execute(
    select(Product).options(selectinload(Product.category))
    )
    products = res.scalars().all()
    return products

async def get_products_by_category(category_id: str, db: AsyncSession):
    res = await db.execute(select(Category).where(Category.id == category_id))
    category = res.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    res = await db.execute(select(Product).where(Product.category_id == category_id))
    return res.scalars().all()


async def get_product_by_id(product_id: str, db: AsyncSession):
    res = await db.execute(select(Product).where(Product.id == product_id))
    producto = res.scalars().first()
    if not producto:
        raise HTTPException(status_code=404, detail="Product not found")
    return producto

async def delete_product(
    product_id: str, db: AsyncSession
):
    product = await get_product_by_id(product_id, db)
    
    await db.delete(product)
    await db.commit()
    
    return {"message": "Product was delete"}

async def create_product(
    product: product_schema.ProductCreate,
    db: AsyncSession
):
    category = None
    if product.category_id:
        res = await db.execute(
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
        category=category
    )
    
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product
    


