from abc import ABC, abstractmethod

"""Абстракный класс конвертера"""
class AbstractConverter(ABC):

    """Абстракный метод для конвертации"""
    @abstractmethod
    def convert(self, obj):
        pass