
from src.core.functions import get_fields
from src.logics.responses.abstract_response import AbstractResponse


class CsvResponse(AbstractResponse):
    """Класс для формирования ответа в формате CSV"""

    #метод формирования запроса
    @classmethod
    def build(cls, data: list):
        super().build(data)
        if not data:
            return ""

        # Шапка
        result = []
        fields = get_fields(data[0])
        result.append(list(fields.keys()))

        # Данные
        for item in data:
            temp = []
            for field in fields:
                temp.append(str(getattr(item, field)))
            result.append(temp)

        text = ""
        for row in result:
            text+=";".join(row)+'\n'
        return text
