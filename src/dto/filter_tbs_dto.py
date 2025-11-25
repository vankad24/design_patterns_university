from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto


# Пример:
# {
#     "start_date": "2025-01-02",
#     "end_date": "2025-02-01",
#     "transaction_filters":
#         [
#             {
#                 "field_name": "storage.id",
#                 "value": "7dc27e96-e6ad-4e5e-8c56-84e00667e3d7"
#             }
#         ],
#     "result_filters":
#         [
#             {
#                 "field_name": "change_in_balance",
#                 "value": 0,
#                 "op": "!="
#             }
#         ],
#     "result_sorts":
#         {
#             "field_names": ["end_balance"],
#             "descending": false
#         }
# }


# класс dto для фильтрации и сортировки tbs в запросе
@dataclass
class FilterTbsDto(AbstractDto):
    start_date: str = ""
    end_date: str = ""
    transaction_filters: list[FilterDto] = field(default_factory=list)
    result_filters: list[FilterDto] = field(default_factory=list)
    result_sorts: SortingDto = None


