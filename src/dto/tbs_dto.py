from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId


# класс dto для подсчёта элемента сальдовой ведомости
@dataclass
class TurnoverBalanceItemDto(AbstractDto):
    storage: CachedId = None
    product: CachedId = None
    unit: CachedId = None
    start_balance: float = 0.0
    inflows: float = 0.0
    outflows: float = 0.0
