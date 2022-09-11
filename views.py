"""Module to implement views. View must be Callable, takes 1 argument: request
and must return instance of web_framework.ext.responses.Response or it child-class"""
import datetime

from schema import AccountInfo
from ton_client_api import TonClientAPI
from web_framework.ext.responses import HTMLResponse
from web_framework.ext.status import Status
from web_framework.ext.utils import render_html


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
    response = render_html('index.html', context)
    return HTMLResponse(body=response, status=Status.HTTP_200_OK)


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

    response = render_html('contact.html', context)
    return HTMLResponse(body=response, status=Status.HTTP_200_OK)


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
    response = render_html('address.html', context)
    return HTMLResponse(body=response, status=Status.HTTP_200_OK)
