from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .order_item import OrderItemCreate, OrderItemRead


class OrderStatus(str, Enum):
    in_progress = "in_progress"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.in_progress


class OrderCreate(BaseModel):
    status: OrderStatus = OrderStatus.in_progress
    items: List[OrderItemCreate]


class OrderUpdateStatus(BaseModel):
    status: OrderStatus


class OrderRead(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)
