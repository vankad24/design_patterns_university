from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId


# класс dto для транзакций
@dataclass
class ProductRemainDto(AbstractDto):
    # Значение (сумма) транзакции
    value: float = 0.0

    # Ссылка на единицу измерения
    unit: CachedId = None

    # Ссылка на продукт
    product: CachedId = None

    # Ссылка на хранилище
    storage: CachedId = None