from enum import StrEnum

from src.core.singletone import Singleton


class RepoKeys(StrEnum):
    """
    Ключи для доступа к различным типам данных в репозитории.
    Используется как единый источник, чтобы избежать "магических строк".
    """
    MEASUREMENT_UNITS = "measurement_units"
    PRODUCT_GROUPS = "product_groups"
    PRODUCTS = "products"
    INGREDIENTS = "ingredients"
    RECIPES = "recipes"
    STORAGES = "storages"
    TRANSACTIONS = "transactions"


class Repository(metaclass=Singleton):
    """
    Репозиторий для хранения всех моделей приложения в памяти.
    Использует паттерн Singleton для того, чтобы существовал только один экземпляр.

    __data: внутренний словарь вида {key: {id: объект}}, где key берется из RepoKeys
    """
    __data: dict = None

    def __init__(self):
        """
        Инициализация репозитория.
        Для каждого ключа из RepoKeys создается пустой словарь для хранения объектов.
        """
        self.__data = {}
        for key in RepoKeys:
            self.__data[str(key)] = {}  # ключи хранятся как строки

    @property
    def data(self):
        """
        Доступ к данным репозитория.
        Возвращает внутренний словарь с объектами.
        """
        return self.__data
