from src.core.abstract_response import AbstractResponse
from src.logics.responses.csv_response import CsvResponse
from src.models.validators.exceptions import OperationException


class FactoryEntities:
    _match = {
        "csv": CsvResponse
    }

    def create(self, r_format: str) -> type[AbstractResponse]:
        if r_format not in self._match:
            raise OperationException("Формат неверный")
        return self._match[r_format]

