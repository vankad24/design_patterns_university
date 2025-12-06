import abc

from src.core.observer.event_params import AbstractEventParams
from src.core.observer.event_type import EventType
from src.models.validators.functions import validate_val


class EventListener:
    """
    Обработка события
    """
    @abc.abstractmethod
    def handle(self, event: EventType, params: AbstractEventParams)->bool:
        validate_val(event, (str, EventType), check_func=EventType.has)
        # True чтобы остановить дальнейшую обработку события
        return False

