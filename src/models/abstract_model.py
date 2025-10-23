import uuid
from abc import ABC, abstractmethod

from src.models.validators.decorators import validate_setter


class AbstractModel(ABC):
    """
    Абстрактный базовый класс для моделей с уникальным идентификатором.
    """
    _id: str = ""

    def __init__(self):
        self._id = str(uuid.uuid4())

    @property
    def id(self) -> str:
        """
        Возвращает уникальный идентификатор объекта.
        """
        return self._id

    @id.setter
    @validate_setter(str, 36)
    def id(self, value: str):
        self._id = value

    def __eq__(self, other) -> bool:
        """
        Сравнивает два объекта по их уникальным идентификаторам.
        """
        if isinstance(other, AbstractModel):
            return self.id == other.id
        return False

    @staticmethod
    def from_dto(dto, cache: dict):
        pass