import uuid
from abc import abstractmethod, ABC

from src.models.validators.decorators import validate_setter
from src.models.validators.functions import validate_val


class AbstractModel(ABC):
    __id: str = uuid.uuid4().hex

    def load_from_dict(self, data: dict):
        validate_val(data, dict)
        for key, value in data.items():
            if not key.startswith("_") and hasattr(self, key):
                setattr(self, key, value)

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    @validate_setter(str, 32)
    def id(self, value: str):
        self.__id = value

    def __eq__(self, other) -> bool:
        if isinstance(other, AbstractModel):
            return self.id == other.id
        return False