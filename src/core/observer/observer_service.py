
from src.core.observer.event_listener import EventListener
from src.core.observer.event_params import AbstractEventParams
from src.core.observer.event_type import EventType
from src.core.singletone import Singleton
from src.models.validators.functions import validate_val

"""
Реализация наблюдателя
"""
class ObserverService(metaclass=Singleton):

    def __init__(self):
        self.listeners: dict[EventType, list[EventListener]] = {k: list() for k in EventType.values()}

    """
    Добавить слушателя
    """
    def add(self, event: str|EventType, listener: EventListener):
        validate_val(listener, EventListener)
        self.listeners[EventType(event)].append(listener)

    """
    Удалить слушателя
    """
    def delete(self, event: str|EventType,  listener: EventListener) -> bool:
        listeners = self.listeners[EventType(event)]
        if listener in listeners:
            listeners.remove(listener)
            return True
        return False

    """
    Вызвать событие
    """
    def make_event(self, event: str|EventType, params: AbstractEventParams):
        for listener in self.listeners[EventType(event)]:
            need_to_stop = listener.handle(event, params)
            # Если вернулось True, останавливаем обработку события
            if need_to_stop:
                break
