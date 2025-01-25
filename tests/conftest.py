from datetime import datetime

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ecommerce_project.db import Base, get_db, ProductsTable, UsersTable, OrdersTable, CartItemsTable
from ecommerce_project.app import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Before running the tests, create tables and populate the test database with sample data."""
    sample_users = [
        UsersTable(name="User 1", email="user1@example.com", phone_number="1234567890"),
        UsersTable(name="User 2", email="user2@example.com", phone_number="0987654321"),
    ]
    sample_products = [
        ProductsTable(name="Product 1", description="Description 1", category="Category 1", unit_price=10.0,
                      quantity=100),
        ProductsTable(name="Product 2", description="Description 2", category="Category 2", unit_price=20.0,
                      quantity=200),
    ]
    sample_orders = [
        OrdersTable(user_id=1, total_price=30.0, order_timestamp=datetime.now()),
    ]
    sample_cart_items = [
        CartItemsTable(order_id=1, product_id=1, quantity=3),
        CartItemsTable(order_id=1, product_id=2, quantity=3),
    ]
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with AsyncSession(bind=conn) as session:
            # add sample data to the test database
            session.add_all(sample_products)
            session.add_all(sample_users)
            session.add_all(sample_orders)
            session.add_all(sample_cart_items)
            await session.commit()
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def test_db():
    """Provide a testing session for the test client"""
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def test_client(test_db):
    """Provide a test client with the overwritten, test database session"""
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()