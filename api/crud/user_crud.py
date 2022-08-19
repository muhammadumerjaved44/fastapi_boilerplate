from typing import Optional, Union
from sqlalchemy.orm import Session
from models import User
from schemas import CreateUserIn, UpdateUserIn
from auth import get_password_hash
from sqlalchemy.exc import IntegrityError


def get(id: int, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.id == id).first()
    return user


def get_by_email(email: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_all(db: Session) -> Union[list[User], list]:
    users = db.query(User).all()
    return users


def create(user_in: CreateUserIn, db: Session) -> Optional[User]:
    try:
        password = get_password_hash(user_in.password)
        user_in.password = password
        user = User(**user_in.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        return None


def update(id: int, user_in: UpdateUserIn, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return None
    user.first_name = user_in.first_name
    user.last_name = user_in.last_name
    db.commit()
    db.refresh(user)
    return user


def delete(id: int, db: Session) -> int:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return id
