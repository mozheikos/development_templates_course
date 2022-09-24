from api.schema import CoursesListResponse
from web_framework.views import ListView, JSONViewMixin

from mainapp.models import Courses


class CoursesList(JSONViewMixin, ListView):
    """Courses List endpoint"""
    model = Courses

    def get(self) -> dict:
        courses = self.get_queryset()
        return CoursesListResponse(result=[x.__dict__ for x in courses]).dict()
