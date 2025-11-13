import json

from src.logics.factory_converters import FactoryConverters
from src.logics.responses.abstract_response import AbstractResponse


class JsonResponse(AbstractResponse):
    """Класс для формирования ответа в формате JSON"""

    #метод формирования запроса
    @classmethod
    def build(cls, data):
        return json.dumps(FactoryConverters.convert(data), ensure_ascii=False)

