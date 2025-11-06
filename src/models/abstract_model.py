import uuid
from abc import ABC, abstractmethod

from src.dto.abstract_dto import AbstractDto
from src.models.validators.decorators import validate_setter


class AbstractModel(ABC):
    """
    Абстрактный базовый класс для моделей с уникальным идентификатором.
    """

    # соответствующий модели dto класс
    DTO_CLASS = AbstractDto

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

    def __repr__(self):
        class_name = self.__class__.__name__
        fields = ', '.join(f'{key}={value!r}' for key, value in self.__dict__.items())
        return f'{class_name}({fields})'

    @staticmethod
    def from_dto(dto, cache: dict):
        pass

    # Отдельный общий метод для формирования Dto структуры
    def to_dto(self):
        pass
