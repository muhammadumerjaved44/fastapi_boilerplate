from pydantic import BaseModel


class RequestDemoIn(BaseModel):
    email: str
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
