from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, status
from schemas import RequestDemoIn, RequestDemoOut
import models
import auth
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from config import settings


router = APIRouter()


# ping end point for checking if the API is working
@router.get("/ping")
async def ping():

    response: dict = {"message": "Working."}
    return response


@router.post("/request_demo")
async def request_demo(user_details: RequestDemoIn):
    """setup endpoint for client data email

    Args:
        user_details (RequestDemoIn): client data 

    Returns:
        _type_: dictionary 
    """
    msg = f"Email : {user_details.email} \nName : {user_details.name}\nPhone_Number  : {user_details.phone_number}\nJob_Title : {user_details.job_title}\nInstitute : {user_details.institute}"
    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email(settings.STELLO_EMAIL)
    to_email = To(user_details.email)
    subject = "User Details"
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return {"message": "Mail sent"}
