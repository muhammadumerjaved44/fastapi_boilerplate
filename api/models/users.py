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
    contacts = relationship("Contact", cascade="all, delete-orphan")
    contact_csvs = relationship("ContactCSV", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", cascade="all, delete-orphan")
