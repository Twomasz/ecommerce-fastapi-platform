from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class ProductsTable(Base):
    __tablename__ = "products"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # relationships
    order_items = relationship("CartItemsTable", back_populates="product")
