import uuid
from abc import abstractmethod, ABC

class AbstractModel(ABC):
    __id: str = uuid.uuid4().hex

    def load_from_dict(self, data:dict):
        public_fields = set(filter(lambda x: not x.startswith("_"), dir(self)))
        matching_keys = public_fields & data.keys()
        for key in matching_keys:
            setattr(self, key, data[key])

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