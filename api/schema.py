"""Data models for api"""
from typing import List

from pydantic import BaseModel, validator

from mainapp.models import Categories


class CourseItem(BaseModel):
    id: int
    kind: str
    category: str
    title: str
    description: str
    info: str

    @validator('category', pre=True)
    def get_category_title(cls, value: Categories) -> str:
        return value.title


class CoursesListResponse(BaseModel):
    result: List[CourseItem]
