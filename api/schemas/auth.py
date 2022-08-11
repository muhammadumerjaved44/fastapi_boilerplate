from pydantic import BaseModel
from typing import List, Union


class LoginIn(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {"example": {"email": "admin@mail.com", "password": "password",}}


class LoginOut(BaseModel):
    token: str
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: Union[List[str], str] = []
