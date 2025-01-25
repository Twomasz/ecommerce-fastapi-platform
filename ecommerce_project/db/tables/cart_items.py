from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class CartItemsTable(Base):
    __tablename__ = "cart_items"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    # relationships
    order = relationship("OrdersTable", back_populates="order_items")
    product = relationship("ProductsTable", back_populates="order_items")
