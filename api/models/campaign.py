from xmlrpc.client import Boolean
from sqlalchemy.sql import func
from sqlalchemy import Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.sql.schema import Column
from db.session import Base


class Campaign(Base):
    """This model has user's broadcasted campaign/message details"""

    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True, index=True)
    via_sms = Column(Boolean)
    via_email = Column(Boolean)
    audience_number = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
