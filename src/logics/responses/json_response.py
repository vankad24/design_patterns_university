import json

from src.core.functions import get_fields
from src.logics.factory_converters import FactoryConverters
from src.logics.responses.abstract_response import AbstractResponse


class JsonResponse(AbstractResponse):
    """Класс для формирования ответа в формате JSON"""

    #метод формирования запроса
    def build(self, data: list):
        super().build(data)
        return json.dumps(FactoryConverters.convert(data))

