from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import product_schema
from ..services.product_service import ProductService
from ..utils.service_factory import service_factory
from uuid import UUID

from typing import List

router = APIRouter(prefix="/product", tags=["product"])

@router.get("/by_ids")
async def get_products_by_ids(
    service: ProductService = Depends(service_factory(ProductService)),
    ids: List[str] = Query(...)
):
    products = await service.get_products_by_id(product_id=ids)
    return products
    
@router.get("/testids")
async def test_ids(ids: List[UUID] = Query(...)):
    return {"received_ids": [str(i) for i in ids]}


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

@router.patch("/{product_id}")
async def patch_product(
    product_id: str,
    data: str = Form(...),
    image: UploadFile = File(None),
    service: ProductService = Depends(service_factory(ProductService))
):
    return await service.update_product(product_id, data, image)

@router.post("/")
async def create_category(
    data: str = Form(...),
    image: UploadFile = File(None),
    service: ProductService = Depends(service_factory(ProductService))
):
    
    created_category = await service.create_product(data=data, image=image)
    return created_category

    

