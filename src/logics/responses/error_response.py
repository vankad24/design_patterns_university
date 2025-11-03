import json

from src.core.functions import get_fields
from src.logics.factory_converters import FactoryConverters
from src.logics.responses.abstract_response import AbstractResponse


class ErrorResponse(AbstractResponse):
    """Класс для формирования ответа в формате JSON"""

    #метод формирования запроса
    @classmethod
    def build(cls, data: str):
        return f"Error response: {data}"

