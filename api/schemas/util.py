from typing import Union
from pydantic import BaseModel, EmailStr


class RequestDemoIn(BaseModel):
    email: EmailStr
    name: str
    phone_number: str
    job_title: str
    institute: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@mail.com",
                "name": "John Alexander",
                "phone_number": "12345678912",
                "job_title": "Administrator",
                "institute": "University of Houston",
            }
        }


class RequestDemoOut(BaseModel):
    message: str


class Contact(BaseModel):
    student_id: Union[str, None]
    first_name: str
    last_name: str
    preferred_email: str
    crc_email: Union[str, None]
    application_email: Union[str, None]
    day_phone_number: Union[str, None]
    evening_phone_number: Union[str, None]
    major: Union[str, None]
    cac: Union[str, None]
    age: Union[int, None]
    gender: Union[str, None]
    race_ethnicity: Union[str, None]
    new_student: Union[str, None]
    athlete: Union[str, None]
    puente: Union[str, None]
    diop: Union[str, None]
    reported_disability: Union[str, None]
    income_level_self_reported: Union[str, None]
    bog: Union[str, None]
    cal_works: Union[str, None]
    eops: Union[str, None]
    care: Union[str, None]
    homeless: Union[str, None]
    need_based_federal_aid: Union[str, None]
    completed_units: Union[float, None]
    gpa: Union[float, None]
    units_completed_including_district: Union[float, None]
    enrolled_districtwide: Union[str, None]

    class Config:
        orm_mode = True


class Contacts(BaseModel):
    contacts: list[Contact]


class MessageTagsOut(BaseModel):
    tags: list[str]


class MessageTemplate(BaseModel):
    subject: str
    message: str

    class Config:
        orm_mode = True


class MessageTemplatesOut(BaseModel):
    message_templates: list[MessageTemplate]
