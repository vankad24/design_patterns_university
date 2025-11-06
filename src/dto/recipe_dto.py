from dataclasses import dataclass, field
from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId

# класс dto для рецепта
@dataclass
class RecipeDto(AbstractDto):
    name: str = ""
    cooking_time: str = ""
    steps: list[str] = field(default_factory=list)
    ingredients: list[CachedId] = field(default_factory=list)
