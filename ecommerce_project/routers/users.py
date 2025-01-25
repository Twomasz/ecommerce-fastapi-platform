from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ecommerce_project.db import get_db, UsersTable
from ecommerce_project.models import User, UserCreate


router = APIRouter()


@router.get("/", response_model=list[User])
async def list_users(db: AsyncSession = Depends(get_db)) -> Sequence[UsersTable]:
    """Endpoint to get all users"""
    query = select(UsersTable)
    result = await db.execute(query)
    users = result.scalars().all()

    return users


@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> dict:
    """Endpoint to register a new user. Checks if the email is already used"""
    query = select(UsersTable).where(UsersTable.email == user.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=400, detail=f"Email '{user.email}' already registered")

    new_user = UsersTable(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error registering user")

    return {
        'message': 'User registered successfully',
        'user': User.model_validate(new_user)
    }


@router.get("/id/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UsersTable:
    """Endpoint to get user by ID"""
    query = select(UsersTable).where(UsersTable.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/id/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)) -> UsersTable:
    """Endpoint to update user by ID"""
    query = select(UsersTable).where(UsersTable.id == user_id)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.phone_number = user.phone_number

    try:
        await db.commit()
        await db.refresh(existing_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error updating user")

    return existing_user


@router.delete("/id/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """Endpoint to delete user by ID"""
    query = select(UsersTable).where(UsersTable.id == user_id)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(existing_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting user")

    return {"message": "User deleted successfully"}