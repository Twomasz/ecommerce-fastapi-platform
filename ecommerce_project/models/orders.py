from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Order(BaseModel):
    id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    order_timestamp: datetime

    # enable reading from ORM tables
    model_config = ConfigDict(from_attributes=True)


class _OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class PlaceOrder(BaseModel):
    user_id: int = Field(..., gt=0)
    items: list[_OrderItem]
