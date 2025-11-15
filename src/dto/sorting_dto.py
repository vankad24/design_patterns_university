from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto


# класс dto для сортировки
@dataclass
class SortingDto(AbstractDto):
    field_names: list[str] = field(default_factory=list)
    descending: bool = False

