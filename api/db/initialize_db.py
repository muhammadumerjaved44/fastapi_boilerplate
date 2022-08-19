from models import User, DefaultMessageTemplate
from db.session import SessionLocal
from config import settings
from auth import get_password_hash


def initialize_db():
    with SessionLocal() as db:
        super_user = (
            db.query(User).filter_by(email=settings.FIRST_SUPERUSER_EMAIL).one_or_none()
        )
        if not super_user:
            super_user = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_active=True,
                scope="superuser",
            )
            db.add(super_user)
            db.commit()
            db.refresh(super_user)

        default_templates = [
            {
                "subject": "Register Class Reminder",
                "message": 'Hi <span class="mention" data-mention="@first_name">@first_name</span>, don\'t forget to register for classes by August 1st.',
            },
            {
                "subject": "Tutoring Lab",
                "message": 'Hi <span class="mention" data-mention="@first_name">@first_name</span>, our tutoring lab is open M-F from 8:00am to 5:00pm.',
            },
            {
                "subject": "First Day",
                "message": "Good morning! Welcome to the first day of classes!",
            },
            {
                "subject": "Financial Aid Reminder",
                "message": "If you haven't filed for financial aid, make sure you do it before the deadline on Friday.",
            },
            {
                "subject": "FASFA Incomplete Reminder",
                "message": 'Hi <span class="mention" data-mention="@first_name">@first_name</span>, your FASFA is incomplete. Call 555-555-5555 if you need help completing it.',
            },
        ]
        default_template_exist = db.query(DefaultMessageTemplate).first()
        if not default_template_exist:
            for default_template in default_templates:
                new_default_template = DefaultMessageTemplate(
                    subject=default_template["subject"],
                    message=default_template["message"],
                )
                db.add(new_default_template)
                db.commit()
                db.refresh(new_default_template)
