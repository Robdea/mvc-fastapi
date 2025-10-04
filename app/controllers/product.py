from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import product_schema
from ..services.product_service import ProductService
from ..utils.service_factory import service_factory
import shutil
import os
router = APIRouter(prefix="/product", tags=["product"])


@router.get("/", response_model=list[product_schema.ProductOut])
async def get_all(
    service: ProductService = Depends(service_factory(ProductService))
):
    list_products = await service.get_products()
    return list_products

@router.get("/{product_id}", response_model=product_schema.ProductOut)
async def get_by_id(
    product_id:str,
    service: ProductService = Depends(service_factory(ProductService))
):
    product = await service.get_product_by_id(product_id=product_id)
    return product

@router.delete("/{product_id}")
async def delete(
    product_id: str,
    service: ProductService = Depends(service_factory(ProductService))
):
    return await service.delete_product(product_id)    

@router.get("/by-category/{category_id}", response_model=list[product_schema.ProductOut])
async def list_products_by_category(
    category_id: str, 
    service: ProductService = Depends(service_factory(ProductService))
):
    return await service.get_products_by_category(category_id)

@router.post("/")
async def create_category(
    data: str = Form(...),
    image: UploadFile = File(None),
    service: ProductService = Depends(service_factory(ProductService))
):
    
    created_category = await service.create_product(data=data, image=image)
    return created_category

    

