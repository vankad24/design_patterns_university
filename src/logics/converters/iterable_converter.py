
from src.logics.converters.abstract_converter import AbstractConverter
from src.logics.factory_converters import FactoryConverters

"""Конвертер для итерируемых объектов"""
class IterableConverter(AbstractConverter):

    """Переопределённый метод convert"""
    def convert(self, obj):
        result = []
        for item in obj:
            result.append(FactoryConverters.convert(item))
        return result

