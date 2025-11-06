from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto
from src.dto.company_dto import CompanyDto


# класс dto для настроек
@dataclass
class SettingsDto(AbstractDto):
    company: CompanyDto = None
    default_response_format: str = 'json'
    first_start: bool = True
