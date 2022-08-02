from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql.schema import Column
from db.session import Base


class MessageTemplate(Base):
    __tablename__ = "message_template"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(100), nullable=False)
    message = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
