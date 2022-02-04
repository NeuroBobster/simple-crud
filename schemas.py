from pydantic import BaseModel
from typing import Union


# Create User Base Model
class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: Union[str, None]
    email: Union[str, None]


class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True