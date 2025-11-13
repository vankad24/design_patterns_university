from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId


# класс dto для фильтрации
@dataclass
class FilterDto(AbstractDto):
    field_name: str = ""
    value: object = None
    op: str = "=="
