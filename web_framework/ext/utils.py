"""
Utils module
"""
import jinja2
from typing import Type

from config import TEMPLATES_PATH
from web_framework.ext.responses import HTMLResponse
from web_framework.ext.status import Status


def render_html(template: str, context: dict) -> HTMLResponse:
    """
    Render jinja template
    :param template:
    :param context:
    :return:
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template(template)

    return HTMLResponse(body=template.render(context=context), status=Status.HTTP_200_OK)


def get_class_from_string(cls: Type, name: str) -> Type:
    """Return sublclass of class (cls) by int name"""
    for item in cls.__subclasses__():
        if item.__name__ == name:
            return item
