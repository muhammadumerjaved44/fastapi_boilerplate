from datetime import timedelta
from db.session import get_db
from config import settings
from schemas import Token
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from .auth import authenticate_user, create_access_token

router = APIRouter()


@router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """login user

    Args:
        form_data (OAuth2PasswordRequestForm, optional): oauth2 form . Defaults to Depends().
        db (Session, optional): database connection

    Raises:
        HTTPException: 400, incorrect username or password

    Returns:
        _type_: access token and type
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scope},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "scope": user.scope}
