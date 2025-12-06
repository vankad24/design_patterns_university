from dataclasses import asdict
from enum import StrEnum

from src.core.singletone import Singleton
from src.models.abstract_model import AbstractModel


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
    PRODUCT_REMAINS = "product_remains"


class Repository(metaclass=Singleton):
    """
    Репозиторий для хранения всех моделей приложения в памяти.
    Использует паттерн Singleton для того, чтобы существовал только один экземпляр.

    __data: внутренний словарь вида {key: {id: объект}}, где key берется из RepoKeys
    """
    __data: dict[str, dict] = None

    # ключ для сохранения в конфиг
    CONFIG_KEY = 'models'

    def __init__(self):
        """
        Инициализация репозитория.
        Для каждого ключа из RepoKeys создается пустой словарь для хранения объектов.
        """
        self.__data = {}
        for key in RepoKeys:
            self.__data[str(key)] = {}  # ключи хранятся как строки

    @property
    def data(self) -> dict[str, dict]:
        """
        Доступ к данным репозитория.
        Возвращает внутренний словарь с объектами.
        """
        return self.__data

    def get_values(self, key) -> list:
        """
            Получить список всех значений по ключу из репозитория
        """
        return list(self.data[key].values())

    def dump(self) -> dict:
        """
            Возвращает словарь с данными для сохранения моделей
        """
        return {self.CONFIG_KEY: {key: map(lambda x: asdict(x.to_dto()), self.__data[key].values()) for key in self.__data}}
