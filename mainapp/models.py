"""Create your models here. Pay attention that all models must be inherited
web_framework.ext.models.Model"""
from typing import List

from web_framework.ext.decorators import register_model
from web_framework.ext.models import Model
from web_framework.notifications import Subject


@register_model
class Categories(Model):
    """Course categories"""
    def __init__(self, title: str, description: str, parent_id: int = None):
        super().__init__()
        self.title = title
        self.description = description
        self.category = self.set_parent_category(parent_id) if parent_id else parent_id
        self.children = []
        self.courses = []

    def get_courses(self) -> list:
        """get courses list"""
        result = [*self.courses]
        for category in self.children:
            result.extend(category.get_courses())

        return result

    def set_parent_category(self, parent_id: int):
        """
        Create two-direction connection between parent and child category
        :param parent_id: int
        :return: Categories
        """
        category = self.objects['categories'].get(parent_id, None)
        if not category:
            raise AttributeError(f"Category with id = {parent_id} does not exist")
        category.children.append(self)
        return category

    def __iter__(self):
        self.iterstate = -1
        return self

    def __next__(self):
        self.iterstate += 1
        if self.iterstate == len(self.courses):
            raise StopIteration
        return self.courses[self.iterstate]


@register_model
class Users(Model):
    """User"""

    def __init__(self, name: str, password: str, email: str, phone: str, age: int, is_staff: bool = False):
        super().__init__()
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.age = age
        self.is_staff = is_staff
        self.courses = []

    def join_course(self, course):
        course.students.append(self)
        self.courses.append(course)
        self.notify(f"Successfully joined course {course.title}")


class Student(Subject, Users):
    pass


class Teacher(Subject, Users):
    def __init__(self, name: str, password: str, email: str, phone: str, age: int, skill: str):
        super().__init__(name, password, email, phone, age, True)
        self.skill = skill


@register_model
class Courses(Model):
    def __init__(self, title: str, category_id: int, description: str, info: str):
        super().__init__()
        self.kind = self.get_kind()
        self.category = None
        self.title = title
        self.description = description
        self.info = info
        self.teacher = None
        self.students: List[Users] = []
        self.set_category(category_id)

    def _notify(self, msg: str):
        if self.teacher:
            self.teacher.notify(msg)
        for student in self.students:
            student.notify(msg)

    def add_teacher(self, teacher: Teacher):
        self.teacher = teacher
        teacher.courses.append(self)
        msg = f"Преподаватель {teacher.name} назначен на курс {self.title}"
        self._notify(msg)

    @classmethod
    def edit_course(cls, course_id: int, **kwargs):
        course: Courses = cls.get_by_id(course_id)
        for key, value in kwargs.items():
            if not hasattr(course, key):
                raise AttributeError(f"Wrong attribute: '{key}'")

            setattr(course, key, value)

        msg = f'В курсе {course.title} произошли изменения. Подробности на портале'
        course._notify(msg)

    @classmethod
    def get_kinds(cls) -> list:
        """Returns list of subclasses"""
        return cls.__subclasses__()

    @classmethod
    def get_kind(cls) -> str:
        """Returns kind of course by classname"""
        kind = list(cls.__name__)
        return ''.join(map(lambda x: f" {x.lower()}" if x.isupper() else x, kind)).strip()

    def set_category(self, category_id: int) -> None:
        """
        Create two-direction connection between course and category
        :param category_id: int
        """
        category: Categories = self.objects['categories'].get(category_id, None)
        if not category:
            raise AttributeError(f"Category with id = {category_id} does not exist")

        self.category = category
        category.courses.append(self)

    def __iter__(self):
        self.iterstate = -1
        return self

    def __next__(self):
        self.iterstate += 1
        if self.iterstate == len(self.students):
            raise StopIteration
        return self.students[self.iterstate]


class OfflineCourse(Courses):
    pass


class OnlineCourse(Courses):
    pass
