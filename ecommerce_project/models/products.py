from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=5)
    category: str = Field(..., min_length=1, max_length=50)
    unit_price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class Product(ProductCreate):
    id: int = Field(..., gt=0)
    # inherited fields from ProductCreate

    # enable reading from ORM tables
    model_config = ConfigDict(from_attributes=True)