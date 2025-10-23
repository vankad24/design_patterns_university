from src.core.abstract_response import AbstractResponse
from src.logics.response_csv import ResponseCsv
from src.models.validators.exceptions import OperationException


class FactoryEntities:
    _match = {
        "csv": ResponseCsv
    }

    def create(self, r_format: str) -> type[AbstractResponse]:
        if r_format not in self._match:
            raise OperationException("Формат неверный")
        return self._match[r_format]

