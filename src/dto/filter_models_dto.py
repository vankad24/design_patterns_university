from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto


# Пример:
# {
#     "model": "products",
#     "filters":[
#             {
#                 "field_name": "group.name",
#                 "value": "Продукты питания"
#             }
#         ],
#     "sorts":
#         {
#             "field_names": ["name"],
#             "descending": false
#         }
# }

# класс dto для фильтрации и сортировки моделей
@dataclass
class FilterModelsDto(AbstractDto):
    model: str = ""
    filters: list[FilterDto] = field(default_factory=list)
    sorts: SortingDto = None


