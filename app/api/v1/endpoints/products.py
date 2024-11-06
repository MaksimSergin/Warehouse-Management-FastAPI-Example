from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ProductNotFoundError
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product as product_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    existing_product = await product_service.get_product_by_name(db, name=product.name)
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists.")

    return await product_service.create_product(db, product=product)


@router.get("/", response_model=List[ProductRead])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    products = await product_service.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await product_service.get_product(db, product_id=product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, updates: ProductUpdate, db: AsyncSession = Depends(get_db)):
    try:
        db_product = await product_service.get_product(db, product_id=product_id)
        return await product_service.update_product(db, db_product=db_product, updates=updates)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_product = await product_service.get_product(db, product_id=product_id)
        await product_service.delete_product(db, db_product=db_product)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
