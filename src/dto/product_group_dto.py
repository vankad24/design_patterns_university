from dataclasses import dataclass
from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId

# класс dto для групп номенклатуры
@dataclass
class ProductGroupDto(AbstractDto):
    name: str = ""