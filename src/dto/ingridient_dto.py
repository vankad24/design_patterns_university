from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId


# класс dto для ингредиента рецепта
@dataclass
class IngredientDto(AbstractDto):
    product: CachedId = None
    amount: float = 0.0
    unit: CachedId = None
