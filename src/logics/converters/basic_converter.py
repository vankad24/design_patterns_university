from src.logics.converters.abstract_converter import AbstractConverter

"""Конвертер примитивных типов"""
class BasicConverter(AbstractConverter):

    """Переопределённый метод convert

    Для примитивных типов не делает никакого преобразования
    """
    def convert(self, obj) -> dict:
        return obj
