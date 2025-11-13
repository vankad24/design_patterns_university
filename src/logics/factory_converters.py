
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
    """
    Фабрика, предназначенная для выбора и создания подходящего объекта-конвертера
    (наследника AbstractConverter) на основе типа входного объекта.
    Используется для стандартизированного преобразования различных типов данных
    (модели, даты, списки, базовые типы) в словарь или другую форму для дальнейшей сериализации (например, в JSON).
    """
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
        Возвращает соответствующий экземпляр конвертера для заданного типа `t`.

        Метод итерирует по зарегистрированным типам и проверяет, является ли
        заданный тип `t` подклассом одного из зарегистрированных типов (или совпадает с ним).

        :param t: Тип объекта, для которого требуется конвертер.
        :return: Экземпляр соответствующего класса-конвертера (наследника AbstractConverter).
        :raises ArgumentException: Если подходящий конвертер для типа не найден.
        """
        # Итерируем по ключам словаря (типам или кортежам типов)
        for types, converter_class in FactoryConverters._type_to_converter.items():
            # Превращаем types в кортеж, если это не кортеж (например, datetime)
            if not isinstance(types, tuple):
                types = (types,)

            # Проверяем, является ли t подклассом любого из типов в кортеже 'types'.
            if issubclass(t, types):
                return converter_class()

        # Если конвертер не найден
        raise ArgumentException(f"Не удалось создать конвертер для типа:'{t.__name__}'")

    @staticmethod
    def convert(obj):
        """
        Основной метод конвертации.

        Получает конвертер, соответствующий типу объекта `obj`, и вызывает его метод `convert()`.

        :param obj: Объект любого типа для конвертации.
        :return: Результат работы метода `convert` выбранного конвертера (обычно словарь).
        """
        return FactoryConverters.get_converter(type(obj)).convert(obj)