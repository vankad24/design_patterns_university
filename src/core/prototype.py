import operator
import re

from src.core.functions import get_nested_attr
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto
from src.models.validators.functions import validate_val


# Класс - прототип
class Prototype:
    _data: list = []

    _operator_to_func = {
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        # Дополнительно:
        "in": operator.contains, # x in iterable
        "notin": lambda x, y: x not in y,
        "contains": lambda x, y: y in x,
        "notcontains": lambda x, y: y not in x,
        "and": operator.and_,  # Побитовое И
        "or": operator.or_,  # Побитовое ИЛИ
        "xor": operator.xor,  # Побитовое исключающее ИЛИ
        "like": lambda s, pattern: bool(re.fullmatch(pattern, s))
    }

    # Набор данных
    @property
    def data(self):
        return self._data

    def __init__(self, data: list):
        validate_val(data, list)
        self._data = data

    def clone(self, data: list = None)-> "Prototype":
        inner_data = self._data if data is None else data
        instance = Prototype(inner_data)
        return instance

    # Универсальная функция фильтрации с поддержкой вложенных структур
    def filter(self, dto: FilterDto) -> "Prototype":
        result = filter(lambda item: self._operator_to_func[dto.op](get_nested_attr(item, dto.field_name.split(".")), dto.value), self.data)
        return self.clone(list(result))

    def filter_mul(self, dtos: list[FilterDto]) -> "Prototype":
        result = self
        for dto in dtos:
            result = result.filter(dto)
        return result

    def sort(self, dto: SortingDto):
        if not dto:
            return self
        return self.clone(sorted(self._data, key=lambda item: [get_nested_attr(item, field.split(".")) for field in dto.field_names], reverse=dto.descending))