from sqlalchemy.orm import Session
from models import ContactCSV


def create(
    s3_uri: str,
    s3_bucket: str,
    user_id: int,
    db: Session,
) -> ContactCSV:
    contact_csv = ContactCSV(
        s3_uri=s3_uri,
        s3_bucket=s3_bucket,
        user_id=user_id,
    )
    db.add(contact_csv)
    db.commit()
    db.refresh(contact_csv)
    return contact_csv
