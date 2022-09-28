from api.schema import CoursesListResponse
from web_framework.views import ListView, JSONViewMixin

from mainapp.models import Course


class CoursesList(JSONViewMixin, ListView):
    """Courses List endpoint"""
    model = Course

    def get(self) -> dict:
        courses = self.get_queryset()
        return CoursesListResponse(result=[x.dict() for x in courses]).dict()
