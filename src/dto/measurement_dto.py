from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId


# класс dto для единиц измерения
@dataclass
class MeasurementUnitDto(AbstractDto):
    name: str = ""
    conversion_factor: float = 1
    base_unit: CachedId = None
