from abc import ABC, abstractmethod
from src.models.validators.functions import validate_val


class AbstractResponse(ABC):

    @classmethod
    def build(cls, data: list) -> str:
        validate_val(data, list, check_func=lambda x:len(x)>0)

        return ""



