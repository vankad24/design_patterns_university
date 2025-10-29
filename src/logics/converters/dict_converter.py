
from src.logics.converters.abstract_converter import AbstractConverter

"""Конвертер для словарей"""
class DictConverter(AbstractConverter):

    """Переопределённый метод convert"""
    def convert(self, obj) -> dict:
        result = dict()
        for key, value in obj.items():

            from src.logics.factory_converters import FactoryConverters
            result[key] = FactoryConverters.convert(value)
        return result


