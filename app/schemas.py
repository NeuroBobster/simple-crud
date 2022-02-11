from pydantic import BaseModel, EmailStr, validator
from typing import Optional


# Create User Base Model
class UserBase(BaseModel):
    name: str
    email: EmailStr

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True