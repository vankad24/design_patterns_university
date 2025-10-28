
from src.core.functions import get_fields
from src.logics.responses.abstract_response import AbstractResponse


class CsvResponse(AbstractResponse):
    """Класс для формирования ответа в формате CSV"""

    #метод формирования запроса
    def build(self, data: list):
        text = super().build(data)

        # Шапка
        item = data[0]
        fields = get_fields(item)
        for filed in fields:
            text+=f"{filed};"

        # Данные
        return text
