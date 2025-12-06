from enum import StrEnum


class EventType(StrEnum):
    MODEL_ADD = "MODEL_ADD"
    MODEL_REMOVE = "MODEL_REMOVE"

    @classmethod
    def values(cls) -> list[str]:
        return list(map(str, cls))

    @classmethod
    def get_names(cls) -> list[str]:
        return list(map(lambda x: x.name, cls))

    @classmethod
    def has(cls, val):
        if isinstance(val, cls):
            return val in cls
        return val in cls.get_names()

    # def __eq__(self, other):
