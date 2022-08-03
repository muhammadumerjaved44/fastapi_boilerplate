# from api.models import user
from fastapi import HTTPException, Depends, APIRouter
from schemas import LoginIn, LoginOut
from sqlalchemy.orm import Session
import auth
from db.session import get_db
from models import User
from schemas import UserSchema, Users, AddUser, UserUpdateSchema
from typing import List
router = APIRouter()


@router.get("/{id}",response_model=UserSchema)
def userList(id:int,session : Session=Depends(get_db)):
    user = session.query(User).get(id)
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    response: UserSchema = user
    return response

@router.get("/",response_model=Users )
def userList(session : Session=Depends(get_db)):
    users = session.query(User).all()
    response: UserSchema = users
    response: Users = Users(users=users)
    return response

@router.post("/")
def addUser(user: AddUser, session : Session=Depends(get_db)):
    userObj = User(**user.dict())
    session.add(userObj)
    session.commit()
    session.refresh(userObj)   
    return userObj

@router.put("/{id}")
def updateUser(id:int, user:UserUpdateSchema, session : Session=Depends(get_db)):
    userObj = session.query(User).get(id)
    userObj.first_name = user.first_name
    userObj.last_name = user.last_name
    session.commit()
    return userObj

@router.delete("/{id}")
def deleteUser(id:int, session : Session=Depends(get_db)):
    userObj = session.query(User).get(id)
    session.delete(userObj)
    session.commit()
    session.close
    return userObj.first_name+"  deleted"