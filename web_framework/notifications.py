"""Module to implement pattern 'Observer' for notification"""
from typing import Set


class Notificator:
    """Base notificator"""
    def __init__(self, notify_field_name: str):
        self.field = notify_field_name
        self.subject = None

    def send(self, msg: str):
        raise NotImplementedError


"""Сейчас оба класса обсерверов выглядят одинково, но на самом деле алгоритм
отправки электронной почты и смс разный и методы send() в реальности должны
быть реализованы каждый по-своему"""


class EmailNotificator(Notificator):
    """Send notification to email"""

    def send(self, msg: str):

        address = getattr(self.subject, self.field, None)
        if address:
            print('-' * 50)
            print(f"Email notification\nto address: {address}\n\n{msg}")
            print('-' * 50)


class SMSNotificator(Notificator):
    """Send notification to phone"""

    def send(self, msg: str):

        phone = getattr(self.subject, self.field, None)
        if phone:
            print('-' * 50)
            print(f"SMS notification\nto phone: {phone}\n\n{msg}")
            print('-' * 50)


class Subject:
    """Base subject"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers: Set[Notificator] = set()

    def subscribe(self, observer: Notificator):
        observer.subject = self
        self._observers.add(observer)

    def unsubscribe(self, observer: Notificator):
        observer.subject = None
        self._observers.discard(observer)

    def notify(self, msg: str):
        for observer in self._observers:
            observer.send(msg)
