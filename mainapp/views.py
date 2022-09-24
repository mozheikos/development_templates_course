"""Module to implement views. View must be Callable, takes 1 argument: request
and must return instance of web_framework.ext.responses.Response or it child-class"""
import datetime
import os

from mainapp.models import Categories, Courses, Student
from mainapp.schema import CreateStudentRequest, CourseEditRequest, JoinCourseRequest
from web_framework.ext.logging import Logger, FileLogger, ConsoleLogger
from web_framework.ext.models import Engine
from web_framework.ext.responses import HTMLResponse
from web_framework.ext.utils import render_html, get_class_from_string
from web_framework.notifications import EmailNotificator, SMSNotificator
from web_framework.router import Router
from web_framework.views import CreateView, TemplateViewMixin, DetailView, ListView

site = Engine()

logger = Logger.get_logger('main')

file_logger = FileLogger('log.log')
console_logger = ConsoleLogger()

logger.add_logger(file_logger)
logger.add_logger(console_logger)

router = Router(namespace='education')


def contacts_view(request: dict) -> HTMLResponse:
    """
    contacts page
    :param request:
    :return:
    """
    context = {
        'title': 'Contacts',
        'year': datetime.date.today().year
    }
    if request['method'] == 'post':
        user = request['body'].get('user_name', '')
        email = request['body'].get('user_email', '')
        message = request['body'].get('user_message', '')
        alert = f"New email message\nUser: {user}\nAddress: {email}\nText: {message}"
        print(alert)

        context['display'] = 'block'
        context['result'] = 'Success'

    else:
        context['display'] = 'none'

    return render_html('contact.html', context)


def index_view(request: dict) -> HTMLResponse:
    context = {
        'title': 'Education',
        'year': datetime.date.today().year
    }
    return render_html('index.html', context)


@router.route('/')
def education_view(request: dict) -> HTMLResponse:

    category_id = request['params'].get('category_id', 0)
    category = Categories.get_by_id(int(category_id))

    categories = list(filter(lambda x: x.category == category, Categories.get_list()))

    if category:
        courses = category.get_courses()

    else:
        courses = Courses.get_list()

    context = {
        'title': 'Education',
        'year': datetime.date.today().year,
        'category': category,
        'categories': categories,
        'categories_total': len(categories),
        'courses': courses,
        'courses_total': len(courses)
    }
    return render_html('categories.html', context)


@router.route('/add_category')
def create_category(request: dict) -> HTMLResponse:

    context = {
        'title': 'Add category',
        'year': datetime.date.today().year
    }

    if request['method'] == 'get':
        parent_id = int(request['params'].get('parent_id', 0))
        context['parent'] = Categories.get_by_id(parent_id)

    else:
        parent_id = int(request['body'].get('parent'))
        cat_title = request['body'].get('title')
        cat_description = request['body'].get('description')

        category = site.models.create(Categories, cat_title, cat_description, parent_id or None)

        context['created'] = category.id

        logger.log(f"Category {category.title} created")
    return render_html('category_form.html', context)


@router.route('/add_course')
def create_course(request: dict) -> HTMLResponse:

    context = {
        'title': 'Add category',
        'year': datetime.date.today().year
    }

    if request['method'] == 'get':
        category_id = request['params'].get('category_id')
        context["category"] = Categories.get_by_id(int(category_id))
        context['kinds'] = Courses.get_kinds()

    else:
        kind = get_class_from_string(Courses, request['body']['cls'])
        category_id = int(request['body'].get('category_id'))
        title = request['body'].get('title')
        description = request['body'].get('description')
        info = request['body'].get('info')
        site.models.create(kind, title, category_id, description, info)
        context['created'] = category_id

        logger.log(f"Course {title} created")

    return render_html('course_form.html', context)


class CreateStudent(TemplateViewMixin, CreateView):
    request_model = CreateStudentRequest
    model = Student
    template = 'register_form.html'
    context_params = {
        'title': "Registration",
        'year': datetime.date.today().year
    }

    def get(self):
        return {}

    def post(self):
        student = self.engine.models.create(
            self.model,
            **self.request.body.dict(exclude={'subscribe_email', 'subscribe_sms'})
        )

        if self.request.body.subscribe_email:
            email_notificator = EmailNotificator('email')
            student.subscribe(email_notificator)
        if self.request.body.subscribe_sms:
            sms_notificator = SMSNotificator('phone')
            student.subscribe(sms_notificator)

        return {
            'created': True
        }


class StudentProfile(TemplateViewMixin, DetailView):
    model = Student
    collection_tag = 'student'
    template = 'student_profile.html'
    request_model = JoinCourseRequest
    context_params = {
        'title': 'Student Profile',
        'year': datetime.date.today().year
    }

    def get(self) -> dict:
        context = super().get()
        courses = Courses.get_list()
        context['courses'] = courses
        return context

    def post(self) -> dict:
        student = Student.get_by_id(self.request.body.student_id)
        course = Courses.get_by_id(self.request.body.course_id)
        student.join_course(course)
        return {
            'student': student,
            'courses': Courses.get_list()
        }


class ViewCourse(TemplateViewMixin, DetailView):
    """Detail info about course"""
    collection_tag = 'course'
    model = Courses
    template = 'course_detail.html'
    context_params = {
        'title': 'Course Details',
        'year': datetime.date.today().year
    }


class EditCourse(TemplateViewMixin, DetailView):
    model = Courses
    template = 'course_edit_form.html'
    request_model = CourseEditRequest
    collection_tag = 'course'
    context_params = {
        'title': 'Edit course',
        'year': datetime.date.today().year
    }

    def post(self):

        self.model.edit_course(**self.request.body.dict(exclude_none=True))
        course = self.model.get_by_id(self.request.body.course_id)
        return {
            'created': course.id,
            'course': course
        }


class StudentsList(TemplateViewMixin, ListView):
    template = 'students.html'
    model = Student
    collection_tag = 'students'
    context_params = {
        'title': 'Students',
        'year': datetime.date.today().year
    }