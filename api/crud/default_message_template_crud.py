from sqlalchemy.orm import Session
from typing import Union
from models import DefaultMessageTemplate


def get_all(db: Session) -> Union[list[DefaultMessageTemplate], list]:
    default_message_templates = db.query(DefaultMessageTemplate).all()
    return default_message_templates
