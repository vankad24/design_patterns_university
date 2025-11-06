from dataclasses import dataclass
from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId

# класс dto для склада
@dataclass
class StorageDto(AbstractDto):
    name: str = ""
    address: str = ""
