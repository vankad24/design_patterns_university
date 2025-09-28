import uuid
from abc import abstractmethod, ABC

from src.models.validators.decorators import validate_setter
from src.models.validators.functions import validate_val


class AbstractModel(ABC):
    """
    Абстрактный базовый класс для моделей с уникальным идентификатором.
    """
    __id: str = ""

    def __init__(self):
        self.__id = uuid.uuid4().hex

    def load_from_dict(self, data: dict):
        """
        Загружает данные из словаря в атрибуты объекта.
        Игнорирует ключи, начинающиеся с '_', и отсутствующие атрибуты.
        """
        validate_val(data, dict)
        for key, value in data.items():
            if not key.startswith("_") and hasattr(self, key):
                setattr(self, key, value)

    @property
    def id(self) -> str:
        """
        Возвращает уникальный идентификатор объекта.
        """
        return self.__id

    @id.setter
    @validate_setter(str, 32)
    def id(self, value: str):
        self.__id = value

    def __eq__(self, other) -> bool:
        """
        Сравнивает два объекта по их уникальным идентификаторам.
        """
        if isinstance(other, AbstractModel):
            return self.id == other.id
        return False