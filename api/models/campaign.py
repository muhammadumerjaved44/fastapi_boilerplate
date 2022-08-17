from xmlrpc.client import Boolean
from sqlalchemy.sql import func
from sqlalchemy import Integer, DateTime, Boolean, String, ForeignKey
from sqlalchemy.sql.schema import Column
from db.session import Base


class Campaign(Base):
    """This model has user's broadcasted campaign/message details"""

    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True, index=True)
    via_sms = Column(Boolean, nullable=False)
    via_email = Column(Boolean, nullable=False)
    message = Column(String(1000), nullable=False)
    audience_number = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
