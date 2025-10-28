
from src.core.functions import get_fields, get_type_hints_without_underscore
from src.logics.responses.abstract_response import AbstractResponse
from src.models.validators.exceptions import ArgumentException
from src.models.validators.functions import validate_val


class MarkdownResponse(AbstractResponse):
    """Класс для формирования ответа в формате CSV"""


    """
    Сформитровать данные в формате markdown
    """
    def build(self, data: list) -> str:
        validate_val(data, list)
        if len(data) == 0:
            raise ArgumentException("Некоррекно переданы параметры!")

        result = ""
        for item in data:
            result += self._build_item(item)

        return result    


    """
    Сформировать данные по одному элементу
    """
    def _build_item(self, item) -> str:
        if item is None:   
            return ""
        
        # Заголовок
        caption = type(item).__name__
        result = f"# {caption}\n"
        fields = get_type_hints_without_underscore(type(item)).keys()

        # Формирование заголовков столбцов таблицы
        headers_row = "|".join(fields)
        result += f"|{headers_row}|\n"

        # Добавляем разделительную линию
        separator_line = ":--|" * len(fields)
        result += f"|{separator_line}\n"

        # Заполняем строки значениями полей
        values_row = []
        for field in fields:
            value = getattr(item, field)
            values_row.append(str(value))
        
        values_row_str = "|".join(values_row)
        result += f"|{values_row_str}|\n"
        return result

        