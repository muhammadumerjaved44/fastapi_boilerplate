from sqlalchemy.orm import Session
from models import Campaign


def create(
    via_sms: bool,
    via_email: bool,
    message: str,
    audience_number: int,
    user_id: int,
    db: Session,
) -> Campaign:
    campaign = Campaign(
        via_sms=via_sms,
        via_email=via_email,
        message=message,
        audience_number=audience_number,
        user_id=user_id,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign
