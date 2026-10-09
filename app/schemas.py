from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import date, datetime
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    enrollment_date: Optional[date] = None

    @field_validator('date_of_birth')
    @classmethod
    def dob_not_future(cls, v: date):
        if v > date.today():
            raise ValueError('date_of_birth cannot be in the future')
        return v

    @field_validator('enrollment_date')
    @classmethod
    def enrollment_not_future(cls, v: Optional[date]):
        if v and v > date.today():
            raise ValueError('enrollment_date cannot be in the future')
        return v

    @model_validator(mode='after')
    def check_contact(self):
        if not self.email and not self.phone:
            raise ValueError('At least one of email or phone must be provided')
        return self

class StudentCreate(StudentBase):
    student_id: str = Field(..., min_length=1, max_length=20, pattern=r'^[A-Za-z0-9_-]+$')

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    enrollment_date: Optional[date] = None

    @field_validator('date_of_birth')
    @classmethod
    def dob_not_future(cls, v: Optional[date]):
        if v and v > date.today():
            raise ValueError('date_of_birth cannot be in the future')
        return v

    @field_validator('enrollment_date')
    @classmethod
    def enrollment_not_future(cls, v: Optional[date]):
        if v and v > date.today():
            raise ValueError('enrollment_date cannot be in the future')
        return v

class StudentReplace(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    student_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

class AskResponse(BaseModel):
    answer: str
    model: str
    records_used: int