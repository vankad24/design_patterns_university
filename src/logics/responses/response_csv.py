from src.core.abstract_response import AbstractResponse
from src.core.functions import get_fields
from src.core.response_format import ResponseFormat


class ResponseCsv(AbstractResponse):
    def build(self, data: list):
        text = super().build(data)

        # Шапка
        item = data[0]
        fields = get_fields(item)
        for filed in fields:
            text+=f"{filed};"

        # Данные
        return text
