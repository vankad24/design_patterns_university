from dataclasses import dataclass
from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId

# класс dto для организаций
@dataclass
class CompanyDto(AbstractDto):
    name: str = ""
    inn: str = ""
    account: str = ""
    corr_account: str = ""
    bik: str = ""
    ownership: str = ""
