from abc import ABC, abstractmethod
from src.models.validators.functions import validate_val


class AbstractResponse(ABC):

    @abstractmethod
    def build(self, data: list) -> str:
        validate_val(data, list, check_func=lambda x:len(x)>0)

        return ""

