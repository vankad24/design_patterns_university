
from src.logics.converters.abstract_converter import AbstractConverter
from src.logics.factory_converters import FactoryConverters

"""Конвертер для словарей"""
class DictConverter(AbstractConverter):

    """Переопределённый метод convert"""
    def convert(self, obj) -> dict:
        result = dict()
        for key, value in obj.items():
            result[key] = FactoryConverters.convert(value)
        return result


