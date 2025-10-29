
from src.logics.converters.abstract_converter import AbstractConverter

"""Конвертер для итерируемых объектов"""
class IterableConverter(AbstractConverter):

    """Переопределённый метод convert"""
    def convert(self, obj):
        result = []
        for item in obj:
            from src.logics.factory_converters import FactoryConverters
            result.append(FactoryConverters.convert(item))
        return result

