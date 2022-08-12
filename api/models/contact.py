from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.sql.schema import Column
from db.session import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    preferred_email = Column(String(255), unique=True)
    crc_email = Column(String(255))
    application_email = Column(String(255))
    day_phone_number = Column(String(20))
    evening_phone_number = Column(String(20))
    major = Column(String(255))
    cac = Column(String(255))
    age = Column(Integer)
    gender = Column(String(50))
    race_ethnicity = Column(String(50))
    new_student = Column(String(50))
    athlete = Column(String(50))
    puente = Column(String(50))
    diop = Column(String(50))
    reported_disability = Column(String(50))
    income_level_self_reported = Column(String(255))
    bog = Column(String(255))
    cal_works = Column(String(50))
    eops = Column(String(50))
    care = Column(String(50))
    homeless = Column(String(50))
    need_based_federal_aid = Column(String(50))
    completed_units = Column(Float)
    gpa = Column(Float)
    units_completed_including_district = Column(Float)
    enrolled_districtwide = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
