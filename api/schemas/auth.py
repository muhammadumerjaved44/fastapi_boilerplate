from pydantic import BaseModel


class LoginIn(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {"example": {"email": "admin@mail.com", "password": "password",}}


class LoginOut(BaseModel):
    token: str
    is_admin: bool
