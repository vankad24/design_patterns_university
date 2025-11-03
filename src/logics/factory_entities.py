from src.logics.responses.abstract_response import AbstractResponse
from src.logics.responses.csv_response import CsvResponse
from src.logics.responses.json_response import JsonResponse
from src.logics.responses.markdown_response import MarkdownResponse
from src.models.validators.exceptions import OperationException


class FactoryEntities:
    _match = {
        "csv": CsvResponse,
        'json': JsonResponse,
        'markdown': MarkdownResponse,
    }

    def create(self, r_format: str) -> type[AbstractResponse]:
        if r_format not in self._match:
            raise OperationException("Формат неверный")
        return self._match[r_format]

