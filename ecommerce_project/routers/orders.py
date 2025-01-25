from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ecommerce_project.db import get_db, OrdersTable, CartItemsTable, ProductsTable
from ecommerce_project.models import Order, PlaceOrder


router = APIRouter()


@router.get("/", response_model=list[Order])
async def list_orders(db: AsyncSession = Depends(get_db)) -> Sequence[OrdersTable]:
    """Endpoint to get all orders"""
    query = select(OrdersTable)
    result = await db.execute(query)
    orders = result.scalars().all()

    return orders


@router.get("/id/{order_id}", response_model=Order)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint to get order by ID"""
    query = select(OrdersTable).where(OrdersTable.id == order_id)
    result = await db.execute(query)
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.post("/place_order", response_model=Order)
async def place_order(p_order: PlaceOrder, db: AsyncSession = Depends(get_db)) -> OrdersTable:
    """Endpoint to place an order. Decreases product quantity and fills order_items table."""
    # check if user exists
    query = select(OrdersTable).where(OrdersTable.user_id == p_order.user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {p_order.user_id} not found, please register first")

    # check product quantities
    for item in p_order.items:
        query = select(ProductsTable).where(ProductsTable.id == item.product_id)
        result = await db.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
        if product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough quantity for product ID {item.product_id}")

    # (start transaction) create empty order to get the unique ID
    new_order = OrdersTable(
        user_id=p_order.user_id,
        total_price=(total_price := 0),  # total_price will be calculated later
        order_timestamp=datetime.now()
    )
    db.add(new_order)
    await db.flush()

    for item in p_order.items:
        query = select(ProductsTable).where(ProductsTable.id == item.product_id)
        result = await db.execute(query)
        product = result.scalar_one_or_none()

        product.quantity -= item.quantity
        total_price += product.unit_price * item.quantity

        order_item = CartItemsTable(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    new_order.total_price = total_price
    try:
        await db.commit()
        await db.refresh(new_order)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error placing order")

    return new_order


@router.get("/history/users/{user_id}", response_model=list[Order])
async def get_order_history(user_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint to get order history for a user"""
    query = select(OrdersTable).where(OrdersTable.user_id == user_id)
    result = await db.execute(query)
    orders = result.scalars().all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    return orders