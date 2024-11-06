from sqlalchemy.orm import Session
from typing import Optional
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate


def get_order_item(db: Session, order_item_id: int) -> Optional[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.id == order_item_id).first()


def create_order_item(db: Session, order_item: OrderItemCreate) -> OrderItem:
    db_order_item = OrderItem(
        product_id=order_item.product_id,
        quantity=order_item.quantity
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item
