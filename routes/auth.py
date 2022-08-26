from datetime import datetime, timedelta
from typing import List, Union
from db.session import get_db
from config import settings
from models import User
from schemas import AddUser, TokenData, Token
from sqlalchemy.orm import Session

from fastapi import Depends, APIRouter, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login/",
    scopes={
        "superuser": "All access",
        "admin": "Read items",
        "staff": "have access staff responsibilty",
        "user": "user access",
        "guest": "guest mode",
    },
)


router = APIRouter()

def get_user(username,  db: Session):
    """Search user by username

    Args:
        user_name (_type_): Username

    Returns:
        _type_: User Credentials
    """
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return
    else:
        return AddUser(
                username= user.email,
                password= user.password,
                first_name= user.first_name,
                last_name= user.last_name,
                is_active= user.is_active,
                scope = user.scope
        )


def verify_password(plain_password, hashed_password):
    """verify password

    Args:
        plain_password (_type_): password without hashed
        hashed_password (bool): hased password

    Returns:
        _type_: verification detail
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):

    """convert plain to hash password

    Args:
        password (_type_): password

    Returns:
        _type_: hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session):
    """for authentication

    Args:
        username (str): username
        password (str): password
        db (Session): database connection

    Returns:
        _type_: authenticated user if conditions true
    """
    user = get_user(username,  db)
    if not user:
        return False
    try:
        if not verify_password(password, user.password):
            return False
    except Exception:
        pass
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """create acces token

    Args:
        data (dict): data
        expires_delta (Union[timedelta, None], optional): time . Defaults to None.

    Returns:
        _type_: token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """get current user after authorization

    Args:
        security_scopes (SecurityScopes): for using scopes
        token (str, optional): token
        db (Session, optional): database connection

    Raises:
        credentials_exception: 401, not validate credentials
        credentials_exception: _description_
        credentials_exception: _description_
        HTTPException: 401, not enough permissions

    Returns:
        _type_: _description_
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:

        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(token_data.username,  db)

    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: AddUser = Security(get_current_user, scopes=[])
):
    """for cehcking active user

    Args:
        current_user (AddUser, optional): for checking scope

    Raises:
        HTTPException: 400, not active

    Returns:
        _type_: current_user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
