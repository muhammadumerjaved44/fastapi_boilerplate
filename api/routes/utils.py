from email_validator import validate_email, EmailNotValidError
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    Depends,
    status,
    BackgroundTasks,
)
from schemas import (
    RequestDemoIn,
    RequestDemoOut,
    Contacts,
    MessageTagsOut,
    MessageTemplatesOut,
)
from sqlalchemy import inspect
import pandas as pd
import numpy as np
from io import StringIO
import auth
from models import User, Contact, MessageTemplate
import pydantic
from db.session import get_db
from sqlalchemy.orm import Session
from background_tasks import upload_csv_to_s3, save_csv_contacts
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
    to_email = To(settings.STELLO_EMAIL)
    subject = "User Details"
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return {"message": "Mail sent"}


@router.get("/message-tags", response_model=MessageTagsOut)
async def get_message_tags():
    """endpoint for getting message tags (filtered contacts model's column names)

    Args:
        None

    Returns:
        MessageTagsOut: list of filtered contacts model's column names
    """

    excluded_tags = ["user_id", "id"]
    tags = inspect(Contact).columns.keys()
    tags = [f"@{tag}" for tag in tags if tag not in excluded_tags]
    response: MessageTagsOut = MessageTagsOut(tags=tags)
    return response


@router.get("/message-templates", response_model=MessageTemplatesOut)
async def get_message_templates(
    db: Session = Depends(get_db),
):
    """endpoint for getting message templates from database

    Args:
        None

    Returns:
        MessageTemplatesOut: list of MessageTemplate model objects
    """

    message_templates = db.query(MessageTemplate).all()
    response: MessageTemplatesOut = MessageTemplatesOut(
        message_templates=message_templates
    )
    return response


@router.post("/upload-csv", response_model=Contacts)
async def upload_csv(
    csv_file: UploadFile,
    background_tasks: BackgroundTasks,
    user: User = Depends(auth.get_current_active_user),
):
    """This endpoint accepts a CSV file with a specific schema then uploads it to S3,
        converts it into a list of dictionaries and returns the list.

    Args:
        csv_file (UploadFile): CSV file with specific schema

    Returns:
        UploadCSVOut: list of dictionaries of contacts schema
    """

    # reading with pandas
    file_bytes = StringIO(csv_file.file.read().decode())
    contacts_df = pd.read_csv(file_bytes)

    # validating required columns
    if not all(
        x in contacts_df.columns.tolist()
        for x in ["First.Name", "Last.Name", "Preferred.Email"]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required column(s) are missing!",
        )

    # validating null/missing values in the required columns
    if (
        contacts_df["First.Name"].isna().sum()
        or contacts_df["Last.Name"].isna().sum()
        or contacts_df["Preferred.Email"].isna().sum()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A value in the required columns ('First.Name', 'Last.Name', 'Preferred.Email') is null/missing",
        )

    # uploading csv to aws s3 by background task
    background_tasks.add_task(
        upload_csv_to_s3,
        csv_file=csv_file,
        user_id=user.id,
    )

    # cleaning csv data
    contacts_df = contacts_df.replace(np.nan, None)
    contacts_df["Preferred.Email"] = contacts_df["Preferred.Email"].str.lower()

    contacts_df = contacts_df.rename(
        columns={
            "Student.ID": "student_id",
            "First.Name": "first_name",
            "Last.Name": "last_name",
            "Preferred.Email": "preferred_email",
            "CRC.Email": "crc_email",
            "Application.Email": "application_email",
            "Day.Phone": "day_phone_number",
            "Eve.Phone": "evening_phone_number",
            "Major": "major",
            "CAC": "cac",
            "Age": "age",
            "Gender": "gender",
            "Race.Ethnicity": "race_ethnicity",
            "New.Student": "new_student",
            "Athlete": "athlete",
            "Puente": "puente",
            "Diop": "diop",
            "Reported.Disability": "reported_disability",
            "Income.Level..Self.Reported.": "income_level_self_reported",
            "BOG": "bog",
            "CalWorks": "cal_works",
            "EOPS": "eops",
            "CARE": "care",
            "Homeless": "homeless",
            "Need.Based.Federal.Aid": "need_based_federal_aid",
            "Completed.Units": "completed_units",
            "GPA": "gpa",
            "Units.Completed..including.District.": "units_completed_including_district",
            "Enrolled.Districtwide": "enrolled_districtwide",
        }
    )
    contact_dict_list = contacts_df.to_dict("records")

    # if CSV data has type validation issue then respond with 400 Bad request
    try:
        response: Contacts = Contacts(contacts=contact_dict_list)
    except pydantic.error_wrappers.ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV data not valid according to defined schema. Try checking data types of values in age, gpa, completed units, etc.",
        )

    # saving contacts to
    background_tasks.add_task(
        save_csv_contacts,
        user_id=user.id,
        contacts=response.contacts,
    )

    return response
