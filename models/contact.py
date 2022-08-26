from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.schema import Column
from db.session import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    preferred_email = Column(String(255))
    crc_email = Column(String(255))
    application_email = Column(String(255))
    day_phone_number = Column(String(20))
    evening_phone_number = Column(String(20))
    major = Column(String(255))
    cac = Column(String(255))
    age = Column(Integer)
    gender = Column(String(50))
    race_ethnicity = Column(String(50))
    new_student = Column(Boolean)
    athlete = Column(Boolean)
    puente = Column(Boolean)
    diop = Column(Boolean)
    reported_disability = Column(Boolean)
    income_level_self_reported = Column(String(255))
    bog = Column(String(255))
    cal_works = Column(Boolean)
    eops = Column(Boolean)
    care = Column(Boolean)
    homeless = Column(Boolean)
    need_based_federal_aid = Column(Boolean)
    completed_units = Column(Integer)
    gpa = Column(Integer)
    units_completed_including_district = Column(Integer)
    enrolled_districtwide = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
