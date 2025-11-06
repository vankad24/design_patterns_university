from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto


# класс dto для групп номенклатуры
@dataclass
class ProductGroupDto(AbstractDto):
    name: str = ""