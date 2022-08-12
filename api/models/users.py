from sqlalchemy import Integer, String, Boolean
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=False)
    scope = Column(String(10))
    contacts = relationship("Contact")
    contact_csvs = relationship("ContactCSV")
    campaigns = relationship("Campaign")
