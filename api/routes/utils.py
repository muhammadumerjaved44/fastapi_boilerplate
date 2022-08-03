from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException
from schemas import RequestDemoIn, RequestDemoOut
import models
import auth

router = APIRouter()


# ping end point for checking if the API is working
@router.get("/ping")
async def ping():

    response: dict = {"message": "Working."}
    return response


@router.get("/hash_password")
async def hash_password(password: str):

    hashed_password = auth.get_password_hash(password)
    response: dict = {"hashed_password": hashed_password}
    return response


@router.post("/request_demo", response_model=RequestDemoOut)
async def request_demo(user_details: RequestDemoIn):

    try:
        validate_email(user_details.email).email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Email not valid")

    response: RequestDemoOut = RequestDemoOut(
        message="Demo request successfully accepted"
    )
    return response
