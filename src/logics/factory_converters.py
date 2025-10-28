
from datetime import datetime
from collections.abc import Iterable
from src.logics.converters.abstract_converter import AbstractConverter
from src.logics.converters.basic_converter import BasicConverter
from src.logics.converters.datetime_converter import DatetimeConverter
from src.logics.converters.dict_converter import DictConverter
from src.logics.converters.iterable_converter import IterableConverter
from src.logics.converters.model_converter import ModelConverter
from src.models.abstract_model import AbstractModel
from src.models.validators.exceptions import ArgumentException

"""Класс-фабрика для конвертации объектов и списков в словарь"""
class FactoryConverters:
    @staticmethod
    def get_converter(t: type) -> AbstractConverter:
        if t is None or issubclass(t, (bool, int, float, str)):
            return BasicConverter()
        elif issubclass(t, (datetime,)):
            return DatetimeConverter()
        elif issubclass(t, (AbstractModel,)):
            return ModelConverter()
        elif issubclass(t, (dict,)):
            return DictConverter()
        elif issubclass(t, (Iterable,)):
            return IterableConverter()
        else:
            raise ArgumentException(f"Не удалось создать конвертер для типа:'{t.__name__}'")

    @staticmethod
    def convert(obj):
        return FactoryConverters.get_converter(type(obj)).convert(obj)