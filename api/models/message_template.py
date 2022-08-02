from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql.schema import Column
from db.session import Base


class MessageTemplate(Base):
    __tablename__ = "message_template"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
