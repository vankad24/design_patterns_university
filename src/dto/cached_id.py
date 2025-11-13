from src.dto.abstract_dto import AbstractDto


class CachedId(AbstractDto):
    """
    Класс для объекта передачи данных (DTO), используемого для кэширования
    идентификаторов уже созданных моделей.

    Наследует от AbstractDto, автоматически получая поле 'id: str',
    генерируемое как UUID по умолчанию.
    """
    ...