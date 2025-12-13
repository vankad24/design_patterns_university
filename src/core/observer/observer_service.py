from typing import Callable

from src.core.observer.event_models import AbstractEvent
from src.core.observer.event_type import EventType
from src.core.singletone import Singleton
from src.models.validators.functions import validate_val

"""
Реализация наблюдателя
"""
class ObserverService(metaclass=Singleton):

    def __init__(self):
        self.callbacks: dict[EventType, list[Callable]] = {str(k): list() for k in EventType}

    """
    """
    def add(self, event_type: str | EventType, callback: Callable):
        validate_val(callback, Callable)
        self.callbacks[EventType(event_type)].append(callback)

    """
    """
    def delete(self, event_type: str | EventType, callback: Callable) -> bool:
        listeners = self.callbacks[EventType(event_type)]
        if callback in listeners:
            listeners.remove(callback)
            return True
        return False

    """
    """
    def make_event(self, event: AbstractEvent):
        validate_val(event, AbstractEvent)
        for callback in self.callbacks[event.event_type]:
            need_to_stop = callback(event)
            # Если вернулось True, останавливаем обработку события
            if need_to_stop:
                break

        # Широковещательный
        for callback in self.callbacks[EventType.BROADCAST]:
            need_to_stop = callback(event)
            # Если вернулось True, останавливаем обработку события
            if need_to_stop:
                break
