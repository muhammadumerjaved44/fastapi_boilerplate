from typing import Optional
from sqlalchemy.orm import Session
from models import Contact


def get_by_preferred_email(
    preferred_email: str, user_id: int, db: Session
) -> Optional[Contact]:
    contact = (
        db.query(Contact)
        .filter(Contact.preferred_email == preferred_email, user_id == user_id)
        .first()
    )
    return contact


def create_multi(contacts: list[Contact], db: Session):
    db.add_all(contacts)
    db.commit()
    return
