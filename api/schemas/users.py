from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class CreateUserIn(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    scope: str
    is_active: bool


class CreateUserOut(BaseModel):
    message: str


class UserSchema(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr

    class Config:
        orm_mode = True


class Users(BaseModel):
    users: List[UserSchema]


class UpdateUserIn(BaseModel):
    first_name: str
    last_name: str


class UpdateUserOut(BaseModel):
    message: str


class DeleteUserOut(BaseModel):
    message: str


class CampaignSchema(BaseModel):
    via_sms: bool
    via_email: bool
    message: str
    audience_number: int
    created_at: datetime

    class Config:
        orm_mode = True


class GetCampaignOut(BaseModel):
    campaigns: list[CampaignSchema]


class BroadcastMessageOut(BaseModel):
    message: str


class BroadcastMessageIn(BaseModel):
    is_sms: bool
    is_email: bool
    subject: str
    message: str
    emails: set[EmailStr]
