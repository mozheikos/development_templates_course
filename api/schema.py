"""Data models for api"""
from typing import List

from pydantic import BaseModel


class CourseItem(BaseModel):
    id: int
    kind: str
    title: str
    description: str
    info: str


class CoursesListResponse(BaseModel):
    result: List[CourseItem]
