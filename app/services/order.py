from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from sqlalchemy.orm import selectinload

from app.models import OrderItem
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderStatus
from app.services.product import get_product
from app.core.exceptions import InsufficientStockError, ProductNotFoundError


async def get_order(db: AsyncSession, order_id: int) -> Order:
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    return result.scalars().first()


async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_order(db: AsyncSession, order: OrderCreate) -> Order:
    db_order = Order(status=order.status or OrderStatus.in_progress)
    async with db.begin():
        for item in order.items:
            product = await get_product(db, item.product_id)
            if not product:
                raise ProductNotFoundError(f"Product with id {item.product_id} does not exist.")
            if product.quantity < item.quantity:
                raise InsufficientStockError(f"Insufficient quantity for product {product.name}.")
            product.quantity -= item.quantity

            db_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
            db_order.items.append(db_item)
        db.add(db_order)
    await db.refresh(db_order)
    return db_order


async def update_order_status(db: AsyncSession, db_order: Order, status: OrderStatus) -> Order:
    db_order.status = status
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order
