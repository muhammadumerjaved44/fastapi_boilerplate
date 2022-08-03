from pydantic import BaseModel


class RequestDemoIn(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone_number: str
    job_title: str
    institute: str


class RequestDemoOut(BaseModel):
    message: str
