from dataclasses import dataclass
from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId

# класс dto для продуктов
@dataclass
class ProductDto(AbstractDto):
    name: str = ""
    full_name: str = ""
    unit: CachedId = None
    group: CachedId = None
