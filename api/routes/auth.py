from fastapi import HTTPException, Depends, APIRouter
from schemas import LoginIn, LoginOut
from sqlalchemy.orm import Session
import auth
from db.session import get_db
from models import User


router = APIRouter()


@router.post("/login", response_model=LoginOut)
def login(auth_details: LoginIn, db: Session = Depends(get_db)):

    # getting user
    user = db.query(User).filter(User.email == auth_details.email).first()

    # checking if user not found or password is invalid
    if (user is None) or (
        not auth.verify_password(auth_details.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid email and/or password")

    # generating new token
    token = auth.encode_token(user.email)

    response: LoginOut = LoginOut(token=token, is_admin=user.is_admin)
    return response
