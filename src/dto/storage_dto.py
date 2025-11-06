from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto


# класс dto для склада
@dataclass
class StorageDto(AbstractDto):
    name: str = ""
    address: str = ""
