"""Create your models here. Pay attention that all models must be inherited
web_framework.ext.models.Model"""

from web_framework.ext.models import Model


class Categories(Model):
    """Course categories"""
    def __init__(self, title: str, description: str, parent_id: int = None):
        super().__init__()
        self.title = title
        self.description = description
        self.category = self.set_parent_category(parent_id) if parent_id else parent_id
        self.children = []
        self.courses = []

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


class Users(Model):
    """User"""
    def __init__(self, name: str, age: int, is_staff: bool = False):
        super().__init__()
        self.name = name
        self.age = age
        self.is_staff = is_staff


class Student(Users):
    pass


class Teacher(Users):
    def __init__(self, name: str, age: int, skill: str):
        super().__init__(name, age, True)
        self.skill = skill


class Courses(Model):
    def __init__(self, title: str, category_id: int, description: str, info: str):
        super().__init__()
        self.kind = self.get_kind()
        self.category = None
        self.title = title
        self.description = description
        self.info = info
        self.set_category(category_id)

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


class OfflineCourse(Courses):
    pass


class OnlineCourse(Courses):
    pass
