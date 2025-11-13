from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto
from src.dto.filter_dto import FilterDto

# Пример
# {
#         "filters": {
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
#         },
#         "sorting":[
#             "unit_name"
#         ]
#     }


# класс dto для фильтрации
@dataclass
class FilterSortingDto(AbstractDto):
    filters: list[FilterDto] = field(default_factory=list)
    sorting: list[str] = field(default_factory=list)

