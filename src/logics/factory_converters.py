
from collections.abc import Iterable
from datetime import datetime
from types import NoneType
from typing import Type

from src.logics.converters.abstract_converter import AbstractConverter
from src.logics.converters.basic_converter import BasicConverter
from src.logics.converters.datetime_converter import DatetimeConverter
from src.logics.converters.dict_converter import DictConverter
from src.logics.converters.iterable_converter import IterableConverter
from src.logics.converters.model_converter import ModelConverter
from src.logics.turnover_balance_sheet import TurnoverBalanceItem
from src.models.abstract_model import AbstractModel
from src.models.validators.exceptions import ArgumentException

"""Класс-фабрика для конвертации объектов и списков в словарь"""
class FactoryConverters:
    # Определяем словарь, который сопоставляет базовые типы с соответствующими конвертерами.
    _type_to_converter = {
        (bool, int, float, str, NoneType): BasicConverter,
        datetime: DatetimeConverter,
        (AbstractModel, TurnoverBalanceItem): ModelConverter,
        dict: DictConverter,
        Iterable: IterableConverter,
    }

    @staticmethod
    def get_converter(t: Type) -> AbstractConverter:
        """
        Возвращает соответствующий конвертер для заданного типа.
        """
        # Итерируем по ключам словаря (типам или кортежам типов)
        for types, converter_class in FactoryConverters._type_to_converter.items():
            # Превращаем types в кортеж, если это не кортеж (например, datetime)
            if not isinstance(types, tuple):
                types = (types,)

            if issubclass(t, types):
                return converter_class()

        # Если конвертер не найден
        raise ArgumentException(f"Не удалось создать конвертер для типа:'{t.__name__}'")

    @staticmethod
    def convert(obj):
        return FactoryConverters.get_converter(type(obj)).convert(obj)