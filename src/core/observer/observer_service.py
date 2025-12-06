
from src.core.observer.event_listener import EventListener
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
    Добавить объект под наблюдение
    """
    def add(self, event: str|EventType, obj):
        validate_val(obj, EventListener)
        self.listeners[EventType(event)].append(obj)

    """
    Удалить из под наблюдения
    """
    def delete(self, obj) -> bool:
        for key, listeners in self.listeners.items():
            if obj in listeners:
                self.listeners[key].remove(obj)
                return True
        return False

    """
    Вызвать событие
    """
    def make_event(self, event: str|EventType, params):
        for listener in self.listeners[EventType(event)]:
            need_to_stop = listener.handle(event, params)
            # Если вернулось True, останавливаем обработку события
            if need_to_stop:
                break
