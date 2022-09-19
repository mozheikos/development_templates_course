"""Module to implement views. View must be Callable, takes 1 argument: request
and must return instance of web_framework.ext.responses.Response or it child-class"""
import datetime
import os

from web_framework.ext.logging import Logger
from web_framework.ext.models import Engine
from web_framework.ext.responses import HTMLResponse
from web_framework.ext.utils import render_html, get_class_from_string

from models import Categories, Courses
from schema import AccountInfo
from ton_client_api import TonClientAPI


site = Engine()
logger = Logger.get_logger('main')
logger.path = os.path.join(os.getcwd(), 'log.log')


def index_view(request: dict) -> HTMLResponse:
    """
    Index handler
    :param request:
    :return:
    """
    context = {
        'title': 'Main page',
        'year': datetime.date.today().year
    }
    return render_html('index.html', context)


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


def address_view(request: dict) -> HTMLResponse:
    """
    address page
    :param request:
    :return:
    """
    context = {
        'title': 'Address',
        'year': datetime.date.today().year
    }
    info = AccountInfo(
        id='Account ID',
        acc_type_name='Frozen / Active / Deleted / Uninit',
        code_hash='Hash of account code',
        data_hash='Hash of account data'
    )
    if request['method'] == 'post':
        address = request['body'].get('address', None)
        if address:
            api = TonClientAPI()
            info = api.get_info(address=address)

    context['wallet'] = info.dict()
    return render_html('address.html', context)


def education_view(request: dict) -> HTMLResponse:
    context = {
        'title': 'Education',
        'year': datetime.date.today().year
    }
    return render_html('education.html', context)


def programm_view(request: dict) -> HTMLResponse:

    category_id = request['params'].get('category_id', 0)
    category = Categories.get_by_id(int(category_id))

    categories = list(filter(lambda x: x.category == category, Categories.get_list()))

    if category:
        courses = category.get_courses()

    else:
        courses = Courses.get_list()

    context = {
        'title': 'Programm',
        'year': datetime.date.today().year,
        'category': category,
        'categories': categories,
        'categories_total': len(categories),
        'courses': courses,
        'courses_total': len(courses)
    }
    return render_html('categories.html', context)


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
