"""Module with data models"""


class Model:
    """Abstract Factory"""

    increment: int = 0
    objects: dict = {}

    def __init_subclass__(cls, **kwargs):
        """Creation of objects dict keys"""
        if cls.__base__ == Model:
            cls.objects[cls.__name__.lower()] = {}

    @classmethod
    def get_id(cls) -> int:
        """Classmethod for get autoincremented id"""
        cls.increment += 1
        return cls.increment

    @staticmethod
    def create(cls, *args, **kwargs):
        """Creation instances"""

        # Не уверен, к какому паттерну это следует отнести: Абстрактная фабрика или фабричнй метод.
        # Получается, что это вроде как фабричный метод, только не зависящий по сути от конкретного
        # класса. Но наверное все же фабричный метод.
        if isinstance(cls, str):
            cls = eval(cls)

        parent = cls.__mro__[-3]
        instance = cls.__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.id = parent.get_id()

        collection = Model.objects.get(parent.__name__.lower(), None)

        if collection is None:
            raise AttributeError(f"Class {parent.__name__} must be inherited from Model")

        collection[instance.id] = instance

        return instance

    @classmethod
    def get_list(cls) -> list:
        """Get all objects list"""
        key = cls.__mro__[-3].__name__.lower()
        return [x for x in cls.objects.get(key).values() if isinstance(x, cls)]

    @classmethod
    def get_by_id(cls, instance_id: int):
        """Get instance by id"""
        key = cls.__mro__[-3].__name__.lower()
        return cls.objects[key].get(instance_id, None)


class Engine:
    """Main engine class"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton realization"""
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.models = Model
