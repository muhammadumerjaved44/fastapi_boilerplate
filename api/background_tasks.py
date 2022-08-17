import boto3
from config import settings
from fastapi import UploadFile
from datetime import datetime
import os
from models import Contact, ContactCSV
from schemas import Contacts
from db.session import SessionLocal
from sendgrid import SendGridAPIClient
import sendgrid.helpers.mail as sendgrid_mail_helper
from bs4 import BeautifulSoup

s3 = boto3.resource(
    "s3",
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
)

s3_bucket = s3.Bucket(settings.S3_CSV_BUCKET)

sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)


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
        contact_csv = ContactCSV(
            s3_uri=object.key,
            s3_bucket=object.bucket_name,
            user_id=user_id,
        )
        db.add(contact_csv)
        db.commit()


def save_csv_contacts(user_id: int, contacts: Contacts):
    # add or update contacts in db
    with SessionLocal() as db:
        contacts_obj_list = []

        for record in contacts:
            instance = (
                db.query(Contact)
                .filter_by(preferred_email=record.preferred_email, user_id=user_id)
                .one_or_none()
            )
            if instance:
                for attr, new_val in record.dict().items():
                    setattr(instance, attr, new_val)
            else:
                create_kwargs = record.dict()
                contacts_obj_list.append(Contact(**create_kwargs, user_id=user_id))

        db.add_all(contacts_obj_list)
        db.commit()


def broadcast_emails(emails: list[str], message: str, subject: str, user_id: int):
    soup = BeautifulSoup(message, "html.parser")
    tag_spans = soup.select('span[class="mention"]')
    tag_values = dict()

    for email in emails:

        with SessionLocal() as db:
            message_personal = f"{message}"
            contact = (
                db.query(Contact)
                .filter_by(preferred_email=email, user_id=user_id)
                .one_or_none()
            )

            if contact is not None:
                contact_dict = contact.__dict__
                tag_values = dict()
                for tag_span in tag_spans:
                    tag_value = contact_dict[tag_span.text.replace("@", "")]
                    message_personal = message_personal.replace(
                        str(tag_span), tag_value
                    )
                    tag_values[str(tag_span)] = tag_value

                from_email = sendgrid_mail_helper.Email(settings.STELLO_EMAIL)
                to_email = sendgrid_mail_helper.To(email)
                content = sendgrid_mail_helper.Content(
                    "text/html", f"{message_personal}"
                )
                mail = sendgrid_mail_helper.Mail(from_email, to_email, subject, content)
                sendgrid_response = sendgrid_client.client.mail.send.post(
                    request_body=mail.get()
                )


def send_email(to_email: str, subject: str, message: str):
    from_email = sendgrid_mail_helper.Email(settings.STELLO_EMAIL)
    to_email = sendgrid_mail_helper.To(to_email)
    content = sendgrid_mail_helper.Content("text/plain", f"{message}")
    mail = sendgrid_mail_helper.Mail(from_email, to_email, subject, content)
    sendgrid_response = sendgrid_client.client.mail.send.post(request_body=mail.get())
