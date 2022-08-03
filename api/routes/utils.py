from fastapi import APIRouter
import models
import auth

router = APIRouter()


# ping end point for checking if the API is working
@router.get("/ping")
def ping():

    response: dict = {"message": "Working."}
    return response


@router.get("/hash_password")
def ping(password: str):

    hashed_password = auth.get_password_hash(password)
    response: dict = {"hashed_password": hashed_password}
    return response
