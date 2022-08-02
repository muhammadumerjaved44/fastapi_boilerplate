from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql.schema import Column
from db.session import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    school_email = Column(String(255))
    personal_email = Column(String(255))
    mobile_phone_number = Column(String(20))
    home_phone_number = Column(String(20))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
