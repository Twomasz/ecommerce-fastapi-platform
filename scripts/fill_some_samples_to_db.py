from datetime import datetime

import asyncio

from ecommerce_project import db


async def fill_sample_data():
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    async for session in db.get_db():
        sample_users = [
            db.UsersTable(name="User 1", email="user1@example.com", phone_number="1234567890"),
            db.UsersTable(name="User 2", email="user2@example.com", phone_number="0987654321"),
        ]
        sample_products = [
            db.ProductsTable(name="Product 1", description="Description 1", category="Category 1", unit_price=10.0, quantity=100),
            db.ProductsTable(name="Product 2", description="Description 2", category="Category 2", unit_price=20.0, quantity=200),
        ]
        sample_orders = [
            db.OrdersTable(user_id=1, total_price=30.0, order_timestamp=datetime.now()),
        ]
        sample_cart_items = [
            db.CartItemsTable(order_id=1, product_id=1, quantity=3),
            db.CartItemsTable(order_id=1, product_id=2, quantity=3),
        ]

        session.add_all(sample_users)
        session.add_all(sample_products)
        session.add_all(sample_orders)
        session.add_all(sample_cart_items)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(fill_sample_data())
