from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """This class will be used for creating"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=9, max_length=16)


class User(UserCreate):
    """For other purposes than creation, we also need the ID and ORM mode enabled"""
    id: int = Field(..., gt=0)
    # HERE inheritance from UserCreate

    # enable reading from ORM tables
    model_config = ConfigDict(from_attributes=True)
