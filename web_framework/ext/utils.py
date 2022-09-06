"""
Utils module
"""
import jinja2

from config import TEMPLATES_PATH


def render_html(template: str, context: dict) -> str:
    """
    Render jinja template
    :param template:
    :param context:
    :return:
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template(template)

    return template.render(context=context)
