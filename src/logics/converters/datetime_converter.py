
from datetime import datetime

from src.logics.converters.abstract_converter import AbstractConverter

"""Конвертер даты в строку"""
class DatetimeConverter(AbstractConverter):
    """Переопределённый метод convert
    
    Приводит datetime к строковому представлению в заданном формате"""
    def convert(self, obj: datetime) -> str:
        format: str = "%Y-%m-%d %H:%M:%S"
        return obj.strftime(format)

