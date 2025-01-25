from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, Sequence, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ecommerce_project.db import get_db, ProductsTable
from ecommerce_project.models import Product, ProductCreate


router = APIRouter()


@router.get("/", response_model=list[Product])
async def list_products(db: AsyncSession = Depends(get_db)) -> Sequence[ProductsTable]:
    """Endpoint to get all products"""
    query = select(ProductsTable)
    result = await db.execute(query)
    products = result.scalars().all()

    return products

@router.get("/id/{product_id}", response_model=Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)) -> ProductsTable:
    """Endpoint to get product by ID"""
    query = select(ProductsTable).where(ProductsTable.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/fill", response_model=Product)
async def fill_product(product: ProductCreate, db: AsyncSession = Depends(get_db)) -> ProductsTable:
    """Endpoint to fill a product. If it exists, increase the quantity; otherwise, create it."""
    query = select(ProductsTable).where(ProductsTable.name == product.name)
    result = await db.execute(query)
    existing_product = result.scalar_one_or_none()

    if existing_product is not None:
        existing_product.quantity += product.quantity
        try:
            await db.commit()
            await db.refresh(existing_product)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error updating existing product quantity")
        return existing_product
    else:
        new_product = ProductsTable(
            name=product.name,
            description=product.description,
            category=product.category,
            unit_price=product.unit_price,
            quantity=product.quantity
        )
        db.add(new_product)
        try:
            await db.commit()
            await db.refresh(new_product)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error creating product")
        return new_product


@router.get("/search", response_model=list[Product])
async def search_products(
    db: AsyncSession = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by product name"),
    category: Optional[str] = Query(None, description="Filter by product category"),
    min_price: Optional[float] = Query(None, description="Filter by minimum price"),
    max_price: Optional[float] = Query(None, description="Filter by maximum price")
) -> Sequence[ProductsTable]:
    """Endpoint to get all products with optional filters"""
    filters = []
    if name:
        filters.append(ProductsTable.name.ilike(f"%{name}%"))
    if category:
        filters.append(ProductsTable.category.ilike(f"%{category}%"))
    if min_price is not None:
        filters.append(ProductsTable.unit_price >= min_price)
    if max_price is not None:
        filters.append(ProductsTable.unit_price <= max_price)

    query = select(ProductsTable).where(and_(*filters)) if filters else select(ProductsTable)
    result = await db.execute(query)
    products = result.scalars().all()

    return products


@router.delete("/id/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """Endpoint to delete a product by ID"""
    query = select(ProductsTable).where(ProductsTable.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting product")

    return {'message': 'Product deleted successfully'}

