from pydantic import BaseModel, ConfigDict, Field


class CartItem(BaseModel):
    id: int = Field(..., gt=0)
    order_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

    # enable reading from ORM tables
    model_config = ConfigDict(from_attributes=True)
