import boto3
from config import settings
from fastapi import UploadFile
from datetime import datetime
import os
from models import Contact
from schemas import Contacts
from db.session import SessionLocal
from sendgrid import SendGridAPIClient
import sendgrid.helpers.mail as sendgrid_mail_helper
from bs4 import BeautifulSoup
from crud import contact_crud, contact_csv_crud
from twilio.rest import Client as TwilioClient

s3 = boto3.resource(
    "s3",
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
)

s3_bucket = s3.Bucket(settings.S3_CSV_BUCKET)

sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

twilio_client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def upload_csv_to_s3(csv_file: UploadFile, user_id: int):

    # seeking file to start
    csv_file.file.seek(0)

    # preparing file path for S3
    file_name, file_extension = os.path.splitext(csv_file.filename)
    file_s3_parent_folder = settings.S3_CSV_FOLDER
    file_path = f"{file_s3_parent_folder}/{user_id}_{file_name}_{datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')}{file_extension}"

    # uploading file to S3
    object = s3.Object(settings.S3_CSV_BUCKET, file_path)
    object.put(Body=csv_file.file)
    with SessionLocal() as db:
        contact_csv = contact_csv_crud.create(
            s3_uri=object.key, s3_bucket=object.bucket_name, user_id=user_id, db=db
        )


def save_csv_contacts(user_id: int, contacts: Contacts):
    # add or update contacts in db
    with SessionLocal() as db:
        contacts_obj_list = []

        for contact in contacts:
            contact_db = contact_crud.get_by_preferred_email(
                preferred_email=contact.preferred_email, user_id=user_id, db=db
            )

            if contact_db:
                for attribute, new_value in contact.dict().items():
                    setattr(contact_db, attribute, new_value)
            else:
                create_kwargs = contact.dict()
                contacts_obj_list.append(Contact(**create_kwargs, user_id=user_id))

        contact_crud.create_multi(contacts_obj_list, db=db)


def broadcast_message_task(
    emails: list[str],
    message: str,
    subject: str,
    user_id: int,
    via_email: bool,
    via_sms: bool,
):
    soup = BeautifulSoup(message, "html.parser")
    tag_spans = soup.select('span[class="mention"]')

    # subject is required for emails in sendgrid API
    # if subject is empty then replace it with a white space which is converted to (No Subject)
    if not subject:
        subject = " "

    for email in emails:

        with SessionLocal() as db:
            message_personal = f"{message}"
            contact = contact_crud.get_by_preferred_email(
                preferred_email=email, user_id=user_id, db=db
            )

            if contact is not None:
                contact_dict = contact.__dict__

                for tag_span in tag_spans:
                    tag_value = contact_dict[tag_span.text.replace("@", "")]
                    message_personal = message_personal.replace(
                        str(tag_span), tag_value
                    )

                # sending email
                if via_email:
                    from_email = sendgrid_mail_helper.Email(
                        settings.DEFAULT_SENDER_EMAIL
                    )
                    to_email = sendgrid_mail_helper.To(email)
                    content = sendgrid_mail_helper.Content(
                        "text/html", f"{message_personal}"
                    )
                    mail = sendgrid_mail_helper.Mail(
                        from_email, to_email, subject, content
                    )
                    sendgrid_response = sendgrid_client.client.mail.send.post(
                        request_body=mail.get()
                    )

                # sending sms
                if via_sms:
                    soup_sms = BeautifulSoup(message_personal, "html.parser")
                    message_sms = soup_sms.get_text(separator="\n")

                    if settings.ENV in ["development", "testing"]:
                        sms_recipient_number = settings.TWILIO_TO_PHONE_NUMBER
                    elif settings.ENV == "production":
                        sms_recipient_number = contact_dict["day_phone_number"]

                    twilio_sms_response = twilio_client.messages.create(
                        body=message_sms,
                        from_=settings.TWILIO_FROM_PHONE_NUMBER,
                        to=sms_recipient_number,
                    )


def send_email(to_email: str, subject: str, message: str):
    from_email = sendgrid_mail_helper.Email(settings.DEFAULT_SENDER_EMAIL)
    to_email = sendgrid_mail_helper.To(to_email)
    content = sendgrid_mail_helper.Content("text/plain", f"{message}")
    mail = sendgrid_mail_helper.Mail(from_email, to_email, subject, content)
    sendgrid_response = sendgrid_client.client.mail.send.post(request_body=mail.get())
