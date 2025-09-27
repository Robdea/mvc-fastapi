from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import mysql_bd
from ..schemas import product_schema
from ..services import product_service

router = APIRouter(prefix="/product", tags=["product"])


@router.get("/", response_model=list[product_schema.ProductOut])
async def get_all(
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    list_products = await product_service.get_products(db=db)
    return list_products

@router.get("/{product_id}", response_model=product_schema.ProductOut)
async def get_by_id(
    product_id:str,
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    product = await product_service.get_product_by_id(product_id=product_id, db= db)
    return product

@router.delete("/{product_id}")
async def delete(
    product_id: str,
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    return await product_service.delete_product(product_id, db)    

@router.get("/by-category/{category_id}", response_model=list[product_schema.ProductOut])
async def list_products_by_category(
    category_id: str, 
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    return await product_service.get_products_by_category(category_id, db)

@router.post("/", response_model=product_schema.ProductOut)
async def create_category(
    product: product_schema.ProductCreate,
    db: AsyncSession = Depends(mysql_bd.get_db)
):
    created_category = await product_service.create_product(product=product, db=db)
    return created_category

    

