from sqlalchemy import Column, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from ..database import Base


class OrdersTable(Base):
    __tablename__ = "orders"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    order_timestamp = Column(DateTime, nullable=False)

    # relationships
    user = relationship("UsersTable", back_populates="orders")
    order_items = relationship("CartItemsTable", back_populates="order")
