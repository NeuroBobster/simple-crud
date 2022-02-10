from pydantic import BaseModel, EmailStr
from typing import Optional


# Create User Base Model
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True