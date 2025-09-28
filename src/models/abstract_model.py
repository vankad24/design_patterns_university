import uuid
from abc import abstractmethod, ABC

class AbstractModel(ABC):
    __id: str = uuid.uuid4().hex

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if not key.startswith("_") and hasattr(self, key):
                setattr(self, key, value)

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        # todo validate str
        self.__id = value

    def __eq__(self, other) -> bool:
        if issubclass(other, AbstractModel):
            return self.id == other.id
        return False