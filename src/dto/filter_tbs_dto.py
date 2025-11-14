from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto


# класс dto для фильтрации и сортировки tbs в запросе
@dataclass
class FilterTbsDto(AbstractDto):
    start_date: str = ""
    end_date: str = ""
    transaction_filters: list[FilterDto] = field(default_factory=list)
    result_filters: list[FilterDto] = field(default_factory=list)
    result_sorts: SortingDto = None


