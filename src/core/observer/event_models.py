import uuid

from src.core.observer.event_type import EventType
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import validate_val


class AbstractEvent:
    _id: str = ""
    _event_type: EventType = ""

    def __init__(self, event_type: EventType | str, event_id: str | None = None):
        self._id = event_id or str(uuid.uuid4())
        self.event_type = event_type

    @property
    def id(self) -> str:
        """
        Возвращает уникальный идентификатор события.
        """
        return self._id

    @id.setter
    @validate_setter(str, 36)
    def id(self, value: str):
        self._id = value

    @property
    def event_type(self) -> EventType:
        """Возвращает тип события."""
        return self._event_type

    @event_type.setter
    @validate_setter((EventType, str), check_func=EventType)
    def event_type(self, value: EventType):
        self._event_type = EventType(value)

    def __repr__(self):
        class_name = self.__class__.__name__
        fields = ', '.join(f'{key}={value!r}' for key, value in self.__dict__.items())
        return f'{class_name}({fields})'


class AbstractModelEvent(AbstractEvent):
    _model = None

    def __init__(self, event_type: EventType | str, model, event_id: str | None = None):
        super().__init__(event_type, event_id)
        self.model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        from src.models.abstract_model import AbstractModel
        validate_val(value, AbstractModel)
        self._model = value

class DeleteModelEvent(AbstractModelEvent):
    @classmethod
    def create(cls, model, event_id: str = None):
        event = cls(EventType.MODEL_DELETE, model, event_id)
        return event

class AddModelEvent(AbstractModelEvent):
    @classmethod
    def create(cls, model, event_id: str = None):
        event = cls(EventType.MODEL_ADD, model, event_id)
        return event

class ChangeModelEvent(AbstractModelEvent):
    @classmethod
    def create(cls, model, event_id: str = None):
        event = cls(EventType.MODEL_CHANGE, model, event_id)
        return event

class MessageEvent(AbstractEvent):
    _msg = ""

    @property
    def msg(self) -> str:
        return self._msg

    @msg.setter
    @validate_setter(str)
    def msg(self, value: str):
        self._msg = value

class ModelOperationErrorEvent(MessageEvent):
    @classmethod
    def create(cls, msg: str, event_id: str = None):
        event = cls(EventType.MODEL_OPERATION_ERROR, event_id)
        event.msg = msg
        return event

class ModelOperationSuccessEvent(MessageEvent):
    @classmethod
    def create(cls, msg: str, event_id: str = None):
        event = cls(EventType.MODEL_OPERATION_SUCCESS, event_id)
        event.msg = msg
        return event