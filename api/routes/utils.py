from fastapi import APIRouter

router = APIRouter()


# ping end point for checking if the API is working
@router.get("/ping")
def ping():

    response: dict = {"message": "Working."}
    return response
