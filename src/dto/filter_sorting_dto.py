from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto


# Пример
# {
#         "filters":
#             [
#                 {
#                     "filed_name": "name",
#                     "value": "Пшеничная мука"
#                 },
#                 {
#                     "filed_name": "unit",
#                     "value": "кг"
#                 },
#             ]
#         "sorts":
#             {
#                 "filed_names": ["unit", "name"],
#                 "descending": false
#               },
#     }


# класс dto для фильтрации и сортировки
@dataclass
class FilterSortingDto(AbstractDto):
    filters: list[FilterDto] = field(default_factory=list)
    sorts: SortingDto = None

