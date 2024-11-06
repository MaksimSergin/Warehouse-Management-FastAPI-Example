from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.order import OrderCreate, OrderRead, OrderUpdateStatus
from app.services import order as order_service
from app.db.session import get_db
from app.core.exceptions import InsufficientStockError, ProductNotFoundError

router = APIRouter()


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_order = await order_service.create_order(db, order=order)
        return db_order
    except (InsufficientStockError, ProductNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[OrderRead])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    orders = await order_service.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=OrderRead)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    db_order = await order_service.get_order(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return db_order


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(order_id: int, status_update: OrderUpdateStatus, db: AsyncSession = Depends(get_db)):
    db_order = await order_service.get_order(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return await order_service.update_order_status(db, db_order=db_order, status=status_update.status)
