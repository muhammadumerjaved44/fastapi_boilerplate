from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class AddUser(BaseModel):
    email: EmailStr
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


class CampaignSchema(BaseModel):
    via_sms: bool
    via_email: bool
    audience_number: int
    created_at: datetime

    class Config:
        orm_mode = True


class GetCampaignOut(BaseModel):
    campaigns: list[CampaignSchema]
