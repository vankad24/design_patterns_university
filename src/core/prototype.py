import operator
from src.dto.filter_dto import FilterDto
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
        "and": operator.and_,  # Побитовое И
        "or": operator.or_,  # Побитовое ИЛИ
        "xor": operator.xor,  # Побитовое исключающее ИЛИ
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

    # Универсальная функция фильтрации
    def filter(self, dto: FilterDto) -> "Prototype":
        result = filter(lambda item: self._operator_to_func[dto.op](getattr(item, dto.field_name), dto.value), self.data)
        return self.clone(list(result))