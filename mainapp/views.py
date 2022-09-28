"""Module to implement views. View must be Callable, takes 1 argument: request
and must return instance of web_framework.ext.responses.Response or it child-class"""
import datetime

from mainapp.models import Category, Student, Course, Teacher, StudentsCourses
from mainapp.schema import CreateStudentRequest, CourseEditRequest, JoinCourseRequest
from web_framework.ext.logging import Logger, FileLogger, ConsoleLogger
from web_framework.ext.models import Engine
from web_framework.ext.responses import HTMLResponse
from web_framework.ext.utils import render_html
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
    category = site.objects.get_by_id(Category, int(category_id))
    if category:
        categories = site.objects.filter(Category, 'category_id', category.id)
        courses = site.objects.filter(Course, 'category_id', category.id)
    else:
        categories = [x for x in site.objects.get_list(Category) if x.category_id is None]
        courses = site.objects.get_list(Course)

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
        context['parent'] = site.objects.get_by_id(Category, parent_id)

    else:
        parent_id = int(request['body'].get('parent'))
        cat_title = request['body'].get('title')
        cat_description = request['body'].get('description')
        category = Category(
            pk=None,
            title=cat_title,
            description=cat_description,
            category_id=parent_id or None
        )
        site.objects.create(category)
        site.objects.commit()
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
        context["category"] = site.objects.get_by_id(Category, int(category_id))
        context['kinds'] = ['online course', 'offline course']

    else:
        kind = request['body'].get('cls')
        category_id = int(request['body'].get('category_id'))
        title = request['body'].get('title')
        description = request['body'].get('description')
        info = request['body'].get('info')
        course = Course(
            pk=None,
            title=title,
            description=description,
            category_id=category_id,
            kind=kind,
            info=info
        )
        site.objects.create(course)
        site.objects.commit()
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
        student = self.model(**self.request.body.dict())
        self.engine.objects.create(student)
        self.engine.objects.commit()

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
        courses = self.engine.objects.get_list(Course)
        context[self.collection_tag].courses = [
            x.course
            for x in self.engine.objects.filter(
                StudentsCourses, 'student_id', context[self.collection_tag].id
            )
        ]
        context['courses'] = courses
        return context

    def post(self) -> dict:
        student = self.engine.objects.get_by_id(Student, self.request.body.student_id)
        join = StudentsCourses(**self.request.body.dict())
        self.engine.objects.create(join)
        self.engine.objects.commit()
        student.courses = [
            x.course for x in self.engine.objects.filter(StudentsCourses, 'student_id', student.id)
        ]
        return {
            'student': student,
            'courses': self.engine.objects.get_list(Course)
        }


class ViewCourse(TemplateViewMixin, DetailView):
    """Detail info about course"""
    collection_tag = 'course'
    model = Course
    template = 'course_detail.html'
    context_params = {
        'title': 'Course Details',
        'year': datetime.date.today().year
    }


class EditCourse(TemplateViewMixin, DetailView):
    model = Course
    template = 'course_edit_form.html'
    request_model = CourseEditRequest
    collection_tag = 'course'
    context_params = {
        'title': 'Edit course',
        'year': datetime.date.today().year
    }

    def post(self):
        course = self.engine.objects.get_by_id(self.model, self.request.body.course_id)
        course.edit_course(**self.request.body.dict(exclude_none=True, exclude={'course_id'}))
        self.engine.objects.update(course)
        self.engine.objects.commit()
        students = [x.student for x in self.engine.objects.filter(StudentsCourses, 'course_id', course.id)]
        for student in students:
            student.notify(f"Course {course.title} edited.")

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
