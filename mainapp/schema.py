"""
Module define dataclasses
"""
from typing import Optional, Dict

from pydantic import BaseModel, validator, root_validator

from web_framework.ext.schema import BaseRequest


class AccountInfo(BaseModel):
    """Account data model"""

    id: str
    acc_type_name: str
    balance: float = 0.0
    code_hash: str
    data_hash: str

    @validator('balance', pre=True)
    def get_balance(cls, value: str) -> float:
        """Converts blockchain account balance to real EVER"""
        return int(value) / 10**9


class CreateStudent(BaseModel):
    name: str
    password: str
    email: str
    phone: str
    age: int
    is_staff: bool = False
    subscribe_email: bool = False
    subscribe_sms: bool = False


class CreateStudentRequest(BaseRequest):
    """Register Student Request model"""
    body: Optional[CreateStudent]


class CourseEdit(BaseModel):
    course_id: int
    title: Optional[str]
    description: Optional[str]
    info: Optional[str]

    @root_validator(pre=True)
    def pop_unset(cls, values: Dict[str, str]) -> Dict[str, Optional[str]]:
        return {k: v for k, v in values.items() if v}


class CourseEditRequest(BaseRequest):
    body: Optional[CourseEdit]


class JoinCourse(BaseModel):
    student_id: int
    course_id: int


class JoinCourseRequest(BaseRequest):
    body: Optional[JoinCourse]