"""Create your models here. Pay attention that all models must be inherited
web_framework.ext.models.Model"""
from typing import Optional, List

from web_framework.database.types import Field, INTEGER, TEXT
from web_framework.ext.decorators import register_model
from web_framework.ext.models import Model, Engine
from web_framework.notifications import Subject, EmailNotificator, SMSNotificator


engine = Engine()


@register_model
class Category(Model):

    __tablename__ = 'categories'

    id = Field(INTEGER, primary_key=True, autoincrement=True)
    title = Field(TEXT)
    description = Field(TEXT)
    category_id = Field(INTEGER, nullable=True)

    def __init__(self, pk: Optional[int], title: str, description: str, category_id: int):
        super().__init__(pk)
        self.title = title
        self.description = description
        self.category_id = category_id
        self.courses = []

    @property
    def category(self):
        return engine.objects.get_by_id(self.__class__, self.category_id)


class User(Subject, Model):
    __tablename__ = ''

    def __init__(
            self, pk: Optional[int], name: str, password: str,
            email: str, phone: str, age: int, subscribe_email: int = 0, subscribe_sms: int = 0
    ):
        super().__init__(pk)
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.age = age
        self.subscribe_email = subscribe_email
        self.subscribe_sms = subscribe_sms
        if self.subscribe_email:
            notificator_email = EmailNotificator()
            self.subscribe(notificator_email)
        if self.subscribe_sms:
            notificator_sms = SMSNotificator()
            self.subscribe(notificator_sms)


@register_model
class Student(User):
    __tablename__ = 'students'

    id = Field(INTEGER, primary_key=True, autoincrement=True)
    name = Field(TEXT)
    password = Field(TEXT)
    email = Field(TEXT)
    phone = Field(TEXT)
    age = Field(INTEGER)
    subscribe_email = Field(INTEGER)
    subscribe_sms = Field(INTEGER)

    def __init__(
            self, pk: Optional[int], name: str, password: str,
            email: str, phone: str, age: int, subscribe_email: int = 0, subscribe_sms: int = 0
    ):
        super().__init__(pk, name, password, email, phone, age, subscribe_email, subscribe_sms)
        self.courses = []


@register_model
class Teacher(User):
    __tablename__ = 'teachers'

    id = Field(INTEGER, primary_key=True, autoincrement=True)
    name = Field(TEXT)
    password = Field(TEXT)
    email = Field(TEXT)
    phone = Field(TEXT)
    age = Field(INTEGER)
    skill = Field(TEXT)
    subscribe_email = Field(INTEGER)
    subscribe_sms = Field(INTEGER)

    def __init__(
            self, pk: Optional[int], name: str, password: str, email: str,
            phone: str, age: int, skill: str, subscribe_email: int = 0, subscribe_sms: int = 0
    ):
        super().__init__(pk, name, password, email, phone, age, subscribe_email, subscribe_sms)
        self.skill = skill
        self.courses = []


@register_model
class Course(Model):
    __tablename__ = 'courses'

    id = Field(INTEGER, primary_key=True, autoincrement=True)
    title = Field(TEXT, nullable=False)
    description = Field(TEXT)
    category_id = Field(INTEGER, nullable=False)
    teacher_id = Field(INTEGER)
    kind = Field(TEXT, nullable=False)
    info = Field(TEXT)

    def __init__(
            self, pk: Optional[int], title: str, description: str,
            category_id: int, teacher_id: Optional[int], kind: str, info: str
    ):
        super().__init__(pk)
        self.title = title
        self.description = description
        self.category_id = category_id
        self.teacher_id = teacher_id
        self.kind = kind
        self.info = info
        self.students: List[Student] = []

    @property
    def teacher(self):
        return engine.objects.get_by_id(Teacher, self.teacher_id)

    @property
    def category(self):
        return engine.objects.get_by_id(Category, self.category_id)

    def edit_course(self, **kwargs):
        for k, v in kwargs.items():
            try:
                self.__dict__[k] = v
            except KeyError:
                continue


@register_model
class StudentsCourses(Model):
    __tablename__ = 'students_courses'

    id = Field(INTEGER, primary_key=True, autoincrement=True)
    student_id = Field(INTEGER, nullable=False)
    course_id = Field(INTEGER, nullable=False)

    def __init__(self, pk: Optional[int], student_id: int, course_id: int):
        super().__init__(pk)
        self.student_id = student_id
        self.course_id = course_id

    @property
    def student(self):
        return engine.objects.get_by_id(Student, self.student_id)

    @property
    def course(self):
        return engine.objects.get_by_id(Course, self.course_id)
