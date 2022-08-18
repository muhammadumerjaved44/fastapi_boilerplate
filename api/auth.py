from datetime import datetime, timedelta
from typing import List, Union
from db.session import get_db
from config import settings
from models import User
from schemas import CreateUserIn, TokenData
from sqlalchemy.orm import Session

from fastapi import Depends, APIRouter, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scopes={
        "superuser": "All access",
        "admin": "Read items",
        "staff": "have access staff responsibilty",
        "user": "user access",
        "guest": "guest mode",
    },
)


router = APIRouter()


def verify_password(plain_password, hashed_password):
    """verify password

    Args:
        plain_password (_type_): password without hashed
        hashed_password (bool): hased password

    Returns:
        string: verification detail
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):

    """convert plain to hash password

    Args:
        password (_type_): password

    Returns:
        string: hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session):
    """for authentication

    Args:
        username (str): username
        password (str): password
        db (Session): database connection

    Returns:
        False or User model: user if authenticated otherwise returns False
    """
    user = db.query(User).filter(User.email == username).first()
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
        str: token
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
        HTTPException:
                    - 401, not enough permissions
                    - 401, Could not validate credentials

    Returns:
        User model: if authenticated then returns user otherwise status 401
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
    user = db.query(User).filter(User.email == token_data.username).first()

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
    current_user: CreateUserIn = Security(get_current_user, scopes=[])
):
    """for cehcking active user

    Args:
        current_user (AddUser, optional): for checking scope

    Raises:
        HTTPException: 400, not active

    Returns:
        User model: if user is active then returns user otherwise status 400
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
