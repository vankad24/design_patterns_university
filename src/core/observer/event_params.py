import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.models.validators.decorators import validate_setter


class AbstractEventParams:
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



class DeleteModelEventParams(AbstractEventParams):
    @staticmethod
    def create(model_id):
        event = DeleteModelEventParams()
        event.id = model_id
        return event