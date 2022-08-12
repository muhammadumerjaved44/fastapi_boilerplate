from pydantic import BaseModel, EmailStr
from typing import List


class AddUser(BaseModel):
    username: EmailStr
    password: str
    first_name: str
    last_name: str
    scope: str
    is_active: bool


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Users(BaseModel):
    users: List[UserSchema]


class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
