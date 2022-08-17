from sqlalchemy import Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.sql.schema import Column
from db.session import Base


class ContactCSV(Base):
    """This model has users uploaded csv's details"""

    __tablename__ = "contact_csv"

    id = Column(Integer, primary_key=True, index=True)
    s3_uri = Column(String(255))
    s3_bucket = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
