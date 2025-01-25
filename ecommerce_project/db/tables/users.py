from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class UsersTable(Base):
    __tablename__ = "users"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)

    # relationships
    orders = relationship("OrdersTable", back_populates="user")
