from pydantic import BaseModel
from typing import List

class AddUser(BaseModel):
    email:str
    password:str
    first_name:str
    last_name:str
    is_admin: bool
    is_active:bool 
    
    
class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    
    class Config:
        orm_mode = True

class Users(BaseModel):
    users: List[UserSchema]
    

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str